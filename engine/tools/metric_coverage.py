#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""指标实测覆盖（METRIC-COVERAGE v1.0）。

把 `metrics-dictionary.json` 的 38 项指标从「注册了公式与阈值、但多数从未被计算」
推进到「工具可测子集产出实测值」，并输出覆盖率与缺口清单（批次 B）。

口径：
  - measured：本模块或既有工具可算出 0–1 的实测值；
  - probe：分母为 0 不可判（如 L-03 无比阈值）或探测记录缺失 / 不可判（A-05），
    显式标注不伪造；
  - llm：语义判定项，不伪造实测值（2026-11-19 七项 LLM 兜底已全部接线为机械代理，
    当前无 LLM 项）；
  - fallback：暂无接线（进入 tech-debt-ledger）。

2026-11-19 接线：A-01（复用 IGI-05 断言级测量）/ A-03（真值核对 + 代理组合）/
L-03（阈值三处一致代理）/ R-03（跨业务线重复段落代理）；R-03 随之由 LLM 转 TOOL。
2026-11-19 A-03 数据治理：新增 `a03_truth_check()`，读结构化登记册
`engine/tools/indicator-truth-registry.json`（R01–R09）与报告显式数值比对对，
输出 一致/差异/不可比；A-03 计分改为真值核对一致率与代理一致率的组合。
2026-11-19 A-05 接线：复用 `source_check --probe` 定期落盘的
`engine/audit/records/link-probe.json`（见 `a05_link_reachability`）。
2026-11-19 N-6 接线：A-02 / A-04 / L-01 / L-02 / L-04 / L-05 / R-05 由 LLM 兜底
转为 TOOL 机械代理（公式见字典与本模块函数 docstring）；均为代理口径，不得当作
语义达标。

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
    detect_report,
    iter_business_dirs,
    iter_business_reports,
    iter_reports,
    load_layout,
    processed_data_dir,
)
from gate_period import AUTO as GATE_AUTO  # noqa: E402
from gate_period import resolve as resolve_gate_period  # noqa: E402
from indicator_sidecar import SIDECAR_PATH  # noqa: E402

DICT_PATH = Path(__file__).resolve().parent / "metrics-dictionary.json"

# 链接可达率探测记录（source_check --probe --emit 定期落盘，无时间戳）
LINK_PROBE_PATH = ROOT / "engine" / "audit" / "records" / "link-probe.json"

# A-03 真值核对结构化登记册（R01–R09；字段：指标编号 / 最新值 / 周期 / 来源 URL / 核验状态）
TRUTH_REGISTRY_PATH = Path(__file__).resolve().parent / "indicator-truth-registry.json"

# 仅探测型指标（不伪造实测值）：A-05 已接线为读定期落盘记录，当前无仅探测项；
# 保留该集合用于未来「必须现场探测」的指标。
PROBE_METRICS: set[str] = set()
# 语义判定项（LLM / 人工）：2026-11-19 起七项均已接线为机械代理，当前为空。
LLM_METRICS: set[str] = set()

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
        # 周报 period 形如 YYYY-MM-DD，取所属自然月；月/季/年报为 YYYY-MM / YYYY-Qn。
        m = re.fullmatch(r"(\d{4})-(\d{2})(?:-\d{2})?", latest.period or "")
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

# 显式数值对（A-03 代理口径 2026-11-19 校准）：指标编号 + 可选分隔符（=／：／，）
# + 数值（后不接字母，避免 「K01 3M EIBOR」 误取 3）+ 可选单位。
_VALUE_PAIR_RE = re.compile(
    r"\b([A-Z]{1,2}\d{2})\b\s*[=＝:：]?\s*(\d[\d,\.]*)(?![\dA-Za-z])(?!\s*[-/]\s*\d)"
    r"\s*(?:%|bp|个|项|亿|万|元|美元|AED|次|年|月|日|点|sqft|桶|户|家|人)?"
)
# 阈值表达式（L-03 代理口径 2026-11-19）：比较符 + 数字 + 可选百分号
_THRESH_RE = re.compile(r"[≥≤<>]=?\s*\d+(?:\.\d+)?\s*%?")
# 阈值/触发语境标记：数值对处于该语境时为阈值而非指标值（A-03 真值核对排除，
# 避免把行动卡阈值「R06 20%」误取为指标值）。
_THRESHOLD_CTX_RE = re.compile(r"阈值|触发条件|≥|≤|仍\s*[><]")


def _in_threshold_context(plain: str, start: int) -> bool:
    """数值对起始处前 40 字内是否处于阈值/触发语境。"""
    return bool(_THRESHOLD_CTX_RE.search(plain[max(0, start - 40):start]))
