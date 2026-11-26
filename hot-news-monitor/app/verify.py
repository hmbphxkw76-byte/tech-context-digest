"""机器可判定的抽样核验：字段完整性 / 来源白名单 / 链接格式 / 热度重算 / 时间线有序。

语义级「内容准确性」无法由脚本判定，只输出待人工复核清单（见 ACCURACY_NOTE）。
示例数据（is_demo=True）不计入通过口径，单独标注。
"""
from __future__ import annotations

import random
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from .aggregate import classify, compute_heat
from .fetch import load_config
from .models import Snapshot
from .store import Store

ACCURACY_NOTE = (
    "机器核验仅覆盖结构 / 来源 / 数值一致性；语义准确性需人工对照原文复核，"
    "本脚本输出待复核清单（标题 + 链接），不替代人工判断。"
)

# 明确禁止的中文媒体域名片段（禁止信源的机械兜底，双保险）
FORBIDDEN_HOST_PARTS = (
    "xinhuanet", "people.com.cn", "cctv", "cri.cn", "chinadaily", "globaltimes",
    "caixin", "sina.com", "sohu.com", "163.com", "qq.com", "thepaper.cn",
    "huanqiu", "guancha.cn",
)

TIER_OK = {"official", "rating", "media_t1", "media"}
URL_RE = re.compile(r"^https?://[^\s]+$")


def verify_items(snapshot: Snapshot, n: int = 100, seed: int = 20261126) -> dict[str, Any]:
    cfg = load_config()
    allowed = {str(s["id"]) for s in cfg.get("sources", ())}
    weights = dict(cfg.get("heat_weights", {}))
    all_items = [it for e in snapshot.events for it in e.items]
    real = [it for it in all_items if not it.is_demo]
    rng = random.Random(seed)
    sample = rng.sample(real, min(n, len(real))) if real else []

    failures: list[dict[str, str]] = []
    reviewed: list[dict[str, str]] = []
    for it in sample:
        problems: list[str] = []
        if not it.title.strip():
            problems.append("title_empty")
        if not it.source_id or it.source_id not in allowed:
            problems.append("source_not_whitelisted")
        if it.tier not in TIER_OK:
            problems.append("tier_invalid")
        if it.url:
            if not URL_RE.match(it.url):
                problems.append("url_malformed")
            else:
                host = (urlparse(it.url).hostname or "").lower()
                if any(p in host for p in FORBIDDEN_HOST_PARTS):
                    problems.append("forbidden_chinese_media_host")
        try:
            datetime.strptime(it.published_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            problems.append("timestamp_unparsable")
        if problems:
            failures.append({"id": it.id, "title": it.title[:60], "problems": ",".join(problems)})
        else:
            reviewed.append({"id": it.id, "title": it.title[:80], "url": it.url})

    heat_bad = 0
    now = datetime.now(timezone.utc)
    for e in snapshot.events:
        expect = compute_heat(e.items, weights, now)
        if abs(expect - float(e.heat)) > 1.0:
            heat_bad += 1
    tag_bad = sum(1 for e in snapshot.events if classify(e.title) != e.tag)

    return {
        "generated_at": snapshot.generated_at,
        "mode": snapshot.mode,
        "total_items": len(all_items),
        "real_items": len(real),
        "demo_items": len(all_items) - len(real),
        "sampled": len(sample),
        "passed": len(reviewed),
        "failed": failures,
        "heat_mismatch_events": heat_bad,
        "tag_mismatch_events": tag_bad,
        "manual_review_queue": reviewed[:20],
        "accuracy_note": ACCURACY_NOTE,
    }


def verify_from_store(store: Store, n: int = 100) -> dict[str, Any]:
    snap = store.load_state()
    if snap is None:
        from .pipeline import refresh
        snap = refresh(store)
    return verify_items(snap, n=n)
