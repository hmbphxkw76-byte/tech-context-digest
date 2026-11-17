# -*- coding: utf-8 -*-
"""插件注册（T4）：自动发现 semantic_checks 包内的 check 函数。"""
from __future__ import annotations

import importlib
import pkgutil

from .base import Block, CheckContext, Finding


def load_checks() -> list:
    """加载全部内置检查项 -> [(name, func)]。"""
    import semantic_checks as pkg

    out = []
    for mod in pkgutil.iter_modules(pkg.__path__):
        if mod.name.startswith("_"):
            continue
        m = importlib.import_module(f"semantic_checks.{mod.name}")
        fn = getattr(m, "check", None)
        if callable(fn):
            out.append((mod.name, fn))
    return out


def run_checks(blocks: list[Block], ctx: CheckContext,
               names: list[str] | None = None) -> list[Finding]:
    """对变更块执行指定检查项（names=None 表示全部）。"""
    findings: list[Finding] = []
    for name, fn in load_checks():
        if names and name not in names:
            continue
        findings.extend(fn(blocks, ctx))
    return findings
