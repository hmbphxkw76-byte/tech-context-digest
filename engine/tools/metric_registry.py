#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""指标注册与单一事实源服务（T3）。

指标定义与阈值唯一来源为 `metrics-dictionary.json`；本模块提供：
  - 字典读取 / 别名解析 / 阈值求值（audit L3 与 quality rubric 共用）；
  - 归一化存储（data/processed/<theme>/<维度段...>/metrics/metrics.csv）；
  - 适配器：xlsx 登记册 / Markdown 台账 → 归一化行。

阈值表达式支持：>= <= > < = 与百分数（自动归一为小数）。
退出码：0 通过；1 用法或数据错误；2 存在不达标项。

用法：
    python engine/tools/metric_registry.py list
    python engine/tools/metric_registry.py get A-01
    python engine/tools/metric_registry.py eval A-01 0.97
    python engine/tools/metric_registry.py export --xlsx <path> --out <csv>
    python engine/tools/metric_registry.py export --md <path> --out <csv>
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, processed_data_dir  # noqa: E402

DICT_PATH = Path(__file__).resolve().parent / "metrics-dictionary.json"
REQUIRED_FIELDS = ("date", "indicator_id", "value", "unit", "caliber", "source_id", "status")
VALID_STATUS = {"已核验", "部分核验", "未核验"}


# ---------------------------------------------------------------- 字典

