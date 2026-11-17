"""决策交付门禁（DECISION-DELIVERY-SPEC v1.0）。

检查：
    DC-01 决策卡字段：结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度（decision-hub 强制）
    DC-02 行动协议：触发条件 + 阈值 + 责任角色 + 时限 + 可观测验证指标，且三档优先级
    DC-03 场景切片：投资决策 / 就业决策 / 政策制定
    DC-04 ex-ante 标注：信号灯 / 阈值处含「预校准（ex-ante）」

新报告缺项 = [E]；历史报告 = [W]。退出码 0/1/2。

用法：
    python engine/tools/decision_hub_check.py
    python engine/tools/decision_hub_check.py --gate-period 2026-12
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, detect_report, iter_business_dirs  # noqa: E402

DEFAULT_GATE = "2026-12"
HUB_LINE = "decision-hub"

_PROTOCOL_KEYS = ("触发条件", "阈值", "责任角色", "时限", "验证指标")
_PRIO_KEYS = ("立即行动", "持续观察", "仅记录存档")
_SLICE_KEYS = ("投资决策", "就业决策", "政策制定")
_CARD_KEYS = ("结论", "证据强度", "触发条件", "反向证据", "信息充分度")


def _period_key(period: str) -> tuple:
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", period)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{4})-(\d{2})", period)
    if m:
        return (int(m.group(1)), int(m.group(2)), 0)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if m:
        return (int(m.group(1)), int(m.group(2)) * 3, 0)
    m = re.fullmatch(r"(\d{4})", period)
    if m:
        return (int(m.group(1)), 12, 31)
    return (0, 0, 0)


def _period_of(name: str) -> str:
    det = detect_report(name)
    return det[1] if det else ""


def check_text(text: str, business_line: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    is_hub = HUB_LINE in business_line

    # DC-01 决策卡（decision-hub 强制；其他报告含「决策卡」字样时同样检查）
    if is_hub or "决策卡" in text:
        missing = [k for k in _CARD_KEYS if k not in text]
        if missing:
            out.append(("DC-01", f"决策卡缺字段：{'、'.join(missing)}"))

    # DC-02 行动协议（含「可执行启示 / 行动 / 行动项」的报告）
    if any(k in text for k in ("可执行启示", "行动项", "行动协议", "立即行动", "持续观察")):
        missing = [k for k in _PROTOCOL_KEYS if k not in text]
        if missing:
            out.append(("DC-02", f"行动协议缺要素：{'、'.join(missing)}"))
        if not all(k in text for k in _PRIO_KEYS):
            out.append(("DC-02", "行动项未按三档优先级（立即行动 / 持续观察 / 仅记录存档）划分"))

    # DC-03 场景切片
    if is_hub or "场景切片" in text:
        hit = [k for k in _SLICE_KEYS if k in text]
        if is_hub:
            missing = [k for k in _SLICE_KEYS if k not in text]
            if missing:
                out.append(("DC-03", f"决策仪表盘场景切片缺：{'、'.join(missing)}"))
        elif not hit:
            out.append(("DC-03", "未声明任何场景切片（投资决策 / 就业决策 / 政策制定）"))

    # DC-04 ex-ante 标注（含信号灯 / 阈值的报告）
    if ("信号灯" in text or "阈值" in text) and "预校准" not in text and "ex-ante" not in text:
        out.append(("DC-04", "信号灯 / 阈值处缺「预校准（ex-ante）」标注"))
    return out


def iter_targets(only_file: str | None):
    if only_file:
        p = ROOT / only_file
        return [(p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8", errors="replace"),
                 _period_of(p.name), "")]
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            out.append((f"{b.rel}/reports/{f.name}",
                        f.read_text(encoding="utf-8", errors="replace"),
                        _period_of(f.name), b.rel))
    return out


def run(only_file: str | None, gate: str) -> tuple[int, int, list[str]]:
    errors = warnings = 0
    lines = []
    targets = iter_targets(only_file)
    if not targets:
        lines.append("决策交付门禁：未发现报告，跳过")
        return 0, 0, lines
    for rel, text, period, bline in targets:
        findings = check_text(text, bline)
        if not findings:
            continue
        is_new = bool(period) and _period_key(period) >= _period_key(gate)
        for rule, msg in findings:
            level = "E" if is_new else "W"
            if level == "E":
                errors += 1
            else:
                warnings += 1
            tag = "新报告" if is_new else "历史报告"
            lines.append(f"[{level}] {rel}（{tag}，周期 {period or '未识别'}）{rule}：{msg}")
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="决策交付门禁")
    ap.add_argument("--file")
    ap.add_argument("--gate-period", default=DEFAULT_GATE)
    args = ap.parse_args()
    errors, warnings, lines = run(args.file, args.gate_period)
    for line in lines:
        print(line)
    if errors:
        print(f"决策交付门禁失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"决策交付门禁：{warnings} 项历史报告警告（不阻断）")
        return 2
    print("决策交付门禁通过：决策卡 / 行动协议 / 场景切片 / ex-ante 齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
