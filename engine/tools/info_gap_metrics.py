#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""信息差指数（IGI，Information Gap Index）实测计算。

目标：把「消除信息差」从口号变成可计算、可比较、可证明的指标。八度口径的唯一
事实源是 `metrics-dictionary.json` 的 IGI-01..IGI-08；本模块只负责**测量**。

  IGI-01 主题覆盖率   = 有业务线（business-config）的主题数 / layout.json 注册主题数
  IGI-02 业务线覆盖率 = 有 ≥1 份正式报告的业务线数 / 已声明业务线数
  IGI-03 时效健康度   = 最新报告期次距当前 ≤1 个节拍周期的业务线占比
  IGI-04 来源登记覆盖率 = 报告内外部 URL 能在对应 source_registry 匹配的比例
  IGI-05 关键断言核验率 = 含数字的正文断言块中带来源指针的比例
                        （口径 2026-11-19 校准：块类型 = li / p + div.kpi /
                         stat-strip；指针含登记册指标编号 / 决策卡编号 /
                         等级+括注来源 / 非自链接外链；剔除页头 / 图注 /
                         案例等非断言块；td 不纳入，与 R4 同口径）
  IGI-06 决策卡完备率 = 通过卡片级字段校验的决策卡占比
  IGI-07 摘要合规率   = 无 ID-04 越级的报告数 / 有决策摘要的报告数
  IGI-08 信息差指数   = 1 − 加权缺口（权重见 WEIGHTS）

用法：
    python engine/tools/info_gap_metrics.py            # 打印八度实测值
    python engine/tools/info_gap_metrics.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    ROOT,
    iter_business_dirs,
    iter_business_reports,
    iter_reports,
    load_layout,
    processed_data_dir,
)

# IGI-08 权重（合计 1.0）：覆盖类权重最高——信息差首先来自「没有覆盖」
WEIGHTS = {
    "IGI-01": 0.25, "IGI-02": 0.15, "IGI-03": 0.15, "IGI-04": 0.15,
    "IGI-05": 0.10, "IGI-06": 0.10, "IGI-07": 0.10,
}

# 各节拍「健康」允许的时效容差（月）
_FRESHNESS_TOLERANCE_MONTHS = {"monthly": 1, "weekly": 1, "quarterly": 3, "annual": 12, "baseline": 1}

_URL_RE = re.compile(r"https?://[^\s\"'<>]+")
_FC_RE = re.compile(r"\[FC-[A-Z]+-\d+\]")
_SRC_LABEL_RE = re.compile(r"(来源|出处|来源机构|source_id|取自|引自)\s*[:：]?")
_HREF_RE = re.compile(r'<a\b[^>]*href\s*=\s*"(https?://[^"]*)"', re.IGNORECASE)
# 指向本仓库自身的链接是内部指针，不作为来源指针（防「自链接充数」，与 source_check 同口径）
_SELF_LINK_RE = re.compile(r"https?://(?:www\.)?github\.com/[\w.\-]+/tech-context-digest/")
_LVL_INFER_ASSUMP_RE = re.compile(
    r'<span class="lvl lvl-(?:inferred|assumption)">\s*(?:推断|假设)\s*</span>')
