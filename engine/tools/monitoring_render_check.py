#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""监测报告渲染规范门禁（MONITORING-RENDER-CHECK v1.0）。

补齐「规范有、门禁不查」缺口：`engine/templates/monitoring-common-spec.md`
第二 / 三 / 四 / 六节中**机械可判定**的条款此前无门禁覆盖，本门禁逐条接线。

  MON-01 图注齐备（[W]）：每个 `.chart-box` 图表容器下应有 `.chart-note`；
        `.chart-eh` 数量不得多于 `.chart-note`（每张图都要有图注）。
  MON-02 口径并列（[W]）：图注 / 图表标题出现「并列 / 多口径 / 分轴 / 双轴」时，
        须注明「不可相减 / 禁止相减 / 不可合并 / 不可比」等口径警示。
  MON-03 列宽塌缩（[W]）：≥7 列表逐列估算表头文本需求宽，声明宽度不足则告警
        （规范 §3：百分比宽度小于表头需求宽时应整表改用内容适配 px）。
  MON-04 noopener（[W]）：外部 http(s) 链接须 `target="_blank"` + `rel` 含 `noopener`
        （指向本仓库自身的链接为内部指针，豁免）。
  MON-05 原生 title（[W]）：不得以浏览器原生 `title` 承载 URL 提示
        （规范 §6 要求自定义 tooltip）。

退出码：0 = 通过；1 = 存在 [E]；2 = 仅 [W]。当前全部条款定为 [W]（存量不阻断），
新报告升级 [E] 需另行评估。
用法：python engine/tools/monitoring_render_check.py [--quiet]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import iter_business_dirs  # noqa: E402

# 容器宽度基准（px），用于百分比列宽 → 像素换算（与 page-build-spec 最大宽度一致）
CONTAINER_PX = 1160
WIDE_TABLE_COLS = 7
# 表头文本需求宽估算：CJK 全角 14px、ASCII 8px、内边距 16px
CJK_PX = 14
ASCII_PX = 8
CELL_PADDING_PX = 16

NOTE_RE = re.compile(r'<(?:p|div) class="chart-note"[^>]*>(.*?)</(?:p|div)>', re.DOTALL)
BOX_START_RE = re.compile(r'<div class="chart-box">')
BOX_TITLE_RE = re.compile(r'<h[34][^>]*>(.*?)</h[34]>', re.DOTALL)
EH_RE = re.compile(r'class="chart-eh"')
TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL)
TH_RE = re.compile(r"<th\b[^>]*>(.*?)</th>", re.DOTALL)
TH_TAG_RE = re.compile(r"<th\b[^>]*>", re.DOTALL)
WIDTH_RE = re.compile(r"width:\s*([0-9.]+)(%|px)")
LINK_RE = re.compile(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>')
NATIVE_TITLE_RE = re.compile(r'<a\b[^>]*title="https?://')
REPO_SELF_HOSTS = ("github.com/hmbphxkw76-byte/tech-context-digest",)
CALIBER_KEY_RE = re.compile(r"并列|多口径|分轴|双轴")
CALIBER_OK_RE = re.compile(
    r"不可.{0,4}相减|禁止.{0,4}相减|不可合并|禁止合并|不合并|不可比|口径不同|统计域不同|统计周期不同")
TAG_RE = re.compile(r"<[^>]+>")


def _plain(html: str) -> str:
    return TAG_RE.sub("", html).strip()


def _header_demand_px(header_html: str) -> int:
    """表头文本需求宽（px）估算。"""
    text = _plain(header_html)
    width = sum(CJK_PX if ord(ch) > 0x2E80 else ASCII_PX for ch in text)
    return width + CELL_PADDING_PX


def _is_self_link(url: str) -> bool:
    return any(host in url for host in REPO_SELF_HOSTS)


def collect_reports() -> list[Path]:
    out: list[Path] = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if reports.is_dir():
            out.extend(sorted(reports.rglob("*.html")))
    return out


def check_report(path: Path) -> tuple[list[str], list[str]]:
    """-> ([E] 列表, [W] 列表)。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    errs: list[str] = []
    warns: list[str] = []

    # MON-01 图注齐备
    starts = [m.start() for m in BOX_START_RE.finditer(text)]
    for idx, s in enumerate(starts):
        e = starts[idx + 1] if idx + 1 < len(starts) else len(text)
        if not NOTE_RE.search(text[s:e]):
            warns.append(f"MON-01 图表容器 #{idx + 1} 缺少 .chart-note")
    n_eh = len(EH_RE.findall(text))
    n_note = len(NOTE_RE.findall(text))
    if n_eh > n_note:
        warns.append(f"MON-01 图表 {n_eh} 张但图注仅 {n_note} 条")

    # MON-02 口径并列须注明不可相减（按图表块整体判定：标题 + 图注）
    if starts:
        segments = []
        for idx, s in enumerate(starts):
            e = starts[idx + 1] if idx + 1 < len(starts) else len(text)
            block = text[s:e]
            title = BOX_TITLE_RE.search(block)
            note = NOTE_RE.search(block)
            segments.append(
                (title.group(1) if title else "") + "\n" + (note.group(1) if note else ""))
    else:
        segments = list(NOTE_RE.findall(text))
    for i, seg in enumerate(segments, 1):
        plain = _plain(seg)
        if CALIBER_KEY_RE.search(plain) and not CALIBER_OK_RE.search(plain):
            warns.append(f"MON-02 口径并列未注明「不可相减」：{plain[:60]}")

    # MON-03 列宽塌缩
    for i, tbl in enumerate(TABLE_RE.findall(text), 1):
        bodies = TH_RE.findall(tbl)
        tags = TH_TAG_RE.findall(tbl)
        if len(bodies) < WIDE_TABLE_COLS:
            continue
        for j, (body, tag) in enumerate(zip(bodies, tags)):
            m = WIDTH_RE.search(tag)
            if not m:
                warns.append(f"MON-03 第 {i} 表第 {j + 1} 列表头未声明列宽")
                continue
            val = float(m.group(1))
            px = val / 100 * CONTAINER_PX if m.group(2) == "%" else val
            demand = _header_demand_px(body)
            if px < demand:
                warns.append(
                    f"MON-03 第 {i} 表第 {j + 1} 列宽 {m.group(0)} 小于表头需求 ~{demand}px"
                    f"（{_plain(body)[:16]}）")

    # MON-04 noopener
    for m in LINK_RE.finditer(text):
        url = m.group(1)
        if _is_self_link(url):
            continue
        tag = m.group(0)
        if 'target="_blank"' not in tag or "noopener" not in tag:
            warns.append(f"MON-04 外部链接缺 target/_blank 或 noopener：{url[:70]}")

    # MON-05 原生 title 承载 URL
    for m in NATIVE_TITLE_RE.finditer(text):
        warns.append(f"MON-05 以原生 title 承载 URL 提示（应用自定义 tooltip）：{m.group(0)[:70]}")

    return errs, warns


def main() -> int:
    quiet = "--quiet" in sys.argv[1:]
    reports = collect_reports()
    n_err = n_warn = n_ok = 0
    for path in reports:
        errs, warns = check_report(path)
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
        f"监测渲染规范校验：{n_ok} 通过 / {n_err} 错误 / {n_warn} 警告"
        f"（检查 {len(reports)} 份报告）"
    )
    if n_err:
        return 1
    if n_warn:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
