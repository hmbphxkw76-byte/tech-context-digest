#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""看板-台账一致与版本治理门禁（CONSISTENCY-CHECK v1.0）。

补齐「规范有、门禁不查」缺口中的语义一致性条款：

  LC-01 台账结构（[W]）：声明 `{{REGISTRY_PATH}}` 为 md-ledger 的业务线，台账须含
        「数据看板追踪表」与「已修正事实清单」两个区块。
  LC-02 看板-报告一致（[W]）：台账看板追踪表的「指标」名须出现在该业务线最新报告中
        （名称级一致；数值级一致 A-03 属 LLM / 人工判定，不在此伪造）。
  VG-01 读数时点（[W]）：周期报告（月 / 季 / 年 / 周）须含「读数时点」。
  VG-02 版本治理（[W]）：报告声明语义版本 `vN`（N ≥ 2）时，须含「已修正事实清单」
        且其中有条目（核心事实修正留痕）；v1.x 基线允许「首期为空」。

退出码：0 = 通过；1 = 存在 [E]；2 = 仅 [W]。
用法：python engine/tools/consistency_check.py [--quiet]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs, iter_business_reports  # noqa: E402

REGISTRY_RE = re.compile(r"\{\{REGISTRY_PATH\}\}\s*=\s*(\S+)")
LEDGER_TABLE_RE = re.compile(r"数据看板追踪表[^\n]*\n+(.*?)(?:\n\s*\n|\Z)", re.DOTALL)
LEDGER_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
LEDGER_SEP_RE = re.compile(r"^\|[\s\-:|]+\|\s*$")
FIXED_LIST_RE = re.compile(r"已修正事实清单")
READING_TIME_RE = re.compile(r"读数时点")
# 语义版本 vN（N 为 1–2 位）；vYYYY.MM.DD 为读数时点标识，不由本规则判定
SEMVER_RE = re.compile(r"报告版本\s*v(\d{1,2})(?!\d)(?:\.\d+)*")
# 台账首列若为板块名，则指标名取第二列
BOARD_SECTIONS = {
    "基准与评估", "AI 安全与红队", "大模型与 Agent", "AI 编码与开发工具",
    "AI 应用与商业化", "跨板块", "宏观", "能源", "汇率", "利率",
}
TAG_RE = re.compile(r"<[^>]+>")


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", TAG_RE.sub("", s))


def _period_key(period: str) -> tuple:
    s = period or ""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s) or re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"(\d{4})-Q([1-4])", s)
    if m:
        return (int(m.group(1)), int(m.group(2)) * 3)
    m = re.fullmatch(r"(\d{4})", s)
    if m:
        return (int(m.group(1)), 0)
    return (0, 0)


def parse_ledger_rows(text: str) -> list[list[str]]:
    """解析 md-ledger 的「数据看板追踪表」-> 行（单元格列表）。"""
    m = LEDGER_TABLE_RE.search(text)
    if not m:
        return []
    rows: list[list[str]] = []
    for ln in m.group(1).splitlines():
        s = ln.strip()
        if not s.startswith("|") or LEDGER_SEP_RE.match(s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or cells[0] in ("板块", "指标"):
            continue
        rows.append(cells)
    return rows


def metric_name(cells: list[str]) -> str:
    if len(cells) > 1 and cells[0] in BOARD_SECTIONS:
        return cells[1]
    return cells[0]


def check_ledger(b, config_text: str) -> list[str]:
    warns: list[str] = []
    m = REGISTRY_RE.search(config_text)
    if not m:
        return warns
    reg_rel = m.group(1).strip()
    reg_path = ROOT / reg_rel
    if reg_path.suffix.lower() not in (".md", ".markdown"):
        return warns  # xlsx / json 登记册另有门禁（metric_registry / decision_hub）
    if not reg_path.exists():
        warns.append(f"LC-01 台账缺失：{reg_rel}")
        return warns
    text = reg_path.read_text(encoding="utf-8", errors="replace")
    is_ledger = "md-ledger" in text or "数据看板追踪表" in text
    if not is_ledger:
        return warns  # md-table 等其他格式由各自门禁覆盖
    if "数据看板追踪表" not in text:
        warns.append(f"LC-01 台账缺「数据看板追踪表」：{reg_rel}")
    if not FIXED_LIST_RE.search(text):
        warns.append(f"LC-01 台账缺「已修正事实清单」：{reg_rel}")

    rows = parse_ledger_rows(text)
    reports = sorted(iter_business_reports(b), key=lambda r: _period_key(r.period))
    if not reports:
        return warns
    latest = reports[-1]
    report_text = _norm((ROOT / latest.rel).read_text(encoding="utf-8", errors="replace"))
    for cells in rows:
        name = _norm(metric_name(cells))
        if name and name not in report_text:
            warns.append(f"LC-02 看板指标未出现在最新报告（{latest.period}）：{name}")
    return warns


def check_version(report_path: Path, text: str) -> list[str]:
    warns: list[str] = []
    name = report_path.name
    if "baseline" not in name and not READING_TIME_RE.search(text):
        warns.append("VG-01 周期报告缺「读数时点」")
    m = SEMVER_RE.search(text)
    if m and int(m.group(1)) >= 2:
        if not FIXED_LIST_RE.search(text):
            warns.append(f"VG-02 语义版本 v{m.group(1)} 缺「已修正事实清单」")
        else:
            section = text.split("已修正事实清单", 1)[1]
            if re.search(r"首期为空|无已修正事实清单条目|0\s*条", section[:400]) and "|" not in section[:400]:
                warns.append(f"VG-02 语义版本 v{m.group(1)} 的修正清单为空")
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description="看板-台账一致与版本治理门禁")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    n_err = n_warn = 0

    for b in iter_business_dirs():
        config = b.path / "prompts" / "business-config.md"
        config_text = config.read_text(encoding="utf-8", errors="replace") if config.exists() else ""
        for msg in check_ledger(b, config_text):
            n_warn += 1
            print(f"[W] {b.rel}: {msg}")

    for b in iter_business_dirs():
        for r in sorted(iter_business_reports(b), key=lambda r: _period_key(r.period)):
            path = ROOT / r.rel
            text = path.read_text(encoding="utf-8", errors="replace")
            for msg in check_version(path, text):
                n_warn += 1
                print(f"[W] {r.rel}: {msg}")

    if not args.quiet or n_warn:
        print(f"一致性校验：{n_warn} 警告 / {n_err} 错误")
    if n_err:
        return 1
    return 2 if n_warn else 0


if __name__ == "__main__":
    sys.exit(main())
