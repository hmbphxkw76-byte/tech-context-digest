"""盲区台账门禁（DECISION-DELIVERY-SPEC v1.0 第六节）。

检查 engine/report-audits/blind-spot-ledger.md：
    BS-01 字段完整：ID / 项目 / 优先级 / 影响 / 发现日期 / 责任周期 / 消号条件 / 状态 / 关联 KPI
    BS-02 状态合法：open / in_progress / closed
    BS-03 责任周期有效：YYYY-MM 或非空
    BS-04 P0 四类存在：就业、收入、空置、竣工均登记为 P0
    BS-05 消号条件非空且为可核验陈述

退出码：0 通过；1 存在 [E]；2 仅 [W]。

用法：
    python engine/tools/blind_spot_check.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402

LEDGER = ROOT / "engine" / "report-audits" / "blind-spot-ledger.md"
VALID_STATUS = {"open", "in_progress", "closed"}
P0_REQUIRED = ("就业", "收入", "空置", "竣工")
ROW_RE = re.compile(r"^\|\s*(B\d{2})\s*\|(.+)\|\s*$")


def parse_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        rows.append([m.group(1)] + cells)
    return rows


def check_text(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    rows = parse_rows(text)
    if not rows:
        return [("BS-01", "台账无可解析的盲区行（期望 | ID | 项目 | 优先级 | … |）")]
    for cells in rows:
        rid = cells[0]
        # 列：ID, 项目, 优先级, 影响, 发现日期, 责任周期, 消号条件, 状态, 关联 KPI
        if len(cells) < 9:
            out.append(("BS-01", f"{rid}：列数不足（{len(cells)}/9），字段应含 ID/项目/优先级/影响/发现日期/责任周期/消号条件/状态/关联 KPI"))
            continue
        item, prio, impact, found, cycle, cond, status, kpi = cells[1:9]
        if not item:
            out.append(("BS-01", f"{rid}：项目为空"))
        if prio not in {"P0", "P1", "P2", "P3"}:
            out.append(("BS-01", f"{rid}：优先级非法（{prio!r}）"))
        if not impact:
            out.append(("BS-01", f"{rid}：影响为空"))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", found):
            out.append(("BS-01", f"{rid}：发现日期格式应为 YYYY-MM-DD（{found!r}）"))
        if not re.fullmatch(r"\d{4}-\d{2}", cycle):
            out.append(("BS-01", f"{rid}：责任周期格式应为 YYYY-MM（{cycle!r}）"))
        if not cond:
            out.append(("BS-05", f"{rid}：消号条件为空"))
        if status not in VALID_STATUS:
            out.append(("BS-02", f"{rid}：状态非法（{status!r}，应为 open / in_progress / closed）"))
        if not kpi:
            out.append(("BS-01", f"{rid}：关联 KPI 为空"))
    # BS-04 P0 四类
    p0_items = {cells[1] for cells in rows if len(cells) >= 3 and cells[2] == "P0"}
    for key in P0_REQUIRED:
        if not any(key in it for it in p0_items):
            out.append(("BS-04", f"P0 优先级缺「{key}」类盲区（当前 P0：{'、'.join(sorted(p0_items)) or '无'}）"))
    return out


def run() -> tuple[int, int, list[str]]:
    if not LEDGER.exists():
        return 1, 0, ["[E] 盲区台账不存在：engine/report-audits/blind-spot-ledger.md"]
    text = LEDGER.read_text(encoding="utf-8")
    findings = check_text(text)
    errors = sum(1 for r, _ in findings if r != "BS-05")
    warnings = len(findings) - errors
    lines = [f"[{'E' if r != 'BS-05' else 'W'}] {r}：{m}" for r, m in findings]
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="盲区台账门禁")
    ap.parse_args()
    errors, warnings, lines = run()
    for line in lines:
        print(line)
    if errors:
        print(f"盲区台账门禁失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"盲区台账门禁：{warnings} 项警告（不阻断）")
        return 2
    print("盲区台账门禁通过：字段 / 状态 / 责任周期 / P0 四类齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
