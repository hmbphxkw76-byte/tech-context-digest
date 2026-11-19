#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""finding→规则回写台账（FINDING-RULE-LEDGER v1.0）。

把「纠错闭环」升级为「学习闭环」：每个 L3 / 质量 finding 必须映射到预防规则
（新增校验项 / 提示词条款 / 模板修订 / 规范条款），并跟踪规则命中，防止同类错误复发。

单一事实源：`engine/audit/records/finding-rules.json`。本工具只读写该文件，不新增
第二套台账；与 `engine/quality/repair-sop.md` 的关系为**指针**（不复制 SOP 正文）。

确定性：无时间戳 / 无随机数；写盘按 `finding_id` 排序，`sort_keys=True`、`indent=2`，
同输入重放字节一致（`check` 校验）。

用法：
    python engine/tools/finding_rule.py register --finding-id F5-1 --source <rel> \
        --root-cause <text> --rule <text> --rule-type 校验项 --rule-location <rel> \
        [--report <rel>] [--location <text>] [--keywords k1,k2] \
        [--status 新建] [--fix-status 已修复] [--hit-count 0]
    python engine/tools/finding_rule.py match --text "..." [--threshold 1] [--json]
    python engine/tools/finding_rule.py stats [--json]
    python engine/tools/finding_rule.py check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "engine" / "audit" / "records" / "finding-rules.json"
SPEC_ID = "FINDING-RULE-LEDGER v1.0"
SCHEMA_VERSION = "1.0"

# 预防规则类型：新增校验项 / 提示词条款 / 模板修订 / 规范条款。
RULE_TYPES = ("校验项", "提示词条款", "模板修订", "规范条款")
# 状态：已映射（既有规则）/ 新建（本台账新登记）/ 待补规则（尚无规则）。
STATUSES = ("已映射", "新建", "待补规则")
DEFAULT_STATUS = "新建"
TIMESTAMP_KEYS = ("timestamp", "generated_at", "updated_at", "created_at")

REQUIRED_FIELDS = ("finding_id", "source", "root_cause", "prevention_rule",
                   "rule_type", "rule_location")

_ASCII_TOKEN_RE = re.compile(r"[a-z0-9]+")
_CJK_RUN_RE = re.compile(r"[\u4e00-\u9fff]+")


# ---------------------------------------------------------------- 纯逻辑

def new_ledger() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "spec": SPEC_ID,
        "ledger": "finding-rules",
        "description": "finding→预防规则回写台账：每个 L3 / 质量 finding 映射到预防规则并跟踪命中。",
        "rule_types": list(RULE_TYPES),
        "statuses": list(STATUSES),
        "records": [],
    }


def _terms(text: str) -> set[str]:
    """确定性词条集合：ASCII 词（小写，len≥2）+ 中文二元组。"""
    out: set[str] = set()
    for tok in _ASCII_TOKEN_RE.findall((text or "").lower()):
        if len(tok) >= 2:
            out.add(tok)
    for run in _CJK_RUN_RE.findall(text or ""):
        for i in range(len(run) - 1):
            out.add(run[i:i + 2])
    return out


def score_record(text: str, rec: dict) -> tuple[int, list[str]]:
    """命中打分：关键词命中为主（每词 2 分），无关键词时退回词条重叠。"""
    t = (text or "").lower()
    kw_hits = sorted({kw for kw in rec.get("keywords", [])
                      if isinstance(kw, str) and kw and kw.lower() in t})
    if kw_hits:
        return len(kw_hits) * 2, kw_hits
    t_terms = _terms(text)
    r_terms = _terms(" ".join([str(rec.get("root_cause", "")),
                               str(rec.get("prevention_rule", ""))]))
    overlap = sorted(t_terms & r_terms)
    return len(overlap), overlap[:8]


def validate_record(rec: dict) -> list[str]:
    problems: list[str] = []
    if not isinstance(rec, dict):
        return ["record 非对象"]
    for f in REQUIRED_FIELDS:
        if not str(rec.get(f, "")).strip():
            problems.append(f"缺必填字段 {f}")
    if rec.get("rule_type") and rec.get("rule_type") not in RULE_TYPES:
        problems.append(f"rule_type 非法：{rec.get('rule_type')!r}")
    if rec.get("status") and rec.get("status") not in STATUSES:
        problems.append(f"status 非法：{rec.get('status')!r}")
    hc = rec.get("hit_count", 0)
    if not isinstance(hc, int) or isinstance(hc, bool) or hc < 0:
        problems.append(f"hit_count 须为非负整数：{hc!r}")
    kws = rec.get("keywords", [])
    if not isinstance(kws, list) or any(
            (not isinstance(k, str)) or not k.strip() for k in kws):
        problems.append("keywords 须为非空字符串列表")
    return problems


