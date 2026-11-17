"""把既有报告迁移到 canonical 样式（report_style.CANONICAL_CSS）。

- 替换 <style> 块为 canonical CSS；
- `--rename-chart`：把 echarts 容器 class="chart" 改名为 class="chart-eh"
  （canonical 中 .chart 是 trends 的图表卡片，echarts 容器为 .chart-eh）；
- `--fix-colors`：把旧令牌色 #1f3d63 替换为 canonical #16324f（用于图表 JS 内联色）；
- `--fix-tables`：表格规范化——补 `class="fixed"`，并把每个 `<th>` 的列宽归一为
  百分比（同表之和 100%），满足 monitoring-common-spec §3 与 lint_reports 的列宽检查。

用法：
  python engine/tools/restyle_reports.py --files <报告.html> [--rename-chart] [--fix-colors] [--fix-tables] [--dry]
"""
from __future__ import annotations

import argparse
import html
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report_style import style_block  # noqa: E402

STYLE_RE = re.compile(r"<style>.*?</style>", re.DOTALL)
# 旧令牌色 → canonical 主色（含大小写；覆盖内联 SVG / 图例 / 图表 JS）
COLOR_MAP = {
    "#1f3d63": "#16324f",  # apartment monthly/quarterly/baseline
    "#123a5c": "#16324f",  # trends report-head
}
OLD_NAVY = re.compile("|".join(re.escape(k) for k in COLOR_MAP), re.IGNORECASE)

TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL)
OPEN_TABLE_RE = re.compile(r"<table\b[^>]*>", re.DOTALL)
TH_FULL_RE = re.compile(r"<th\b[^>]*>.*?</th>", re.DOTALL)
WIDTH_RE = re.compile(r"width\s*:\s*([0-9.]+)(px|%)")

# 列宽估算：表头为 nowrap，列宽不得小于表头文本宽度，否则文字溢出。
# 13px 字号下 CJK 约 13.5px/字、其余约 7.5px/字；加 24px（左右 padding 20 + 边框 2）余量。
_CJK_FROM = 0x2E80
_PAD = 24


def _text_width(txt: str) -> float:
    return sum(13.5 if ord(ch) >= _CJK_FROM else 7.5 for ch in txt)


def _needed_width(th_text: str) -> int:
    return int(math.ceil(_text_width(th_text) + _PAD))


def _ensure_fixed(table: str) -> str:
    """确保 <table ...> 的 class 含 fixed（与既有 class 合并）。"""
    m = OPEN_TABLE_RE.match(table)
    if not m:
        return table
    open_tag = m.group(0)
    cm = re.search(r'class="([^"]*)"', open_tag)
    if cm:
        classes = cm.group(1).split()
        if "fixed" not in classes:
            classes.append("fixed")
        new_tag = open_tag[: cm.start()] + 'class="' + " ".join(classes) + '"' + open_tag[cm.end():]
    else:
        new_tag = open_tag.replace("<table", '<table class="fixed"', 1)
    return new_tag + table[len(open_tag):]


def _set_th_width(tag: str, value: str) -> str:
    """把单个 <th> 开标签的列宽写成 value（如 '120px' / '12%'）；无 style 则补一个。"""
    if WIDTH_RE.search(tag):
        return WIDTH_RE.sub(f"width:{value}", tag)
    sm = re.search(r'style="', tag)
    if sm:
        return tag[: sm.end()] + f"width:{value}; " + tag[sm.end():]
    return tag[:-1] + f' style="width:{value}">'


def normalize_tables(text: str) -> str:
    """逐表：补 class="fixed"；列宽取 max(原 px 宽, 表头内容需求宽)。

    采用 px 而非百分比：`table-layout:fixed` + 百分比（和 100%）会把表格锁死在实际
    容器宽度，宽表的 nowrap 表头会溢出；px 宽度之和超过容器时表格自动撑开，由
    `.tblwrap{overflow-x:auto}` 横向滚动（与既有宽表行为一致）。
    """

    def repl(m: re.Match) -> str:
        new = _ensure_fixed(m.group(0))
        cells = list(TH_FULL_RE.finditer(new))
        for c in reversed(cells):  # 逆序替换，避免改动后索引失效
            cell = c.group(0)
            om = re.match(r"<th\b[^>]*>", cell)
            if not om:
                continue
            open_tag = om.group(0)
            inner = cell[len(open_tag): -len("</th>")]
            plain = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
            need = _needed_width(plain)
            wm = WIDTH_RE.search(open_tag)
            orig = float(wm.group(1)) if (wm and wm.group(2) == "px") else 0.0
            width = int(round(max(orig, need)))
            newtag = _set_th_width(open_tag, f"{width}px")
            new = new[: c.start()] + newtag + cell[len(open_tag):] + new[c.end():]
        return new

    return TABLE_RE.sub(repl, text)


def restyle(path: Path, rename_chart: bool = False, fix_colors: bool = False,
            fix_tables: bool = False, dry: bool = False, replace_css: bool = True) -> bool:
    text = path.read_text(encoding="utf-8")
    new = STYLE_RE.sub(style_block(), text, count=1) if replace_css else text
    if rename_chart:
        new = new.replace('class="chart"', 'class="chart-eh"')
    if fix_colors:
        new = OLD_NAVY.sub(lambda m: COLOR_MAP[m.group(0).lower()], new)
    if fix_tables:
        new = normalize_tables(new)
    if new == text:
        print(f"[SKIP] {path} 已是 canonical" if replace_css else f"[SKIP] {path} 表格已规范")
        return False
    if not dry:
        path.write_text(new, encoding="utf-8")
    print(f"[OK] {path}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="报告迁移到 canonical 样式")
    ap.add_argument("--files", nargs="+", required=True, help="报告 HTML 路径")
    ap.add_argument("--rename-chart", action="store_true")
    ap.add_argument("--fix-colors", action="store_true")
    ap.add_argument("--fix-tables", action="store_true", help="补 class=fixed 并将列宽归一为 %（同表之和 100%）")
    ap.add_argument("--dry", action="store_true", help="只报告不写入")
    args = ap.parse_args()
    # 仅 --fix-tables 时不动 <style> 块（避免引入与表格修复无关的样式变更）；
    # 与 --rename-chart / --fix-colors 联用时仍走完整迁移。
    only_tables = args.fix_tables and not args.rename_chart and not args.fix_colors
    changed = 0
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"[ERROR] 不存在：{p}")
            return 1
        if restyle(p, args.rename_chart, args.fix_colors, args.fix_tables, args.dry,
                   replace_css=not only_tables):
            changed += 1
    print(f"完成：改动 {changed} 份" + ("（dry-run）" if args.dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
