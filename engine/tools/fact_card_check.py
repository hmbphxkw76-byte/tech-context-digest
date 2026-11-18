"""事实卡片门禁（INFORMATION-LAYERING-SPEC v1.0 第五节）。

检查：
    FC-01 卡片库结构：字段齐全、card_id 唯一、枚举合法、来源非空
    FC-02 报告引用可解析：报告内 [FC-…] 引用必须命中卡片库
    FC-03 共享域覆盖：security / industry-research / competitive-intelligence 的
         新报告须至少引用 1 张卡片（历史报告只警告）

退出码：0 通过；1 存在 [E]；2 仅 [W]。

用法：
    python engine/tools/fact_card_check.py
    python engine/tools/fact_card_check.py --json
    python engine/tools/fact_card_check.py --gate-period 2026-12
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, detect_report, iter_business_dirs  # noqa: E402
from gate_period import AUTO, resolve as resolve_period  # noqa: E402

DEFAULT_GATE = AUTO
CARD_DIR = ROOT / "engine" / "fact_cards"
REQUIRED_FIELDS = ("card_id", "fact", "source", "tier", "verify_status", "level", "updated", "indicators")
VALID_TIERS = {1, 2, 3, 4}
VALID_VERIFY = {"已核验", "部分核验", "未核验"}
VALID_LEVEL = {"已核验事实", "部分核验", "推断", "假设"}
FC_RE = re.compile(r"\[FC-([A-Z]+)-(\d+)\]")
SHARED_DOMAINS = ("security", "industry-research", "competitive-intelligence")


def load_cards() -> tuple[dict[str, dict], list[str]]:
    """-> (cards by id, errors)。"""
    cards: dict[str, dict] = {}
    errors: list[str] = []
    if not CARD_DIR.is_dir():
        return cards, [f"事实卡片目录不存在：{CARD_DIR.relative_to(ROOT).as_posix()}"]
    for f in sorted(CARD_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{f.name}：JSON 解析失败 {e}")
            continue
        for c in data.get("cards", []):
            missing = [k for k in REQUIRED_FIELDS if k not in c]
            if missing:
                errors.append(f"{f.name}：卡片缺字段 {missing}（{c.get('card_id', '?')}）")
                continue
            cid = c["card_id"]
            if cid in cards:
                errors.append(f"{f.name}：card_id 重复 {cid}")
                continue
            if c["tier"] not in VALID_TIERS:
                errors.append(f"{cid}：tier 非法 {c['tier']}")
            if c["verify_status"] not in VALID_VERIFY:
                errors.append(f"{cid}：verify_status 非法 {c['verify_status']}")
            if c["level"] not in VALID_LEVEL:
                errors.append(f"{cid}：level 非法 {c['level']}")
            if not str(c["source"]).strip():
                errors.append(f"{cid}：source 为空")
            if not isinstance(c["indicators"], list):
                errors.append(f"{cid}：indicators 须为列表")
            cards[cid] = c
    return cards, errors


def _period_key(period: str) -> tuple:
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", period)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{4})-(\d{2})", period)
    if m:
        return (int(m.group(1)), int(m.group(2)), 0)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if m:
        return (int(m.group(1)), int(m.group(2)) * 3, 0)
    m = re.fullmatch(r"(\d{4})", period)
    if m:
        return (int(m.group(1)), 12, 31)
    return (0, 0, 0)


def _period_of(name: str) -> str:
    det = detect_report(name)
    return det[1] if det else ""


def iter_report_refs():
    """-> [(relpath, text, period, business_line)]。"""
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            out.append((f"{b.rel}/reports/{f.name}",
                        f.read_text(encoding="utf-8", errors="replace"),
                        _period_of(f.name), b.rel))
    return out


def run(gate: str) -> tuple[int, int, list[str], dict]:
    gate = resolve_period(gate)
    errors = warnings = 0
    lines: list[str] = []
    cards, card_errors = load_cards()
    for msg in card_errors:
        errors += 1
        lines.append(f"[E] 事实卡片库：{msg}")
    if not cards and not card_errors:
        errors += 1
        lines.append("[E] 事实卡片库：未找到任何卡片")

    stats = {"cards": len(cards), "reports": 0, "refs": 0, "missing_refs": 0}
    for rel, text, period, bline in iter_report_refs():
        stats["reports"] += 1
        refs = {f"FC-{m.group(1)}-{int(m.group(2)):03d}" for m in FC_RE.finditer(text)}
        stats["refs"] += len(refs)
        for cid in sorted(refs):
            if cid not in cards:
                stats["missing_refs"] += 1
                errors += 1
                lines.append(f"[E] {rel}：引用不存在的卡片 {cid}")
        is_new = bool(period) and _period_key(period) >= _period_key(gate)
        if any(d in bline for d in SHARED_DOMAINS) and not refs:
            if is_new:
                errors += 1
                lines.append(f"[E] {rel}：共享事实域新报告未引用任何 [FC-…] 卡片")
            else:
                warnings += 1
                lines.append(f"[W] {rel}：共享事实域历史报告未引用 [FC-…] 卡片（不阻断）")
    return errors, warnings, lines, stats


def main() -> int:
    ap = argparse.ArgumentParser(description="事实卡片门禁")
    ap.add_argument("--gate-period", default=DEFAULT_GATE)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    errors, warnings, lines, stats = run(args.gate_period)
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "stats": stats,
                          "lines": lines}, ensure_ascii=False, indent=2))
    else:
        for line in lines:
            print(line)
    if errors:
        print(f"事实卡片门禁失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"事实卡片门禁：{warnings} 项历史报告警告（不阻断）")
        return 2
    print(f"事实卡片门禁通过：卡片 {stats['cards']} 张，引用 {stats['refs']} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