_PARA_RE = re.compile(r"<li[^>]*>.*?</li>|<p[^>]*>.*?</p>", re.DOTALL)
# 来源/链接段落特征（机构名 + 域名/URL），用于 R-03 排除共享引用
_SRC_LINK_RE = re.compile(r"https?://|www\.|[\w-]+\.(?:com|ae|org|net|gov|edu|io|ai|cn|news|media)\b", re.I)
# 规范强制共享的 boilerplate（源自 engine/templates/*/prompt-*-template.md 与通用基座）：
# 这些段落按规范必须一致，属共享模板而非内容同质化，R-03 不计入。
_BOILERPLATE_RE = re.compile(
    r"按来源分级分组|基线首期：新增=全部基线项|来源与时点：数据截止|九节固化锚"
    r"|假设：已登记|推断：影响对象矩阵|基线属性：本报告|版本治理：本报告"
    r"|规则：未取得官方原文|已修正事实清单|本期为核验/收敛型轻运行"
    r"|机制框架的「影响量级」|本基线只处理官方文本|监测节拍：事件触发"
    r"|本主题暂无事实卡片库|本报告为基线首期|基线v1\.0固定"
    r"|来源按「官方一手|数据截止：")
# 指标编号（用于 L-03 判定「阈值是否与指标相邻」）
_ID_NEAR_RE = re.compile(r"\b[A-Z]{1,2}\d{2}\b")
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


def a05_link_reachability(path: Path | None = None) -> tuple[float | None, str]:
    """明确链接可达率：ok / (ok + dead)。

    数据源：`source_check.py --probe --emit engine/audit/records/link-probe.json`
    （scheduled-maintenance 定期落盘，`{probed, dead, unreachable, ok}`，无时间戳）。
    口径（2026-11-19 校准）：分母仅含**可判定**链接（明确可达 ok + 明确死链
    dead）；unreachable（超时 / 反爬 / 网络异常）为环境性不可判，不计入分母——
    避免把反爬拦截误判为报告质量问题，但计数在明细中显式呈现。
    记录缺失 / 非法 / 分母为 0 时返回 None，由 `measure()` 显式标 probe，不伪造。
    确定性：只读定期落盘记录，不取墙钟（与 C-05 的 gate-period 锚点口径同，
    见 gate_period.py）；仅记录内容变更才引起读数变化。
    """
    p = Path(path) if path is not None else LINK_PROBE_PATH
    if not p.exists():
        return None, "链接探测记录缺失（source_check --probe 未落盘）"
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "链接探测记录不可解析"
    if not isinstance(rec, dict):
        return None, "链接探测记录格式非法"
    probed = rec.get("probed")
    ok = rec.get("ok")
    dead = rec.get("dead", 0)
    unreachable = rec.get("unreachable", 0)
    if (not isinstance(probed, int) or not isinstance(ok, int)
            or not isinstance(dead, int) or not isinstance(unreachable, int)
            or isinstance(probed, bool) or isinstance(ok, bool) or isinstance(dead, bool)
            or probed <= 0 or ok < 0 or dead < 0 or unreachable < 0 or ok > probed):
        return None, f"链接探测记录不可判（probed={probed!r}, ok={ok!r}, dead={dead!r}）"
    denom = ok + dead
    if denom <= 0:
        return None, "无可判定链接（分母 0，不可判）"
    return _ratio(ok, denom), \
        f"{ok}/{denom} 可判定链接明确可达（死链 {dead}；环境不可达 {unreachable} 不计入分母）"


def a03_numeric_consistency(reports: dict[str, str]) -> tuple[float, str]:
    """数值一致率（代理）：同一指标编号的**显式数值对**取值是否一致。

    口径（2026-11-19 校准）：仅认「指标编号 + 可选分隔符（=／：／，）+ 数值
    （后不接字母）+ 可选单位」的规范数值对，天然排除日期、区间上界、枚举与
    公司名（如 G42/M42）造成的伪冲突。分母为**显式数值对数**（非编号出现数），
    分母偏小会显式呈现；与登记册的真值核对见 `a03_truth_check`（sidecar 版，
    辅助不计分）。
    """
    total = conflict = 0
    for text in reports.values():
        plain = _plain(_clean(text))
        by_id: dict[str, set[str]] = {}
        for m in _VALUE_PAIR_RE.finditer(plain):
            by_id.setdefault(m.group(1), set()).add(_norm_num(m.group(2)))
        for vs in by_id.values():
            total += 1
            if len(vs) > 1:
                conflict += 1
    return _ratio(total - conflict, total), f"冲突 {conflict}/{total} 显式数值对"


