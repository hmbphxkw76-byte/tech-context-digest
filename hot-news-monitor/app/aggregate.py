"""聚合：分类标签、标题相似度聚类、热度计算与事件装配。

- 分类：固定中文标签 + 英文关键词映射（KEYWORD_TAGS），未命中归入「国际要闻」。
- 聚类：标题分词后 Jaccard ≥ CLUSTER_JACCARD 或共享实词 ≥ CLUSTER_OVERLAP 判同事件，
  并查集合并；事件 id 取簇内最早报道的 item.id（稳定可重放）。
- 热度：heat = min(100, HEAT_GAIN × Σ source_weight × exp(-age_hours / HALF_LIFE_H))，
  随时间指数衰减；每次刷新追加 heat_series 采样点形成趋势。
- 阈值：heat ≥ threshold → level 1（高优先级置顶）；≥ 0.5×threshold → 2；其余 3。
"""
from __future__ import annotations

import math
import re
from datetime import datetime, timezone
from typing import Any, Iterable

from .models import HeatPoint, HotEvent, NewsItem
from .store import utc_now_iso

CLUSTER_JACCARD = 0.34
CLUSTER_OVERLAP = 2
HEAT_GAIN = 8.0
HALF_LIFE_H = 12.0

TAGS = (
    "政治", "经济", "金融", "科技", "军事安全", "能源",
    "社会民生", "公共卫生", "环境", "国际关系", "国际要闻",
)

KEYWORD_TAGS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("军事安全", ("military", "missile", "strike", "attack", "war", "conflict", "defence", "defense", "navy", "drone", "ceasefire", "troops")),
    ("能源", ("oil", "gas", "opec", "crude", "energy", "petrol", "pipeline", "lng")),
    ("金融", ("bank", "fed ", "federal reserve", "interest rate", "market", "stocks", "bonds", "default", "imf", "recession", "inflation", "currency")),
    ("科技", ("ai ", "artificial intelligence", "chip", "semiconductor", "tech", "cyber", "google", "openai", "antitrust", "data center", "quantum")),
    ("公共卫生", ("covid", "vaccine", "pandemic", "who ", "outbreak", "health", "disease", "ebola", "mpox")),
    ("环境", ("climate", "wildfire", "flood", "hurricane", "storm", "earthquake", "emission", "cop29", "cop30", "drought")),
    ("政治", ("election", "president", "parliament", "senate", "minister", "vote", "coalition", "government", "policy", "sanction", "summit")),
    ("经济", ("economy", "trade", "tariff", "gdp", "jobs", "unemployment", "export", "import", "supply chain")),
    ("社会民生", ("protest", "strike action", "migration", "refugee", "housing", "education", "crime", "police")),
    ("国际关系", ("diplomatic", "embassy", "treaty", "un ", "nato", "eu ", "asean", "talks", "negotiation", "alliance")),
)

STOPWORDS = frozenset(
    "the a an and or of to in on for with at by from as is are was were be been it its this that "
    "these those after before over under between into out up down about says said new more other "
    "than then them they we you he she his her their our your not no but if when while during".split()
)


def tokenize(text: str) -> list[str]:
    return [w for w in re.split(r"[^a-z0-9]+", (text or "").lower()) if len(w) >= 3 and w not in STOPWORDS]


def classify(title: str) -> str:
    low = f"{(title or '').lower()} "
    for tag, kws in KEYWORD_TAGS:
        if any(kw in low for kw in kws):
            return tag
    return "国际要闻"


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def cluster(items: list[NewsItem]) -> list[list[NewsItem]]:
    """把报道按标题相似度聚成事件簇（O(n²)，n 为单次抓取量，量级可控）。"""
    n = len(items)
    if n == 0:
        return []
    tokens = [set(tokenize(it.title)) for it in items]
    uf = _UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            inter = len(tokens[i] & tokens[j])
            if inter >= CLUSTER_OVERLAP or jaccard(tokens[i], tokens[j]) >= CLUSTER_JACCARD:
                uf.union(i, j)
    groups: dict[int, list[NewsItem]] = {}
    for idx, it in enumerate(items):
        groups.setdefault(uf.find(idx), []).append(it)
    return list(groups.values())


