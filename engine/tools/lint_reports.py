"""报告内容校验 lint（CI: scheduled-maintenance / content-update / ci.yml 的 lint 步骤）。

扫描各业务线 reports/*.html，执行监测报告通用规范的人工校验清单（第 9 节）中
可程序化的项目。退出码：0 = 通过；1 = 存在错误项；2 = 仅存在警告项。

错误项（阻断）：
- thead / tbody / table 标签不配对、重复 </tbody>
- 畸形 <th scope="col"ead> 写法

警告项（不阻断）：
- 多列表（≥6 列）<th> 未声明百分比列宽
- <img> 缺少 alt 属性
- <table> 缺少 class="fixed"
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import iter_business_dirs  # noqa: E402

TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL)
OPEN_TABLE_RE = re.compile(r"<table\b[^>]*>", re.DOTALL)
TH_RE = re.compile(r"<th\b[^>]*>", re.DOTALL)


def _has_fixed_class(tbl: str) -> bool:
    """表格开标签的 class 是否含 fixed（按 class token 判定，支持合并类名）。"""
    m = OPEN_TABLE_RE.match(tbl)
    return bool(m and re.search(r'class="[^"]*\bfixed\b', m.group(0)))


def lint_html(text: str) -> list[tuple[str, str]]:
    """对单份 HTML 文本执行 lint -> [(level, message), ...]，level in {'E','W'}。"""
    issues: list[tuple[str, str]] = []

    # 标签配对（注意 '<tbody' 不会误匹配 '</tbody'）
    for tag in ("thead", "tbody", "table"):
        open_n = len(re.findall(rf"<{tag}\b", text))
        close_n = len(re.findall(rf"</{tag}>", text))
        if open_n != close_n:
            issues.append(("E", f"<{tag}> 标签不配对（开 {open_n} / 闭 {close_n}）"))
    if text.count("</tbody>") > len(re.findall(r"<tbody\b", text)):
        issues.append(("E", "存在多余的 </tbody>（疑似重复闭合）"))

    # 畸形 th 写法
    if re.search(r'<th[^>]*scope="col"ead', text):
        issues.append(("E", '存在畸形 <th scope="col"ead> 写法'))

    # 逐表检查
    for i, tbl in enumerate(TABLE_RE.findall(text), start=1):
        if not _has_fixed_class(tbl):
            issues.append(("W", f"第 {i} 张表格缺少 class=\"fixed\"（列宽声明规范）"))
        ths = TH_RE.findall(tbl)
        if len(ths) >= 6:
            no_width = [t for t in ths if "width:" not in t]
            if no_width:
                issues.append(
                    ("W", f"第 {i} 张表格（{len(ths)} 列）有 {len(no_width)} 个 <th> 未声明百分比列宽")
                )

    # 图片可访问性
    for m in re.finditer(r"<img\b[^>]*>", text):
        if "alt=" not in m.group(0):
            issues.append(("W", "<img> 缺少 alt 属性（可访问性）"))

    return issues


def collect_report_htmls():
    """收集全部业务线 reports/*.html -> [(relpath, Path)]。"""
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            out.append((f"{b.rel}/reports/{f.name}", f))
    return out


def main() -> int:
    targets = collect_report_htmls()
    if not targets:
        print("lint：未发现报告 HTML，跳过")
        return 0
    errors = warnings = 0
    for rel, path in targets:
        text = path.read_text(encoding="utf-8", errors="replace")
        issues = lint_html(text)
        if not issues:
            print(f"[OK] {rel}")
            continue
        for level, msg in issues:
            print(f"[{level}] {rel}: {msg}")
            if level == "E":
                errors += 1
            else:
                warnings += 1
    if errors:
        print(f"lint 失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"lint 存在 {warnings} 项警告（无错误，不阻断）")
        return 2
    print(f"lint 通过：{len(targets)} 份报告全部合格")
    return 0


if __name__ == "__main__":
    sys.exit(main())
