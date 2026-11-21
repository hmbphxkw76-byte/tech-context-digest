# -*- coding: utf-8 -*-
"""分类边界单元测试（classify_reports.py 双校验 / P2-3）。

覆盖采集与分类全流程的边界：地区/细分线索、节拍白名单、多候选、
大小写、项目制命名、无候选。
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("classify_reports", ROOT / "engine" / "tools" / "classify_reports.py")
cr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cr)


class TestDoubleValidation(unittest.TestCase):
    def test_region_and_cycle_agree(self):
        sig = cr.owner_signals("real-estate_apartment_2026-11_monthly.html")
        self.assertEqual(sig["owner"], "content/economy/dubai/apartment")
        self.assertTrue(sig["region_hit"])
        self.assertTrue(sig["cycle_ok"])

    def test_cycle_mismatch_is_unknown(self):
        """地区线索命中但节拍与类型不符 -> 需人工（防误搬）。"""
        sig = cr.owner_signals("real-estate_apartment_2026-11_weekly.html")
        self.assertTrue(sig["region_hit"])
        self.assertFalse(sig["cycle_ok"])
        self.assertIsNone(sig["owner"])

    def test_unique_property_hit_assigns(self):
        """apartment 细分唯一命中经济公寓业务线 -> 自动归位。"""
        sig = cr.owner_signals("apartment_2026-11_monthly.html")
        self.assertEqual(sig["property_hits"], ["content/economy/dubai/apartment"])
        self.assertEqual(sig["owner"], "content/economy/dubai/apartment")

    def test_property_ambiguous(self):
        """competitive-intelligence 同时命中 AI 安全 / AI 应用两条线 -> 候选不唯一，需人工。"""
        sig = cr.owner_signals("competitive-intelligence_2026-11_monthly.html")
        self.assertEqual(len(sig["property_hits"]), 2)
        self.assertIsNone(sig["owner"])

    def test_region_mismatch_is_unknown(self):
        """地区线索与候选业务线 region 不一致 -> 需人工。"""
        sig = cr.owner_signals("dubai_trends_2026-11-13_weekly.html")
        self.assertEqual(sig["regions_in_name"], ["dubai"])
        self.assertEqual(sig["property_hits"], [])
        self.assertIsNone(sig["owner"])

    def test_no_candidate_is_unknown(self):
        sig = cr.owner_signals("2026-11_monthly.html")
        self.assertEqual(sig["candidates"], [])
        self.assertIsNone(sig["owner"])

    def test_case_insensitive_region(self):
        sig = cr.owner_signals("REAL-ESTATE_APARTMENT_2026-11_monthly.html")
        self.assertEqual(sig["owner"], "content/economy/dubai/apartment")

    def test_project_naming_requires_human(self):
        """项目制命名无法校验节拍 -> 不自动归位。"""
        sig = cr.owner_signals("real-estate_apartment_2026-11-13_topic.html")
        self.assertIsNone(sig["cycle"])
        self.assertFalse(sig["cycle_ok"])
        self.assertIsNone(sig["owner"])

    def test_owner_of_matches_signals(self):
        self.assertIsNotNone(cr.owner_of("apartment_2026-11_monthly.html"))
        self.assertIsNone(cr.owner_of("apartment_2026-11_weekly.html"))
        # ai-security/dubai 归位后 region 缺省，含地区词的名称被 region 一致性排除
        self.assertIsNone(cr.owner_of("dubai_security_2026-11_monthly.html"))


class TestStraysScope(unittest.TestCase):
    def test_strays_only_root_and_templates(self):
        for f in cr.strays():
            rel = f.relative_to(ROOT)
            self.assertTrue(len(rel.parts) == 1 or rel.parts[0] == "src", rel)


if __name__ == "__main__":
    unittest.main()