def validate_ledger(data: dict) -> list[str]:
    problems: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version 须为 {SCHEMA_VERSION}")
    recs = data.get("records")
    if not isinstance(recs, list):
        return problems + ["records 须为列表"]
    ids: list = []
    for r in recs:
        fid = r.get("finding_id") if isinstance(r, dict) else "?"
        problems += [f"{fid}: {p}" for p in validate_record(r)]
        ids.append(fid)
    if len(ids) != len(set(ids)):
        problems.append("finding_id 重复")
    return problems


def _normalized(data: dict) -> dict:
    out = dict(data)
    out["records"] = sorted(out.get("records", []),
                            key=lambda r: str(r.get("finding_id", "")))
    return out


def render(data: dict) -> str:
    return json.dumps(_normalized(data), ensure_ascii=False,
                      indent=2, sort_keys=True) + "\n"


# ---------------------------------------------------------------- 读写

def load(path: Path | None = None) -> dict:
    p = Path(path) if path else DEFAULT_PATH
    if not p.exists():
        return new_ledger()
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"台账根须为对象：{p}")
    data.setdefault("records", [])
    return data


def save(data: dict, path: Path | None = None) -> Path:
    p = Path(path) if path else DEFAULT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(data), encoding="utf-8")
    return p


def build_record(finding_id: str, source: str, root_cause: str,
                 prevention_rule: str, rule_type: str, rule_location: str,
                 report: str = "", location: str = "",
                 keywords: list[str] | None = None,
                 hit_count: int | None = None, status: str = DEFAULT_STATUS,
                 fix_status: str = "") -> dict:
    return {
        "finding_id": finding_id,
        "source": source,
        "report": report,
        "location": location,
        "root_cause": root_cause,
        "prevention_rule": prevention_rule,
        "rule_type": rule_type,
        "rule_location": rule_location,
        "keywords": [k for k in (keywords or []) if k and k.strip()],
        "hit_count": 0 if hit_count is None else int(hit_count),
        "status": status,
        "fix_status": fix_status,
    }


def register(record: dict, path: Path | None = None) -> dict:
    """登记 / 更新一条 finding→规则记录（同 finding_id 覆盖式更新）。"""
    problems = validate_record(record)
    if problems:
        raise ValueError("; ".join(problems))
    data = load(path)
    recs = data.get("records", [])
    idx = next((i for i, r in enumerate(recs)
                if r.get("finding_id") == record.get("finding_id")), None)
    if idx is None:
        recs.append(record)
    else:
        merged = dict(recs[idx])
        merged.update(record)
        # 未显式给 hit_count 时保留既有计数（避免重登清零）。
        if record.get("hit_count") is None:
            merged["hit_count"] = int(recs[idx].get("hit_count", 0))
        recs[idx] = merged
    data["records"] = recs
    save(data, path)
    return record


def match(text: str, path: Path | None = None, threshold: int = 1) -> list[dict]:
    """新 finding 与已有规则相似即提示（确定性打分，按分数降序）。"""
    data = load(path)
    out: list[dict] = []
    for rec in data.get("records", []):
        score, hits = score_record(text, rec)
        if score >= threshold:
            out.append({
                "finding_id": rec.get("finding_id"),
                "score": score,
                "matched": hits,
                "rule_type": rec.get("rule_type"),
                "rule_location": rec.get("rule_location"),
                "prevention_rule": rec.get("prevention_rule"),
                "status": rec.get("status"),
                "hit_count": rec.get("hit_count", 0),
            })
    out.sort(key=lambda x: (-x["score"], str(x["finding_id"])))
    return out


def stats(path: Path | None = None) -> dict:
    data = load(path)
    recs = data.get("records", [])
    by_status = {s: 0 for s in STATUSES}
    by_type = {t: 0 for t in RULE_TYPES}
    for r in recs:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
        by_type[r.get("rule_type", "?")] = by_type.get(r.get("rule_type", "?"), 0) + 1
    mapped = sum(1 for r in recs if r.get("status") in ("已映射", "新建"))
    top = sorted(recs, key=lambda r: (-int(r.get("hit_count", 0)),
                                      str(r.get("finding_id"))))[:5]
    return {
        "total": len(recs),
        "mapping_rate": (mapped / len(recs)) if recs else 1.0,
        "mapped": mapped,
        "pending": by_status.get("待补规则", 0),
        "by_status": by_status,
        "by_rule_type": by_type,
        "total_hits": sum(int(r.get("hit_count", 0)) for r in recs),
        "top_hit": [{"finding_id": r.get("finding_id"),
                     "hit_count": r.get("hit_count", 0)} for r in top],
    }


