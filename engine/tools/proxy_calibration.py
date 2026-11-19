#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""代理指标抽样校准（PROXY-CALIBRATION v1.0，方案 T-02）。

问题：代理口径指标（A-03 / L-03 / IGI-05 等）「达标」不等于信息质量达标
（Goodhart 风险）。本工具建立**代理判定 → 人工真值**的抽样校准，量化代理的
precision / recall，并留口径版本与样本留痕。

工作流（两步，人工核验不可跳过）：

  1) 抽样落表：`--metric <ID> --n 200 --emit`
     分层抽样（主题 / 业务线 / 断言类型）→ 落样本表到 records 目录
     （`engine/audit/records` 下 `proxy-calibration/` 子目录）的 `<metric>.json`；
     每单元含 `proxy_verdict`（代理判定）与 `truth: null`（待人工核验）。
  2) 评分：`--metric <ID> --score --emit`（样本表 truth 已人工填齐）
     或 `--score --truth <fixture.json>`（测试 / 复核用真值文件）
     → 混淆矩阵 TP/FP/FN/TN + precision / recall / F1 + 口径版本号，回写记录。

口径版本：`CALIBER_VERSION = proxy-calibration-v1.0`。口径变更须升版本并留理由
（不得为提升代理值放宽分母 / 块类型）。
确定性：抽样对 `(metric, n, seed, 语料)` 字节可重放（`--seed` 默认固定值，
抽取顺序按 uid 哈希排序，不取墙钟、不用 Python `hash()`）；记录含 `--date`
（默认当天，ISO）与样本数。**无人工核验时 truth 一律为 null，结果不产出**
（不编造校准数值）。

已接线代理目标（unit 抽取复用既有工具，保证与指标实测同口径）：
  IGI-05 / A-01  含数字断言块（li / p / div.kpi / stat-strip，剔除非断言块；
                 代理判定 = 窗口内存在来源指针，复用 `info_gap_metrics`）
  A-03           报告内同指标编号的显式数值对（复用 `metric_coverage` 的
                 `_VALUE_PAIR_RE`；代理判定 = 同报告内取值唯一）
其余代理指标（见 `PROXY_METRICS`）：字典已加 `calibration` 备注，unit 抽取
**待接线**——工具显式报「未接线」并退出，不伪造校准值。

用法：
    python engine/tools/proxy_calibration.py --list
    python engine/tools/proxy_calibration.py --metric IGI-05 --n 200 --emit
    python engine/tools/proxy_calibration.py --metric IGI-05 --score --emit
    python engine/tools/proxy_calibration.py --metric A-03 --score --truth <fixture.json>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_reports  # noqa: E402

SCHEMA_VERSION = "1.0"
CALIBER_VERSION = "proxy-calibration-v1.0"
RECORDS_DIR = ROOT / "engine" / "audit" / "records" / "proxy-calibration"
DEFAULT_N = 200
DEFAULT_SEED = 20261119

# 代理口径指标清单（方案 T-02）：字典 note 含「代理」、或工具 docstring 明示
# 「代理」、或与被标定代理同口径（A-01 与 IGI-05 同测量）。
# ⚠️ 只加备注，不改阈值；新增代理指标须同步在此登记。
PROXY_METRICS: tuple[str, ...] = (
    "C-04", "A-01", "A-02", "A-03", "A-04",
    "L-01", "L-02", "L-03", "L-04", "L-05",
    "R-03", "R-05", "I-02", "I-05", "I-06", "IGI-05",
)
# 已接线 unit 抽取的代理目标（其余显式报「未接线」，不伪造）
WIRED_TARGETS: tuple[str, ...] = ("IGI-05", "A-01", "A-03")

DICT_PATH = Path(__file__).resolve().parent / "metrics-dictionary.json"


# ---------------------------------------------------------------- 基础工具

def _uid(*parts: str) -> str:
    """稳定单元标识：sha1（不用 Python hash()，跨进程可重放）。"""
    return hashlib.sha1("\x00".join(parts).encode("utf-8")).hexdigest()[:12]


def _ratio(num: int, den: int) -> float | None:
    return round(num / den, 4) if den else None


def _snippet(text: str, limit: int = 160) -> str:
    """人工核验用摘要：压平空白、限长（不截断关键数值）。"""
    s = " ".join((text or "").split())
    return s[:limit]