def load_dictionary(path: Path = DICT_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def metric_ids(dictionary: dict) -> list[str]:
    return [m["metric_id"] for m in dictionary.get("metrics", [])]


def get_metric(dictionary: dict, metric_id: str) -> dict | None:
    for m in dictionary.get("metrics", []):
        if m.get("metric_id") == metric_id:
            return m
    return None


def by_alias(dictionary: dict, alias: str) -> dict | None:
    for m in dictionary.get("metrics", []):
        if alias in m.get("aliases", []):
            return m
    return None


def resolve_alias(dictionary: dict, alias: str) -> tuple[dict | None, list[str]]:
    """别名解析（唯一性保障）-> (命中指标, 冲突指标 id 列表)。

    别名为跨指标唯一事实源的一部分：若同一别名被多个指标声明，返回首个命中并
    把其余指标 id 作为冲突上报，由 `dictionary_conflicts` / CLI `check` 阻断。
    """
    hits = [m for m in dictionary.get("metrics", []) if alias in m.get("aliases", [])]
    if not hits:
        return None, []
    return hits[0], [m.get("metric_id", "?") for m in hits[1:]]


def dictionary_conflicts(dictionary: dict) -> list[str]:
    """字典冲突检测 -> 说明列表：metric_id 重复 / 别名跨指标重复。"""
    issues: list[str] = []
    ids: dict[str, int] = {}
    for m in dictionary.get("metrics", []):
        mid = str(m.get("metric_id", "")).strip()
        ids[mid] = ids.get(mid, 0) + 1
    for mid, n in ids.items():
        if n > 1:
            issues.append(f"metric_id 重复：{mid} 出现 {n} 次（须唯一）")
    alias_map: dict[str, list[str]] = {}
    for m in dictionary.get("metrics", []):
        for a in m.get("aliases", []) or []:
            alias_map.setdefault(str(a), []).append(str(m.get("metric_id", "?")))
    for alias, owners in alias_map.items():
        if len(owners) > 1:
            issues.append(f"别名冲突：{alias} 同时属于 {owners}（别名须跨指标唯一）")
    return issues


def dedupe_aliases(dictionary: dict) -> tuple[dict, list[str]]:
    """去除重复别名（保留首次归属）-> (新字典, 去除说明)。

    去重处理：同一别名被多个指标声明时，仅保留字典序最靠前的指标归属，
    其余别名移除并记录说明；metric_id 重复不在此处理（须人工修正）。
    """
    removed: list[str] = []
    seen: dict[str, str] = {}
    out = json.loads(json.dumps(dictionary))  # 深拷贝，不改原对象
    for m in out.get("metrics", []):
        keep: list[str] = []
        for a in m.get("aliases", []) or []:
            owner = seen.get(a)
            if owner is None:
                seen[a] = str(m.get("metric_id", "?"))
                keep.append(a)
            else:
                removed.append(f"别名 {a}：从 {m.get('metric_id')} 移除（已归属 {owner}）")
        m["aliases"] = keep
    return out, removed


def check_dictionary(dictionary: dict) -> list[str]:
    """字典全量体检 -> 问题列表（冲突 / 必填字段 / 阈值可解析 / 级别合法）。"""
    issues = list(dictionary_conflicts(dictionary))
    valid_sev = {"P0", "P1", "P2", "P3"}
    valid_det = {"TOOL", "LLM", "MIXED"}
    for m in dictionary.get("metrics", []):
        mid = str(m.get("metric_id", "?"))
        for field in ("metric_id", "name", "formula", "threshold", "severity", "detected_by", "owner"):
            if not str(m.get(field, "")).strip():
                issues.append(f"{mid} 缺字段：{field}")
        try:
            parse_threshold(str(m.get("threshold", "")))
        except ValueError as e:
            issues.append(f"{mid} 阈值不可解析：{e}")
        if str(m.get("severity", "")) not in valid_sev:
            issues.append(f"{mid} severity 非法：{m.get('severity')}（合法 {sorted(valid_sev)}）")
        if str(m.get("detected_by", "")) not in valid_det:
            issues.append(f"{mid} detected_by 非法：{m.get('detected_by')}（合法 {sorted(valid_det)}）")
    return issues


# ---------------------------------------------------------------- 阈值

def parse_threshold(expr: str) -> tuple[str, float]:
    """>=0.95 -> ('>=', 0.95)；100% -> ('=', 1.0)。"""
    s = str(expr).strip().replace(" ", "")
    m = re.fullmatch(r"(>=|<=|>|<|=)?([0-9.]+)(%?)", s)
    if not m:
        raise ValueError(f"无法解析阈值表达式: {expr}")
    op = m.group(1) or "="
    val = float(m.group(2))
    if m.group(3) == "%":
        val = val / 100.0
    return op, val


def _as_float(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace("%", "")
    return float(s) / 100.0 if str(value).strip().endswith("%") else float(s)


def evaluate(expr: str, value) -> tuple[bool, str]:
    op, target = parse_threshold(expr)
    v = _as_float(value)
    ok = {
        ">=": v >= target, "<=": v <= target, ">": v > target,
        "<": v < target, "=": abs(v - target) < 1e-9,
    }[op]
    return ok, f"{v:.4f} {op} {target:.4f} -> {'达标' if ok else '不达标'}"


# ---------------------------------------------------------------- 归一化存储

def normalize_rows(rows: list[dict]) -> tuple[list[dict], list[str]]:
    """校验并归一化数据行 -> (合法行, 错误说明)。"""
    ok_rows: list[dict] = []
    errors: list[str] = []
    for i, r in enumerate(rows, start=1):
        missing = [f for f in REQUIRED_FIELDS if f not in r or r.get(f) in (None, "")]
        if missing:
            errors.append(f"第 {i} 行缺字段：{','.join(missing)}")
            continue
        status = str(r.get("status", ""))
        if status not in VALID_STATUS:
            errors.append(f"第 {i} 行 status 非法：{status}")
            continue
        ok_rows.append({k: r.get(k) for k in REQUIRED_FIELDS})
    return ok_rows, errors


def dedupe_rows(rows: list[dict], case_sensitive: bool = True) -> tuple[list[dict], list[dict], list[dict]]:
    """去重（大小写敏感策略）-> (保留行, 血缘, 冲突明细)。

    键 = (date, indicator_id, caliber)。大小写敏感时按原值精确比对；
    `case_sensitive=False` 时 indicator_id / caliber 归一为小写（date 不变）。
    同键同值 -> 重复（记入血缘）；同键不同值 / 单位 / 来源 -> 冲突（保留首行，记明细）。
    """
    def _k(r: dict) -> tuple:
        iid = str(r.get("indicator_id", ""))
        cal = str(r.get("caliber", ""))
        if not case_sensitive:
            iid, cal = iid.lower(), cal.lower()
        return (str(r.get("date", "")), iid, cal)

    kept: list[dict] = []
    lineage: list[dict] = []
    conflicts: list[dict] = []
    index: dict[tuple, int] = {}
    for i, r in enumerate(rows, start=1):
        key = _k(r)
        if key not in index:
            index[key] = len(kept)
            kept.append({k: r.get(k) for k in REQUIRED_FIELDS})
            lineage.append({"key": list(key), "kept_row": i, "dropped_rows": [], "conflicts": []})
            continue
        pos = index[key]
        a, b = kept[pos], r
        diff = [f for f in ("value", "unit", "source_id") if str(a.get(f)) != str(b.get(f))]
        if diff:
            item = {"key": list(key), "kept_row": lineage[pos]["kept_row"], "fields": diff,
                    "kept": {f: a.get(f) for f in diff}, "incoming": {f: b.get(f) for f in diff}}
            conflicts.append(item)
            lineage[pos]["conflicts"].append(item)
        else:
            lineage[pos]["dropped_rows"].append(i)
    return kept, lineage, conflicts


def measured_from_info_gap() -> dict[str, float]:
    """从 info_gap_metrics 取 IGI-01..08 实测值；不可用时返回空字典（不静默假装达标）。"""
    try:
        from info_gap_metrics import compute
        return dict(compute()["values"])
    except Exception:
        return {}


def check_all_metrics(dictionary: dict, measured: dict[str, float] | None = None) -> dict:
    """全量准确性检查（兜底）-> 报告字典。

    对字典内全部指标逐项给出结论：
      - 有实测值：按 threshold 求值（达标 / 不达标）；
      - 无实测值：走兜底结构校验（字段齐全 / 阈值可解析 / severity 合法），
        标记 fallback=True（不静默跳过任何指标）。
    返回 {metrics: [...], fallback_count, failures, issues}。
    """
    measured = measured or {}
    out: list[dict] = []
    failures: list[str] = []
    issues: list[str] = list(dictionary_conflicts(dictionary))
    for m in dictionary.get("metrics", []):
        mid = str(m.get("metric_id", "?"))
        rec = {"metric_id": mid, "name": m.get("name"), "severity": m.get("severity"),
               "fallback": False, "status": "ok", "detail": ""}
        if mid in measured:
            try:
                ok, detail = evaluate(str(m.get("threshold", "")), measured[mid])
                rec["status"] = "ok" if ok else "fail"
                rec["detail"] = detail
                if not ok:
                    failures.append(mid)
            except ValueError as e:
                rec["status"] = "invalid"
                rec["detail"] = str(e)
                issues.append(f"{mid} 阈值不可解析：{e}")
        else:
            rec["fallback"] = True
            try:
                parse_threshold(str(m.get("threshold", "")))
                rec["detail"] = "无实测值，兜底结构校验通过（阈值可解析）"
            except ValueError as e:
                rec["status"] = "invalid"
                rec["detail"] = str(e)
                issues.append(f"{mid} 兜底校验失败：{e}")
        out.append(rec)
    return {"metrics": out, "fallback_count": sum(1 for r in out if r["fallback"]),
            "failures": failures, "issues": issues}


def store_path(business_rel: str, base: Path = ROOT) -> Path:
    return processed_data_dir(business_rel) / "metrics" / "metrics.csv"


def write_store(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(REQUIRED_FIELDS))
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_store(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- 适配器

def read_xlsx(path: Path) -> list[dict]:
    """读取 xlsx 首个工作表为 dict 行（表头即字段名）。"""
    try:
        from openpyxl import load_workbook
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("缺少 openpyxl，无法读取 xlsx") from e
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        ws = wb.worksheets[0]
        rows = list(ws.iter_rows(values_only=True))
    finally:
        wb.close()
    if not rows:
        return []
    header = [str(c).strip() if c is not None else "" for c in rows[0]]
    out = []
    for r in rows[1:]:
        if all(c is None for c in r):
            continue
        out.append({header[i]: r[i] for i in range(min(len(header), len(r)))})
    return out


def read_md_table(path: Path) -> list[dict]:
    """解析 Markdown 表格（首个表格）为 dict 行。"""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    table: list[list[str]] = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
                continue
            table.append(cells)
        elif table:
            break
    if not table:
        return []
    header = table[0]
    return [{header[i]: row[i] for i in range(min(len(header), len(row)))} for row in table[1:]]


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="指标注册与单一事实源服务")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("get"); p.add_argument("metric_id")
    p = sub.add_parser("eval"); p.add_argument("metric_id"); p.add_argument("value")
    p = sub.add_parser("export")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--xlsx"); src.add_argument("--md")
    p.add_argument("--out", required=True)
    p.add_argument("--status", default=None, help="统一填充 status（如 已核验）")
    p.add_argument("--dedupe", action="store_true", help="按 (date, indicator_id, caliber) 去重")
    p.add_argument("--case-insensitive", action="store_true", help="去重时 indicator_id/caliber 忽略大小写")
    p.add_argument("--lineage", help="输出去重血缘与冲突明细 JSON（与 --dedupe 同用）")
    sub.add_parser("check")
    sub.add_parser("audit").add_argument("--coverage", action="store_true",
                                          help="叠加指标实测覆盖报告（metric_coverage）")
    args = ap.parse_args()

    d = load_dictionary()
    if args.cmd == "list":
        for m in d["metrics"]:
            print(f"{m['metric_id']:<6} {m['severity']:<3} {m['threshold']:<8} {m['name']}")
        return 0
    if args.cmd == "check":
        issues = check_dictionary(d)
        for i in issues:
            print(f"[E] {i}")
        if issues:
            print(f"字典体检失败：{len(issues)} 项问题（别名 / 字段 / 阈值 / 级别）")
            return 1
        print(f"字典体检通过：{len(d['metrics'])} 项指标，别名唯一、字段齐全、阈值可解析")
        return 0
    if args.cmd == "audit":
        measured = measured_from_info_gap()
        coverage_rep = None
        if getattr(args, "coverage", False):
            from metric_coverage import coverage_report, measure
            cov = measure()
            measured = {mid: rec["value"] for mid, rec in cov.items()
                       if rec["value"] is not None}
            coverage_rep = coverage_report(cov)
        rep = check_all_metrics(d, measured)
        for r in rep["metrics"]:
            flag = "FALLBACK" if r["fallback"] else r["status"].upper()
            print(f"[{flag}] {r['metric_id']:<6} {r['severity']:<3} {r['name']}：{r['detail']}")
        print(f"\n[audit] {len(rep['metrics'])} 项全量检查；实测 {len(measured)} 项；"
              f"兜底 {rep['fallback_count']} 项；不达标 {len(rep['failures'])} 项；问题 {len(rep['issues'])} 项")
        if coverage_rep:
            print(f"[coverage] 覆盖 {coverage_rep['total']} 项；{coverage_rep['statuses']}")
            if coverage_rep["gaps"]:
                print(f"[gap] 未实测 {len(coverage_rep['gaps'])} 项："
                      f"{'、'.join(coverage_rep['gaps'])}")
        if rep["issues"]:
            return 1
        if rep["fallback_count"]:
            # 实测数据缺失不得静默放行：显式作为警告上报
            print(f"[W] {rep['fallback_count']} 项指标无实测值（实测数据缺失，仅结构兜底）")
            return 2
        return 2 if rep["failures"] else 0
    if args.cmd == "get":
        m = get_metric(d, args.metric_id) or by_alias(d, args.metric_id)
        if not m:
            print(f"[ERROR] 未找到指标：{args.metric_id}", file=sys.stderr)
            return 1
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "eval":
        m = get_metric(d, args.metric_id)
        if not m:
            print(f"[ERROR] 未找到指标：{args.metric_id}", file=sys.stderr)
            return 1
        ok, detail = evaluate(m["threshold"], args.value)
        print(f"[{'OK' if ok else 'NG'}] {m['metric_id']} {m['name']}：{detail}")
        return 0 if ok else 2
    if args.cmd == "export":
        src_path = Path(args.xlsx or args.md)
        rows = read_xlsx(src_path) if args.xlsx else read_md_table(src_path)
        if args.status:
            for r in rows:
                r.setdefault("status", args.status)
        ok_rows, errors = normalize_rows(rows)
        for e in errors:
            print(f"[W] {e}")
        if args.dedupe:
            kept, lineage, conflicts = dedupe_rows(ok_rows, case_sensitive=not args.case_insensitive)
            print(f"[dedupe] 去重前 {len(ok_rows)} 行 -> 保留 {len(kept)} 行；"
                  f"重复 {sum(len(item['dropped_rows']) for item in lineage)} 行；冲突 {len(conflicts)} 组"
                  f"（大小写{'不敏感' if args.case_insensitive else '敏感'}）")
            for c in conflicts:
                print(f"[CONFLICT] {c['key']} 字段 {c['fields']}：保留 {c['kept']} vs  incoming {c['incoming']}")
            ok_rows = kept
            if args.lineage:
                lp = Path(args.lineage)
                lp.parent.mkdir(parents=True, exist_ok=True)
                lp.write_text(json.dumps({"case_sensitive": not args.case_insensitive,
                                          "kept_rows": len(kept), "lineage": lineage,
                                          "conflicts": conflicts}, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
                print(f"[lineage] 血缘与冲突明细写入 {args.lineage}")
        write_store(ok_rows, Path(args.out))
        print(f"[export] {len(ok_rows)} 行写入 {args.out}（{len(errors)} 项警告）")
        return 0 if not errors else 2
    return 1


if __name__ == "__main__":
    sys.exit(main())