# 正文断言块：列表项 / 段落 + 指标卡（div.kpi / stat-strip）。
# 不取 <td>：表格逐单元格判定误报高（P1-7 实测 164 处），与 R4 同口径；
# 表格数值溯源由 R2 与来源登记承担。
_BLOCK_RE = re.compile(
    r"<li[^>]*>.*?</li>|<p[^>]*>.*?</p>"
    r"|<div[^>]*class=\"[^\"]*\b(?:kpi|stat-strip)\b[^\"]*\"[^>]*>.*?</div>",
    re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_HAS_DIGIT_RE = re.compile(r"\d")
# 来源指针的扩展形态（口径校准 2026-11-19）：
#   ① 登记册指标编号（K/P/M/S/R/RL + 两位数字）——指向单一事实源；
#   ② 决策卡编号（DC-<域>-<序号>）——指向决策卡；
#   ③ 等级+括注来源（已核验/部分核验（机构名））——正文内联来源归属。
_INDICATOR_ID_RE = re.compile(r"\b(?:K|P|M|S|R|RL)\d{2}\b")
_DC_ID_RE = re.compile(r"\bDC-(?:[A-Z]+-)+\d+\b")
_SOURCE_PAREN_RE = re.compile(r"(?:已核验|部分核验)(?:【[^】]*】)?[（(][^）)]+[）)]")
# 非断言块（页头 / 版本 / 覆盖区间 / 图注 / 案例 / 说明）——不含可核验断言，
# 纳入分母会低估核验率，故剔除（口径校准 2026-11-19）。
_META_RE = re.compile(
    r"报告版本|读数时点|数据截止|基线日期|来源语言|受众|覆盖\s*\d{4}"
    r"|市场监测\s*·|安全\s*×|图\s*\d|案例\s*\d|注：|说明：|一句话结论"
    r"|覆盖\s*\d+\s*[项个条]")
_CARD_RE = re.compile(r'<div class="decision-card"')
_CARD_LEVEL_KEYS = ("结论", "证据强度", "反向证据")
_H2_RE = re.compile(r'<h2 class="sec"[^>]*>(.*?)</h2>', re.DOTALL)
_SUMMARY_RE = re.compile(r"(决策摘要|执行摘要|结论先行|核心结论|本周要点|摘要)")
_NOTE_RE = re.compile(r'<div class="(?:note|disc|disclaimer)"[^>]*>.*?</div>', re.DOTALL | re.I)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_STYLE_RE = re.compile(r"<(style|script)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)


def _ratio(num: int, den: int) -> float:
    return round(num / den, 4) if den else 0.0


def _months(period: str) -> int:
    """周期标识 → 绝对月序（月 / 季 / 年 / 周报 ISO 日期统一到月）。

    自持实现，不依赖 `_common` 的周期窗口帮助函数（避免与业务线展示窗口耦合同源）。
    """
    s = period or ""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s) or re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m:
        return int(m.group(1)) * 12 + int(m.group(2)) - 1
    m = re.fullmatch(r"(\d{4})-Q([1-4])", s)
    if m:
        return int(m.group(1)) * 12 + (int(m.group(2)) - 1) * 3
    m = re.fullmatch(r"(\d{4})", s)
    if m:
        return int(m.group(1)) * 12
    return 0


def _clean(html: str) -> str:
    return _STYLE_RE.sub("", _COMMENT_RE.sub("", html))


def _summary_raw(text: str) -> str:
    text = _clean(text)
    ms = list(_H2_RE.finditer(text))
    for i, m in enumerate(ms):
        if _SUMMARY_RE.search(_TAG_RE.sub("", m.group(1))):
            return text[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(text)]
    return ""


def igi_01_theme_coverage() -> tuple[float, dict]:
    layout = load_layout()
    themes = sorted(layout.themes)
    covered = {b.theme for b in iter_business_dirs()}
    n = sum(1 for t in themes if t in covered)
    return _ratio(n, len(themes)), {"covered": sorted(covered), "registered": themes}


def igi_02_business_coverage() -> tuple[float, dict]:
    lines = iter_business_dirs()
    with_report = [b.rel for b in lines
                   if any(r.category == "report" for r in iter_business_reports(b))]
    return _ratio(len(with_report), len(lines)), {"with_report": with_report,
                                                  "declared": [b.rel for b in lines]}


def igi_03_freshness(today: date | None = None) -> tuple[float, dict]:
    today = today or date.today()
    cur = today.year * 12 + (today.month - 1)
    lines = iter_business_dirs()
    healthy, detail = 0, {}
    for b in lines:
        refs = [r for r in iter_business_reports(b) if r.category == "report" and r.period]
        if not refs:
            detail[b.rel] = "无正式报告"
            continue
        latest = max(refs, key=lambda r: _months(r.period))
        tol = _FRESHNESS_TOLERANCE_MONTHS.get(latest.cycle, 1)
        gap = cur - _months(latest.period)
        ok = gap <= tol
        healthy += int(ok)
        detail[b.rel] = f"最新 {latest.period}（{latest.cycle}），滞后 {gap} 个月，容差 {tol}"
    return _ratio(healthy, len(lines)), detail


def igi_04_source_coverage() -> tuple[float, dict]:
    from source_check import extract_urls, load_registry, normalize_url

    matched = total = 0
    detail = {}
    for b in iter_business_dirs():
        reg_path = processed_data_dir(b.rel) / "source_registry.json"
        registry = load_registry(reg_path) if reg_path.exists() else {}
        known = {normalize_url(s.get("url", "")) for s in registry.get("sources", []) if s.get("url")}
        known.discard("")
        for ref in iter_business_reports(b):
            if ref.category != "report":
                continue
            text = (ROOT / ref.rel).read_text(encoding="utf-8", errors="replace")
            urls = {normalize_url(u) for u in extract_urls(text)}
            urls.discard("")
            if not urls:
                continue
            hit = len(urls & known)
            matched += hit
            total += len(urls)
            detail[ref.rel] = f"{hit}/{len(urls)}"
    return _ratio(matched, total), detail


def _source_ptr_hit(window: str) -> bool:
    """窗口内是否存在来源指针。

    口径（2026-11-19 校准）：事实卡片 / fact-ref / data-source-id / 来源标签 /
    外链（须非自链接），**或**登记册指标编号（K/P/M/S/R/RL+两位）/
    决策卡编号（DC-…）/ 等级+括注来源（已核验/部分核验（机构名））。
    空指针（如 `[FC-]`）因编号正则要求数字而不命中，不计入。
    """
    plain = _TAG_RE.sub("", window)
    hrefs = _HREF_RE.findall(window)
    ext_ok = any(not _SELF_LINK_RE.match(h) for h in hrefs)
    return bool(_FC_RE.search(window) or "fact-ref" in window
                or "data-source-id" in window or _SRC_LABEL_RE.search(window)
                or ext_ok
                or _INDICATOR_ID_RE.search(plain) or _DC_ID_RE.search(plain)
                or _SOURCE_PAREN_RE.search(plain))


def _assertion_stats(text: str) -> tuple[int, int]:
    """-> (含数字断言块数, 带来源指针的断言块数)。

    窗口取值：若断言位于表格行内，取**整行**（来源常写在同行来源列）；
    否则取前后各 240 字符。统计 `<li>` / `<p>` 与指标卡（`div.kpi` /
    `stat-strip`）断言块，并剔除页头 / 版本 / 图注 / 案例 / 说明等非断言块
    （见 `_META_RE`）。
    """
    text = _clean(text)
    n_num = n_src = 0
    for m in _BLOCK_RE.finditer(text):
        block = m.group(0)
        plain = _TAG_RE.sub("", block)
        if not _HAS_DIGIT_RE.search(plain):
            continue
        if _META_RE.search(plain):
            continue
        n_num += 1
        tr_start = text.rfind("<tr", 0, m.start())
        tr_end = text.find("</tr>", m.end())
        if tr_start != -1 and tr_end != -1 and tr_end - tr_start < 4000:
            window = text[tr_start: tr_end + 5]
        else:
            window = text[max(0, m.start() - 240): m.end() + 240]
        if _source_ptr_hit(window):
            n_src += 1
    return n_num, n_src


def igi_05_assertion_verification() -> tuple[float, dict]:
    n_num = n_src = 0
    detail = {}
    for ref in iter_reports():
        if ref.category != "report":
            continue
        a, b = _assertion_stats((ROOT / ref.rel).read_text(encoding="utf-8", errors="replace"))
        n_num += a
        n_src += b
        detail[ref.rel] = f"{b}/{a}"
    return _ratio(n_src, n_num), detail


def igi_06_decision_card_completeness() -> tuple[float, dict]:
    total = ok = 0
    detail = {}
    for ref in iter_reports():
        if ref.category != "report":
            continue
        text = _clean((ROOT / ref.rel).read_text(encoding="utf-8", errors="replace"))
        starts = list(_CARD_RE.finditer(text))
        if not starts:
            continue
        good = 0
        for i, m in enumerate(starts):
            seg = text[m.start(): starts[i + 1].start() if i + 1 < len(starts) else len(text)]
            plain = _TAG_RE.sub("", seg)
            good += int(all(k in plain for k in _CARD_LEVEL_KEYS))
        total += len(starts)
        ok += good
        detail[ref.rel] = f"{good}/{len(starts)}"
    return _ratio(ok, total), detail


def igi_07_summary_compliance() -> tuple[float, dict]:
    total = ok = 0
    detail = {}
    for ref in iter_reports():
        if ref.category != "report":
            continue
        seg = _summary_raw((ROOT / ref.rel).read_text(encoding="utf-8", errors="replace"))
        if not seg:
            continue
        total += 1
        body = _NOTE_RE.sub("", seg)
        bad = bool(_LVL_INFER_ASSUMP_RE.search(body))
        plain = _TAG_RE.sub("", body)
        bad = bad or ("假设乘积" in plain and "区间" not in plain)
        ok += int(not bad)
        detail[ref.rel] = "合规" if not bad else "摘要越级"
    return _ratio(ok, total), detail


def compute(today: date | None = None) -> dict:
    """-> {metric_id: {"value": float, "detail": ...}}（IGI-08 为合成值）。"""
    values: dict[str, float] = {}
    details: dict[str, dict] = {}
    for fn, mid in (
        (igi_01_theme_coverage, "IGI-01"),
        (igi_02_business_coverage, "IGI-02"),
        (lambda: igi_03_freshness(today), "IGI-03"),
        (igi_04_source_coverage, "IGI-04"),
        (igi_05_assertion_verification, "IGI-05"),
        (igi_06_decision_card_completeness, "IGI-06"),
        (igi_07_summary_compliance, "IGI-07"),
    ):
        v, d = fn()
        values[mid] = v
        details[mid] = d
    gap = sum(WEIGHTS[mid] * (1 - values[mid]) for mid in WEIGHTS)
    values["IGI-08"] = round(1 - gap, 4)
    details["IGI-08"] = {"weights": WEIGHTS, "formula": "1 - Σ w_i · (1 - IGI-i)"}
    return {"values": values, "details": details}


def main() -> int:
    ap = argparse.ArgumentParser(description="信息差指数（IGI）实测")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rep = compute()
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0
    for mid in sorted(rep["values"]):
        print(f"{mid:<8} {rep['values'][mid]:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
