#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""增量语义 diff（T4）：只对本期相对上期的新增 / 修改块执行语义复核。

依据 engine/report-audits/system-optimization-plan-2026-11-15.md 第 3.4 节。
块级 diff 采用 difflib.SequenceMatcher；变更块驱动 semantic_checks 插件，
结果可写审计记录目录供终审消费。

退出码：0 无 P0/P1；1 用法错误；2 存在 P0/P1 发现。

用法：
    python engine/tools/semantic_diff.py diff <上期文本> <本期文本> [--checks a,b] [--json]
    python engine/tools/semantic_diff.py checks                 # 列出插件
"""
from __future__ import annotations

import argparse
import difflib
import html as _html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_reports  # noqa: E402
from semantic_checks.base import Block, CheckContext  # noqa: E402
from semantic_checks.registry import load_checks, run_checks  # noqa: E402

SEMANTIC_DIR = ROOT / "engine" / "audit" / "records" / "semantic"


_TAG_RE = re.compile(r"<[^>]+>")


def _plain(raw: str) -> str:
    """去 HTML 标签并还原实体。

    报告为自包含 HTML，直接按行切块会把 <th style="width:6%"> 这类标签属性
    当成「带单位关键数字」、把 href 当成来源标注，产生大量假阳性。先在内容层
    归一化，再供分类与语义插件匹配（纯文本输入不受影响）。
    """
    return _html.unescape(_TAG_RE.sub("", raw)).strip()


def iter_blocks(text: str) -> list[Block]:
    """文本 -> 块序列（按非空行切分，识别标题 / 表格 / 列表 / 引用 / 代码）。"""
    blocks: list[Block] = []
    for raw in str(text).splitlines():
        s = _plain(raw)
        if not s:
            continue
        if s.startswith("#"):
            kind = "heading"
        elif s.startswith("|"):
            kind = "table"
        elif s.startswith(">"):
            kind = "quote"
        elif s.startswith("```"):
            kind = "code"
        elif re.match(r"^(?:[-*+]|\d+\.)\s+", s):
            kind = "list"
        else:
            kind = "paragraph"
        blocks.append(Block(kind, s))
    return blocks


def diff_blocks(previous: str, current: str) -> dict:
    """块级 diff -> {added, removed, modified, changed_indices, current_blocks, previous_blocks}。"""
    a = iter_blocks(previous)
    b = iter_blocks(current)
    sm = difflib.SequenceMatcher(a=[x.key for x in a], b=[x.key for x in b], autojunk=False)
    added: set[int] = set()
    removed: set[int] = set()
    modified: list[tuple[int, int]] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            added.update(range(j1, j2))
        elif tag == "delete":
            removed.update(range(i1, i2))
        elif tag == "replace":
            n = min(i2 - i1, j2 - j1)
            for k in range(n):
                modified.append((i1 + k, j1 + k))
            if (j2 - j1) > n:
                added.update(range(j1 + n, j2))
            if (i2 - i1) > n:
                removed.update(range(i1 + n, i2))
    changed = sorted(added | {j for _, j in modified})
    return {
        "added": sorted(added),
        "removed": sorted(removed),
        "modified": modified,
        "changed_indices": changed,
        "previous_blocks": a,
        "current_blocks": b,
    }


def analyze(previous: str, current: str, names: list[str] | None = None) -> dict:
    """执行增量语义分析 -> {diff 摘要, findings}。"""
    d = diff_blocks(previous, current)
    ctx = CheckContext(previous_text=previous, current_text=current,
                       changed_indices=d["changed_indices"])
    findings = run_checks(d["current_blocks"], ctx, names)
    return {
        "added": len(d["added"]),
        "removed": len(d["removed"]),
        "modified": len(d["modified"]),
        "changed_blocks": len(d["changed_indices"]),
        "total_blocks": len(d["current_blocks"]),
        "findings": [
            {"check": f.check, "severity": f.severity, "block_index": f.block_index,
             "message": f.message, "evidence": f.evidence}
            for f in findings
        ],
    }


def _previous_map() -> dict[str, list]:
    """按 (business_line, cycle) 分组并按时序排序 -> {当前 rel: 上期 rel}。"""
    groups: dict[tuple, list] = {}
    for ref in iter_reports():
        if ref.category != "report" or not ref.cycle:
            continue
        groups.setdefault((ref.business_line, ref.cycle), []).append(ref)
    out: dict[str, str] = {}
    for refs in groups.values():
        refs.sort(key=lambda r: (r.period, r.rel))
        for prev, cur in zip(refs, refs[1:]):
            out[cur.rel] = prev.rel
    return out


def scan(out_dir: Path = SEMANTIC_DIR, names: list[str] | None = None) -> dict:
    """对全部正式报告与上期做增量语义分析，结果写入记录目录 -> 汇总字典。

    只对存在上期的报告执行（首期无对比基准，跳过并计数）。
    """
    prev_map = _previous_map()
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for ref in iter_reports():
        if ref.category != "report":
            continue
        prev_rel = prev_map.get(ref.rel)
        rec = {"report": ref.rel, "business_line": ref.business_line, "cycle": ref.cycle,
               "period": ref.period, "previous": prev_rel, "findings": []}
        if prev_rel:
            prev_text = (ROOT / prev_rel).read_text(encoding="utf-8", errors="replace")
            cur_text = (ROOT / ref.rel).read_text(encoding="utf-8", errors="replace")
            ana = analyze(prev_text, cur_text, names)
            rec.update({k: ana[k] for k in ("added", "removed", "modified",
                                            "changed_blocks", "total_blocks")})
            rec["findings"] = ana["findings"]
        results.append(rec)
        slug = re.sub(r"[^A-Za-z0-9]+", "-", ref.rel).strip("-") + ".json"
        (out_dir / slug).write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8")
    findings = sum(len(r["findings"]) for r in results)
    p01 = sum(1 for r in results for f in r["findings"] if f["severity"] in ("P0", "P1"))
    return {"reports": len(results), "compared": sum(1 for r in results if r["previous"]),
            "findings": findings, "p01": p01, "results": results}


def main() -> int:
    ap = argparse.ArgumentParser(description="增量语义 diff（T4）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("diff")
    p.add_argument("previous"); p.add_argument("current")
    p.add_argument("--checks", help="逗号分隔的插件名，缺省全部")
    p.add_argument("--json", action="store_true", dest="as_json")
    p.add_argument("--out", help="将分析结果 JSON 写入指定路径（如审计记录目录）")
    sub.add_parser("checks")
    p = sub.add_parser("scan")
    p.add_argument("--out-dir", default=str(SEMANTIC_DIR))
    p.add_argument("--checks", help="逗号分隔的插件名，缺省全部")
    args = ap.parse_args()

    if args.cmd == "scan":
        names = [s.strip() for s in args.checks.split(",")] if args.checks else None
        rep = scan(Path(args.out_dir), names)
        print(f"[scan] 报告 {rep['reports']} 份；有上期可比 {rep['compared']}；"
              f"发现 {rep['findings']} 项（P0/P1 {rep['p01']}）→ {args.out_dir}")
        return 2 if rep["p01"] else 0

    if args.cmd == "checks":
        for name, _fn in load_checks():
            print(name)
        return 0

    prev = Path(args.previous).read_text(encoding="utf-8", errors="replace")
    cur = Path(args.current).read_text(encoding="utf-8", errors="replace")
    names = [s.strip() for s in args.checks.split(",")] if args.checks else None
    result = analyze(prev, cur, names)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"变更块 {result['changed_blocks']}/{result['total_blocks']}"
              f"（新增 {result['added']} / 修改 {result['modified']} / 删除 {result['removed']}）")
        for f in result["findings"]:
            print(f"[{f['severity']}] {f['check']} block={f['block_index']}: {f['message']}")
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[out] 分析结果已写入 {out}")
    has_issue = any(f["severity"] in ("P0", "P1") for f in result["findings"])
    return 2 if has_issue else 0


if __name__ == "__main__":
    sys.exit(main())
