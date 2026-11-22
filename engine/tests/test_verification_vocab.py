# -*- coding: utf-8 -*-
"""核验状态词表测试（INFORMATION-VERIFICATION-SPEC v1.0 第二节）。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from verification_vocab import (  # noqa: E402
    CARD_STATUSES,
    INFO_LEVELS,
    SOURCE_STATUSES,
    card_to_source,
    consistency_issue,
    info_level_for,
    is_consistent,
    is_decision_safe,
    normalize_card_status,
    normalize_info_level,
    normalize_source_status,
    source_to_card,
)


class TestNormalize(unittest.TestCase):
    """双语词形归一。"""

    def test_source_status_bilingual(self):
        self.assertEqual(normalize_source_status("verified"), "verified")
        self.assertEqual(normalize_source_status("media_unverified"), "media_unverified")
        self.assertEqual(normalize_source_status("unverifiable"), "unverifiable")
        self.assertEqual(normalize_source_status("已核验"), "verified")
        self.assertEqual(normalize_source_status("部分核验"), "media_unverified")
        self.assertEqual(normalize_source_status("未核验"), "unverifiable")

    def test_source_status_alias(self):
        self.assertEqual(normalize_source_status("已核实"), "verified")
        self.assertEqual(normalize_source_status("无法核实"), "unverifiable")
        self.assertEqual(normalize_source_status("待核实"), "unverifiable")

    def test_source_status_whitespace_tolerated(self):
        self.assertEqual(normalize_source_status(" 已核实 "), "verified")

    def test_source_status_invalid(self):
        for bad in ("", None, "unknown", 123):
            self.assertIsNone(normalize_source_status(bad), bad)

    def test_card_status_bilingual(self):
        self.assertEqual(normalize_card_status("已核验"), "已核验")
        self.assertEqual(normalize_card_status("部分核验"), "部分核验")
        self.assertEqual(normalize_card_status("未核验"), "未核验")
        self.assertEqual(normalize_card_status("verified"), "已核验")
        self.assertEqual(normalize_card_status("media_unverified"), "部分核验")
        self.assertEqual(normalize_card_status("unverifiable"), "未核验")

    def test_cross_mapping(self):
        for en in SOURCE_STATUSES:
            cn = source_to_card(en)
            self.assertIn(cn, CARD_STATUSES)
            self.assertEqual(card_to_source(cn), en)

    def test_canonical_sets(self):
        self.assertEqual(set(SOURCE_STATUSES), {"verified", "media_unverified", "unverifiable"})
        self.assertEqual(set(CARD_STATUSES), {"已核验", "部分核验", "未核验"})
        self.assertEqual(set(INFO_LEVELS), {"已核验事实", "部分核验", "推断", "假设"})


class TestConsistency(unittest.TestCase):
    """跨层一致性（信息等级 ≤ 核验状态上限）。"""

    def test_info_level_ceiling(self):
        self.assertEqual(info_level_for("verified", "source"), "已核验事实")
        self.assertEqual(info_level_for("media_unverified", "source"), "部分核验")
        self.assertEqual(info_level_for("unverifiable", "source"), "假设")
        self.assertEqual(info_level_for("已核验", "card"), "已核验事实")
        self.assertEqual(info_level_for("未核验", "card"), "假设")

    def test_info_level_alias(self):
        # 「已核验」是「已核验事实」的别名（报告 inline 标记 / 历史用词），不另立强度。
        self.assertEqual(normalize_info_level("已核验"), "已核验事实")
        self.assertEqual(normalize_info_level("已核验事实"), "已核验事实")
        self.assertEqual(normalize_info_level("部分核验"), "部分核验")
        self.assertIsNone(normalize_info_level("瞎标"))

    def test_consistent_cases(self):
        self.assertTrue(is_consistent("已核验", "verified", "source"))
        self.assertTrue(is_consistent("已核验事实", "verified", "source"))
        self.assertTrue(is_consistent("部分核验", "media_unverified", "source"))
        self.assertTrue(is_consistent("推断", "media_unverified", "source"))
        self.assertTrue(is_consistent("假设", "unverifiable", "source"))

    def test_inconsistent_cases(self):
        # 部分核验来源不得标已核验（本仓库历史问题 F3-2 同型）
        self.assertFalse(is_consistent("已核验", "media_unverified", "source"))
        # 无法核实来源不得标推断
        self.assertFalse(is_consistent("推断", "unverifiable", "source"))
        self.assertFalse(is_consistent("已核验", "未核验", "card"))

    def test_invalid_inputs_are_inconsistent(self):
        self.assertFalse(is_consistent("已核验", "unknown", "source"))
        self.assertFalse(is_consistent("瞎标", "verified", "source"))

    def test_consistency_issue_message(self):
        msg = consistency_issue("已核验", "media_unverified", "source", where="§1")
        self.assertIsNotNone(msg)
        self.assertIn("部分核验", msg)
        self.assertIsNone(consistency_issue("部分核验", "media_unverified", "source"))


class TestDecisionSafe(unittest.TestCase):
    """决策摘要仅允许已核验 + 部分核验。"""

    def test_safe(self):
        self.assertTrue(is_decision_safe("verified", "source"))
        self.assertTrue(is_decision_safe("media_unverified", "source"))
        self.assertTrue(is_decision_safe("部分核验", "card"))

    def test_unsafe(self):
        self.assertFalse(is_decision_safe("unverifiable", "source"))
        self.assertFalse(is_decision_safe("未核验", "card"))


if __name__ == "__main__":
    unittest.main()