def _parse_ts(ts: str) -> datetime | None:
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def compute_heat(items: list[NewsItem], weights: dict[str, float], now: datetime) -> float:
    score = 0.0
    for it in items:
        dt = _parse_ts(it.published_at)
        age_h = max(0.0, (now - dt).total_seconds() / 3600.0) if dt else HALF_LIFE_H * 3
        score += float(weights.get(it.tier, 2.0)) * math.exp(-age_h / HALF_LIFE_H)
    return round(min(100.0, HEAT_GAIN * score), 2)


def _event_title(cluster_items: list[NewsItem]) -> tuple[str, str]:
    """事件标题/标签：优先 Tier 高且最新的报道标题；标签取簇内多数的分类。"""
    rank = {"official": 0, "rating": 0, "media_t1": 1, "media": 2}
    ordered = sorted(
        cluster_items,
        key=lambda it: (rank.get(it.tier, 3), _parse_ts(it.published_at) or datetime.min.replace(tzinfo=timezone.utc)),
    )
    title = ordered[-1].title if ordered else ""
    tags = [classify(it.title) for it in cluster_items]
    tag = max(set(tags), key=tags.count) if tags else "国际要闻"
    return title, tag


def build_events(
    items: list[NewsItem],
    prev_events: Iterable[HotEvent],
    weights: dict[str, float],
    threshold: float,
    now: datetime,
    interval_seconds: int,
) -> list[HotEvent]:
    series_by_id = {e.id: list(e.heat_series) for e in prev_events}
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    events: list[HotEvent] = []
    for grp in cluster(items):
        first = min((it.published_at for it in grp if it.published_at), default=ts)
        last = max((it.published_at for it in grp if it.published_at), default=ts)
        eid = min(grp, key=lambda it: (it.published_at or "9999", it.id)).id
        title, tag = _event_title(grp)
        heat = compute_heat(grp, weights, now)
        level = 1 if heat >= threshold else (2 if heat >= threshold * 0.5 else 3)
        ordered_items = sorted(grp, key=lambda it: (it.published_at or "", it.source_name))
        series = series_by_id.get(eid, [])
        if not series or series[-1].value != heat:
            series.append(HeatPoint(ts=ts, value=heat))
        series = series[-72:]  # 保留近 6 小时（5 分钟粒度）
        events.append(
            HotEvent(
                id=eid,
                title=title,
                tag=tag,
                heat=heat,
                level=level,
                first_seen=first,
                last_seen=last,
                source_ids=sorted({it.source_id for it in grp}),
                items=ordered_items,
                heat_series=series,
            )
        )
    events.sort(key=lambda e: (-e.heat, e.last_seen), reverse=False)
    return events


def build_metrics(events: list[HotEvent], total_items: int) -> dict[str, Any]:
    by_tag: dict[str, int] = {}
    for e in events:
        by_tag[e.tag] = by_tag.get(e.tag, 0) + 1
    return {
        "total_events": len(events),
        "total_items": total_items,
        "top_count": sum(1 for e in events if e.level == 1),
        "by_tag": [{"tag": t, "count": c} for t, c in sorted(by_tag.items(), key=lambda kv: (-kv[1], kv[0]))],
    }


def background_note(event: HotEvent) -> str:
    """背景溯源面板的机械说明（只描述覆盖结构，不做事实断言）。"""
    sources = "、".join(sorted({it.source_name for it in event.items}))
    n = len(event.source_ids)
    if n >= 3:
        verdict = "已达三家以上独立信源交叉，结构上具备互证基础。"
    else:
        verdict = "独立信源不足三家，结论强度有限，建议谨慎采信。"
    return (
        f"本事件由 {n} 家独立信源、{len(event.items)} 篇报道交叉覆盖；"
        f"涉及信源：{sources or '无'}。{verdict}"
        f"当前热度 {event.heat:.1f}（随时间衰减），最近更新 {event.last_seen or '未知'}。"
        f"明细见时间线模块。"
    )


__all__ = [
    "TAGS", "tokenize", "classify", "jaccard", "cluster", "compute_heat",
    "build_events", "build_metrics", "background_note", "utc_now_iso",
]
