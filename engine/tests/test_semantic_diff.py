# -*- coding: utf-8 -*-
"""增量语义 diff 与插件（semantic_diff / T4）单元测试。"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("semantic_diff", ROOT / "engine" / "tools" / "semantic_diff.py")
sd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sd)

from semantic_checks.base import Block, CheckContext  # noqa: E402
from semantic_checks.registry import load_checks  # noqa: E402


class TestBlocks(unittest.TestCase):
    def test_kinds(self):
        blocks = sd.iter_blocks("# 标题\n\n段落\n- 列表\n| a | b |\n> 引用")
        kinds = [b.kind for b in blocks]
        self.assertEqual(kinds, ["heading", "paragraph", "list", "table", "quote"])

    def test_html_tags_stripped(self):
        # 报告为自包含 HTML：标签属性（如 width:6%）不得进入语义匹配
        blocks = sd.iter_blocks('<th style="width:6%">编号</th>\n<tr><td>K01</td></tr>')
        self.assertEqual([b.text for b in blocks], ["编号", "K01"])

    def test_html_entities_unescaped(self):
        blocks = sd.iter_blocks("<p>AED 1,000 &amp; 2</p>")
        self.assertEqual(blocks[0].text, "AED 1,000 & 2")


class TestDiff(unittest.TestCase):
    def test_added_and_removed(self):
        d = sd.diff_blocks("旧段落\n", "旧段落\n新段落\n")
        self.assertEqual(d["added"], [1])
        self.assertEqual(d["removed"], [])

    def test_modified(self):
        d = sd.diff_blocks("数值 4.5\n", "数值 4.6\n")
        self.assertEqual(d["modified"], [(0, 0)])
        self.assertIn(0, d["changed_indices"])


class TestPlugins(unittest.TestCase):
    def test_registry_has_plugins(self):
        self.assertGreaterEqual(len(load_checks()), 4)

    def test_source_trace_finding(self):
        blocks = [Block("paragraph", "规模 1,000 亿")]
        ctx = CheckContext(changed_indices=[0])
        from semantic_checks import source_trace
        self.assertTrue(source_trace.check(blocks, ctx))

    def test_source_trace_accepts_report_source_column(self):
        # 报告来源列的两种约定：级别标签 / 「机构 · 周期」
        blocks = [
            Block("table", "R10/R11 净 4.1–7.6% Peak Trust · 2026-10 · 已核验"),
            Block("table", "许可 48% 官方一手"),
        ]
        ctx = CheckContext(changed_indices=[0, 1])
        from semantic_checks import source_trace
        self.assertEqual(source_trace.check(blocks, ctx), [])

    def test_consistency_conflict(self):
        blocks = [Block("paragraph", "K01: 4.5"), Block("paragraph", "K01: 4.6")]
        ctx = CheckContext(changed_indices=[0, 1])
        from semantic_checks import consistency
        findings = consistency.check(blocks, ctx)
        self.assertTrue(any("K01" in f.message for f in findings))

    def test_consistency_ignores_report_ids(self):
        # G01–G05 / K01 / K02 是编号，不是「指标: 数值」
        blocks = [Block("paragraph", "G01–G05 政策乘数表"), Block("paragraph", "K01 / K02 的传导时滞")]
        ctx = CheckContext(changed_indices=[0, 1])
        from semantic_checks import consistency
        self.assertEqual(consistency.check(blocks, ctx), [])

    def test_inference_and_caliber(self):
        from semantic_checks import caliber, inference
        b = [Block("paragraph", "推断：市场回暖")]
        self.assertTrue(inference.check(b, CheckContext(changed_indices=[0])))
        c = [Block("paragraph", "AED 100 万 与 USD 100")]
        self.assertTrue(caliber.check(c, CheckContext(changed_indices=[0])))

    def test_analyze_end_to_end(self):
        res = sd.analyze("旧\n", "旧\n规模 1,000 亿\n", names=["source_trace"])
        self.assertGreaterEqual(res["changed_blocks"], 1)
        self.assertTrue(any(f["check"] == "source_trace" for f in res["findings"]))


if __name__ == "__main__":
    unittest.main()
