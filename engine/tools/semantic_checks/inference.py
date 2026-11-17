# -*- coding: utf-8 -*-
"""表述逻辑检查（T4 插件）：推断 / 预测须标注依据。"""
from __future__ import annotations

from .base import Block, CheckContext, Finding


def check(blocks: list[Block], ctx: CheckContext) -> list[Finding]:
    out: list[Finding] = []
    for i, b in enumerate(blocks):
        if ctx.changed_indices and i not in ctx.changed_indices:
            continue
        if ("推断" in b.text or "预测" in b.text) and not any(
                k in b.text for k in ("来源", "依据", "http", "已核验")):
            out.append(Finding("inference", "P1", i, "推断/预测未标注依据", b.text[:80]))
    return out