def check(path: Path | None = None) -> list[str]:
    """schema / 字段完整 / 无时间戳 / 可重放 自检。"""
    p = Path(path) if path else DEFAULT_PATH
    if not p.exists():
        return [f"台账不存在：{p}"]
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON 解析失败：{e}"]
    problems = validate_ledger(data)
    blob = json.dumps(data, ensure_ascii=False)
    for k in TIMESTAMP_KEYS:
        if f'"{k}"' in blob:
            problems.append(f"含时间戳字段 {k}（确定性要求无时间戳）")
    if p.read_text(encoding="utf-8") != render(data):
        problems.append("磁盘内容与确定性渲染不一致（非可重放）")
    return problems


# ---------------------------------------------------------------- CLI

def _split_keywords(raw: str) -> list[str]:
    return [k.strip() for k in (raw or "").split(",") if k.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="finding→规则回写台账")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("register", help="登记 / 更新一条 finding→规则记录")
    p.add_argument("--finding-id", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--root-cause", required=True)
    p.add_argument("--rule", required=True)
    p.add_argument("--rule-type", required=True, choices=RULE_TYPES)
    p.add_argument("--rule-location", required=True)
    p.add_argument("--report", default="")
    p.add_argument("--location", default="")
    p.add_argument("--keywords", default="")
    p.add_argument("--hit-count", type=int, default=None)
    p.add_argument("--status", default=DEFAULT_STATUS, choices=STATUSES)
    p.add_argument("--fix-status", default="")
    p.add_argument("--path", default=None, help="覆盖默认台账路径（测试用）")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("match", help="新 finding 与已有规则相似即提示")
    p.add_argument("--text", required=True)
    p.add_argument("--threshold", type=int, default=1)
    p.add_argument("--path", default=None)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("stats", help="台账统计")
    p.add_argument("--path", default=None)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("check", help="schema / 字段 / 无时间戳 / 可重放自检")
    p.add_argument("--path", default=None)

    args = ap.parse_args()
    path = Path(args.path) if getattr(args, "path", None) else None

    if args.cmd == "register":
        rec = build_record(
            finding_id=args.finding_id, source=args.source,
            root_cause=args.root_cause, prevention_rule=args.rule,
            rule_type=args.rule_type, rule_location=args.rule_location,
            report=args.report, location=args.location,
            keywords=_split_keywords(args.keywords),
            hit_count=args.hit_count, status=args.status,
            fix_status=args.fix_status)
        try:
            register(rec, path)
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(rec, ensure_ascii=False, sort_keys=True))
        else:
            print(f"[register] {rec['finding_id']} → {rec['rule_location']} "
                  f"（{rec['rule_type']} / {rec['status']}）")
        return 0

    if args.cmd == "match":
        hits = match(args.text, path, args.threshold)
        if args.json:
            print(json.dumps(hits, ensure_ascii=False, indent=2, sort_keys=True))
        elif hits:
            print(f"[match] 命中 {len(hits)} 条规则：")
            for h in hits:
                print(f"  {h['finding_id']}（score={h['score']}）"
                      f" {h['rule_location']}｜{h['prevention_rule']}")
        else:
            print("[match] 无命中")
        return 0 if hits else 2

    if args.cmd == "stats":
        s = stats(path)
        if args.json:
            print(json.dumps(s, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            print(f"[stats] 记录 {s['total']} 条；映射率 {s['mapping_rate']:.1%}"
                  f"（已映射+新建 {s['mapped']} / 待补规则 {s['pending']}）")
            print(f"        状态分布：{s['by_status']}")
            print(f"        规则类型：{s['by_rule_type']}")
            print(f"        累计命中：{s['total_hits']}；Top：{s['top_hit']}")
        return 0

    if args.cmd == "check":
        problems = check(path)
        if problems:
            for prob in problems:
                print(f"[E] {prob}")
            return 1
        print(f"[OK] schema / 字段 / 无时间戳 / 可重放校验通过："
              f"{ (path or DEFAULT_PATH).relative_to(ROOT) }")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
