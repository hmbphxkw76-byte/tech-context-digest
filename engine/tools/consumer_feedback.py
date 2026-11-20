#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""消费端反馈台账（CONSUMER-FEEDBACK-LEDGER v1.0）。

把「读者反馈 → 纠错 / 回访」落成为可登记的闭环：报告页脚与 hub 页脚的
「反馈 / 纠错」入口（``report_style.feedback_link``）指向仓库 issue 追踪器，
本台账负责把经入口提交的条目**登记**下来，供消费侧指标（CF-01…CF-03）测量。

单一事实源：``engine/audit/records/consumer-feedback.json``。本工具只读写该文件，
不新增第二套台账；与 ``finding_rule.py``（生产侧 finding→规则）互为镜像。

确定性：无时间戳 / 无随机数；写盘按 ``entry_id`` 排序，``sort_keys=True``、
``indent=2``，同输入重放字节一致（``check`` 校验）。

用法：
    python engine/tools/consumer_feedback.py register --entry-id CFB-001 \
        --report content/economy/trends/reports/2026-11-20_weekly.html \
        --kind 纠错 --status open --source "github-issue #123" \
        [--note <text>] [--period 2026-11]
    python engine/tools/consumer_feedback.py list [--kind 纠错] [--status open]
    python engine/tools/consumer_feedback.py stats [--json]
    python engine/tools/consumer_feedback.py check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "engine" / "audit" / "records" / "consumer-feedback.json"
SPEC_ID = "CONSUMER-FEEDBACK-LEDGER v1.0"
SCHEMA_VERSION = "1.0"

# 条目类型：纠错（内容错误 / 口径问题）、回访（读者是否用于决策 / 读到哪一节）。
KINDS = ("纠错", "回访")
STATUSES = ("open", "resolved", "wontfix")
ENTRY_ID_RE = re.compile(r"^CFB-\d{3,}$")
REQUIRED_FIELDS = ("entry_id", "report", "kind", "status", "source", "note", "period")


# ---------------------------------------------------------------- 纯逻辑

def new_ledger() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "spec": SPEC_ID,
        "ledger": "consumer-feedback",
        "description": "消费端反馈台账：经报告 / hub 页脚「反馈 / 纠错」入口提交的纠错与回访条目。",
        "kinds": list(KINDS),
        "statuses": list(STATUSES),
        "records": [],
    }


def render(ledger: dict) -> str:
    """确定性序列化（排序 + sort_keys + indent=2 + 尾换行）。"""
    recs = sorted(ledger.get("records", []), key=lambda r: str(r.get("entry_id", "")))
    doc = {
        "schema_version": ledger.get("schema_version", SCHEMA_VERSION),
        "spec": ledger.get("spec", SPEC_ID),
        "ledger": ledger.get("ledger", "consumer-feedback"),
        "description": ledger.get("description", ""),
        "kinds": list(ledger.get("kinds", KINDS)),
        "statuses": list(ledger.get("statuses", STATUSES)),
        "records": recs,
    }
    return json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def load(path: Path = DEFAULT_PATH) -> dict:
    if not path.exists():
        return new_ledger()
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return new_ledger()


def save(ledger: dict, path: Path = DEFAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(ledger), encoding="utf-8")


def register(ledger: dict, entry_id: str, report: str, kind: str, status: str,
             source: str, note: str = "", period: str = "") -> tuple[dict, list[str]]:
    """登记一条反馈 -> (新台账, 错误说明)。"""
    errs: list[str] = []
    if not ENTRY_ID_RE.match(entry_id or ""):
        errs.append(f"entry_id 格式应为 CFB-NNN：{entry_id!r}")
    if kind not in KINDS:
        errs.append(f"kind 非法：{kind!r}（合法 {list(KINDS)}）")
    if status not in STATUSES:
        errs.append(f"status 非法：{status!r}（合法 {list(STATUSES)}）")
    if not str(report or "").strip():
        errs.append("report 为空")
    if not str(source or "").strip():
        errs.append("source 为空（须注明来源，如 github-issue #N）")
    if period and not re.fullmatch(r"\d{4}-\d{2}", period):
        errs.append(f"period 格式应为 YYYY-MM：{period!r}")
    ids = {str(r.get("entry_id")) for r in ledger.get("records", [])}
    if entry_id in ids:
        errs.append(f"entry_id 重复：{entry_id}")
    if errs:
        return ledger, errs
    rec = {"entry_id": entry_id, "report": report, "kind": kind, "status": status,
           "source": source, "note": note, "period": period}
    out = json.loads(json.dumps(ledger))  # 深拷贝
    out.setdefault("records", []).append(rec)
    return out, []


