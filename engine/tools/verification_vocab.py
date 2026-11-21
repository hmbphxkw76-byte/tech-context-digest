#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""核验状态词表单一事实源（INFORMATION-VERIFICATION-SPEC v1.0）。

本仓库存在两套核验状态表述，语义相同但词形不同，是跨层歧义的主要来源：

  - 数据层 ``source_registry.json`` 的 ``verify_status``：
    英文枚举 ``verified`` / ``media_unverified`` / ``unverifiable``（R8 约定）；
  - 卡片层 ``engine/fact_cards/*.json`` 的 ``verify_status`` 与报告信息等级：
    中文 ``已核验`` / ``部分核验`` / ``未核验``（INFORMATION-LAYERING-SPEC）。

本模块把两者收敛为**一套映射事实源**，消除跨层歧义，并提供跨层一致性判定
（报告信息等级不得高于其来源 / 卡片允许的上限）。

设计取舍：**不改动存量数据**。数据层英文枚举仍为 canonical（沿用 R8 与既有
357 条登记），卡片 / 报告层中文仍为 canonical；本模块只做归一、映射与一致性判定，
使门禁与工具对两套词形都能识别，避免「同一状态两种写法」导致的漏判。

用法（纯函数，供 source_check / fact_card_check / 测试直接调用）：
    from verification_vocab import normalize_source_status, is_consistent
    normalize_source_status("已核验")      # -> "verified"
    normalize_source_status("media_unverified")  # -> "media_unverified"
    normalize_card_status("verified")      # -> "已核验"
    normalize_info_level("已核验")         # -> "已核验事实"（别名归一）
    is_consistent("已核验", "media_unverified")  # -> False（部分核验来源不得标已核验）
"""
from __future__ import annotations

# ── canonical 词表 ──────────────────────────────────────────────────────────
# 数据层（source_registry.json）
SOURCE_STATUSES = ("verified", "media_unverified", "unverifiable")
# 卡片 / 报告层（中文）
CARD_STATUSES = ("已核验", "部分核验", "未核验")
# 信息等级（INFORMATION-LAYERING-SPEC v1.0 第四节）
# canonical 词形以该规范为准：「已核验事实」；「已核验」为报告 inline 标记 / 历史用词别名。
INFO_LEVELS = ("已核验事实", "部分核验", "推断", "假设")

# 同义别名 → canonical（不另立强度）。
LEVEL_ALIASES = {"已核验": "已核验事实"}

SOURCE_TO_CARD = {
    "verified": "已核验",
    "media_unverified": "部分核验",
    "unverifiable": "未核验",
}
CARD_TO_SOURCE = {cn: en for en, cn in SOURCE_TO_CARD.items()}

# 常见中文别名 -> 数据层英文（补足报告 / 卡片中的口语写法）
_SOURCE_ALIASES = {
    "已核实": "verified",
    "部分核实": "media_unverified",
    "无法核实": "unverifiable",
    "待核实": "unverifiable",
    "未核实": "unverifiable",
}

# 信息等级强度（数值越大越强）：假设 < 推断 < 部分核验 < 已核验事实
_INFO_STRENGTH = {lv: i for i, lv in enumerate(reversed(INFO_LEVELS))}

# 核验状态允许的**最高**信息等级（决策摘要仅允许已核验 + 部分核验）：
# verified 可标已核验事实；media_unverified 最高部分核验；unverifiable / 未核验只能作假设。
_SOURCE_CEILING = {
    "verified": "已核验事实",
    "media_unverified": "部分核验",
    "unverifiable": "假设",
}
_CARD_CEILING = {
    "已核验": "已核验事实",
    "部分核验": "部分核验",
    "未核验": "假设",
}

# 可用于决策摘要的状态（INFORMATION-LAYERING-SPEC：决策摘要仅允许已核验 + 部分核验）
DECISION_SAFE_SOURCE = ("verified", "media_unverified")
DECISION_SAFE_CARD = ("已核验", "部分核验")


# ── 归一 ────────────────────────────────────────────────────────────────────
def normalize_source_status(value) -> str | None:
    """任意表述 -> 数据层英文 canonical；无法识别返回 ``None``。"""
    if not isinstance(value, str):
        return None
    v = value.strip().lower()
    if v in SOURCE_STATUSES:
        return v
    # 中文 canonical（CARD_TO_SOURCE 的 key）/ 常见别名
    raw = value.strip()
    if raw in CARD_TO_SOURCE:
        return CARD_TO_SOURCE[raw]
    if raw in _SOURCE_ALIASES:
        return _SOURCE_ALIASES[raw]
    return None


def normalize_card_status(value) -> str | None:
    """任意表述 -> 卡片 / 报告层中文 canonical；无法识别返回 ``None``。"""
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if raw in CARD_STATUSES:
        return raw
    en = normalize_source_status(raw)
    return SOURCE_TO_CARD.get(en) if en else None


def source_to_card(value) -> str | None:
    """数据层状态 -> 卡片 / 报告层中文；无法识别返回 ``None``。"""
    en = normalize_source_status(value)
    return SOURCE_TO_CARD.get(en) if en else None


def card_to_source(value) -> str | None:
    """卡片 / 报告层状态 -> 数据层英文；无法识别返回 ``None``。"""
    cn = normalize_card_status(value)
    return CARD_TO_SOURCE.get(cn) if cn else None


# ── 一致性 ──────────────────────────────────────────────────────────────────
def normalize_info_level(value) -> str | None:
    """信息等级归一：返回 canonical 中文信息等级，非法值返回 ``None``。

    ``已核验`` 是 ``已核验事实`` 的别名（报告 inline 标记与历史用词），
    归一后不产生额外强度；``value`` 已是 INFO_LEVELS 成员时原样返回。
    """
    if value in INFO_LEVELS:
        return value
    return LEVEL_ALIASES.get(value)


def info_level_for(value, kind: str = "source") -> str | None:
    """核验状态 -> 允许的最高信息等级；无法识别返回 ``None``。

    kind ∈ {"source", "card"}；两者语义相同，仅入参词形不同。
    """
    if kind == "source":
        st = normalize_source_status(value)
        return _SOURCE_CEILING.get(st) if st else None
    cn = normalize_card_status(value)
    return _CARD_CEILING.get(cn) if cn else None


def is_decision_safe(value, kind: str = "source") -> bool:
    """该状态是否可用于决策摘要（已核验 / 部分核验）。"""
    if kind == "source":
        return normalize_source_status(value) in DECISION_SAFE_SOURCE
    return normalize_card_status(value) in DECISION_SAFE_CARD


def is_consistent(level: str, status, kind: str = "source") -> bool:
    """报告信息等级是否不高于核验状态允许的上限。

    level  ∈ INFO_LEVELS（已核验事实 / 部分核验 / 推断 / 假设；``已核验`` 为别名）；
    status 为核验状态（kind 决定词形）。
    非法 level / 无法识别的 status 一律返回 False（宁可报不一致，不放过）。
    """
    ceiling = info_level_for(status, kind)
    lv = normalize_info_level(level)
    if ceiling is None or lv is None:
        return False
    return _INFO_STRENGTH[lv] <= _INFO_STRENGTH[ceiling]


def consistency_issue(level: str, status, kind: str = "source",
                      where: str = "") -> str | None:
    """不一致时返回告警消息；一致或无法判定时返回 ``None``."""
    if is_consistent(level, status, kind):
        return None
    ceiling = info_level_for(status, kind)
    loc = f"：{where}" if where else ""
    if ceiling is None:
        return f"{loc} 核验状态「{status}」无法识别，无法支撑信息等级「{level}」"
    return (f"{loc} 信息等级「{level}」高于核验状态「{status}」允许上限 "
            f"「{ceiling}」")
