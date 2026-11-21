"""把既有报告迁移到 canonical 样式（report_style.CANONICAL_CSS）。

- 替换 <style> 块为 canonical CSS；
- `--rename-chart`：把 echarts 容器 class="chart" 改名为 class="chart-eh"
  （canonical 中 .chart 是 trends 的图表卡片，echarts 容器为 .chart-eh）；
- `--fix-colors`：把旧令牌色 #1f3d63 替换为 canonical #16324f（用于图表 JS 内联色）；
- `--fix-tables`：表格规范化——补 `class="fixed"`，并把每个 `<th>` 的列宽归一为
  px（取原 px 宽与表头内容需求宽的较大者），满足 monitoring-common-spec §3 与
  lint_reports 的列宽检查。
- `--add-footer`：在 `</main>` 之后补 canonical 报告页脚（``.report-foot``，含
  「反馈 / 纠错」入口，监控通用规范 §5）；幂等，已含则跳过。

用法：
  python engine/tools/restyle_reports.py --files <报告.html> [--rename-chart] [--fix-colors] [--fix-tables] [--add-footer] [--dry]
"""
from __future__ import annotations

import argparse
import html
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report_style import report_foot, style_block  # noqa: E402

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

# 报告题头统一：旧 audit-mark 顶条 + 各类 header 内文 → jp-life-work 风格
# （navy 标题带 + 浅色 meta 面板 + 绿色审计徽章）。
AUDIT_MARK_RE = re.compile(r'<div class="audit-mark"[^>]*>.*?</div>\s*', re.DOTALL)
HEADER_RE = re.compile(r'<header class="(?:report-head|hero)">.*?</header>', re.DOTALL)
H1_RE = re.compile(r"<h1\b[^>]*>.*?</h1>", re.DOTALL)
TAG_RE = re.compile(r'<span class="tag">.*?</span>', re.DOTALL)
EYEBROW_PATTERNS = (
    re.compile(r'<p class="kicker">.*?</p>', re.DOTALL),
    re.compile(r'<p class="eyebrow">.*?</p>', re.DOTALL),
    re.compile(r'<div class="eyebrow">.*?</div>', re.DOTALL),
    re.compile(r'<div class="hero-kicker">.*?</div>', re.DOTALL),
)
DIV_TAG_RE = re.compile(r"</?div\b[^>]*>")

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


def _plain_text(fragment: str) -> str:
    """去标签并解码实体，用于审计 meta / 标签文本。"""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def _period_from_stem(stem: str) -> str:
    """从文件名前缀取周期（2026-11 / 2026-Q3 / 2026-11-27 / 2026）。"""
    return stem.split("_", 1)[0]


def _type_from_eyebrow(eyebrow: str) -> str:
    text = _plain_text(eyebrow)
    parts = [p.strip() for p in text.split("·") if p.strip()]
    return parts[0] if parts else "报告"


def _extract_eyebrow(inner: str) -> str:
    for pattern in EYEBROW_PATTERNS:
        m = pattern.search(inner)
        if m:
            return m.group(0)
    return ""


def _audit_badge_from_mark(text: str) -> str:
    """把顶部 audit-mark 顶条转为 hero-panel 内的绿色审计徽章。"""
    m = AUDIT_MARK_RE.search(text)
    if not m:
        return (
            '<div class="audit-badge" role="status" aria-label="已审计报告">'
            '<span class="audit-seal">✓ 已审计</span>'
            '<span class="audit-meta">终审通过</span></div>'
        )
    block = m.group(0)
    meta_m = re.search(r'<span class="audit-meta">(.*?)</span>', block, re.DOTALL)
    meta = html.escape(_plain_text(meta_m.group(1))) if meta_m else "终审通过"
    return (
        '<div class="audit-badge" role="status" aria-label="已审计报告">'
        '<span class="audit-seal">✓ 已审计</span>'
        f'<span class="audit-meta">{meta}</span></div>'
    )


