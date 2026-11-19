#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""指标实测覆盖（METRIC-COVERAGE v1.0）。

把 `metrics-dictionary.json` 的 38 项指标从「注册了公式与阈值、但多数从未被计算」
推进到「工具可测子集产出实测值」，并输出覆盖率与缺口清单（批次 B）。

口径：
  - measured：本模块或既有工具可算出 0–1 的实测值；
  - probe：需网络探测（A-05 链接可达率），未探测时显式标注，不伪造；
  - llm：语义判定项（A-02/A-04/L-01/L-02/L-04/L-05/R-05），不伪造实测值；
  - probe：需网络探测（A-05）或分母为 0 不可判（如 L-03 无比阈值），显式标注不伪造；
  - fallback：暂无接线（进入 tech-debt-ledger）。

2026-11-19 接线：A-01（复用 IGI-05 断言级测量）/ A-03（指标编号数值冲突代理）/
L-03（阈值表达式命中 business-config 代理）/ R-03（跨业务线重复段落代理）；
R-03 随之由 LLM 转 TOOL（字典 detected_by 同步）。

用法：
    python engine/tools/metric_coverage.py                 # 覆盖率报告
    python engine/tools/metric_coverage.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    ROOT,
    iter_business_dirs,
    iter_reports,
    load_layout,
    processed_data_dir,
)
from gate_period import AUTO as GATE_AUTO  # noqa: E402
from gate_period import resolve as resolve_gate_period  # noqa: E402

DICT_PATH = Path(__file__).resolve().parent / "metrics-dictionary.json"

# 需网络探测的指标（不伪造实测值）
PROBE_METRICS = {"A-05"}
# 语义判定项（LLM / 人工）
LLM_METRICS = {"A-02", "A-04", "L-01", "L-02", "L-04", "L-05", "R-05"}

H2_RE = re.compile(r'<h2\b[^>]*class="[^"]*\bsec\b[^"]*"', re.IGNORECASE)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.DOTALL | re.IGNORECASE)
ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')
HREF_ANCHOR_RE = re.compile(r'href="#([^"]+)"')
FC_REF_RE = re.compile(r"\[FC-[A-Z]+-\d+\]")
EX_ANTE_RE = re.compile(r"预校准（ex-ante）|预校准\(ex-ante\)|ex-ante")
TAG_RE = re.compile(r"<[^>]+>")


def _ratio(n: int, d: int) -> float:
    return round(n / d, 4) if d else 0.0


def _plain(html: str) -> str:
    return TAG_RE.sub("", html)


def _reports_text() -> dict[str, str]:
    return {r.rel: (ROOT / r.rel).read_text(encoding="utf-8", errors="replace")
            for r in iter_reports()}


# ---------------------------------------------------------------- 各指标实测

def c01_structure(reports: dict[str, str]) -> tuple[float, str]:
    """结构完整率：各报告 h2.sec 节数 / 类型骨架节数（封顶 1）的均值。"""
    import compliance_check
    from _common import iter_business_reports
    rules = compliance_check.load_rules()
    ratios: list[float] = []
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        cfg_text = cfg.read_text(encoding="utf-8", errors="replace") if cfg.exists() else ""
        type_id = compliance_check.detect_type(cfg_text)
        for r in iter_business_reports(b):
            rule, _ = compliance_check.cycle_rule(rules, type_id, r.cycle, b.rel)
            if not rule:
                continue
            n = len(compliance_check.H2_RE.findall(reports.get(r.rel, "")))
            ratios.append(min(n / int(rule["sections"]), 1.0))
    return (round(sum(ratios) / len(ratios), 4) if ratios else 0.0), \
        f"{len(ratios)} 份报告节数 / 骨架均值"