def _apartment_registry() -> tuple[Path | None, dict[str, tuple[str, str]]]:
    """读取最新一期 apartment 登记册 -> {指标编号: (基线值, 统计周期)}。

    数据源：`data/processed/economy/dubai/apartment/*indicator_registry*.xlsx`
    的「年度基线2027 / 首期基线值」表；取文件名周期最新者。读不到返回 (None, {})。
    """
    import openpyxl

    files = sorted((ROOT / "data" / "processed" / "economy" / "dubai" / "apartment")
                   .glob("*indicator_registry*.xlsx"))
    if not files:
        return None, {}
    path = files[-1]
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return path, {}
    reg: dict[str, tuple[str, str]] = {}
    for sh in ("年度基线2027", "首期基线值"):
        if sh not in wb.sheetnames:
            continue
        rows = list(wb[sh].iter_rows(values_only=True))
        hi = next((i for i, r in enumerate(rows) if r and r[0] == "指标编号"), None)
        if hi is None:
            continue
        for r in rows[hi + 1:]:
            if not r or not r[0]:
                continue
            val = str(r[2]).strip() if len(r) > 2 and r[2] is not None else ""
            per = str(r[4]).strip() if len(r) > 4 and r[4] is not None else ""
            num = re.sub(r"[^0-9\.\-]", "", val)
            if num:
                reg.setdefault(str(r[0]).strip(), (_norm_num(num), per))
    return path, reg


def a03_truth_candidates(reports: dict[str, str] | None = None) -> dict:
    """A-03 真值核对（**辅助工具，不计分**）：报告数值 vs apartment 登记册基线。

    ⚠️ 自动抽取无法区分「指标值 / 阈值 / 统计周期」，直接判分将产生伪差异
    （已实测：阈值「R06 20%」被误取为指标值）。故本函数只产出**候选差异清单**
    供人工核验，不纳入 A-03 指标值；自动判分待登记册结构化「最新值 + 周期 +
    来源」字段后再实施（见 tech-debt-ledger）。
    """
    if reports is None:
        reports = {r.rel: (ROOT / r.rel).read_text(encoding="utf-8", errors="replace")
                   for r in iter_reports()}
    path, reg = _apartment_registry()
    if not reg:
        return {"registry": str(path) if path else None, "error": "登记册不可读",
                "compared": 0, "same": 0, "diff": 0, "uncomparable": 0, "diffs": []}
    same = diff = uncomparable = 0
    diffs: list[dict] = []
    for rel, html in reports.items():
        if "/apartment/" not in rel:
            continue
        plain = _plain(_clean(html))
        for m in _VALUE_PAIR_RE.finditer(plain):
            if _in_threshold_context(plain, m.start()):
                continue
            iid, val = m.group(1), _norm_num(m.group(2))
            if iid not in reg:
                uncomparable += 1
                continue
            rv, rper = reg[iid]
            if val == rv:
                same += 1
            else:
                diff += 1
                diffs.append({"report": rel, "indicator": iid, "report_value": val,
                              "registry_value": rv, "registry_period": rper,
                              "note": "需人工判读（可能为阈值 / 周期差异）"})
    return {"registry": str(path), "compared": same + diff, "same": same, "diff": diff,
            "uncomparable": uncomparable, "diffs": diffs}


# ---------------------------------------------------------------- A-03 真值核对（sidecar 版）

_SIDECAR_QUALIFIER_RE = re.compile(r"[><≈~约≥≤]")
_SIDECAR_RANGE_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)\s*$")
_SIDECAR_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
_NUM_TOL = 1e-9


def _sidecar_value_kind(raw: str) -> tuple[str, list[float], tuple[float, float] | None]:
    """解析 sidecar value -> (kind, numbers, range)。

    kind ∈ single / multi / range / qualified / nonnumeric / empty。
    确定性：仅字符串解析，不取墙钟、不联网。
    """
    s = str(raw or "").strip()
    for a, b in (("−", "-"), ("–", "-"), ("—", "-"), (",", "")):
        s = s.replace(a, b)
    if not s:
        return "empty", [], None
    if _SIDECAR_QUALIFIER_RE.search(s):
        return "qualified", [], None
    nums: list[float] = []
    rng: tuple[float, float] | None = None
    for part in s.split("/"):
        p = part.strip()
        if not p:
            continue
        m = _SIDECAR_RANGE_RE.match(p)
        if m:
            lo, hi = float(m.group(1)), float(m.group(2))
            rng = (min(lo, hi), max(lo, hi))
            continue
        if _SIDECAR_NUM_RE.match(p):
            nums.append(float(p))
            continue
        return "nonnumeric", [], None
    if rng is not None:
        return "range", nums, rng
    if len(nums) == 1:
        return "single", nums, None
    if len(nums) > 1:
        return "multi", nums, None
    return "nonnumeric", [], None


