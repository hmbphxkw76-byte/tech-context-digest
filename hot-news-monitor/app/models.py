"""数据模型：新闻条目 / 热点事件 / 快照（dataclass + JSON 序列化）。

字段命名与 API 输出一致（snake_case）；序列化只允许基本类型，保证确定性。
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class NewsItem:
    """单条抓取到的新闻报道（英文原文，来源域命中白名单）。"""

    id: str
    title: str
    url: str
    source_id: str
    source_name: str
    tier: str
    published_at: str  # ISO8601 UTC
    summary: str = ""
    language: str = "en"
    is_demo: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HeatPoint:
    """事件热度采样点（每次刷新追加，形成趋势序列）。"""

    ts: str
    value: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class HotEvent:
    """聚合后的热点事件：一个事件包含多家信源的关联报道。"""

    id: str
    title: str
    tag: str  # 中文分类标签（政治/经济/金融/科技/军事安全/能源/社会民生/公共卫生/环境/国际关系）
    heat: float
    level: int  # 1=高优先级(超阈值置顶) / 2=常规 / 3=低热
    first_seen: str
    last_seen: str
    source_ids: list[str] = field(default_factory=list)
    items: list[NewsItem] = field(default_factory=list)
    heat_series: list[HeatPoint] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "tag": self.tag,
            "heat": round(float(self.heat), 2),
            "level": self.level,
            "is_top": self.level == 1,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "source_ids": list(self.source_ids),
            "items": [i.to_dict() for i in self.items],
            "heat_series": [p.to_dict() for p in self.heat_series],
        }


@dataclass
class Snapshot:
    """一次全量刷新的完整快照（state.json 的内容）。"""

    generated_at: str
    interval_seconds: int
    mode: str  # live | seed | hybrid
    threshold: float  # 高优先级热度阈值
    events: list[HotEvent]
    source_status: list[dict[str, Any]]
    metrics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "interval_seconds": self.interval_seconds,
            "mode": self.mode,
            "threshold": self.threshold,
            "events": [e.to_dict() for e in self.events],
            "source_status": list(self.source_status),
            "metrics": dict(self.metrics),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Snapshot":
        events = []
        for e in data.get("events", []):
            events.append(
                HotEvent(
                    id=str(e["id"]),
                    title=str(e["title"]),
                    tag=str(e["tag"]),
                    heat=float(e.get("heat", 0)),
                    level=int(e.get("level", 2)),
                    first_seen=str(e.get("first_seen", "")),
                    last_seen=str(e.get("last_seen", "")),
                    source_ids=[str(s) for s in e.get("source_ids", ())],
                    items=[NewsItem(**i) for i in e.get("items", ())],
                    heat_series=[HeatPoint(**p) for p in e.get("heat_series", ())],
                )
            )
        return cls(
            generated_at=str(data.get("generated_at", "")),
            interval_seconds=int(data.get("interval_seconds", 21600)),
            mode=str(data.get("mode", "seed")),
            threshold=float(data.get("threshold", 80)),
            events=events,
            source_status=list(data.get("source_status", ())),
            metrics=dict(data.get("metrics", {})),
        )
