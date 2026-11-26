"""固定周期调度器：独立守护线程，按 interval_seconds 触发全量刷新。

- 首次运行（无快照）立即刷新一次；之后严格按周期等待（可中断）。
- 单次刷新异常不致命：捕获并写入 fetch_log，下一周期继续（长跑稳定性）。
- 支持 --immediate 强制首轮立即刷新，便于演示与测试。
"""
from __future__ import annotations

import threading
from typing import Any, Callable

from .pipeline import DEFAULT_INTERVAL, DEFAULT_THRESHOLD, refresh
from .store import Store


class Scheduler(threading.Thread):
    def __init__(
        self,
        store: Store,
        *,
        interval_seconds: int = DEFAULT_INTERVAL,
        threshold: float = DEFAULT_THRESHOLD,
        config: dict[str, Any] | None = None,
        immediate: bool = False,
        on_tick: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__(name="hn-monitor-scheduler", daemon=True)
        self.store = store
        self.interval_seconds = max(5, int(interval_seconds))
        self.threshold = threshold
        self.config = config
        self.immediate = immediate
        self.on_tick = on_tick
        self._stop = threading.Event()

    def _tick(self) -> None:
        try:
            snap = refresh(self.store, config=self.config, threshold=self.threshold,
                           interval_seconds=self.interval_seconds)
            if self.on_tick:
                self.on_tick(f"tick ok mode={snap.mode} events={len(snap.events)}")
        except Exception as exc:  # noqa: BLE001 - 调度器必须吞掉异常保持存活
            self.store.append_fetch_log({"mode": "error", "note": f"{type(exc).__name__}: {exc}"})
            if self.on_tick:
                self.on_tick(f"tick error {type(exc).__name__}")

    def run(self) -> None:
        if self.immediate or self.store.load_state() is None:
            self._tick()
        while not self._stop.wait(self.interval_seconds):
            self._tick()

    def stop(self) -> None:
        self._stop.set()
