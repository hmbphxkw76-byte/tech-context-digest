#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""报告全流程审计留痕（pipeline_audit）。

为 pipeline_runner 提供**全链路追加式审计**：每一次节点执行、门禁判定、
路由 / 退回、闭环触发都写入 `engine/audit/records/pipeline_runs.jsonl`，
保证「每一步可监控、可完整回溯、可全链路复盘」。

设计约束：
- **只追加**：不覆盖、不修改历史记录（与审计报告留痕纪律一致）；
- **结构化**：每行一个 JSON 对象，字段固定（schema_version / ts / run_id / kind / ...）；
- **可回放**：read_run(run_id) 还原单次运行的时序链路。

用法：
    python engine/tools/pipeline_audit.py --run <run_id>
    python engine/tools/pipeline_audit.py --tail 20
    python engine/tools/pipeline_audit.py --rotate          # 超量归档轮转
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_PATH = ROOT / "engine" / "audit" / "records" / "pipeline_runs.jsonl"
ARCHIVE_DIR = AUDIT_PATH.parent / "archive"
DEFAULT_MAX_RECORDS = 200
DEFAULT_KEEP_ARCHIVES = 5
SCHEMA_VERSION = "1.0"


def _now() -> str:
    """ISO-8601（UTC），仅用于审计留痕（生成物确定性约束不适用于审计日志）。"""
    return datetime.now(timezone.utc).isoformat()


def append(record: dict, path: Path = AUDIT_PATH) -> dict:
    """追加一条审计记录（只增不改）。返回补全 ts / schema_version 后的记录。"""
    rec = {"schema_version": SCHEMA_VERSION, "ts": _now(), **record}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def read_all(path: Path = AUDIT_PATH) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def read_run(run_id: str, path: Path = AUDIT_PATH) -> list[dict]:
    return [r for r in read_all(path) if r.get("run_id") == run_id]


def tail(n: int = 20, path: Path = AUDIT_PATH) -> list[dict]:
    return read_all(path)[-n:]


def _archive_name(last_ts: str) -> str:
    safe = re.sub(r"[:/\\ ]", "-", last_ts or "unknown")
    return f"pipeline_runs-{safe}.jsonl"


def rotate(max_records: int = DEFAULT_MAX_RECORDS,
           keep_archives: int = DEFAULT_KEEP_ARCHIVES,
           path: Path = AUDIT_PATH) -> dict:
    """轮转审计运行流水：超过 max_records 行时归档并清空主文件。

    历史记录完整保留在 archive/pipeline_runs-<末条 ts>.jsonl（只迁移不丢弃），
    仅保留最近 keep_archives 份归档，避免 append-only 流水无限增长。
    """
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    lines = [ln for ln in lines if ln.strip()]
    if len(lines) <= max_records:
        return {"rotated": False, "records": len(lines),
                "archived": None, "pruned": []}

    archive_dir = path.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    last_ts = ""
    try:
        last_ts = json.loads(lines[-1]).get("ts", "")
    except json.JSONDecodeError:
        pass
    target = archive_dir / _archive_name(last_ts)
    n = 1
    while target.exists():
        target = archive_dir / _archive_name(last_ts).replace(".jsonl", f"-{n}.jsonl")
        n += 1
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.write_text("", encoding="utf-8")

    archives = sorted(archive_dir.glob("pipeline_runs-*.jsonl"), key=lambda p: p.name)
    pruned = []
    old = archives[:-keep_archives] if keep_archives > 0 else archives
    for p in old:
        p.unlink()
        pruned.append(p.name)
    return {"rotated": True, "records": len(lines),
            "archived": target.name, "pruned": pruned}


def main() -> int:
    ap = argparse.ArgumentParser(description="报告全流程审计留痕查询")
    ap.add_argument("--run", help="按 run_id 还原单次运行链路")
    ap.add_argument("--tail", type=int, default=20, help="查看最近 N 条")
    ap.add_argument("--rotate", action="store_true", help="轮转审计流水（超量归档）")
    ap.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS,
                    help=f"主文件行数阈值（默认 {DEFAULT_MAX_RECORDS}）")
    ap.add_argument("--keep", type=int, default=DEFAULT_KEEP_ARCHIVES,
                    help=f"保留归档份数（默认 {DEFAULT_KEEP_ARCHIVES}）")
    ap.add_argument("--path", default=str(AUDIT_PATH),
                    help="审计流水文件路径（默认 engine/audit/records/pipeline_runs.jsonl）")
    args = ap.parse_args()

    if args.rotate:
        print(json.dumps(rotate(args.max_records, args.keep, path=Path(args.path)),
                         ensure_ascii=False))
        return 0

    if args.run:
        rows = read_run(args.run)
        if not rows:
            print(f"[WARN] 未找到 run_id={args.run}")
            return 2
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
        return 0

    rows = tail(args.tail)
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
