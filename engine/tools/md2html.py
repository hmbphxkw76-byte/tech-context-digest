"""md -> HTML 同步（CI: html-sync / scheduled-maintenance 的 md2html 步骤）。

扫描各业务线 reports/*.md，转换为同名自包含 .html（与 monitoring-common-spec
第 1 节「双格式交付」一致）。纯图表型简报（只出 HTML 的业务线）没有 md 源，
本工具自然跳过。幂等：重复执行产生相同输出。

渲染对齐 monitoring-common-spec 第 3 / 5 节与 canonical 设计系统
（engine/tools/report_style.py）：
  - 页头 `<header class="report-head">`（h1 + 副标题）；
  - 顶部固定导航 `<nav class="report-nav">` + `.nav-tabs` 锚点标签；
  - `<main class="wrap">` 正文，h2 章节重编号 id="sN"；
  - 表格加 class="fixed" 并逐列声明百分比列宽。

退出码：0 = 成功（含无 md 可转换）；1 = 转换失败或依赖缺失。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import iter_business_dirs  # noqa: E402
from report_style import style_block  # noqa: E402

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
__STYLE__
</head>
<body>
<header class="report-head">
  <div class="wrap">
    <h1>__TITLE__</h1>
__SUBTITLE__
  </div>
</header>
__NAV__
<main class="wrap">
__BODY__
</main>
</body>
</html>
"""

H1_RE = re.compile(r"<h1\b[^>]*>.*?</h1>\s*", re.DOTALL)
H2_RE = re.compile(r"<h2\b[^>]*>.*?</h2>", re.DOTALL)
H3_RE = re.compile(r"<h3\b[^>]*>.*?</h3>", re.DOTALL)
TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL)
TH_RE = re.compile(r"<th\b[^>]*>")


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def _with_width(th: str, width: int) -> str:
    """给单个 <th> 补百分比列宽（已含 width: 时跳过，避免重复声明）。"""
    if "width:" in th:
        return th
    if "style=" in th:
        return re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1)}; width:{width}%"', th, count=1)
    return th.replace("<th", f'<th style="width:{width}%"', 1)


def _fix_tables(html: str) -> str:
    """表格加 class="fixed"；表头逐列声明百分比列宽（同表之和 100%）。"""

    def fix(m: re.Match) -> str:
        tbl = m.group(0)
        if 'class="fixed"' not in tbl:
            tbl = tbl.replace("<table", '<table class="fixed"', 1)
        ths = TH_RE.findall(tbl)
        if not ths:
            return tbl
        n = len(ths)
        base, rem = divmod(100, n)
        widths = [base] * n
        widths[-1] += rem
        it = iter(widths)
        return TH_RE.sub(lambda mm: _with_width(mm.group(0), next(it)), tbl)

    return TABLE_RE.sub(fix, html)


def _renumber_h2(html: str) -> tuple[str, str]:
    """h2 重编号 id="sN"，返回 (改写后的 html, 导航标签 html)。"""
    items: list[str] = []

    def repl(m: re.Match) -> str:
        i = len(items) + 1
        items.append(f'<a href="#s{i}">{_strip_tags(m.group(0))}</a>')
        h2 = re.sub(r'\bid="[^"]*"', f'id="s{i}"', m.group(0), count=1)
        if "class=" not in h2:
            h2 = h2.replace("<h2", '<h2 class="sec"', 1)
        return h2

    html = H2_RE.sub(repl, html)
    return html, "\n".join(items)


def convert(md_path: Path) -> str:
    """md 文本 -> 自包含 HTML 文本。依赖 markdown 包（见 requirements.txt）。"""
    try:
        import markdown
    except ImportError:
        print("[ERROR] 缺少 markdown 依赖，请先执行 pip install -r requirements.txt")
        raise SystemExit(1)
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])
    title = md_path.stem
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # 副标题：h1 之后的首个 h3（如有），移入页头
    subtitle = ""
    m_sub = H3_RE.search(body)
    if m_sub:
        subtitle = f'<p class="sub">{_strip_tags(m_sub.group(0))}</p>'
        body = body[: m_sub.start()] + body[m_sub.end():]

    # 标题移入页头
    body = H1_RE.sub("", body, count=1)

    body = _fix_tables(body)
    body, nav_tabs = _renumber_h2(body)

    nav = ""
    if nav_tabs:
        nav = (
            '<nav class="report-nav" aria-label="报告导航">\n'
            '  <div class="wrap">\n'
            f'    <div class="nav-tabs">\n{nav_tabs}\n    </div>\n'
            "  </div>\n"
            "</nav>\n"
        )

    return (
        TEMPLATE
        .replace("__TITLE__", title)
        .replace("__STYLE__", style_block())
        .replace("__SUBTITLE__", subtitle)
        .replace("__NAV__", nav)
        .replace("__BODY__", body.strip())
    )


def collect_md_reports():
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if reports.is_dir():
            out.extend(sorted(reports.glob("*.md")))
    return out


def main() -> int:
    targets = collect_md_reports()
    if not targets:
        print("md2html：无 md 报告源（纯图表型简报只出 HTML），跳过")
        return 0
    ok = 0
    for md in targets:
        try:
            html = convert(md)
            out = md.with_suffix(".html")
            out.write_text(html, encoding="utf-8")
            print(f"[OK] {md} -> {out.name}")
            ok += 1
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001
            print(f"[ERROR] 转换失败 {md}: {e}")
            return 1
    print(f"md2html 完成：转换 {ok} 份")
    return 0


if __name__ == "__main__":
    sys.exit(main())
