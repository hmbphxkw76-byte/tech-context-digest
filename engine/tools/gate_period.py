#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""两级 gate-period 解析（滚动基线，单一事实源）。

规范：engine/docs/report-pipeline-system.md §5.2「两级 gate-period 与退出码」。

问题（2026-11-18 全量重审实测）：原先 `DEFAULT_GATE_PERIOD` / `DEFAULT_SOURCE_GATE_PERIOD`
是**写死的常量**（如 "2026-12" / "2027-01"），随时间推移会让「新报告」判定自动失效
——到 2027-02，2027-01 的报告会被判为历史而降级放行，与「新报告必阻断」的承诺相悖。

本模块把 gate-period 变为**可滚动**：

    resolve("2026-12") -> "2026-12"     # 显式周期：原样返回（CI 可固定口径复现）
    resolve("auto")     -> "2026-12"     # 滚动：当前自然月 + 1（下一周期）

`auto` 为默认值：新报告永远被强制、历史报告永远只警告，且不随时间失效。
"""
from __future__ import annotations

import re
from datetime import date

AUTO = "auto"

# 可解析的周期形态：YYYY-MM-DD / YYYY-MM / YYYY-Qn / YYYY
_PERIOD_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?(-Q[1-4])?$")


def is_auto(period: str | None) -> bool:
    return str(period or "").strip().lower() == AUTO


def resolve(period: str | None, today: date | None = None) -> str:
    """-> 可比较的周期标识（显式周期原样返回；`auto` 解析为「当前自然月 + 1」）。

    解析失败（非法周期）时同样回落到滚动值，保证门禁永不因配置漂移而静默失效。
    """
    raw = str(period or "").strip()
    if raw and not is_auto(raw) and _PERIOD_RE.match(raw):
        return raw
    d = today or date.today()
    y, m = d.year, d.month + 1
    if m > 12:
        y, m = y + 1, 1
    return f"{y}-{m:02d}"


def describe(period: str | None) -> str:
    """人类可读描述（用于 `--list` / 日志）：`auto -> 2026-12`。"""
    raw = str(period or "").strip()
    if is_auto(raw):
        return f"{AUTO} -> {resolve(raw)}"
    return raw or "(未设置)"
