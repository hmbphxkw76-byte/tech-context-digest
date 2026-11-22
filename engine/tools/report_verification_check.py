#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""报告层信息核验门禁（INFORMATION-VERIFICATION-SPEC v1.0 报告层一致性）。

背景：``fact_card_check`` FC-04 只校验**卡片层** ``level ≤ verify_status``；
报告层「信息等级 ↔ 来源核验状态」的逐条一致性长期缺位（规范原列为二期）。
本模块补齐该缺口，使「未核验信息」不得在报告中被呈现为已核验 / 部分核验。

检查项（新报告 [E] 阻断 / 历史报告 [W] 不追溯，两级 gate-period）：

    RV-01 决策摘要纯净：``decision-summary`` 区块内不得出现
         ``lvl-inferred`` / ``lvl-assumption``，不得出现指向 ``unverifiable``
         来源的链接，也不得出现「未核验」来源状态文本。
    RV-02 未核验来源呈现：标注 ``lvl-verified`` / ``lvl-partial`` 的陈述单元，
         若其链接的来源核验状态为 ``unverifiable``（且单元内无已核验 /
         部分核验来源支撑），或标注 ``lvl-verified`` 却仅链接
         ``media_unverified`` 来源，即判不一致。
    RV-03 来源状态文本一致：单元内显式来源状态文本（``· 未核验`` /
         ``· 部分核验``）与 ``lvl-*`` 标记冲突时判不一致。

来源状态取自各业务线 ``data/processed/**/source_registry.json``（R8 约定），
链接按归一化 URL 精确匹配，避免机构名缩写导致的模糊误判。

退出码：0 通过；1 存在 [E]；2 仅 [W]。

用法：
    python engine/tools/report_verification_check.py
    python engine/tools/report_verification_check.py --json
    python engine/tools/report_verification_check.py --gate-period 2026-12
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
from gate_period import resolve as resolve_period  # noqa: E402

DEFAULT_GATE = AUTO
REGISTRY_GLOB = "source_registry.json"

LVL_RE = re.compile(r'class="lvl lvl-(verified|partial|inferred|assumption)"')
HREF_RE = re.compile(r'<a\b[^>]*href="([^"]+)"')
STATUS_TEXT_RE = re.compile(r'(?:·|•|\|)\s*(已核验|部分核验|未核验)')
DECISION_OPEN_RE = re.compile(r'<div class="decision-summary">')
DIV_TOKEN_RE = re.compile(r'<div\b|</div>')

# 信息等级 -> 允许的最低来源状态（用于 RV-02 判定）
LVL_ALLOW = {
    "verified": {"verified"},
    "partial": {"verified", "media_unverified"},
}


# ---------------------------------------------------------------- 来源索引
def _norm_url(u) -> str:
    if not isinstance(u, str):
        return ""
    u = u.strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.rstrip("/")


def load_sources() -> tuple[dict[str, list[tuple[str, str, str]]], list[str]]:
    """-> (归一化 URL -> [(verify_status, business_line, source_id)], errors)。"""
    by_url: dict[str, list[tuple[str, str, str]]] = {}
    errors: list[str] = []
    roots = sorted((ROOT / "data" / "processed").rglob(REGISTRY_GLOB))
    if not roots:
        errors.append("未找到任何 source_registry.json（data/processed/**）")
    for p in roots:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{p.relative_to(ROOT).as_posix()}：JSON 解析失败 {e}")
            continue
        bline = data.get("business_line", "")
        for s in data.get("sources", []) or []:
            url = _norm_url(s.get("url", ""))
            if not url:
                continue
            by_url.setdefault(url, []).append(
                (s.get("verify_status", ""), bline, s.get("source_id", "")))
    return by_url, errors


# ---------------------------------------------------------------- 报告单元
def _decision_blocks(text: str) -> list[tuple[int, int]]:
    """-> [(start, end)]：``decision-summary`` 区块的字符区间（处理嵌套 div）。"""
    spans: list[tuple[int, int]] = []
    for m in DECISION_OPEN_RE.finditer(text):
        i, depth = m.end(), 1
        while i < len(text) and depth:
            tok = DIV_TOKEN_RE.search(text, i)
            if not tok:
                break
            depth += 1 if tok.group(0).startswith("<div") else -1
            i = tok.end()
        spans.append((m.start(), i))
    return spans


def _in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(a <= pos < b for a, b in spans)


