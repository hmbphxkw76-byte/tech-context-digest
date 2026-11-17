# -*- coding: utf-8 -*-
"""决策交付门禁（DECISION-DELIVERY-SPEC v1.0）单元测试。

覆盖 decision_hub_check：DC-01 决策卡字段、DC-02 行动协议、DC-03 场景切片、DC-04 ex-ante。
运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import decision_hub_check as m  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

HUB_TEXT = """
<h2>决策摘要</h2>
<p>决策卡：结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度。</p>
<div>行动协议：触发条件 + 阈值 + 责任角色 + 时限 + 验证指标。</div>
<div>立即行动 / 持续观察 / 仅记录存档。</div>
<div>场景切片：投资决策 / 就业决策 / 政策制定。</div>
<div>信号灯：预校准（ex-ante）。</div>
"""


class TestDecisionHub(unittest.TestCase):
    def test_hub_text_passes(self):
        self.assertEqual(m.check_text(HUB_TEXT, "content/economy/global/decision-hub"), [])

    def test_decision_card_fields_required(self):
        rules = {r for r, _ in m.check_text("决策卡：结论。", "content/economy/global/decision-hub")}
        self.assertIn("DC-01", rules)

    def test_action_protocol_elements(self):
        text = "可执行启示：触发条件 + 阈值。立即行动 / 持续观察 / 仅记录存档。"
        rules = {r for r, _ in m.check_text(text, "x")}
        self.assertIn("DC-02", rules)

    def test_action_priority_tiers(self):
        text = ("可执行启示：触发条件 + 阈值 + 责任角色 + 时限 + 验证指标。"
                "立即行动。")
        rules = {r for r, _ in m.check_text(text, "x")}
        self.assertIn("DC-02", rules)  # 缺持续观察 / 仅记录存档

    def test_hub_requires_all_three_slices(self):
        text = "场景切片：投资决策。"
        rules = {r for r, _ in m.check_text(text, "content/economy/global/decision-hub")}
        self.assertIn("DC-03", rules)

    def test_business_line_needs_one_slice(self):
        rules = {r for r, _ in m.check_text("场景切片：投资决策。", "content/economy/dubai/apartment")}
        self.assertNotIn("DC-03", rules)
        rules2 = {r for r, _ in m.check_text("场景切片：无。", "content/economy/dubai/apartment")}
        self.assertIn("DC-03", rules2)

    def test_ex_ante_annotation(self):
        rules = {r for r, _ in m.check_text("信号灯判定：红灯。", "x")}
        self.assertIn("DC-04", rules)
        rules2 = {r for r, _ in m.check_text("信号灯判定：预校准（ex-ante）。", "x")}
        self.assertNotIn("DC-04", rules2)

    def test_decision_hub_report_passes(self):
        p = ROOT / "content/economy/global/decision-hub/reports/2026-12_baseline_report.html"
        if not p.exists():
            self.skipTest("decision-hub 报告不存在")
        errors, warnings, lines = m.run(str(p.relative_to(ROOT)), "2026-12")
        self.assertEqual(errors, 0, lines)


class TestModelContract(unittest.TestCase):
    """核心决策模型输出契约：参数区间 + 假设，禁止留白（DECISION-DELIVERY-SPEC 第四节）。"""

    def test_stress_test_outputs_ranges(self):
        import stress_test
        results = stress_test.run_all()
        self.assertTrue(results)
        for r in results:
            self.assertTrue(r.loss_range, r.id)
            for lo, hi in r.loss_range.values():
                self.assertLessEqual(lo, hi)

    def test_valuation_outputs_cap_and_dcf(self):
        import valuation
        cr = valuation.cap_rate(60000, 1000000, {"空置": 2000, "维修": 1000})
        self.assertAlmostEqual(cr.gross_cap, 0.06)
        self.assertAlmostEqual(cr.net_cap, 0.057)
        dcf = valuation.dcf([50000, 52000, 54000], [0.044, 0.044, 0.044])
        self.assertGreater(dcf.npv, 0)
        self.assertEqual(len(dcf.pv_periods), 3)

    def test_unverified_policy_has_no_numeric_multiplier(self):
        import policy_multiplier as pm
        pols = pm.load()
        self.assertTrue(pols)
        for p in pols:
            if p.status != "已核验":
                self.assertIsNone(p.multiplier_low, p.id)
                self.assertIsNone(p.multiplier_high, p.id)


if __name__ == "__main__":
    unittest.main()
