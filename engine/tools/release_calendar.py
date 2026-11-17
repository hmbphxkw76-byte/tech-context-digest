#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""发布日历结构化采集（P1-2）。

把 `engine/report-audits/release-calendar.md` 的发布日历表采集为结构化 JSON，
并提供覆盖率 / 下次预期窗口的机器判定，供 update_planner 与人工复核消费。

用法：
    python engine/tools/release_calendar.py --emit engine/report-audits/release-calendar.json
    python engine/tools/release_calendar.py --check
    python engine/tools/release_calendar.py --list

退出码：0 通过；2 覆盖率不足 / 无可解析行；1 用法错误。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import AUDIT_DIR, ROOT  # noqa: E402

CALENDAR_MD = AUDIT_DIR / "release-calendar.md"
SCHEMA_VERSION = "1.0"

# data-acquisition-checklist 的 P0 维度 → 日历来源关键词（覆盖率分子判定）
P0_KEYWORDS = {
    "就业": ("LFS", "DDSE", "Digital Dubai", "劳工"),
    "收入": ("薪酬", "薪资", "QER", "收入"),
    "空置": ("空置", "ValuStrat", "REIDIN", "CBRE", "JLL", "存量"),
    "竣工": ("竣工", "Municipality", "C&W", "Cavendish", "交付"),
    "政策原文": ("u.ae", "centralbank", "dubailand", "RERA", "LTV", "黄金签证", "过户费", "托管", "租金"),
    "宏观高频": ("PMI", "EIA", "CBUAE", "Federal Reserve", "BIS", "宏观", "油价", "汇率"),
}

ISO_RE = re.compile(r"\d{4}-\d{2}(?:-\d{2})?")
YEAR_RE = re.compile(r"\d{4}")


def _split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_calendar(path: Path = CALENDAR_MD) -> list[dict]:
    """解析发布日历表 -> 结构化行（保序）。缺失 / 无表返回空列表。"""
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    header: list[str] = []
    rows: list[dict] = []
    for ln in lines:
        s = ln.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = _split_row(s)
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        if not header:
            header = cells
            continue
        if len(cells) < len(header):
            cells += [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, cells)))
    return rows


def classify_window(row: dict) -> dict:
    """下次预期窗口结构化：kind ∈ iso / year / relative / unknown。"""
    raw = str(row.get("下次预期窗口", "")).strip()
    if ISO_RE.fullmatch(raw):
        return {"raw": raw, "kind": "iso", "date": raw}
    if YEAR_RE.fullmatch(raw):
        return {"raw": raw, "kind": "year", "date": f"{raw}-01-01"}
    if raw:
        return {"raw": raw, "kind": "relative", "date": ""}
    return {"raw": "", "kind": "unknown", "date": ""}


def coverage(rows: list[dict]) -> dict:
    """覆盖率度量：字段完整率 + P0 维度覆盖。"""
    total = len(rows)
    complete = sum(1 for r in rows if str(r.get("下次预期窗口", "")).strip()
                   and str(r.get("入库期限", "")).strip())
    p0_hit = {k: False for k in P0_KEYWORDS}
    for r in rows:
        blob = " ".join(str(v) for v in r.values())
        for dim, kws in P0_KEYWORDS.items():
            if any(kw.lower() in blob.lower() for kw in kws):
                p0_hit[dim] = True
    covered = sum(1 for v in p0_hit.values() if v)
    return {
        "rows": total,
        "field_complete": complete,
        "field_complete_rate": (complete / total) if total else 1.0,
        "p0_dimensions": len(p0_hit),
        "p0_covered": covered,
        "p0_coverage": (covered / len(p0_hit)) if p0_hit else 1.0,
        "missing_p0": [k for k, v in p0_hit.items() if not v],
    }


def build_document(rows: list[dict]) -> dict:
    """构建确定性 JSON 文档（无时间戳）。"""
    out_rows = []
    for i, r in enumerate(rows, start=1):
        item = dict(r)
        item["row"] = i
        item["window"] = classify_window(r)
        out_rows.append(item)
    return {
        "schema_version": SCHEMA_VERSION,
        "source": "engine/report-audits/release-calendar.md",
        "comment": "发布日历结构化采集（单一事实源为 release-calendar.md；本文件为采集产物，确定性无时间戳）。",
        "rows": out_rows,
        "summary": coverage(rows),
    }


def emit(path: Path) -> dict:
    doc = build_document(parse_calendar())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return doc


def main() -> int:
    ap = argparse.ArgumentParser(description="发布日历结构化采集")
    ap.add_argument("--emit", help="输出结构化 JSON 路径（仓库相对或绝对）")
    ap.add_argument("--check", action="store_true", help="覆盖率检查")
    ap.add_argument("--list", action="store_true", help="列出结构化行")
    args = ap.parse_args()

    rows = parse_calendar()
    if not rows:
        print(f"[ERROR] 未解析到发布日历行：{CALENDAR_MD.relative_to(ROOT)}")
        return 2

    if args.emit:
        doc = emit(ROOT / args.emit if not Path(args.emit).is_absolute() else Path(args.emit))
        s = doc["summary"]
        print(f"[emit] {len(doc['rows'])} 行写入 {args.emit}；"
              f"字段完整率 {s['field_complete_rate']:.1%}；P0 覆盖 {s['p0_covered']}/{s['p0_dimensions']}")
        return 0

    if args.list:
        for r in rows:
            print(f"{r.get('来源', ''):<28} | {r.get('指标', ''):<24} | {r.get('频率', ''):<6} | "
                  f"{r.get('下次预期窗口', '')}")
        return 0

    if args.check:
        s = coverage(rows)
        print(f"[check] 行数 {s['rows']}；字段完整率 {s['field_complete_rate']:.1%}；"
              f"P0 覆盖 {s['p0_covered']}/{s['p0_dimensions']} = {s['p0_coverage']:.1%}")
        if s["missing_p0"]:
            print(f"[check] 未覆盖 P0 维度：{', '.join(s['missing_p0'])}")
        return 0 if s["p0_coverage"] >= 1.0 else 2

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