def _metric_name(metric_id: str) -> str:
    try:
        data = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    for m in data.get("metrics", []):
        if m.get("metric_id") == metric_id:
            return str(m.get("name", ""))
    return ""


def proxy_metrics(dictionary: dict | None = None) -> list[str]:
    """按字典顺序返回代理指标 ID（与 metrics-dictionary.json 同步）。"""
    data = dictionary or json.loads(DICT_PATH.read_text(encoding="utf-8"))
    ids = {m.get("metric_id") for m in data.get("metrics", [])}
    # 字典里存在但清单未登记的指标不是代理指标（忽略）；清单登记但字典缺失则显式提示
    absent = [m for m in PROXY_METRICS if m not in ids]
    if absent:
        print(f"[W] 代理清单登记但字典缺失：{', '.join(absent)}", file=sys.stderr)
    return [m for m in PROXY_METRICS if m in ids]


# ---------------------------------------------------------------- unit 抽取

def _block_type(block: str) -> str:
    low = block.lstrip()[:400].lower()
    if low.startswith("<li"):
        return "li"
    if low.startswith("<p"):
        return "p"
    if "stat-strip" in low:
        return "stat-strip"
    if "kpi" in low:
        return "kpi"
    return "other"


def iter_assertion_units(text: str, rel: str) -> list[dict]:
    """含数字断言块 unit（与 IGI-05 / A-01 实测同口径，复用 info_gap_metrics）。

    块类型 = li / p + div.kpi / stat-strip（td 不纳入，与 R4 同口径）；
    剔页头 / 版本 / 图注 / 案例 / 说明等非断言块（`_META_RE`）；
    代理判定 = 同表格行或 ±240 字符窗口内存在来源指针（`_source_ptr_hit`）。
    """
    import info_gap_metrics as ig

    html = ig._clean(text)
    out: list[dict] = []
    for m in ig._BLOCK_RE.finditer(html):
        block = m.group(0)
        plain = ig._TAG_RE.sub("", block)
        if not ig._HAS_DIGIT_RE.search(plain):
            continue
        if ig._META_RE.search(plain):
            continue
        tr_start = html.rfind("<tr", 0, m.start())
        tr_end = html.find("</tr>", m.end())
        if tr_start != -1 and tr_end != -1 and tr_end - tr_start < 4000:
            window = html[tr_start: tr_end + 5]
        else:
            window = html[max(0, m.start() - 240): m.end() + 240]
        out.append({
            "uid": _uid(rel, block),
            "report": rel,
            "block_type": _block_type(block),
            "proxy_verdict": bool(ig._source_ptr_hit(window)),
            "detail": _snippet(plain),
            "truth": None,
        })
    return out


def iter_value_pair_units(text: str, rel: str) -> list[dict]:
    """A-03 显式数值对 unit（复用 metric_coverage 的数值对口径）。

    以「报告 × 指标编号」为一个 unit：代理判定 = 该编号在本报告内显式取值唯一
    （同报告内自相矛盾即代理判不达标）；真值 = 与结构化登记册比对。
    """
    import metric_coverage as mc

    plain = mc._plain(mc._clean(text))
    by_id: dict[str, set[str]] = {}
    for m in mc._VALUE_PAIR_RE.finditer(plain):
        by_id.setdefault(m.group(1), set()).add(mc._norm_num(m.group(2)))
    out: list[dict] = []
    for iid in sorted(by_id):
        vals = sorted(by_id[iid])
        out.append({
            "uid": _uid(rel, "value-pair", iid),
            "report": rel,
            "block_type": "value_pair",
            "proxy_verdict": len(vals) == 1,
            "detail": _snippet(f"{iid} 显式数值 {vals}"),
            "truth": None,
        })
    return out


def collect_units(metric_id: str, reports: dict[str, str]) -> list[dict]:
    """按指标收集全部候选 unit（未抽样）。

    Raises:
        NotImplementedError: 该代理指标 unit 抽取待接线（不伪造）。
    """
    if metric_id not in WIRED_TARGETS:
        raise NotImplementedError(f"代理指标 {metric_id} 的 unit 抽取待接线（不伪造校准值）")
    out: list[dict] = []
    for ref in iter_reports():
        if ref.category != "report":
            continue
        text = reports.get(ref.rel, "")
        if not text:
            continue
        theme = ref.business_line.split("/")[1] if "/" in ref.business_line else ""
        units = (iter_value_pair_units(text, ref.rel) if metric_id == "A-03"
                 else iter_assertion_units(text, ref.rel))
        for u in units:
            u["theme"] = theme
            u["business_line"] = ref.business_line
        out.extend(units)
    return out