def stats(ledger: dict) -> dict:
    """消费侧统计（供 metric_coverage 的 CF-02 / CF-03 复用，不另写一套口径）。"""
    recs = ledger.get("records", [])
    corrections = [r for r in recs if r.get("kind") == "纠错"]
    revisits = [r for r in recs if r.get("kind") == "回访"]
    return {
        "total": len(recs),
        "correction_count": len(corrections),
        "revisit_count": len(revisits),
        "feedback_report_count": len({r.get("report") for r in recs}),
        "revisit_report_count": len({r.get("report") for r in revisits}),
        "by_status": {s: sum(1 for r in recs if r.get("status") == s) for s in STATUSES},
    }


def check(ledger: dict, path: Path = DEFAULT_PATH) -> list[str]:
    """schema / 确定性校验 -> 问题列表。"""
    issues: list[str] = []
    if ledger.get("spec") != SPEC_ID:
        issues.append(f"spec 非法：{ledger.get('spec')!r}")
    recs = ledger.get("records", [])
    seen: set[str] = set()
    for r in recs:
        rid = str(r.get("entry_id", ""))
        for f in REQUIRED_FIELDS:
            if f not in r:
                issues.append(f"{rid} 缺字段：{f}")
        if not ENTRY_ID_RE.match(rid):
            issues.append(f"entry_id 非法：{rid!r}")
        if rid in seen:
            issues.append(f"entry_id 重复：{rid}")
        seen.add(rid)
        if r.get("kind") not in KINDS:
            issues.append(f"{rid} kind 非法：{r.get('kind')!r}")
        if r.get("status") not in STATUSES:
            issues.append(f"{rid} status 非法：{r.get('status')!r}")
        if not str(r.get("report", "")).strip():
            issues.append(f"{rid} report 为空")
        if not str(r.get("source", "")).strip():
            issues.append(f"{rid} source 为空")
    ids = [str(r.get("entry_id", "")) for r in recs]
    if ids != sorted(ids):
        issues.append("records 未按 entry_id 排序")
    if path.exists() and path.read_text(encoding="utf-8") != render(ledger):
        issues.append("台账文件与确定性渲染不一致（请经本工具写入，勿手工编辑）")
    return issues


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="消费端反馈台账")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("register")
    p.add_argument("--entry-id", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--kind", required=True, help="纠错 / 回访")
    p.add_argument("--status", default="open", help="open / resolved / wontfix")
    p.add_argument("--source", required=True, help="来源（如 github-issue #123）")
    p.add_argument("--note", default="")
    p.add_argument("--period", default="", help="YYYY-MM")
    p.add_argument("--path", default=str(DEFAULT_PATH))
    p = sub.add_parser("list")
    p.add_argument("--kind", default=None)
    p.add_argument("--status", default=None)
    p.add_argument("--path", default=str(DEFAULT_PATH))
    p = sub.add_parser("stats")
    p.add_argument("--json", action="store_true")
    p.add_argument("--path", default=str(DEFAULT_PATH))
    p = sub.add_parser("check")
    p.add_argument("--path", default=str(DEFAULT_PATH))
    args = ap.parse_args()

    path = Path(args.path)
    ledger = load(path)

    if args.cmd == "register":
        new, errs = register(ledger, args.entry_id, args.report, args.kind,
                             args.status, args.source, args.note, args.period)
        for e in errs:
            print(f"[E] {e}")
        if errs:
            print(f"登记失败：{len(errs)} 项问题")
            return 1
        save(new, path)
        print(f"[OK] 已登记 {args.entry_id}（{args.kind} / {args.status}）")
        return 0

    if args.cmd == "list":
        recs = [r for r in ledger.get("records", [])
                if (args.kind is None or r.get("kind") == args.kind)
                and (args.status is None or r.get("status") == args.status)]
        if not recs:
            print("（无条目）")
            return 0
        for r in recs:
            print(f"{r['entry_id']}  {r['kind']:<2} {r['status']:<8} {r['report']}  "
                  f"{r['source']}")
        print(f"共 {len(recs)} 条")
        return 0

    if args.cmd == "stats":
        s = stats(ledger)
        if args.json:
            print(json.dumps(s, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        print(f"条目总数 {s['total']}；纠错 {s['correction_count']}；回访 {s['revisit_count']}")
        print(f"有反馈的报告 {s['feedback_report_count']}；有回访的报告 {s['revisit_report_count']}")
        print(f"状态分布：{s['by_status']}")
        return 0

    issues = check(ledger, path)
    for i in issues:
        print(f"[E] {i}")
    if issues:
        print(f"台账校验失败：{len(issues)} 项问题")
        return 1
    print(f"台账校验通过：{len(ledger.get('records', []))} 条记录，schema / 排序 / 确定性一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
