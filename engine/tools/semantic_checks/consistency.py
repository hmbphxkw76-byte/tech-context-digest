# -*- coding: utf-8 -*-
"""一致性检查（T4 插件）：变更块内同一指标不得出现冲突数值。"""
from __future__ import annotations

import re

from .base import Block, CheckContext, Finding

# 负向断言防止把编号（G01–G05、K01 / K02）回溯拆成「G0:1」「G0:5」这类伪指标
IND_RE = re.compile(r"([A-Za-z]{1,3}-?\d{1,3})(?!\d)\s*[:：]?\s*([0-9]+(?:\.[0-9]+)?)")


def check(blocks: list[Block], ctx: CheckContext) -> list[Finding]:
    vals: dict[str, set[float]] = {}
    for i, b in enumerate(blocks):
        if ctx.changed_indices and i not in ctx.changed_indices:
            continue
        for m in IND_RE.finditer(b.text):
            vals.setdefault(m.group(1).upper(), set()).add(float(m.group(2)))
    out: list[Finding] = []
    for k, vs in sorted(vals.items()):
        if len(vs) > 1:
            out.append(Finding("consistency", "P0", -1,
                               f"指标 {k} 出现冲突数值 {sorted(vs)}", ""))
    return out
