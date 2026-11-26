"""编排：一次全量刷新 = 抓取白名单源 → 台账 → 聚合 → 快照落盘。

模式语义：
- live：本轮抓到内容；
- hybrid：本轮未抓到但存在历史快照，按历史内容重算（并标注）；
- seed：既无抓取也无历史，回落到合成示例数据（is_demo=True）。
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from . import fetch as fetch_mod
from .aggregate import build_events, build_metrics
from .models import NewsItem, Snapshot
from .seed import build_seed_items, seed_config
from .store import Store, utc_now_iso

# 阈值为预校准（ex-ante）经验值：media_t1 三源交叉的新事件约达 50+，可通过 --threshold 覆盖
DEFAULT_THRESHOLD = 50.0
DEFAULT_INTERVAL = 300


def refresh(
    store: Store,
    *,
    config: dict[str, Any] | None = None,
    threshold: float = DEFAULT_THRESHOLD,
    interval_seconds: int = DEFAULT_INTERVAL,
) -> Snapshot:
    now = datetime.now(timezone.utc)
    cfg = config or fetch_mod.load_config()
    weights = dict(cfg.get("heat_weights", seed_config()["heat_weights"]))
    prev = store.load_state()

    from concurrent.futures import ThreadPoolExecutor

    sources = fetch_mod.load_sources(cfg)
    status: list[dict[str, Any]] = []
    items: list[NewsItem] = []
    if not sources:  # 离线演示语义：未配置任何信源 -> 直接使用示例数据
        items = build_seed_items()
        mode = "seed"
    else:
        with ThreadPoolExecutor(max_workers=min(6, len(sources))) as pool:
            results = list(pool.map(fetch_mod.fetch_source, sources))
        for got, st in results:  # pool.map 保持源顺序，输出确定性
            status.append(st)
            items.extend(got)
        mode = "live"
        if not items:
            if prev is not None and prev.events:
                items = [it for e in prev.events for it in e.items]
                mode = "hybrid"
            else:
                items = build_seed_items()
                mode = "seed"

    added = store.append_items(items)
    events = build_events(
        items,
        prev_events=prev.events if prev else (),
        weights=weights,
        threshold=threshold,
        now=now,
        interval_seconds=interval_seconds,
    )
    metrics = build_metrics(events, total_items=len(items))
    metrics["new_items_this_run"] = added
    snapshot = Snapshot(
        generated_at=utc_now_iso(),
        interval_seconds=interval_seconds,
        mode=mode,
        threshold=threshold,
        events=events,
        source_status=status,
        metrics=metrics,
    )
    store.save_state(snapshot)
    try:  # 快照落盘后重建专题页（含 current 自动轮换）；失败不阻断刷新
        from .brief import rebuild_all

        written = rebuild_all()
        brief_note = f"briefs rebuilt: {len(written)}"
    except Exception as exc:  # noqa: BLE001
        brief_note = f"brief rebuild failed: {type(exc).__name__}"
    store.append_fetch_log({"brief": brief_note})
    ok = sum(1 for s in status if s.get("ok"))
    store.append_fetch_log({
        "mode": mode,
        "sources_total": len(status),
        "sources_ok": ok,
        "items_fetched": len(items),
        "items_new": added,
        "events": len(events),
        "top_events": sum(1 for e in events if e.level == 1),
    })
    return snapshot


def summarize(snapshot: Snapshot) -> str:
    m = snapshot.metrics
    return (
        f"[{snapshot.generated_at}] mode={snapshot.mode} "
        f"事件 {m['total_events']} / 报道 {m['total_items']} / 高优先级 {m['top_count']}"
    )