def _report_number(tok: str) -> float | None:
    """报告显式数值 -> float；不可解析返回 None。"""
    s = str(tok or "").strip()
    for a, b in (("−", "-"), ("–", "-"), ("—", "-"), (",", "")):
        s = s.replace(a, b)
    if not _SIDECAR_NUM_RE.match(s):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _truth_verdict(kind: str, nums: list[float], rng, report_num: float | None):
    """单条比对判定 -> (一致 / 差异 / 不可比, 原因)。"""
    if report_num is None:
        return "不可比", "报告数值无法解析"
    if kind == "single":
        ok = abs(report_num - nums[0]) <= _NUM_TOL
        return ("一致", "与登记册单值一致") if ok else \
            ("差异", f"报告 {report_num:g} vs 登记册 {nums[0]:g}")
    if kind == "multi":
        ok = any(abs(report_num - n) <= _NUM_TOL for n in nums)
        return ("一致", "命中登记册多口径之一") if ok else \
            ("差异", f"报告 {report_num:g} 不在登记册多口径 {nums} 内")
    if kind == "range":
        lo, hi = rng
        ok = lo - _NUM_TOL <= report_num <= hi + _NUM_TOL
        return ("一致", f"落在登记册区间 [{lo:g}, {hi:g}]") if ok else \
            ("差异", f"报告 {report_num:g} 落在登记册区间 [{lo:g}, {hi:g}] 之外")
    if kind == "qualified":
        return "不可比", "登记册为不等式 / 约数，无法自动判等"
    return "不可比", "登记册值非数值或无法解析"


def a03_truth_check(reports: dict[str, str] | None = None,
                    sidecar_path: Path | None = None) -> dict:
    """A-03 真值核对（结构化登记册版）。

    默认读取 `engine/tools/indicator-truth-registry.json`（R01–R09，字段：指标编号 /
    最新值 / 周期 / 来源 URL / 核验状态）；缺失时回退 `indicator_latest.json` sidecar。
    与 apartment 报告的显式数值对比对，输出 一致 / 差异 / 不可比 明细。
    结果供 `a03_combined` 计分（真值核对一致率 + 代理一致率），也可单独作明细输出。
    """
    if reports is None:
        reports = _reports_text()
    p = (Path(sidecar_path) if sidecar_path is not None
         else (TRUTH_REGISTRY_PATH if TRUTH_REGISTRY_PATH.exists() else SIDECAR_PATH))
    empty = {"sidecar": str(p), "compared": 0, "same": 0, "diff": 0,
             "uncomparable": 0, "records": []}
    if not p.exists():
        return {**empty, "error": "登记册缺失（indicator-truth-registry.json / sidecar 未落盘）"}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {**empty, "error": "登记册不可解析"}
    reg = {str(r.get("indicator_id", "")).strip(): r
           for r in data.get("indicators", []) if r.get("indicator_id")}
    same = diff = uncomparable = 0
    records: list[dict] = []
    for rel, html in reports.items():
        if "/apartment/" not in rel:
            continue
        plain = _plain(_clean(html))
        for m in _VALUE_PAIR_RE.finditer(plain):
            if _in_threshold_context(plain, m.start()):
                continue
            iid, tok = m.group(1), m.group(2)
            if iid not in reg:
                uncomparable += 1
                records.append({"report": rel, "indicator": iid, "report_value": tok,
                                "sidecar_value": None, "unit": "", "period": "",
                                "source": "", "source_url": "",
                                "verification_status": "", "verdict": "不可比",
                                "reason": "报告指标未登记"})
                continue
            rec = reg[iid]
            kind, nums, rng = _sidecar_value_kind(rec.get("value", ""))
            verdict, reason = _truth_verdict(kind, nums, rng, _report_number(tok))
            if verdict == "一致":
                same += 1
            elif verdict == "差异":
                diff += 1
            else:
                uncomparable += 1
            records.append({"report": rel, "indicator": iid, "report_value": tok,
                            "sidecar_value": rec.get("value", ""),
                            "unit": rec.get("unit", ""), "period": rec.get("period", ""),
                            "source": rec.get("source", ""),
                            "source_url": rec.get("source_url", ""),
                            "verification_status": rec.get("verification_status", ""),
                            "verdict": verdict, "reason": reason})
    return {"sidecar": str(p), "compared": same + diff, "same": same, "diff": diff,
            "uncomparable": uncomparable, "records": records}


def a03_combined(reports: dict[str, str] | None = None) -> tuple[float, str]:
    """A-03 计分：0.5 × 真值核对一致率 + 0.5 × 代理一致率。

    真值核对一致率 = 报告数值与结构化登记册比对一致数 / 可比数；可比项为 0 时
    回退代理并显式标注（不伪造真值达标）。代理一致率见 `a03_numeric_consistency`。
    """
    if reports is None:
        reports = _reports_text()
    proxy, proxy_detail = a03_numeric_consistency(reports)
    truth = a03_truth_check(reports)
    compared = int(truth.get("compared", 0) or 0)
    if compared > 0:
        truth_rate = _ratio(truth["same"], compared)
        value = round(0.5 * truth_rate + 0.5 * proxy, 4)
        detail = (f"真值核对 {truth['same']}/{compared}（{truth_rate:.4f}）+ "
                  f"代理 {proxy_detail} → 组合 {value:.4f}")
    else:
        value = proxy
        detail = f"真值核对无可比项，回退代理：{proxy_detail}"
    return value, detail