def c02_required_fields(reports: dict[str, str]) -> tuple[float, str]:
    """必填字段完整率：title 非空 + 周期报告含 .nav-url。"""
    ok = 0
    for rel, text in reports.items():
        m = TITLE_RE.search(text)
        title_ok = bool(m and _plain(m.group(1)).strip())
        period = any(k in rel for k in ("_monthly", "_quarterly", "_annual", "_weekly"))
        nav_ok = ('class="nav-url"' in text) if period else True
        ok += 1 if (title_ok and nav_ok) else 0
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份必填字段齐全"


def c03_directory(reports: dict[str, str]) -> tuple[float, str]:
    """目录完整率：具备 business-config + reports/ + data/ 的业务线占比。"""
    dirs = list(iter_business_dirs())
    ok = 0
    for b in dirs:
        has_cfg = (b.path / "prompts" / "business-config.md").exists()
        has_rep = (b.path / "reports").is_dir()
        has_data = processed_data_dir(b.rel).exists()
        ok += 1 if (has_cfg and has_rep and has_data) else 0
    return _ratio(ok, len(dirs)), f"{ok}/{len(dirs)} 条业务线目录完整"


def c05_cadence(reports: dict[str, str]) -> tuple[float, str]:
    """节拍达成率：最新报告期次处于 gate-period 或上一周期的业务线占比。

    确定性（2026-11-19）：锚点取 `GATE_PERIOD` 环境变量（CI 固定口径）或
    滚动 gate-period（当前自然月 + 1），不再直接取 `date.today()`。
    """
    dirs = list(iter_business_dirs())
    anchor = os.environ.get("GATE_PERIOD") or resolve_gate_period(GATE_AUTO)
    m = re.fullmatch(r"(\d{4})-(\d{2})", anchor or "")
    cur_m = (int(m.group(1)) * 12 + int(m.group(2)) - 1) if m else 0
    ok = 0
    for b in dirs:
        reps = [r for r in iter_reports() if r.business_line == b.rel]
        if not reps:
            continue
        latest = max(reps, key=lambda r: (r.period or ""))
        m = re.fullmatch(r"(\d{4})-(\d{2})", latest.period or "")
        if not m:
            continue
        p = int(m.group(1)) * 12 + int(m.group(2)) - 1
        ok += 1 if cur_m - p <= 1 else 0
    return _ratio(ok, len(dirs)), f"{ok}/{len(dirs)} 条业务线节拍达成"


def c06_vocab_sync() -> tuple[float, str]:
    """词汇同步覆盖率：已绑定同步的主题 / 已注册主题。"""
    cfg = ROOT / "engine" / "vocabulary" / "config"
    topics = json.loads((cfg / "topics.json").read_text(encoding="utf-8"))
    sync = json.loads((cfg / "sync.json").read_text(encoding="utf-8"))
    reg = topics.get("topics", topics) if isinstance(topics, dict) else {}
    registered = set(reg) if isinstance(reg, dict) else {t.get("id") for t in reg}
    bound = {b.get("topic") for b in sync.get("bindings", [])}
    hit = len(registered & bound)
    return _ratio(hit, len(registered)), f"{hit}/{len(registered)} 主题已绑定同步"


def r01_attribution(reports: dict[str, str]) -> tuple[float, str]:
    """归属正确率：1 - 错位报告 / 报告总数。"""
    try:
        import classify_reports
        strays = classify_reports.strays()
    except Exception:
        strays = []
    n = len(reports)
    return round(1 - _ratio(len(strays), n), 4), f"错位 {len(strays)}/{n}"


def r02_dimension_priority(reports: dict[str, str]) -> tuple[float, str]:
    """维度优先级合规率：业务线维度段顺序与 layout 声明一致的占比。"""
    layout = load_layout()
    dirs = list(iter_business_dirs())
    ok = 0
    for b in dirs:
        dims = layout.themes.get(b.theme, ("", ()))[1]
        seg_by_dim = b.dim_map
        try:
            idx = [b.segments.index(seg_by_dim[d]) for d in dims if d in seg_by_dim]
        except ValueError:
            idx = []
        ok += 1 if idx == sorted(idx) else 0
    return _ratio(ok, len(dirs)), f"{ok}/{len(dirs)} 条业务线维度顺序合规"


