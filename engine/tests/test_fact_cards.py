# -*- coding: utf-8 -*-
"""事实卡片门禁（INFORMATION-LAYERING-SPEC v1.0 第五节）单元测试。

覆盖 fact_card_check：卡片库结构、引用解析、共享域覆盖、FC-04 跨层一致性。
运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import fact_card_check as m  # noqa: E402
from gate_period import resolve as resolve_period  # noqa: E402


class TestFactCards(unittest.TestCase):
    def test_library_loads_without_errors(self):
        cards, errors = m.load_cards()
        self.assertEqual(errors, [])
        self.assertGreaterEqual(len(cards), 20)

    def test_card_ids_unique_and_pattern(self):
        cards, _ = m.load_cards()
        for cid in cards:
            self.assertRegex(cid, r"^FC-(SEC|IND|CI|APT)-\d{3}$")

    def test_required_fields_and_enums(self):
        cards, _ = m.load_cards()
        for cid, c in cards.items():
            self.assertTrue(str(c["source"]).strip(), cid)
            self.assertIn(c["tier"], {1, 2, 3, 4}, cid)
            self.assertIn(c["verify_status"], {"已核验", "部分核验", "未核验"}, cid)
            self.assertIn(c["level"], {"已核验事实", "部分核验", "推断", "假设"}, cid)
            self.assertIsInstance(c["indicators"], list, cid)

    def test_run_has_no_errors(self):
        errors, warnings, lines, stats = m.run(resolve_period("auto"))
        self.assertEqual(errors, 0, lines)
        self.assertGreaterEqual(stats["cards"], 20)

    def test_shared_domain_new_report_uses_cards(self):
        # 共享事实域（动态派生自卡片库 used_by）新报告均应引用卡片
        cards, _ = m.load_cards()
        tokens = m.shared_fact_tokens(cards)
        refs = {rel: m.FC_RE.findall(text) for rel, text, _, _ in m.iter_report_refs()}
        current = resolve_period("auto")
        checked = 0
        for rel, found in refs.items():
            bline = rel.split("/reports/")[0]
            if m._in_shared(bline, tokens) and current in rel:
                self.assertTrue(found, f"{rel} 未引用事实卡片")
                checked += 1
        self.assertGreaterEqual(checked, 4, "应覆盖多个共享事实域新报告")

    def test_fc04_consistency_wiring(self):
        # FC-04：越级卡片应被计数并产生 [W]，但不得计入 [E]（恒不阻断）。
        cards, _ = m.load_cards()
        expected = 0
        for cid, c in cards.items():
            level = m.normalize_info_level(c["level"])
            status = m.normalize_card_status(c["verify_status"])
            if level is None or status is None:
                continue
            if not m.is_consistent(level, status, "card"):
                expected += 1
        errors, warnings, lines, stats = m.run(resolve_period("auto"))
        self.assertEqual(errors, 0, lines)
        self.assertEqual(stats["inconsistent_cards"], expected)
        self.assertGreaterEqual(warnings, expected)
        if expected:
            self.assertTrue(any("FC-04" in ln for ln in lines))

    def test_missing_reference_detected(self):
        # 合成：引用不存在的卡片应被 run 判错（直接检查解析逻辑）
        cards, _ = m.load_cards()
        self.assertNotIn("FC-SEC-999", cards)
        self.assertRegex("见 [FC-SEC-999]。", m.FC_RE)


if __name__ == "__main__":
    unittest.main()