def _build_hero(header: str, path: Path, audit_badge: str) -> str:
    """把单份报告 header 重构为 jp-life-work 风格 hero。

    已迁移的 header（含 .hero-band/.hero-panel）原样返回，保证幂等。
    """
    if "hero-band" in header and "hero-panel" in header:
        return header

    m = re.search(r"<header\b[^>]*>(.*)</header>", header, re.DOTALL)
    inner = m.group(1) if m else header

    h1_m = H1_RE.search(inner)
    h1 = h1_m.group(0) if h1_m else ""
    inner = inner[: h1_m.start()] + inner[h1_m.end():] if h1_m else inner

    eyebrow = _extract_eyebrow(inner)
    if eyebrow:
        inner = inner.replace(eyebrow, "", 1)

    tags = TAG_RE.findall(inner)
    inner = TAG_RE.sub("", inner)

    # 展平 hero-inner / hero-line / hero-abstract / wrap 等包装 div，
    # 保留其中的 meta 文本、段落、定义列表与结论摘要。
    meta = DIV_TAG_RE.sub("", inner)
    meta = "\n".join(line.strip() for line in meta.splitlines() if line.strip())

    period = html.escape(_period_from_stem(path.stem))
    period_tag = f'<span class="tag">{period}</span>'
    if tags:
        tags_html = period_tag + "".join(tags)
    else:
        type_label = html.escape(_type_from_eyebrow(eyebrow))
        tags_html = period_tag + f'<span class="tag">{type_label}</span>'

    eyebrow_html = f"        {eyebrow}\n" if eyebrow else ""
    return (
        '<header class="hero">\n'
        '  <div class="hero-band">\n'
        '    <div class="wrap">\n'
        '      <div class="hero-top">\n'
        f"{eyebrow_html}"
        f'        <div class="tags">{tags_html}</div>\n'
        "      </div>\n"
        f"      {h1}\n"
        "    </div>\n"
        "  </div>\n"
        '  <div class="wrap">\n'
        '    <div class="hero-panel">\n'
        f'      <div class="meta-grid">{meta}</div>\n'
        f"      {audit_badge}\n"
        "    </div>\n"
        "  </div>\n"
        "</header>"
    )


def _unify_hero(text: str, path: Path) -> str:
    """移除顶部 audit-mark，并把报告 header 统一为 jp-life-work 风格 hero。"""
    audit_badge = _audit_badge_from_mark(text)
    text = AUDIT_MARK_RE.sub("", text, count=1)
    return HEADER_RE.sub(
        lambda m: _build_hero(m.group(0), path, audit_badge), text, count=1
    )


def ensure_footer(text: str) -> str:
    """在 ``</main>`` 之后插入 canonical 报告页脚（监控通用规范 §5）。

    已含 ``report-foot`` 则原样返回（幂等）；无 ``</main>`` 时回退到 ``</body>`` 之前。
    """
    if "report-foot" in text:
        return text
    foot = report_foot()
    idx = text.rfind("</main>")
    if idx != -1:
        end = idx + len("</main>")
        return text[:end] + "\n" + foot + text[end:]
    idx = text.rfind("</body>")
    if idx != -1:
        return text[:idx] + foot + "\n" + text[idx:]
    return text + "\n" + foot


def restyle(path: Path, rename_chart: bool = False, fix_colors: bool = False,
            fix_tables: bool = False, dry: bool = False, replace_css: bool = True,
            add_footer: bool = False, unify_hero: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    new = STYLE_RE.sub(style_block(), text, count=1) if replace_css else text
    if rename_chart:
        new = new.replace('class="chart"', 'class="chart-eh"')
    if fix_colors:
        new = OLD_NAVY.sub(lambda m: COLOR_MAP[m.group(0).lower()], new)
    if fix_tables:
        new = normalize_tables(new)
    if add_footer:
        new = ensure_footer(new)
    if unify_hero:
        new = _unify_hero(new, path)
    if new == text:
        print(f"[SKIP] {path} 已是 canonical" if replace_css else f"[SKIP] {path} 无需改动")
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
    ap.add_argument("--fix-tables", action="store_true", help="补 class=fixed 并将列宽归一为 px（原 px 宽与表头需求宽取较大者）")
    ap.add_argument("--add-footer", action="store_true",
                    help="在 </main> 之后补 canonical 报告页脚（含反馈 / 纠错入口）")
    ap.add_argument("--unify-hero", action="store_true",
                    help="移除顶部 audit-mark，统一为 jp-life-work 风格 hero 题头")
    ap.add_argument("--dry", action="store_true", help="只报告不写入")
    args = ap.parse_args()
    # 仅 --fix-tables / --add-footer 时不动 <style> 块（避免引入与该修复无关的样式变更）；
    # 与 --rename-chart / --fix-colors / --unify-hero 联用时仍走完整迁移。
    only_tables = args.fix_tables and not args.rename_chart and not args.fix_colors
    skip_css = only_tables or args.add_footer
    changed = 0
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"[ERROR] 不存在：{p}")
            return 1
        if restyle(p, args.rename_chart, args.fix_colors, args.fix_tables, args.dry,
                   replace_css=not skip_css, add_footer=args.add_footer,
                   unify_hero=args.unify_hero):
            changed += 1
    print(f"完成：改动 {changed} 份" + ("（dry-run）" if args.dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
