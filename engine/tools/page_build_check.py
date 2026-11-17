"""页面构建规范校验（PAGE-BUILD-SPEC v1.0，engine/docs/page-build-spec.md §8）。

扫描 hub 页（index.html / reader.html）与全部报告页（各业务线 reports/*.html），
校验：设计令牌 / 结构骨架 / 可访问性 / 兼容性 / 性能 / 生成确定性。

退出码：0 = 通过；1 = 存在 [E] 错误；2 = 仅 [W] 警告。
用法：python engine/tools/page_build_check.py [--quiet]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs  # noqa: E402

CANONICAL_NAVY = "--navy:#16324f"
# 已废弃的私有主色：出现即视为规范漂移
DRIFT_COLORS = ("#1f3d63", "#123a5c", "#1a1a2e", "#16213e")
HUB_PAGES = ("index.html", "reader.html")
MAX_HUB_BYTES = 100 * 1024
MAX_REPORT_BYTES = int(1.5 * 1024 * 1024)


def collect_pages() -> list[tuple[str, Path]]:
    """-> [(kind, path)]，kind ∈ {hub, report}。"""
    pages: list[tuple[str, Path]] = [("hub", ROOT / p) for p in HUB_PAGES]
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if reports.is_dir():
            pages.extend(("report", f) for f in sorted(reports.rglob("*.html")))
    return [(k, p) for k, p in pages if p.exists()]


def check_page(kind: str, path: Path) -> tuple[list[str], list[str]]:
    """-> ([E] 列表, [W] 列表)。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    errs: list[str] = []
    warns: list[str] = []

    # P01 文档基础
    if not re.search(r"<html\b[^>]*\blang=", text):
        errs.append("P01 缺少 <html lang>")
    if 'name="viewport"' not in text:
        errs.append("P01 缺少 viewport meta")
    if "charset=" not in text:
        errs.append("P01 缺少 charset")
    # P02 canonical 主色
    if CANONICAL_NAVY not in text:
        errs.append(f"P02 缺少 canonical 主色 {CANONICAL_NAVY}")
    # P03 漂移色
    low = text.lower()
    for c in DRIFT_COLORS:
        if c in low:
            errs.append(f"P03 存在漂移色 {c}")
    # P04–P07 可访问性 / 兼容性底线
    if "skip-link" not in text:
        errs.append("P04 缺少 .skip-link 跳转链接")
    if "focus-visible" not in text and ":focus" not in text:
        errs.append("P05 缺少焦点样式 :focus-visible/:focus")
    if "prefers-reduced-motion" not in text:
        errs.append("P06 缺少 prefers-reduced-motion")
    if "@media print" not in text:
        errs.append("P07 缺少 @media print")
    # P08 表格语义配平
    if text.count("<thead") != text.count("</thead>") or text.count("<tbody") != text.count("</tbody>"):
        errs.append("P08 <thead>/<tbody> 不配平")
    # P12 生成确定性
    if "最近生成" in text:
        errs.append("P12 生成物含「最近生成」时间戳（不确定性）")
    # P14 体积预算
    size = len(text.encode("utf-8"))
    budget = MAX_HUB_BYTES if kind == "hub" else MAX_REPORT_BYTES
    if size > budget:
        warns.append(f"P14 体积 {size / 1024:.0f}KB 超预算 {budget / 1024:.0f}KB")
    # P15 图片替代文本
    if re.search(r"<img\b(?![^>]*\balt=)[^>]*>", text):
        warns.append("P15 存在缺 alt 的 <img>")

    if kind == "report":
        # P09 报告骨架
        has_head = re.search(r'<header\b[^>]*class="[^"]*(report-head|hero)', text) is not None
        if not (has_head and 'class="report-nav"' in text and 'class="wrap"' in text):
            errs.append("P09 报告骨架不完整（需 header.report-head/.hero + nav.report-nav + .wrap）")
        # P10 章节与锚点
        if "<h2" in text and 'class="sec"' not in text:
            errs.append('P10 <h2> 缺少 class="sec"')
        # P11 echarts 容器类名
        if "echarts" in low and 'class="chart"' in text:
            errs.append("P11 echarts 容器应使用 .chart-eh（canonical 中 .chart 是图表卡片）")
        # P13 报告 URL 导航（规范仅要求周期报告：月 / 季 / 年）
        if "baseline" not in path.name and 'class="nav-url"' not in text:
            warns.append("P13 缺少 .nav-url（周期报告建议）")

    return errs, warns


def main() -> int:
    quiet = "--quiet" in sys.argv[1:]
    n_err = n_warn = n_ok = 0
    for kind, path in collect_pages():
        errs, warns = check_page(kind, path)
        if not errs and not warns:
            n_ok += 1
            if not quiet:
                print(f"[OK] {path}")
            continue
        for msg in errs:
            n_err += 1
            print(f"[E] {path}: {msg}")
        for msg in warns:
            n_warn += 1
            print(f"[W] {path}: {msg}")
    print(
        f"页面规范校验：{n_ok} 通过 / {n_err} 错误 / {n_warn} 警告"
        f"（检查 {len(collect_pages())} 个页面）"
    )
    if n_err:
        return 1
    if n_warn:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