# 「有意泛化」阈值形态：比较符 + 纯数字（无单位），后接泛化量词（项 / 个 / 条 / 轮 / 家 / 次 / 单 / 起 / 件 / 位 / 名）
_GENERALIZED_THRESH_RE = re.compile(r"^[≥≤<>]=?\s*\d+(?:\.\d+)?$")
_GENERALIZED_UNIT_RE = re.compile(r"^\s*(?:项|个|条|轮|家|次|单|起|件|位|名)")


def _config_section(text: str, heading: str) -> str:
    """business-config 指定二级节正文（`## <heading>...` 至下一 `## `）。"""
    m = re.search(rf"## {re.escape(heading)}[^\n]*\n(.*?)(?:\n## |\Z)", text or "", re.DOTALL)
    return m.group(1) if m else ""


def _l03_k_tokens(cfg_text: str) -> set[str]:
    """business-config 第五节 K 系信号阈值集合（用于登记册一致性校验）。"""
    tokens: set[str] = set()
    for line in _config_section(cfg_text, "五、信号规则阈值").splitlines():
        if re.match(r"\s*\|?\s*K\d{2}\b", line):
            tokens |= _thresh_tokens(line)
    return tokens


def _registry_threshold_tokens() -> dict[str, set[str]]:
    """业务线 → 结构化登记册（xlsx「信号规则」表）阈值集合；无则不含该业务线。"""
    import openpyxl

    out: dict[str, set[str]] = {}
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        if not cfg.exists():
            continue
        m = re.search(r"\{\{REGISTRY_PATH\}\}\s*=\s*(\S+)",
                      cfg.read_text(encoding="utf-8", errors="replace"))
        if not m:
            continue
        path = ROOT / m.group(1)
        if not path.exists() or path.suffix.lower() != ".xlsx":
            continue
        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        except Exception:
            continue
        try:
            if "信号规则" not in wb.sheetnames:
                continue
            rows = list(wb["信号规则"].iter_rows(values_only=True))
        finally:
            wb.close()
        out[b.rel] = _thresh_tokens(
            "\n".join(" ".join(str(c) for c in r if c is not None) for r in rows))
    return out


def l03_threshold_consistency(reports: dict[str, str]) -> tuple[float | None, str]:
    """阈值三处一致率（代理）：报告 ↔ business-config ↔ 登记册。

    口径升级（2026-11-19）：
      ① 分母仅统计与指标编号相邻（80 字符内）的阈值表达式；
      ② 「有意泛化」排除：未命中 business-config 阈值集合、且匹配泛化形态
         （比较符 + 纯数字，后接泛化量词）的表达式不计入分母，逐条列出并说明理由；
      ③ 登记册一致性：对存在结构化阈值表（xlsx 信号规则）的业务线，business-config
         的 K 系阈值须为登记册阈值集合子集，否则相应表达式判不命中。
    分母为 0（无可比阈值）时返回 None，由 `measure()` 标为 probe，不静默给 0。
    """
    reg_th = _registry_threshold_tokens()
    hit = total = 0
    excluded: list[dict] = []
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        cfg_text = cfg.read_text(encoding="utf-8", errors="replace") if cfg.exists() else ""
        cfg_th = _thresh_tokens(_plain(_clean(cfg_text))) if cfg_text else set()
        if not cfg_th:
            continue
        k_th = _l03_k_tokens(cfg_text)
        reg = reg_th.get(b.rel, set())
        for r in iter_reports():
            if r.business_line != b.rel:
                continue
            plain = _plain(_clean(reports.get(r.rel, "")))
            for m in _THRESH_RE.finditer(plain):
                pre = plain[max(0, m.start() - 80): m.start()]
                if not _ID_NEAR_RE.search(pre):
                    continue
                tok = m.group(0).replace(" ", "")
                if (tok not in cfg_th and _GENERALIZED_THRESH_RE.match(tok)
                        and _GENERALIZED_UNIT_RE.match(plain[m.end(): m.end() + 4])):
                    excluded.append({"report": r.rel, "expression": tok,
                                    "reason": "有意泛化（非配置阈值）"})
                    continue
                total += 1
                ok = tok in cfg_th
                if ok and tok in k_th and reg:
                    ok = tok in reg
                hit += 1 if ok else 0
    if not total:
        return None, "无可比阈值（分母 0，不可判）"
    detail = f"{hit}/{total} 指标相关阈值命中 business-config / 登记册"
    if excluded:
        detail += f"（排除有意泛化 {len(excluded)}：" \
                 f"{'、'.join(sorted({e['expression'] for e in excluded}))}）"
    return _ratio(hit, total), detail