# ---------------------------------------------------------------- 分层抽样

def _stratum_key(unit: dict) -> tuple[str, str, str]:
    return (unit.get("theme", ""), unit.get("business_line", ""), unit.get("block_type", ""))


def stratified_sample(units: list[dict], n: int, seed: int = DEFAULT_SEED,
                      metric_id: str = "") -> tuple[list[dict], dict]:
    """分层抽样（主题 / 业务线 / 断言类型），比例分配 + 最大余数法。

    确定性：层内按 `(seed, metric, uid)` 哈希排序取前 k，不取墙钟。
    n >= 总数时全取并标 `truncated=True`（不静默截断）。
    """
    if n <= 0:
        raise ValueError(f"抽样数须为正整数：{n}")
    total = len(units)
    if total == 0:
        return [], {"requested_n": n, "total": 0, "truncated": False, "allocated": {}}
    if n >= total:
        return sorted(units, key=lambda u: u["uid"]), {
            "requested_n": n, "total": total, "truncated": True, "allocated": {}}

    strata: dict[tuple[str, str, str], list[dict]] = {}
    for u in sorted(units, key=lambda x: x["uid"]):
        strata.setdefault(_stratum_key(u), []).append(u)
    keys = sorted(strata)
    quotas = {k: n * len(strata[k]) / total for k in keys}
    alloc = {k: int(quotas[k]) for k in keys}
    remainder = n - sum(alloc.values())
    for k in sorted(keys, key=lambda k: (-(quotas[k] - alloc[k]), k))[:remainder]:
        alloc[k] += 1
    # 覆盖保障：样本量不小于层数时，每层至少 1（从最大层匀出），避免薄层失声
    if n >= len(keys):
        for k in keys:
            if alloc[k] == 0:
                donor = max(keys, key=lambda x: (alloc[x], x))
                if alloc[donor] > 1:
                    alloc[donor] -= 1
                    alloc[k] = 1

    picked: list[dict] = []
    for k in keys:
        pool = sorted(strata[k], key=lambda u: _uid(str(seed), metric_id, u["uid"]))
        picked.extend(pool[:alloc[k]])
    picked.sort(key=lambda u: u["uid"])
    return picked, {
        "requested_n": n, "total": total, "truncated": False,
        "allocated": {"|".join(k): alloc[k] for k in keys},
    }


# ---------------------------------------------------------------- 混淆矩阵

def confusion(units: list[dict]) -> dict:
    """代理判定 vs 人工真值 -> 混淆矩阵 + precision / recall / F1。

    truth 为 None 的单元不计入分母，并在 `pending` 显式呈现；
    precision / recall 分母为 0 时返回 None（不静默给 0）。
    """
    rows = [u for u in units if u.get("truth") is not None]
    tp = sum(1 for u in rows if u["proxy_verdict"] and u["truth"])
    fp = sum(1 for u in rows if u["proxy_verdict"] and not u["truth"])
    fn = sum(1 for u in rows if not u["proxy_verdict"] and u["truth"])
    tn = sum(1 for u in rows if not u["proxy_verdict"] and not u["truth"])
    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    if precision is None or recall is None:
        f1 = None
    elif precision + recall == 0:
        f1 = 0.0
    else:
        f1 = round(2 * precision * recall / (precision + recall), 4)
    return {
        "n": len(rows), "pending": len(units) - len(rows),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": precision, "recall": recall, "f1": f1,
        "agreement": _ratio(tp + tn, len(rows)),
        "proxy_positive": tp + fp, "truth_positive": tp + fn,
    }


# ---------------------------------------------------------------- 记录读写

def build_record(metric_id: str, units: list[dict], sample: dict, run_date: str,
                 result: dict | None = None, note: str = "") -> dict:
    """校准记录（确定性 JSON：排序键、无时间戳；日期为显式 `--date`）。"""
    strata: dict[str, int] = {}
    for u in units:
        key = "|".join(_stratum_key(u))
        strata[key] = strata.get(key, 0) + 1
    pending = sum(1 for u in units if u.get("truth") is None)
    return {
        "schema_version": SCHEMA_VERSION,
        "caliber_version": CALIBER_VERSION,
        "metric_id": metric_id,
        "metric_name": _metric_name(metric_id),
        "date": run_date,
        "requested_n": sample.get("requested_n"),
        "sample_size": len(units),
        "seed": sample.get("seed"),
        "sampling": {k: v for k, v in sample.items() if k != "seed"},
        "strata": {k: strata[k] for k in sorted(strata)},
        "pending_truth": pending,
        "result": result,
        "note": note,
        "units": units,
    }


