#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""提示词一致性门禁（PROMPT-CONSISTENCY-CHECK v1.0）。

补齐 P1-10：泛用版 / 类型模板 / business-config 三者口径一致，且业务配置只实例化、
不复述规范正文。

  PC-01 注册表一致（[W]）：`template-registry.md` 第二节「已接入业务线」须与实际
        `content/` 业务线集合一致（双向：登记缺失 / 实际未登记）。
  PC-02 复述规范（[W]）：business-config 不得复述规范正文关键句（信息等级 / 决策卡 /
        ex-ante / 新增信息模块），应改为指针引用（`information-layering-spec.md` 等）。
  PC-03 周期模板齐备（[W]）：business-config 声明的周期提示词须存在于该业务线
        `prompts/` 目录（防「声明有、文件缺」）。

退出码：0 = 通过；1 = 存在 [E]；2 = 仅 [W]。
用法：python engine/tools/prompt_consistency_check.py [--quiet]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs  # noqa: E402

REGISTRY = ROOT / "engine" / "templates" / "template-registry.md"
REGISTRY_ROW_RE = re.compile(r"^\|\s*([a-z0-9-]+)\s*\|.*\|\s*([^|]+)\|\s*$")
REGISTRY_SECTIONS = [
    "决策摘要仅引用已核验", "触发条件 + 阈值 + 责任角色 + 时限 + 验证指标",
    "预校准（ex-ante）", "本期新增", "已核验 / 部分核验 / 推断 / 假设",
]
PROMPT_FILE_RE = re.compile(r"prompt-[a-z0-9-]+\.md")
DECLARED_PROMPT_RE = re.compile(r"prompt-[a-z0-9-]+\.md")


def _registry_lines() -> list[str]:
    text = REGISTRY.read_text(encoding="utf-8")
    m = re.search(r"## 二、已注册类型清单(.*?)(?:## 三、|\Z)", text, re.DOTALL)
    return m.group(1).splitlines() if m else []


def pc01_registry() -> list[str]:
    warns: list[str] = []
    registered: set[str] = set()
    for ln in _registry_lines():
        m = REGISTRY_ROW_RE.match(ln.strip())
        if not m:
            continue
        cell = m.group(2)
        for part in re.split(r"[；;、]", cell):
            part = part.strip()
            if part.startswith("content/"):
                registered.add(part)
    actual = {b.rel for b in iter_business_dirs()}
    for rel in sorted(registered - actual):
        warns.append(f"PC-01 注册表登记的业务线不存在：{rel}")
    for rel in sorted(actual - registered):
        warns.append(f"PC-01 实际业务线未登记到类型注册表：{rel}")
    return warns


def pc02_restatement() -> list[str]:
    warns: list[str] = []
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        if not cfg.exists():
            continue
        text = cfg.read_text(encoding="utf-8", errors="replace")
        hit = [s for s in REGISTRY_SECTIONS if s in text]
        if hit:
            warns.append(f"PC-02 business-config 复述规范正文（应改指针）：{b.rel}：{'、'.join(hit[:2])}")
    return warns


def pc03_prompt_files() -> list[str]:
    warns: list[str] = []
    for b in iter_business_dirs():
        cfg = b.path / "prompts" / "business-config.md"
        if not cfg.exists():
            continue
        text = cfg.read_text(encoding="utf-8", errors="replace")
        declared = set(DECLARED_PROMPT_RE.findall(text))
        existing = {f.name for f in (b.path / "prompts").glob("prompt-*.md")}
        for name in sorted(declared - existing):
            # 通用基座 / 类型模板位于 engine/，非业务线本地文件，不在此校验
            if name == "prompt-<cycle>.md" or "generic" in name or name.endswith("-template.md"):
                continue
            warns.append(f"PC-03 business-config 声明的提示词缺失：{b.rel}：{name}")
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description="提示词一致性门禁")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    warns = pc01_registry() + pc02_restatement() + pc03_prompt_files()
    for w in warns:
        print(f"[W] {w}")
    if not args.quiet or warns:
        print(f"提示词一致性校验：{len(warns)} 警告")
    return 2 if warns else 0


if __name__ == "__main__":
    sys.exit(main())