# ---------------------------------------------------------------- N-6 机械代理（2026-11-19）

def _a02_entry_compliant(text: str, source: dict) -> bool:
    """单条来源条目分级合规：tier=4 需邻近『需核实原文』，tier=3 需邻近门户标注。"""
    import source_check

    u = source.get("url")
    if not isinstance(u, str) or not u:
        return True
    tier = source.get("tier")
    if tier == 4:
        return source_check.proximity_ok(text, u, source_check.MEDIA_MARKER)
    if tier == 3:
        return source_check.proximity_ok(text, u, source_check.PORTAL_MARKERS)
    return True


def a02_source_grading(reports: dict[str, str]) -> tuple[float | None, str]:
    """A-02 来源分级合规率（代理）：复用 source_check 分级结果。

    报告引用的来源登记条目中，tier=4 邻近『需核实原文』、tier=3 邻近
    『卖方预期/情绪/参考』即合规；分母为报告实际引用的可判定条目数。
    """
    import source_check

    comp = total = 0
    for b in iter_business_dirs():
        reg = source_check.load_registry(processed_data_dir(b.rel) / "source_registry.json")
        sources = reg.get("sources", []) if isinstance(reg, dict) else []
        if not sources:
            continue
        for r in iter_business_reports(b):
            text = reports.get(r.rel, "")
            if not text:
                continue
            norm = {source_check.normalize_url(u) for u in source_check.extract_urls(text)}
            for s in sources:
                u = s.get("url")
                if not u or source_check.normalize_url(u) not in norm:
                    continue
                total += 1
                comp += 1 if _a02_entry_compliant(text, s) else 0
    if not total:
        return None, "无可判定来源条目（分母 0，不可判）"
    return _ratio(comp, total), f"{comp}/{total} 来源条目分级合规"


def _a04_entry_fresh(period: str, cycle: str, updated: str) -> bool | None:
    """单条数据条目是否在声明时效内；无周期 / 无 updated 返回 None（不可判）。"""
    from info_gap_metrics import _FRESHNESS_TOLERANCE_MONTHS, _months

    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(updated or "").strip())
    if not m or not period:
        return None
    tol = _FRESHNESS_TOLERANCE_MONTHS.get(cycle, 1)
    return _months(period) - _months(f"{m.group(1)}-{m.group(2)}") <= tol


def a04_freshness(reports: dict[str, str]) -> tuple[float | None, str]:
    """A-04 新鲜度合规率（代理）：来源登记条目 updated 在声明时效内。

    数据条目 = 报告引用的来源登记条目（以 `updated` 为数据时点代理）；声明时效 =
    报告期次 − 周期容忍（info_gap_metrics._FRESHNESS_TOLERANCE_MONTHS）；
    合规 = updated 不早于窗口下限。分母 0 标 probe。
    """
    import source_check

    comp = total = 0
    for b in iter_business_dirs():
        reg = source_check.load_registry(processed_data_dir(b.rel) / "source_registry.json")
        sources = reg.get("sources", []) if isinstance(reg, dict) else []
        if not sources:
            continue
        for r in iter_business_reports(b):
            text = reports.get(r.rel, "")
            if not text or not r.period:
                continue
            norm = {source_check.normalize_url(u) for u in source_check.extract_urls(text)}
            for s in sources:
                u = s.get("url")
                if not u or source_check.normalize_url(u) not in norm:
                    continue
                fresh = _a04_entry_fresh(r.period, r.cycle, str(s.get("updated", "")))
                if fresh is None:
                    continue
                total += 1
                comp += 1 if fresh else 0
    if not total:
        return None, "无可判定数据条目（分母 0，不可判）"
    return _ratio(comp, total), f"{comp}/{total} 数据条目在声明时效内"


def l01_cross_section(reports: dict[str, str]) -> tuple[float | None, str]:
    """L-01 跨章节数值一致率（代理）：同一指标跨 h2.sec 章节取值冲突。"""
    total = conflict = 0
    for text in reports.values():
        html = _clean(text)
        ms = list(H2_RE.finditer(html))
        if not ms:
            continue
        by_id: dict[str, set[str]] = {}
        for i, m in enumerate(ms):
            seg = _plain(html[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(html)])
            for vm in _VALUE_PAIR_RE.finditer(seg):
                by_id.setdefault(vm.group(1), set()).add(_norm_num(vm.group(2)))
        for vs in by_id.values():
            total += 1
            if len(vs) > 1:
                conflict += 1
    if not total:
        return None, "无可比指标（分母 0，不可判）"
    return _ratio(total - conflict, total), f"冲突 {conflict}/{total} 指标跨章节一致"