def render_record(record: dict) -> str:
    return json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def record_path(records_dir: Path | None, metric_id: str) -> Path:
    return (records_dir or RECORDS_DIR) / f"{metric_id}.json"


def load_record(records_dir: Path | None, metric_id: str) -> dict | None:
    p = record_path(records_dir, metric_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def write_record(record: dict, records_dir: Path | None = None) -> Path:
    p = record_path(records_dir, record["metric_id"])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_record(record), encoding="utf-8")
    return p


def load_truth(path: str | Path) -> dict[str, bool]:
    """读人工真值文件 -> {uid: bool}。

    支持三种形态：`{"<uid>": true}` 映射；`{"all": true|false}`；
    `{"units": [{"uid": ..., "truth": ...}, ...]}`。
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("all"), bool):
        return {"__all__": bool(data["all"])}
    if isinstance(data, dict) and isinstance(data.get("units"), list):
        return {str(u["uid"]): bool(u["truth"]) for u in data["units"]
                if u.get("truth") is not None}
    if isinstance(data, dict):
        return {str(k): bool(v) for k, v in data.items() if isinstance(v, bool)}
    raise ValueError(f"真值文件形态不识别：{path}")


def apply_truth(units: list[dict], truth: dict[str, bool]) -> int:
    """把真值映射应用到 unit（`__all__` 覆盖全部）-> 命中条数。"""
    hit = 0
    for u in units:
        if "__all__" in truth:
            u["truth"] = truth["__all__"]
            hit += 1
        elif u["uid"] in truth:
            u["truth"] = truth[u["uid"]]
            hit += 1
    return hit


def export_csv(units: list[dict], path: str | Path) -> Path:
    """导出人工核验表（CSV：truth 留空待填）。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["uid", "report", "theme", "business_line", "block_type",
                    "proxy_verdict", "truth", "detail"])
        for u in units:
            w.writerow([u["uid"], u["report"], u.get("theme", ""),
                        u.get("business_line", ""), u.get("block_type", ""),
                        "1" if u["proxy_verdict"] else "0",
                        "" if u.get("truth") is None else ("1" if u["truth"] else "0"),
                        u.get("detail", "")])
    return p


# ---------------------------------------------------------------- CLI

def _reports_text() -> dict[str, str]:
    return {r.rel: (ROOT / r.rel).read_text(encoding="utf-8", errors="replace")
            for r in iter_reports() if r.category == "report"}


def _print_result(metric_id: str, record: dict) -> None:
    res = record.get("result")
    print(f"指标：{metric_id} {record.get('metric_name', '')}")
    print(f"口径版本：{record['caliber_version']}；日期：{record['date']}；"
          f"样本数：{record['sample_size']}（请求 {record['requested_n']}）")
    if res is None:
        print(f"结果：待人工核验（truth 未填齐 {record['pending_truth']} 条）——不产出 precision / recall")
        return
    print(f"混淆矩阵：TP={res['tp']} FP={res['fp']} FN={res['fn']} TN={res['tn']}"
          f"（n={res['n']}，pending={res['pending']}）")
    print(f"precision={res['precision']}  recall={res['recall']}  f1={res['f1']}  "
          f"一致率={res['agreement']}")
    print("⚠️ 代理达标 ≠ 真值达标：以上为代理判定与人工真值的抽样一致性，非语义达标证明")


