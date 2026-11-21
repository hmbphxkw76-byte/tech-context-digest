"""事实卡片门禁（INFORMATION-LAYERING-SPEC v1.0 第五节）。

检查：
    FC-01 卡片库结构：字段齐全、card_id 唯一、枚举合法、来源非空
    FC-02 报告引用可解析：报告内 [FC-…] 引用必须命中卡片库
    FC-03 共享域覆盖：有事实卡片库的业务线（动态派生自卡片库 used_by）的
         新报告须至少引用 1 张卡片（历史报告只警告）
    FC-04 跨层一致性：卡片 level 不得高于 verify_status 允许上限（调用
         verification_vocab.is_consistent，恒 [W]，不阻断；词表归一后判定）

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
from gate_period import AUTO  # noqa: E402
from gate_period import resolve as resolve_period
from verification_vocab import (  # noqa: E402
    consistency_issue,
    is_consistent,
    normalize_card_status,
    normalize_info_level,
)

DEFAULT_GATE = AUTO
CARD_DIR = ROOT / "engine" / "fact_cards"
REQUIRED_FIELDS = ("card_id", "fact", "source", "tier", "verify_status", "level", "updated", "indicators")
VALID_TIERS = {1, 2, 3, 4}
VALID_VERIFY = {"已核验", "部分核验", "未核验"}
VALID_LEVEL = {"已核验事实", "部分核验", "推断", "假设"}
FC_RE = re.compile(r"\[FC-([A-Z]+)-(\d+)\]")


def shared_fact_tokens(cards: dict[str, dict]) -> set[str]:
    """共享事实域业务线标识：由卡片库 used_by 动态派生（单一事实源）。"""
    tokens: set[str] = set()
    for c in cards.values():
        for bl in c.get("used_by", []) or []:
            tokens.add(str(bl))
    return tokens


def _in_shared(line: str, tokens: set[str]) -> bool:
    """业务线 rel 的任一路径段命中卡片库 used_by 标识即视为共享事实域。"""
    return bool(set(Path(line).parts) & tokens)


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
            if normalize_card_status(c["verify_status"]) is None:
                errors.append(f"{cid}：verify_status 非法 {c['verify_status']}"
                              f"（须为 {' / '.join(sorted(VALID_VERIFY))} 或其英文同义）")
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

    stats = {"cards": len(cards), "reports": 0, "refs": 0, "missing_refs": 0,
             "inconsistent_cards": 0}
    # FC-04 卡片信息等级 ≤ 核验状态上限（结构化一致性，恒 [W]）。
    # 合法性（枚举 / 词形）由 FC-01 负责，此处只在两值均可归一后判定，避免重复告警。
    for cid in sorted(cards):
        c = cards[cid]
        level = normalize_info_level(c["level"])
        status = normalize_card_status(c["verify_status"])
        if level is None or status is None:
            continue
        if not is_consistent(level, status, "card"):
            stats["inconsistent_cards"] += 1
            warnings += 1
            lines.append(f"[W] 事实卡片库{consistency_issue(level, status, 'card', where=cid)}"
                         f"（FC-04，不阻断）")
    tokens = shared_fact_tokens(cards)
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
        if _in_shared(bline, tokens) and not refs:
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
        print(f"事实卡片门禁：{warnings} 项警告（不阻断；含 FC-04 越级卡片 "
              f"{stats['inconsistent_cards']} 张）")
        return 2
    print(f"事实卡片门禁通过：卡片 {stats['cards']} 张，引用 {stats['refs']} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