def _terminology_entries(cfg_text: str) -> list[list[str]]:
    """解析 business-config 第三节「术语口径区分」条目 → 术语对列表。"""
    entries: list[list[str]] = []
    for line in _config_section(cfg_text, "三、术语口径区分").splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        body = re.sub(r"\*\*", "", line.lstrip("-").strip())
        terms = [re.sub(r"[（(].*?[)）]", "", x).strip() for x in re.split(r"[≠；;]", body)]
        terms = [x for x in terms if len(x) >= 2]
        if len(terms) >= 2:
            entries.append(terms)
    return entries


def _has_caliber_conflation(plain: str, terms: list[str]) -> bool:
    """术语对是否出现显式混用模式（=／即／等同／折算／合并）。"""
    for i in range(len(terms)):
        for j in range(len(terms)):
            if i == j:
                continue
            a, b = re.escape(terms[i]), re.escape(terms[j])
            for pat in (rf"{a}\s*[=＝]\s*{b}",
                        rf"{a}\s*即\s*{b}",
                        rf"{a}\s*等同(?:于)?\s*{b}",
                        rf"{a}\s*折算\s*(?:为)?\s*{b}",
                        rf"{a}\s*合并\s*(?:为)?\s*{b}",
                        rf"{a}\s*/\s*{b}\s*(?:口径|折算|合并)"):
                if re.search(pat, plain):
                    return True
    return False


def l02_caliber_consistency(reports: dict[str, str]) -> tuple[float | None, str]:
    """L-02 口径一致率（代理）：未检出术语口径显式混用的条目占比（负向检查）。"""
    ok = total = 0
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        if not cfg.exists():
            continue
        entries = _terminology_entries(cfg.read_text(encoding="utf-8", errors="replace"))
        if not entries:
            continue
        for r in iter_business_reports(b):
            plain = _plain(_clean(reports.get(r.rel, "")))
            for terms in entries:
                total += 1
                if not _has_caliber_conflation(plain, terms):
                    ok += 1
    if not total:
        return None, "无可比口径条目（分母 0，不可判）"
    return _ratio(ok, total), f"{ok}/{total} 口径条目未检出混用"


def l04_conclusion_evidence(reports: dict[str, str]) -> tuple[float | None, str]:
    """L-04 结论-证据一致率（代理）：决策卡结论有非空证据强度支撑。"""
    import decision_hub_check as dhc

    total = ok = 0
    for text in reports.values():
        t = dhc._strip_noise(text)
        for blk in dhc._blocks(t, dhc._CARD_RE):
            plain = dhc._TAG_RE.sub("", blk)
            if "结论" not in plain:
                continue
            total += 1
            m = re.search(r"证据强度：(.*?)(?:触发条件|反向证据|信息充分度|$)", plain, re.DOTALL)
            if m and m.group(1).strip():
                ok += 1
    if not total:
        return None, "无可比结论（分母 0，不可判）"
    return _ratio(ok, total), f"{ok}/{total} 结论有证据强度支撑"


_TL_ITEM_RE = re.compile(r'<div class="tl-item">.*?<div class="tl-date">(.*?)</div>', re.DOTALL)


def _period_year_month(period: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"(\d{4})-(\d{2})", period or "")
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.fullmatch(r"(\d{4})-Q([1-4])", period or "")
    if m:
        return int(m.group(1)), int(m.group(2)) * 3
    m = re.fullmatch(r"(\d{4})", period or "")
    if m:
        return int(m.group(1)), 1
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", period or "")
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def _parse_timeline_dates(items: list[str], period: str) -> list[tuple[int, int, int]]:
    """解析时间线日期；MM-DD 按报告期次与时间线顺序解析年。"""
    pm = _period_year_month(period)
    if not pm:
        return []
    py, _pmonth = pm
    out: list[tuple[int, int, int]] = []
    prev: tuple[int, int, int] | None = None
    for raw in items:
        s = _plain(raw).strip()
        d: tuple[int, int, int] | None = None
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
        if m:
            d = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if d is None:
            m = re.fullmatch(r"(\d{4})-(\d{2})", s)
            if m:
                d = (int(m.group(1)), int(m.group(2)), 0)
        if d is None:
            m = re.fullmatch(r"(\d{4})", s)
            if m:
                d = (int(m.group(1)), 1, 1)
        if d is None:
            m = re.fullmatch(r"(\d{1,2})-(\d{1,2})(?:/(\d{1,2})-(\d{1,2}))?", s)
            if m:
                mm, dd = int(m.group(1)), int(m.group(2))
                cands = [(y, mm, dd) for y in (py - 1, py, py + 1)
                         if prev is None or (y, mm, dd) >= prev]
                d = min(cands) if cands else (py, mm, dd)
        if d is not None:
            out.append(d)
            prev = d
    return out


