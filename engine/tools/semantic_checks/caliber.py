# -*- coding: utf-8 -*-
"""口径检查（T4 插件）：多口径数值并列须显式标注口径。"""
from __future__ import annotations

from .base import Block, CheckContext, Finding

UNITS = ("AED", "USD", "%", "亿", "万", "bp", "pp")


def check(blocks: list[Block], ctx: CheckContext) -> list[Finding]:
    out: list[Finding] = []
    for i, b in enumerate(blocks):
        if ctx.changed_indices and i not in ctx.changed_indices:
            continue
        if sum(1 for u in UNITS if u in b.text) >= 2 and "口径" not in b.text:
            out.append(Finding("caliber", "P1", i, "多口径数值并列但未标注口径", b.text[:80]))
    return out
