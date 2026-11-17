# -*- coding: utf-8 -*-
"""三层提示词继承体系一致性单元测试。

层级：L1 通用基座（`prompt-generic-base.md`）→ L2 类型模板（`engine/templates/<类型ID>/`）
→ L3 业务提示词（业务线 `prompts/`）。冲突优先级：业务提示词 ＞ 业务配置 ＞ 类型模板
＞ 通用基座 ＞ 通用规范。

把「后续会话在三层机制下开发不冲突、不混乱」固化为可拦截断言：

- 通用层根部文件与类型目录必备模板齐全；
- 通用层不出现业务关键词（防止业务内容污染通用层）；
- 类型模板均声明继承通用基座；
- 业务配置 / 周期提示词的继承声明引用**已注册**类型，且两者类型一致；
- 周期提示词引用 business-config；
- 提示词与配置中的相对链接全部可解析；
- 提示词使用的运行变量在「基座框架 ∪ 业务配置声明 ∪ 本提示词声明」内有定义。

CI 经 `python -m unittest discover -s engine/tests` 自动接入，无需改 ci.yml。
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

from _common import (  # noqa: E402
    BUSINESS_KEYWORDS,
    REQUIRED_TEMPLATE_FILES,
    TEMPLATE_DIR,
    TEMPLATE_TYPE_DIRS,
    iter_business_dirs,
)

TYPE_REF_RE = re.compile(r"engine/templates/([a-z0-9]+(?:-[a-z0-9]+)*)/")
LINK_RE = re.compile(r"\]\(([^)]+)\)")
VAR_RE = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
VAR_DECL_RE = re.compile(r"^\{\{([A-Z][A-Z0-9_]*)\}\}\s*=", re.MULTILINE)
TEMPLATE_GLOB = "prompt-*-template.md"

# business-config 必须声明的变量（与 validate.py 口径一致；来源登记变量见 T1 入口拦截）
CORE_CONFIG_VARS = (
    "{{REGION}}",
    "{{TOPIC}}",
    "{{REGISTRY_PATH}}",
    "{{SOURCE_LANGUAGE_RULE}}",
    "{{SOURCE_REGISTRY_PATH}}",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _base_vars() -> frozenset[str]:
    """从通用基座第二节变量块解析框架变量名（与基座同进同退，避免重复维护）。"""
    text = _read(TEMPLATE_DIR / "prompt-generic-base.md")
    sec = text.split("## 二、通用运行变量框架", 1)[1].split("\n## ", 1)[0]
    m = re.search(r"```\n(.*?)```", sec, re.DOTALL)
    assert m, "通用基座第二节变量块缺失"
    return frozenset(re.findall(r"^\{\{([A-Z0-9_]+)\}\}", m.group(1), re.MULTILINE))


def _links(text: str) -> list[str]:
    out = []
    for m in LINK_RE.finditer(text):
        href = m.group(1).split("#", 1)[0].strip()
        if href and not href.startswith(("http://", "https://", "mailto:")):
            out.append(href)
    return out


class TestGenericLayer(unittest.TestCase):
    """L1 / L2：通用层完整、类型模板继承基座、无业务关键词泄漏。"""

    def test_root_required_files(self):
        for name in REQUIRED_TEMPLATE_FILES:
            self.assertTrue((TEMPLATE_DIR / name).exists(), name)

    def test_type_dirs_have_required_templates(self):
        for type_id, files in TEMPLATE_TYPE_DIRS.items():
            tdir = TEMPLATE_DIR / type_id
            self.assertTrue(tdir.is_dir(), type_id)
            for name in files:
                self.assertTrue((tdir / name).exists(), f"{type_id}/{name}")

    def test_no_business_keywords_in_generic_layer(self):
        for md in sorted(TEMPLATE_DIR.rglob("*.md")):
            text = _read(md)
            for kw in BUSINESS_KEYWORDS:
                self.assertNotIn(kw, text, f"{md.relative_to(ROOT)} 出现业务关键词「{kw}」")

    def test_type_templates_inherit_base(self):
        for type_id in TEMPLATE_TYPE_DIRS:
            for md in sorted((TEMPLATE_DIR / type_id).glob(TEMPLATE_GLOB)):
                self.assertIn("prompt-generic-base.md", _read(md), md.relative_to(ROOT))

    def test_base_var_framework_parses(self):
        vars_ = _base_vars()
        self.assertIn("REGION", vars_)
        self.assertIn("SOURCE_REGISTRY_PATH", vars_)


class TestBusinessLayer(unittest.TestCase):
    """L3：业务配置与周期提示词的继承声明、类型引用、链接与变量闭环。"""

    def setUp(self):
        self.businesses = iter_business_dirs()
        self.assertTrue(self.businesses, "未识别到任何业务线")

    def test_config_declares_registered_type(self):
        for b in self.businesses:
            config = b.path / "prompts" / "business-config.md"
            self.assertTrue(config.exists(), b.rel)
            refs = TYPE_REF_RE.findall(_read(config))
            self.assertTrue(refs, f"{b.rel}: business-config 未引用 engine/templates/<类型ID>/")
            for t in refs:
                self.assertIn(t, TEMPLATE_TYPE_DIRS, f"{b.rel}: 引用未注册类型「{t}」")

    def test_config_core_vars(self):
        for b in self.businesses:
            text = _read(b.path / "prompts" / "business-config.md")
            for var in CORE_CONFIG_VARS:
                self.assertIn(var, text, f"{b.rel}: business-config 缺变量 {var}")

    def test_prompts_inherit_same_type_and_config(self):
        for b in self.businesses:
            config_refs = set(TYPE_REF_RE.findall(_read(b.path / "prompts" / "business-config.md")))
            prompts = sorted((b.path / "prompts").glob("prompt-*.md"))
            self.assertTrue(prompts, f"{b.rel}: 无周期提示词")
            for p in prompts:
                text = _read(p)
                refs = set(TYPE_REF_RE.findall(text))
                self.assertTrue(refs, f"{b.rel}/{p.name}: 无类型模板引用")
                for t in refs:
                    self.assertIn(t, TEMPLATE_TYPE_DIRS, f"{b.rel}/{p.name}: 引用未注册类型「{t}」")
                self.assertLessEqual(refs, config_refs,
                                     f"{b.rel}/{p.name}: 类型 {sorted(refs)} 与业务配置 {sorted(config_refs)} 不一致")
                self.assertIn("business-config.md", text, f"{b.rel}/{p.name}: 未引用 business-config.md")

    def test_links_resolve(self):
        targets = [TEMPLATE_DIR / name for name in REQUIRED_TEMPLATE_FILES if name.endswith(".md")]
        targets += [md for md in TEMPLATE_DIR.rglob("*.md")]
        for b in self.businesses:
            targets.append(b.path / "prompts" / "business-config.md")
            targets += sorted((b.path / "prompts").glob("prompt-*.md"))
        for md in targets:
            for href in _links(_read(md)):
                self.assertTrue((md.parent / href).resolve().exists(),
                                f"{md.relative_to(ROOT)} 断链 -> {href}")

    def test_prompt_variables_are_defined(self):
        base = _base_vars()
        for b in self.businesses:
            cfg_declared = set(VAR_DECL_RE.findall(_read(b.path / "prompts" / "business-config.md")))
            for p in sorted((b.path / "prompts").glob("prompt-*.md")):
                text = _read(p)
                used = set(VAR_RE.findall(text))
                declared = set(VAR_DECL_RE.findall(text))
                undef = sorted(used - base - cfg_declared - declared)
                self.assertFalse(undef, f"{b.rel}/{p.name}: 未定义变量 {undef}")


if __name__ == "__main__":
    unittest.main()
