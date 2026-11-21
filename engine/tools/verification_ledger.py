#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""核验台账哈希链（INFORMATION-VERIFICATION-SPEC v1.0 第 2 节）。

参照「来源核验留痕」思路，为本仓库建立 **append-only 核验台账**：
每一次来源核验（登记 / 复核 / 状态变更）都追加一条事件，事件通过
``hash = sha256(prev_hash + canonical_json(payload))`` 串联成哈希链，
使「核验记录被篡改 / 删减」可被机器判定。

台账文件：``engine/audit/records/verification_ledger.jsonl``（生成物豁免路径，
确定性可重放；事件按 seq 递增追加，**禁止重写既有行**）。

事件结构（每行一个 JSON）：
    {"seq": 1, "prev_hash": "<64hex>", "hash": "<64hex>", "ts": "...",
     "actor": "agent", "event": "source_verified", "payload": {...}}

  - ``ts`` 为追加时刻（元数据，不入 hash，便于确定性重放）；
  - ``payload`` 为业务字段（business_line / source_id / verify_status /
    method / snapshot_date / archive_hash / report 等），参与哈希。

子命令：
    verify                       校验链完整性（seq 连续 / prev_hash 链接 / hash 重算）
    status                       台账统计（条数 / 事件类型 / 覆盖业务线）
    backfill --force             从现有 source_registry.json 回填初始台账（幂等）
    append --event E --payload J 追加一条事件（供人工 / 脚本留痕）

退出码：0 通过；1 链断裂 / 存在错误；2 用法错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs, processed_data_dir  # noqa: E402

LEDGER_PATH = ROOT / "engine" / "audit" / "records" / "verification_ledger.jsonl"
LEDGER_SCHEMA = "1.0"
GENESIS_HASH = "0" * 64

# 事件类型（受控词表；新增须同步 INFORMATION-VERIFICATION-SPEC 第 2 节）
EVENT_SOURCE_VERIFIED = "source_verified"
EVENT_SOURCE_REVIEWED = "source_reviewed"
EVENT_SOURCE_STATUS_CHANGED = "source_status_changed"
KNOWN_EVENTS = (EVENT_SOURCE_VERIFIED, EVENT_SOURCE_REVIEWED,
                EVENT_SOURCE_STATUS_CHANGED)


# ── 基础 ────────────────────────────────────────────────────────────────────
def canonical_json(obj) -> str:
    """确定性 JSON（排序键、紧凑分隔、保留非 ASCII）。"""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), default=str)


def compute_hash(prev_hash: str, payload: dict) -> str:
    """sha256(prev_hash + canonical_json(payload))。"""
    return hashlib.sha256(
        (prev_hash + canonical_json(payload)).encode("utf-8")).hexdigest()


def _ledger_path(ledger_path: str | Path | None = None) -> Path:
    return Path(ledger_path) if ledger_path else LEDGER_PATH


def iter_events(ledger_path: str | Path | None = None) -> list[dict]:
    """读取台账全部事件（文件不存在返回空列表）。"""
    p = _ledger_path(ledger_path)
    if not p.exists():
        return []
    out: list[dict] = []
    for ln, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        try:
            out.append(json.loads(s))
        except json.JSONDecodeError as e:
            raise ValueError(f"台账第 {ln} 行非法 JSON：{e}") from e
    return out


def last_event(ledger_path: str | Path | None = None) -> dict | None:
    evs = iter_events(ledger_path)
    return evs[-1] if evs else None


# ── 校验 ────────────────────────────────────────────────────────────────────
def verify(ledger_path: str | Path | None = None) -> tuple[bool, list[str], dict]:
    """校验哈希链 -> (ok, problems, stats)。

    校验三项：① seq 从 1 连续递增；② 每条 prev_hash 等于上一条 hash
    （首条为 GENESIS_HASH）；③ 每条 hash 由 prev_hash + payload 重算一致。
    空台账视为合法（尚未启用）。
    """
    p = _ledger_path(ledger_path)
    problems: list[str] = []
    stats = {"records": 0, "events": {}, "business_lines": 0}
    if not p.exists():
        return True, problems, stats
    prev = GENESIS_HASH
    records = 0
    events: dict[str, int] = {}
    lines: list[str] = []
    try:
        lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    except OSError as e:
        return False, [f"台账读取失败：{e}"], stats
    for i, line in enumerate(lines, 1):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            problems.append(f"第 {i} 行非法 JSON：{e}")
            continue
        records += 1
        seq = rec.get("seq")
        if seq != i:
            problems.append(f"第 {i} 行 seq={seq!r} 不连续（应为 {i}）")
        if rec.get("prev_hash") != prev:
            problems.append(f"第 {i} 行 prev_hash 断裂（存 {rec.get('prev_hash')!r}，应 {prev!r}）")
        payload = rec.get("payload", {})
        expect = compute_hash(prev, payload if isinstance(payload, dict) else {})
        if rec.get("hash") != expect:
            problems.append(f"第 {i} 行 hash 校验失败（存 {rec.get('hash')!r}，算 {expect!r}）")
        ev = str(rec.get("event", ""))
        events[ev] = events.get(ev, 0) + 1
        prev = rec.get("hash") if isinstance(rec.get("hash"), str) else prev
    stats["records"] = records
    stats["events"] = events
    bls = {str(r.get("payload", {}).get("business_line", "")) for r in map(_safe_json, lines)}
    stats["business_lines"] = len({b for b in bls if b})
    return (not problems), problems, stats