def main() -> int:
    ap = argparse.ArgumentParser(description="代理指标抽样校准（PROXY-CALIBRATION v1.0）")
    ap.add_argument("--metric", help="代理指标 ID（如 IGI-05 / A-01 / A-03）")
    ap.add_argument("--n", type=int, default=DEFAULT_N, help=f"抽样数（默认 {DEFAULT_N} 断言）")
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED, help=f"抽样种子（默认 {DEFAULT_SEED}）")
    ap.add_argument("--date", help="校准日期（ISO，默认当天；建议显式固定以便复现）")
    ap.add_argument("--emit", action="store_true",
                    help="落记录到 records 目录（engine/audit/records 下 proxy-calibration/ 子目录）")
    ap.add_argument("--score", action="store_true", help="读样本表真值 -> 混淆矩阵 + precision/recall/F1")
    ap.add_argument("--truth", help="真值文件（测试 / 复核；{uid: bool} / {all: bool} / {units: [...]}）")
    ap.add_argument("--records-dir",
                    help="记录目录（默认 engine/audit/records 下 proxy-calibration/ 子目录）")
    ap.add_argument("--export-csv", help="导出人工核验 CSV（truth 留空）")
    ap.add_argument("--list", action="store_true", help="列出代理指标与接线状态")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出记录")
    args = ap.parse_args()

    dictionary = json.loads(DICT_PATH.read_text(encoding="utf-8"))
    proxies = proxy_metrics(dictionary)

    if args.list:
        for mid in proxies:
            print(f"{mid:<8} {'已接线' if mid in WIRED_TARGETS else '待接线'}  {_metric_name(mid)}")
        return 0

    if not args.metric:
        ap.error("须指定 --metric（或 --list 查看代理指标）")
    metric_id = args.metric
    if metric_id not in proxies:
        print(f"[ERROR] {metric_id} 不是登记的代理指标（--list 查看）；不伪造校准值", file=sys.stderr)
        return 1

    records_dir = Path(args.records_dir) if args.records_dir else None
    run_date = args.date or date.today().isoformat()
    reports = _reports_text()

    if args.score:
        sheet = load_record(records_dir, metric_id)
        if sheet is not None:
            units = sheet["units"]
            sample = {"requested_n": sheet.get("requested_n"), "seed": sheet.get("seed")}
        elif args.truth:
            try:
                units_all = collect_units(metric_id, reports)
            except NotImplementedError as e:
                print(f"[ERROR] {e}", file=sys.stderr)
                return 1
            units, sampling = stratified_sample(units_all, args.n, args.seed, metric_id)
            sample = {**sampling, "seed": args.seed}
        else:
            print(f"[ERROR] 无样本表且未给 --truth：先 `--metric {metric_id} --emit` 落表并由人工核验 truth",
                  file=sys.stderr)
            return 1
        if args.truth:
            try:
                apply_truth(units, load_truth(args.truth))
            except (OSError, ValueError, json.JSONDecodeError) as e:
                print(f"[ERROR] 真值文件不可用：{e}", file=sys.stderr)
                return 1
        pending = sum(1 for u in units if u.get("truth") is None)
        if pending:
            # 不伪造：truth 未填齐时不产出 precision / recall
            record = build_record(metric_id, units, sample, run_date, result=None,
                                  note=f"待人工核验 {pending} 条（不产出 precision / recall）")
            if args.emit:
                print(f"[emit] {write_record(record, records_dir)}")
            if args.json:
                print(render_record(record), end="")
            else:
                _print_result(metric_id, record)
            return 0
        result = confusion(units)
        record = build_record(metric_id, units, sample, run_date, result=result,
                              note="人工真值已填齐")
        if args.emit:
            print(f"[emit] {write_record(record, records_dir)}")
        if args.json:
            print(render_record(record), end="")
        else:
            _print_result(metric_id, record)
        return 0

    try:
        units_all = collect_units(metric_id, reports)
    except NotImplementedError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1
    if not units_all:
        print(f"[ERROR] {metric_id} 无可用 unit（语料为空）", file=sys.stderr)
        return 1
    units, sampling = stratified_sample(units_all, args.n, args.seed, metric_id)
    sample = {**sampling, "seed": args.seed}
    record = build_record(metric_id, units, sample, run_date,
                          result=None, note="抽样落表，待人工核验 truth")
    if args.emit:
        print(f"[emit] {write_record(record, records_dir)}")
    if args.export_csv:
        print(f"[csv] {export_csv(units, args.export_csv)}")
    if args.json:
        print(render_record(record), end="")
    else:
        _print_result(metric_id, record)
        by_type: dict[str, int] = {}
        for u in units:
            by_type[u["block_type"]] = by_type.get(u["block_type"], 0) + 1
        print(f"分层：{ {k: by_type[k] for k in sorted(by_type)} }；"
              f"代理判定基线：positive {sum(1 for u in units if u['proxy_verdict'])}/{len(units)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