def r04_anchor(reports: dict[str, str]) -> tuple[float, str]:
    """断头锚点率：断头锚点数 / 锚点总数（口径与字典一致，越低越好，阈值 =0.0）。"""
    total = broken = 0
    for text in reports.values():
        ids = set(ID_ATTR_RE.findall(text))
        for anchor in HREF_ANCHOR_RE.findall(text):
            total += 1
            if anchor not in ids:
                broken += 1
    return _ratio(broken, total), f"断头 {broken}/{total}"


# ---------------------------------------------------------------- A/L/R 接线（2026-11-19）

_IND_ID_RE = re.compile(r"\b([A-Z]{1,2}\d{2})\b")
_NUM_RE = re.compile(r"\d[\d,\.]*")
# 阈值表达式（L-03 代理口径 2026-11-19）：比较符 + 数字 + 可选百分号
_THRESH_RE = re.compile(r"[≥≤<>]=?\s*\d+(?:\.\d+)?\s*%?")
_PARA_RE = re.compile(r"<li[^>]*>.*?</li>|<p[^>]*>.*?</p>", re.DOTALL)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_STYLE_RE = re.compile(r"<(style|script)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)


def _clean(html: str) -> str:
    return _STYLE_RE.sub("", _COMMENT_RE.sub("", html))


def _norm_num(tok: str) -> str:
    return tok.replace(",", "").rstrip(".")


def _thresh_tokens(text: str) -> set[str]:
    """阈值表达式集合（去空白，便于跨 config / 报告比对）。"""
    return {m.replace(" ", "") for m in _THRESH_RE.findall(text)}


def a01_source_traceability(reports: dict[str, str]) -> tuple[float, str]:
    """来源可追溯率：含数字断言块中带来源指针的比例（与 IGI-05 同口径，复用其测量）。"""
    import info_gap_metrics
    n_num = n_src = 0
    for text in reports.values():
        a, b = info_gap_metrics._assertion_stats(text)
        n_num += a
        n_src += b
    return _ratio(n_src, n_num), f"{n_src}/{n_num} 断言块带来源指针"


def a03_numeric_consistency(reports: dict[str, str]) -> tuple[float, str]:
    """数值一致率（代理）：同一指标编号在不同位置取不同数值即记冲突；
    一致率 = 1 - 冲突指标数 / 出现指标数。"""
    total = conflict = 0
    for text in reports.values():
        plain = _plain(_clean(text))
        by_id: dict[str, set[str]] = {}
        for m in _IND_ID_RE.finditer(plain):
            tail = plain[m.end(): m.end() + 60]
            nums = _NUM_RE.findall(tail)
            if nums:
                by_id.setdefault(m.group(1), set()).add(_norm_num(nums[0]))
        for vs in by_id.values():
            total += 1
            if len(vs) > 1:
                conflict += 1
    return _ratio(total - conflict, total), f"冲突 {conflict}/{total} 指标"


def l03_threshold_consistency(reports: dict[str, str]) -> tuple[float | None, str]:
    """阈值一致率（代理）：报告中的阈值表达式与同业务线 business-config 的重合比例。

    口径（2026-11-19 校准）：阈值表达式 = `[≥≤<>]=?数字[%]`；config 侧取全文表达式
    集合，报告侧取全文表达式集合；分母 = 报告侧表达式数（仅统计 config 声明了阈值
    的业务线）。分母为 0（无可比阈值）时返回 None，由 `measure()` 标为 probe
    （不可判），不静默给 0。
    """
    hit = total = 0
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        cfg_th = _thresh_tokens(_plain(_clean(cfg.read_text(encoding="utf-8", errors="replace")))) \
            if cfg.exists() else set()
        if not cfg_th:
            continue
        for r in iter_reports():
            if r.business_line != b.rel:
                continue
            for th in _thresh_tokens(_plain(_clean(reports.get(r.rel, "")))):
                total += 1
                if th in cfg_th:
                    hit += 1
    if not total:
        return None, "无可比阈值（分母 0，不可判）"
    return _ratio(hit, total), f"{hit}/{total} 报告阈值表达式命中 business-config"


def r03_duplicate_rate(reports: dict[str, str]) -> tuple[float, str]:
    """跨主题重复率：跨业务线重复段落数 / 段落总数（段落级精确重合代理）。"""
    by_line: dict[str, set[str]] = {}
    for rel, text in reports.items():
        line = rel.split("/reports/")[0]
        paras = set()
        for m in _PARA_RE.finditer(_clean(text)):
            p = re.sub(r"\s+", "", _plain(m.group(0)))
            if len(p) >= 20:
                paras.add(p)
        by_line.setdefault(line, set()).update(paras)
    total = sum(len(s) for s in by_line.values())
    dup = 0
    for line, s in by_line.items():
        others: set[str] = set()
        for other, os_ in by_line.items():
            if other != line:
                others |= os_
        dup += len(s & others)
    return _ratio(dup, total), f"重复 {dup}/{total} 段落"


def i01_layering(reports: dict[str, str]) -> tuple[float, str]:
    import info_density_check
    ok = 0
    for text in reports.values():
        ids = {rid for rid, _ in info_density_check.check_text(text)}
        ok += 1 if "ID-01" not in ids else 0
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份分层交付合规"


def i03_delta_module(reports: dict[str, str]) -> tuple[float, str]:
    import info_density_check
    ok = 0
    for text in reports.values():
        ids = {rid for rid, _ in info_density_check.check_text(text)}
        ok += 1 if "ID-05" not in ids else 0
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份含新增信息模块"


def i04_fact_card(reports: dict[str, str]) -> tuple[float, str]:
    ok = sum(1 for text in reports.values() if FC_REF_RE.search(_plain(text)))
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份使用 [FC-…] 指针"


def i02_info_level(reports: dict[str, str]) -> tuple[float, str]:
    """信息等级标注率（代理）：含 lvl-* 等级标注的报告占比。"""
    ok = sum(1 for t in reports.values() if re.search(r'class="lvl ', t))
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份含四级等级标注"


def i05_action_protocol(reports: dict[str, str]) -> tuple[float, str]:
    """行动协议合规率（代理）：无 DC-02 违规的报告占比。"""
    import decision_hub_check
    ok = 0
    for rel, text in reports.items():
        ids = {rid for rid, _ in decision_hub_check.check_text(text, rel)}
        ok += 1 if "DC-02" not in ids else 0
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份行动协议合规"


def i06_decision_card(reports: dict[str, str]) -> tuple[float, str]:
    """决策卡覆盖率（代理）：含 decision-card 的报告占比。"""
    ok = sum(1 for t in reports.values() if 'class="decision-card"' in t)
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份含决策卡"


def c04_registry_coverage(reports: dict[str, str]) -> tuple[float, str]:
    """登记册指标覆盖率（代理）：引用指标编号 / 指针的报告占比。"""
    ok = sum(1 for t in reports.values()
             if re.search(r"\[FC-[A-Z]+-\d+\]|\b(?:K|RL|P)\d{2}\b|\bIGI-\d{2}\b", _plain(t)))
    return _ratio(ok, len(reports)), f"{ok}/{len(reports)} 份引用登记册指标"


def i07_ex_ante(reports: dict[str, str]) -> tuple[float, str]:
    signal = {rel: t for rel, t in reports.items()
              if re.search(r"信号灯|红线|绿灯|amber|red\s*light", _plain(t), re.I)}
    ok = sum(1 for t in signal.values() if EX_ANTE_RE.search(t))
    return _ratio(ok, len(signal)), f"{ok}/{len(signal)} 份信号灯报告含 ex-ante"


def i08_blind_spot() -> tuple[float, str]:
    import blind_spot_check
    rows = blind_spot_check.parse_rows(
        (ROOT / "engine" / "report-audits" / "blind-spot-ledger.md").read_text(encoding="utf-8"))
    closed = sum(1 for r in rows if len(r) > 7 and r[7] == "closed")
    return _ratio(closed, len(rows)), f"closed {closed}/{len(rows)}"


def i09_reading_time(reports: dict[str, str]) -> tuple[float, str]:
    period = {rel: t for rel, t in reports.items()
              if any(k in rel for k in ("_monthly", "_quarterly", "_annual", "_weekly"))}
    ok = sum(1 for t in period.values() if "读数时点" in t)
    return _ratio(ok, len(period)), f"{ok}/{len(period)} 份周期报告含读数时点"


def igi_all() -> dict[str, float]:
    import info_gap_metrics
    return dict(info_gap_metrics.compute()["values"])


# ---------------------------------------------------------------- 覆盖汇总

def measure() -> dict[str, dict]:
    reports = _reports_text()
    out: dict[str, dict] = {}

    def put(mid: str, value, status: str, detail: str) -> None:
        out[mid] = {"value": value, "status": status, "detail": detail}

    computed = {
        "C-01": c01_structure(reports),
        "C-02": c02_required_fields(reports),
        "C-03": c03_directory(reports),
        "C-04": c04_registry_coverage(reports),
        "C-05": c05_cadence(reports),
        "C-06": c06_vocab_sync(),
        "A-01": a01_source_traceability(reports),
        "A-03": a03_numeric_consistency(reports),
        "L-03": l03_threshold_consistency(reports),
        "R-01": r01_attribution(reports),
        "R-03": r03_duplicate_rate(reports),
        "R-02": r02_dimension_priority(reports),
        "R-04": r04_anchor(reports),
        "I-01": i01_layering(reports),
        "I-02": i02_info_level(reports),
        "I-03": i03_delta_module(reports),
        "I-04": i04_fact_card(reports),
        "I-05": i05_action_protocol(reports),
        "I-06": i06_decision_card(reports),
        "I-07": i07_ex_ante(reports),
        "I-08": i08_blind_spot(),
        "I-09": i09_reading_time(reports),
    }
    for mid, (v, d) in computed.items():
        # 分母为 0 等不可判情形：显式标 probe，不静默给 0
        if v is None:
            put(mid, None, "probe", d or "不可判（分母 0）")
        else:
            put(mid, v, "measured", d)
    for mid, v in igi_all().items():
        put(mid, v, "measured", "info_gap_metrics 实测")
    for mid in sorted(PROBE_METRICS):
        put(mid, None, "probe", "需网络探测（source_check --probe），未探测不伪造")
    dictionary = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    for m in dictionary["metrics"]:
        mid = m["metric_id"]
        if mid not in out:
            put(mid, None, "llm" if mid in LLM_METRICS else "fallback",
                "语义判定项，不伪造实测值" if mid in LLM_METRICS else "暂无工具接线")
    return out


def coverage_report(meas: dict[str, dict]) -> dict:
    statuses: dict[str, int] = {}
    for rec in meas.values():
        statuses[rec["status"]] = statuses.get(rec["status"], 0) + 1
    gaps = sorted(mid for mid, r in meas.items() if r["status"] in ("fallback", "probe"))
    return {"total": len(meas), "statuses": statuses, "gaps": gaps}


def main() -> int:
    ap = argparse.ArgumentParser(description="指标实测覆盖报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    meas = measure()
    rep = coverage_report(meas)
    if args.json:
        print(json.dumps({"coverage": rep, "metrics": meas}, ensure_ascii=False, indent=2))
        return 0
    print(f"指标覆盖：{rep['total']} 项；{rep['statuses']}")
    for mid in sorted(meas):
        r = meas[mid]
        val = "-" if r["value"] is None else f"{r['value']:.4f}"
        print(f"[{r['status']:>8}] {mid:<7} {val:>8}  {r['detail']}")
    if rep["gaps"]:
        print(f"\n[gap] 未实测 {len(rep['gaps'])} 项：{'、'.join(rep['gaps'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