def _safe_json(line: str):
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return {}


# ── 追加 ────────────────────────────────────────────────────────────────────
def append(event: str, payload: dict, actor: str = "agent",
           ledger_path: str | Path | None = None,
           ts: str | None = None) -> dict:
    """追加一条事件（append-only）-> 新记录。

    绝不重写既有行；``ts`` 缺省留空（由调用方 / CI 提供，避免非确定性）。
    """
    if event not in KNOWN_EVENTS:
        raise ValueError(f"未知事件类型：{event}（须为 {' / '.join(KNOWN_EVENTS)}）")
    p = _ledger_path(ledger_path)
    last = last_event(p)
    prev = last["hash"] if last else GENESIS_HASH
    seq = (last["seq"] + 1) if last else 1
    rec = {
        "seq": seq,
        "prev_hash": prev,
        "hash": compute_hash(prev, payload),
        "ts": ts or "",
        "actor": actor,
        "event": event,
        "payload": payload,
    }
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(canonical_json(rec) + "\n")
    return rec


# ── 回填 ────────────────────────────────────────────────────────────────────
def collect_registries() -> list[tuple[str, dict]]:
    """-> [(business_line, registry)]，按 business_line 排序（确定性）。"""
    out: list[tuple[str, dict]] = []
    for b in iter_business_dirs():
        reg_path = processed_data_dir(b.rel) / "source_registry.json"
        if not reg_path.exists():
            continue
        try:
            data = json.loads(reg_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        out.append((b.rel, data))
    return sorted(out, key=lambda kv: kv[0])


def backfill_from_registries(actor: str = "backfill", force: bool = False,
                             ledger_path: str | Path | None = None) -> int:
    """从现有 source_registry 回填初始台账 -> 追加条数。

    幂等：台账已非空且未 ``force`` 时返回 0（不重复回填）。
    确定性：按 (business_line, source_id) 排序后追加。
    """
    p = _ledger_path(ledger_path)
    if p.exists() and p.stat().st_size > 0 and not force:
        return 0
    n = 0
    for business_line, reg in collect_registries():
        sources = reg.get("sources", []) if isinstance(reg, dict) else []
        for s in sorted(sources, key=lambda x: str(x.get("source_id", ""))):
            ev = (EVENT_SOURCE_STATUS_CHANGED if s.get("verify_status") in
                  ("media_unverified", "unverifiable") else EVENT_SOURCE_VERIFIED)
            append(ev, {
                "business_line": business_line,
                "source_id": str(s.get("source_id", "")),
                "verify_status": str(s.get("verify_status", "")),
                "method": str((s.get("evidence") or {}).get("method", "")),
                "snapshot_date": str((s.get("evidence") or {}).get("snapshot_date", "")),
                "archive_hash": str((s.get("evidence") or {}).get("archive_hash", "")),
            }, actor=actor, ledger_path=p)
            n += 1
    return n


# ── CLI ─────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="核验台账哈希链")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verify", help="校验链完整性")
    sub.add_parser("status", help="台账统计")
    p = sub.add_parser("backfill", help="从 source_registry 回填初始台账")
    p.add_argument("--force", action="store_true", help="台账非空时仍重填")
    p.add_argument("--actor", default="backfill")
    p = sub.add_parser("append", help="追加一条事件")
    p.add_argument("--event", required=True, choices=KNOWN_EVENTS)
    p.add_argument("--payload", required=True, help="JSON 对象字符串")
    p.add_argument("--actor", default="agent")
    p.add_argument("--ts", default="")
    args = ap.parse_args()

    if args.cmd == "verify":
        ok, problems, stats = verify()
        print(f"核验台账：{stats['records']} 条记录，覆盖 "
              f"{stats['business_lines']} 条业务线，事件 {stats['events']}")
        for m in problems:
            print(f"[E] {m}")
        if not ok:
            print(f"核验台账校验失败：{len(problems)} 处问题（链断裂 / 篡改）")
            return 1
        print("核验台账校验通过：seq 连续、prev_hash 链接、hash 重算一致")
        return 0

    if args.cmd == "status":
        ok, problems, stats = verify()
        print(json.dumps({"ok": ok, "problems": problems, **stats},
                         ensure_ascii=False, indent=2))
        return 0 if ok else 1

    if args.cmd == "backfill":
        n = backfill_from_registries(actor=args.actor, force=args.force)
        print(f"核验台账回填：追加 {n} 条事件")
        return 0

    if args.cmd == "append":
        try:
            payload = json.loads(args.payload)
        except json.JSONDecodeError as e:
            print(f"[E] --payload 非法 JSON：{e}")
            return 2
        if not isinstance(payload, dict):
            print("[E] --payload 须为 JSON 对象")
            return 2
        rec = append(args.event, payload, actor=args.actor, ts=args.ts)
        print(f"已追加 seq={rec['seq']} hash={rec['hash']}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