def iter_report_units(text: str):
    """-> [(unit_html, is_decision)]（tr / li / p 块级单元）。

    只取 **非嵌套** 块级标签：报表表格行（tr）、列表项（li）、段落（p）。
    不取通用 div——报告用 div 包裹整表 / 时间线，会把多个陈述并成一个单元，
    导致「单元内来源集合」被稀释而漏判。
    """
    spans = _decision_blocks(text)
    out = []
    for m in re.finditer(r'<(tr|li|p)\b.*?</\1>', text, re.DOTALL):
        out.append((m.group(0), _in_spans(m.start(), spans)))
    return out


def iter_reports() -> list[tuple[str, str, str]]:
    """-> [(relpath, period, text)]。"""
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            det = detect_report(f.name)
            out.append((f"{b.rel}/reports/{f.name}",
                        det[1] if det else "", f.read_text(encoding="utf-8", errors="replace")))
    return out


# ---------------------------------------------------------------- 周期
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


# ---------------------------------------------------------------- 主流程
def run(gate: str, sources: dict[str, list[tuple[str, str, str]]] | None = None,
        reports: list[tuple[str, str, str]] | None = None
        ) -> tuple[int, int, list[str], dict]:
    gate = resolve_period(gate)
    errors = warnings = 0
    lines: list[str] = []
    if sources is None:
        by_url, src_errors = load_sources()
        for msg in src_errors:
            errors += 1
            lines.append(f"[E] 来源登记：{msg}")
    else:
        by_url = sources
    if reports is None:
        reports = iter_reports()

    stats = {"reports": 0, "units": 0, "decision_units": 0,
             "unverifiable_links": 0, "rv01": 0, "rv02": 0, "rv03": 0}

    def flag(rel: str, rule: str, is_new: bool, msg: str) -> None:
        nonlocal errors, warnings
        if is_new:
            errors += 1
            lines.append(f"[E] {rel}：{msg}（{rule}）")
        else:
            warnings += 1
            lines.append(f"[W] {rel}：{msg}（{rule}，历史不追溯）")

    for rel, period, text in reports:
        stats["reports"] += 1
        is_new = bool(period) and _period_key(period) >= _period_key(gate)
        for unit, is_decision in iter_report_units(text):
            lvl_m = LVL_RE.search(unit)
            if not lvl_m:
                continue
            stats["units"] += 1
            if is_decision:
                stats["decision_units"] += 1
            lvl = lvl_m.group(1)
            statuses = set()
            for href in HREF_RE.findall(unit):
                for st, _bl, _sid in by_url.get(_norm_url(href), []):
                    statuses.add(st)
            if "unverifiable" in statuses:
                stats["unverifiable_links"] += 1

            # RV-01 决策摘要纯净
            if is_decision:
                if lvl in ("inferred", "assumption"):
                    stats["rv01"] += 1
                    flag(rel, "RV-01", is_new,
                         f"决策摘要出现「{lvl}」信息等级（仅允许已核验 / 部分核验）")
                if "unverifiable" in statuses:
                    stats["rv01"] += 1
                    flag(rel, "RV-01", is_new, "决策摘要链接未核验（unverifiable）来源")
                if "未核验" in unit:
                    stats["rv01"] += 1
                    flag(rel, "RV-01", is_new, "决策摘要出现「未核验」来源状态文本")

            # RV-02 未核验来源呈现
            if lvl in ("verified", "partial"):
                allowed = LVL_ALLOW[lvl]
                if "unverifiable" in statuses and not (statuses & allowed):
                    stats["rv02"] += 1
                    flag(rel, "RV-02", is_new,
                         f"信息等级「{lvl}」的陈述仅链接未核验（unverifiable）来源")
                elif lvl == "verified" and "verified" not in statuses \
                        and "media_unverified" in statuses:
                    stats["rv02"] += 1
                    flag(rel, "RV-02", is_new,
                         "信息等级「已核验」的陈述仅链接部分核验（media_unverified）来源")

            # RV-03 来源状态文本一致
            stm = STATUS_TEXT_RE.search(unit)
            if stm:
                text_status = stm.group(1)
                bad = ((text_status == "未核验" and lvl in ("verified", "partial"))
                       or (text_status == "部分核验" and lvl == "verified"))
                if bad:
                    stats["rv03"] += 1
                    flag(rel, "RV-03", is_new,
                         f"来源状态文本「{text_status}」与信息等级「{lvl}」冲突")
    return errors, warnings, lines, stats


def main() -> int:
    ap = argparse.ArgumentParser(description="报告层信息核验门禁")
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
        print(f"报告层信息核验门禁失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"报告层信息核验门禁：{warnings} 项警告（不阻断）")
        return 2
    print(f"报告层信息核验门禁通过：报告 {stats['reports']} 份，"
          f"等级单元 {stats['units']} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
