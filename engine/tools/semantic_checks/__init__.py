# -*- coding: utf-8 -*-
"""语义检查插件包（T4）。

每个插件模块实现 `check(blocks, ctx) -> list[Finding]`，可插拔接入增量语义复核。
新增检查项只需在包内新增模块并实现同名函数，不改主流程。
"""
from .base import Block, CheckContext, Finding

__all__ = ["Block", "CheckContext", "Finding"]