def l05_timeline_consistency(reports: dict[str, str]) -> tuple[float | None, str]:
    """L-05 时间线一致率（代理）：时间线事件无日期倒置。"""
    ok = total = 0
    for rel, text in reports.items():
        det = detect_report(Path(rel).name)
        period = det[1] if det else ""
        items = _TL_ITEM_RE.findall(_clean(text))
        dates = _parse_timeline_dates(items, period)
        for i, d in enumerate(dates):
            total += 1
            if i == 0 or d >= dates[i - 1]:
                ok += 1
    if not total:
        return None, "无可解析时间线事件（分母 0，不可判）"
    return _ratio(ok, total), f"{ok}/{total} 时间线事件无日期倒置"


def _topic_tokens(cfg_text: str) -> list[str]:
    m = re.search(r"\{\{TOPIC\}\}\s*=\s*(.+)", cfg_text)
    if not m:
        return []
    s = re.sub(r"[（(].*?[)）]", "", m.group(1))
    return [x for x in re.split(r"\s+|·|/|—|-", s) if len(x) >= 2]


def r05_topic_content_match(reports: dict[str, str]) -> tuple[float | None, str]:
    """R-05 主题-内容匹配率（代理）：报告命中业务线 {{TOPIC}} 主题词。"""
    hit = total = 0
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        if not cfg.exists():
            continue
        toks = _topic_tokens(cfg.read_text(encoding="utf-8", errors="replace"))
        if not toks:
            continue
        for r in iter_business_reports(b):
            text = reports.get(r.rel, "")
            if not text:
                continue
            total += 1
            title = TITLE_RE.search(text)
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
            head = (title.group(1) if title else "") + " " + (h1.group(1) if h1 else "")
            body = _plain(text)
            if any(t in head or t in body for t in toks):
                hit += 1
    if not total:
        return None, "无可判报告（分母 0，不可判）"
    return _ratio(hit, total), f"{hit}/{total} 报告命中业务线主题词"


def r03_duplicate_rate(reports: dict[str, str]) -> tuple[float, str]:
    """跨主题重复率：跨业务线重复段落数 / 段落总数（段落级精确重合代理）。"""
    by_line: dict[str, set[str]] = {}
    for rel, text in reports.items():
        line = rel.split("/reports/")[0]
        paras = set()
        for m in _PARA_RE.finditer(_clean(text)):
            p = re.sub(r"\s+", "", _plain(m.group(0)))
            if len(p) < 20:
                continue
            # 来源/链接段落（机构名 + URL / 域名）是共享引用，不属于「内容同质化」；
            # 排除后 R-03 只衡量分析性正文的跨主题重复。
            if _SRC_LINK_RE.search(p):
                continue
            if _BOILERPLATE_RE.search(p):
                continue
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


def _shared_fact_tokens() -> set[str]:
    """有事实卡片库的业务线标识（动态派生自 engine/fact_cards/*.json 的 used_by）。"""
    tokens: set[str] = set()
    card_dir = ROOT / "engine" / "fact_cards"
    if not card_dir.is_dir():
        return tokens
    for f in sorted(card_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for c in data.get("cards", []):
            for bl in c.get("used_by", []) or []:
                tokens.add(str(bl))
    return tokens


def _in_shared_fact(line: str, tokens: set[str]) -> bool:
    """业务线 rel 的任一路径段命中卡片库 used_by 标识即视为共享事实域。"""
    return bool(set(Path(line).parts) & tokens)


def i04_fact_card(reports: dict[str, str]) -> tuple[float, str]:
    """事实卡片引用率：有事实卡片库的业务线报告中引用 [FC-…] 的占比。

    口径（2026-11-19 对齐字典）：分母 = 有卡片库的业务线（动态派生自
    engine/fact_cards/*.json 的 used_by）的报告数；分子 = 其中引用 [FC-…] 的
    报告数。无卡片库的业务线不计入分母（不静默给 0）。
    """
    tokens = _shared_fact_tokens()
    scoped = {rel: t for rel, t in reports.items()
              if _in_shared_fact(rel.split("/reports/")[0], tokens)}
    ok = sum(1 for t in scoped.values() if FC_REF_RE.search(_plain(t)))
    return _ratio(ok, len(scoped)), \
        f"{ok}/{len(scoped)} 份共享事实域报告使用 [FC-…] 指针"


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
        "A-02": a02_source_grading(reports),
        "A-03": a03_combined(reports),
        "A-04": a04_freshness(reports),
        "A-05": a05_link_reachability(),
        "L-01": l01_cross_section(reports),
        "L-02": l02_caliber_consistency(reports),
        "L-03": l03_threshold_consistency(reports),
        "L-04": l04_conclusion_evidence(reports),
        "L-05": l05_timeline_consistency(reports),
        "R-01": r01_attribution(reports),
        "R-03": r03_duplicate_rate(reports),
        "R-02": r02_dimension_priority(reports),
        "R-04": r04_anchor(reports),
        "R-05": r05_topic_content_match(reports),
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
