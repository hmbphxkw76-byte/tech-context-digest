# -*- coding: utf-8 -*-
"""来源可追溯检查（T4 插件）：变更块内关键数字须有来源标注。"""
from __future__ import annotations

import re

from .base import Block, CheckContext, Finding

NUMBER_UNIT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:AED|USD|EUR|GBP|\$|€|£|%|亿|万|千|百万|十亿|bp|bps|pp|sqft|m²|套|宗|人)")
# 除 URL 与「来源/参考」字样外，还识别本报告体系的来源列约定：
# 级别标签（官方一手/官方通讯社/行业机构/媒体转述）与「机构 · 周期」格式。
SOURCE_RE = re.compile(
    r"(https?://|来源|参考|Source|\[Source"
    r"|官方一手|官方通讯社|行业机构|媒体转述"
    r"|[·•]\s*\d{4}-\d{2})",
    re.I,
)


def check(blocks: list[Block], ctx: CheckContext) -> list[Finding]:
    out: list[Finding] = []
    for i, b in enumerate(blocks):
        if ctx.changed_indices and i not in ctx.changed_indices:
            continue
        if NUMBER_UNIT_RE.search(b.text) and not SOURCE_RE.search(b.text):
            out.append(Finding("source_trace", "P0", i,
                               "变更块含带单位关键数字但无来源标注", b.text[:80]))
    return out
