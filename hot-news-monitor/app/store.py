"""运行时存储：state.json 快照 + fetch_log.jsonl / items.jsonl 台账。

- state.json：最近一次全量快照（Snapshot.to_dict），写前先备份为 state.prev.json；
  写采用 tmp + replace 原子替换，损坏时可回退 prev，保证断点恢复。
- runtime/ 目录整体不入库（见 hot-news-monitor/.gitignore）。
- 台账 append-only：items.jsonl 以 item.id 去重，fetch_log.jsonl 记录每次刷新结果。
"""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .models import NewsItem, Snapshot


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Store:
    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root) if root else Path(__file__).resolve().parents[1] / "runtime"
        self.state_path = self.root / "state.json"
        self.prev_path = self.root / "state.prev.json"
        self.log_path = self.root / "fetch_log.jsonl"
        self.items_path = self.root / "items.jsonl"

    def ensure(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------ state
    def save_state(self, snapshot: Snapshot) -> None:
        """原子写入快照；prev 恒为最近一次成功快照，供文件损坏时回退。"""
        self.ensure()
        data = snapshot.to_dict()
        tmp = self.root / "state.tmp.json"
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, self.state_path)
        shutil.copy2(self.state_path, self.prev_path)

    def load_state(self) -> Snapshot | None:
        """读取快照；主文件缺失 / 损坏时回退 state.prev.json。"""
        for path in (self.state_path, self.prev_path):
            if not path.exists():
                continue
            try:
                return Snapshot.from_dict(json.loads(path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
        return None

    # ------------------------------------------------------------ ledger
    def append_fetch_log(self, record: dict[str, Any]) -> None:
        self.ensure()
        record = {"ts": utc_now_iso(), **record}
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    def append_items(self, items: Iterable[NewsItem]) -> int:
        """台账追加（按 id 去重），返回新增条数。"""
        self.ensure()
        seen: set[str] = set()
        if self.items_path.exists():
            for line in self.items_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    seen.add(str(json.loads(line)["id"]))
                except (json.JSONDecodeError, KeyError):
                    continue
        added = 0
        with self.items_path.open("a", encoding="utf-8") as fh:
            for it in items:
                if it.id in seen:
                    continue
                seen.add(it.id)
                fh.write(json.dumps(it.to_dict(), ensure_ascii=False) + "\n")
                added += 1
        return added

    def known_item_ids(self) -> set[str]:
        ids: set[str] = set()
        if not self.items_path.exists():
            return ids
        for line in self.items_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ids.add(str(json.loads(line)["id"]))
            except (json.JSONDecodeError, KeyError):
                continue
        return ids
