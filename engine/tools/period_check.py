#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""报告周期校验（CI: optimization_gate 统一入口）。

规则（报告落款周期 = 产出当天的自然月，单一事实源见 gate_period.py）：

    报告 period 晚于当前自然月 -> [E]（阻断）

原因：落款到未来周期的报告会声称覆盖尚未发生的「未来数据窗口」，
向读者放大信息差（2026-11-20 曾产出落款 2026-12 / 2027-01 的报告，
其监测窗口延伸到 2026-12-15 / 2027-01-15，属算术虚构）。

月 / 季 / 年 / 周统一换算为绝对月序比较；无法识别的周期跳过（命名校验由
validate.py / classify_reports.py 承载）。

退出码：0 通过；1 存在 `[E]`；2 仅 `[W]`（本检查不产生 `[W]`）。

用法：
    python engine/tools/period_check.py
    python engine/tools/period_check.py --gate-period auto
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import iter_reports  # noqa: E402
from gate_period import AUTO  # noqa: E402
from gate_period import resolve as resolve_period  # noqa: E402

# 周期形态：YYYY / YYYY-MM / YYYY-MM-DD / YYYY-Qn
_PERIOD_RE = re.compile(r"^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?(?:-Q([1-4]))?$")


def abs_month(period: str) -> int | None:
    """周期标识 -> 绝对月序（年 * 12 + 月序）；无法识别返回 None。

    '2026-11' -> 2026*12+10；'2026-Q3' -> 2026*12+6；'2026' -> 2026*12；
    '2026-11-27' -> 2026*12+10。
    """
    m = _PERIOD_RE.match(period or "")
    if not m:
        return None
    y = int(m.group(1))
    if m.group(4):  # 季度：锚定季首月
        return y * 12 + (int(m.group(4)) - 1) * 3
    if m.group(2):  # 月 / 周（日期）
        return y * 12 + (int(m.group(2)) - 1)
    return y * 12  # 年度：锚定 1 月


def run(gate_period: str = AUTO) -> tuple[list[str], list[str], list[str]]:
    """-> (errors, warnings, lines)。

    gate_period 仅为「当前自然月」的解析基准：默认 `auto`（当前自然月），
    显式传 YYYY-MM 可固定口径复现。
    """
    current = resolve_period(gate_period)
    cur_m = abs_month(current)
    errors: list[str] = []
    warnings: list[str] = []
    lines: list[str] = []
    if cur_m is None:
        return errors, warnings, lines
    for r in iter_reports():
        if not r.period:
            continue
        pm = abs_month(r.period)
        if pm is None or pm <= cur_m:
            continue
        msg = (f"[E] {r.rel}（{r.cycle} {r.period}）：落款周期晚于当前自然月 {current}"
               f"——报告声称覆盖未来数据窗口")
        errors.append(msg)
        lines.append(msg)
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="报告周期校验（不得晚于当前自然月）")
    ap.add_argument("--gate-period", default=AUTO,
                    help="当前自然月解析基准（默认 auto = 当前自然月）")
    args = ap.parse_args()
    errors, _warnings, lines = run(args.gate_period)
    for line in lines:
        print(line)
    if errors:
        print(f"报告周期校验失败：{len(errors)} 份报告落款周期晚于当前自然月")
        return 1
    print("报告周期校验通过：无未来周期报告")
    return 0


if __name__ == "__main__":
    sys.exit(main())
