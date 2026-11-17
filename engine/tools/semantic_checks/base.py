# -*- coding: utf-8 -*-
"""语义检查插件公共类型（T4）。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Block:
    """文本块（段落 / 标题 / 列表项 / 表格行 / 引用 / 代码块）。"""

    kind: str
    text: str
    key: str = ""

    def __post_init__(self) -> None:
        if not self.key:
            object.__setattr__(self, "key", _normalize(self.text))


def _normalize(s: str) -> str:
    return " ".join(s.split()).strip().lower()


@dataclass
class CheckContext:
    """检查上下文：提供本期 / 上期文本与变更块索引。"""

    previous_text: str = ""
    current_text: str = ""
    changed_indices: list[int] = field(default_factory=list)


@dataclass
class Finding:
    check: str
    severity: str  # P0 / P1 / P2
    block_index: int
    message: str
    evidence: str = ""
