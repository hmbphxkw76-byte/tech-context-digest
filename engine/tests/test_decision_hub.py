# -*- coding: utf-8 -*-
"""决策交付门禁（DECISION-DELIVERY-SPEC v1.0）单元测试。

覆盖 decision_hub_check：DC-01 决策卡字段、DC-02 行动协议、DC-03 场景切片、DC-04 ex-ante、DC-08 证据强度一致性、DC-09 置信度字段。
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
        self.assertEqual(m.check_text(HUB_TEXT, "content/economy/insight"), [])

    def test_decision_card_fields_required(self):
        rules = {r for r, _ in m.check_text("决策卡：结论。", "content/economy/insight")}
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
        rules = {r for r, _ in m.check_text(text, "content/economy/insight")}
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

    @staticmethod
    def _action(threshold):
        return ('可执行启示：触发条件 + 阈值 + 责任角色 + 时限 + 验证指标。'
                '立即行动 / 持续观察 / 仅记录存档。'
                '<div class="a-head"><span class="a-title">t</span></div>'
                '<div class="a-meta"><b>触发条件：</b>x<br>'
                f'<b>阈值：</b>{threshold}<br>'
                '<b>责任角色：</b>y<br><b>时限：</b>2026-12-31<br>'
                '<b>验证指标：</b>z</div>')

    def test_action_threshold_must_be_observable(self):
        """P1-4：阈值须为数值 / 区间 / 日期，定性表述告警。"""
        rules = {r for r, _ in m.check_text(self._action("定性表述"), "x")}
        self.assertIn("DC-02", rules)
        rules2 = {r for r, _ in m.check_text(self._action("≥1 轮 / 2026-12-31 前"), "x")}
        self.assertNotIn("DC-02", rules2)

    def test_decision_hub_report_passes(self):
        p = ROOT / "content/economy/insight/reports/2026-12_baseline_report.html"
        if not p.exists():
            self.skipTest("decision-hub 报告不存在")
        errors, warnings, lines = m.run(str(p.relative_to(ROOT)), "2026-12")
        self.assertEqual(errors, 0, lines)


class TestConfidenceField(unittest.TestCase):
    """DC-09：决策卡 confidence 字段（数值 [0,1] 或 Kent 词表），恒为 [W]。"""

    @staticmethod
    def _card(conf=None):
        conf_html = "" if conf is None else f'<div><span class="k">置信度：</span>{conf}</div>'
        return ('<div class="decision-card">'
                '<div class="dc-head"><span class="dc-title">DC-X-01 · x</span>'
                '<span class="ev-mid">证据强度：中</span></div>'
                '<div class="dc-grid">'
                '<div><span class="k">结论：</span>c</div>'
                '<div><span class="k">反向证据：</span>r</div>'
                f'{conf_html}'
                '</div></div>')

    def test_missing_confidence_warns(self):
        rules = {r for r, _ in m.check_text(self._card(), "content/economy/insight")}
        self.assertIn("DC-09", rules)

    def test_numeric_confidence_ok(self):
        rules = {r for r, _ in m.check_text(self._card("0.55（中）"), "content/economy/insight")}
        self.assertNotIn("DC-09", rules)

    def test_kent_word_confidence_ok(self):
        for word in ("高", "中高", "中", "中低", "低"):
            rules = {r for r, _ in m.check_text(self._card(word), "content/economy/insight")}
            self.assertNotIn("DC-09", rules, word)

    def test_approx_numeric_confidence_ok(self):
        rules = {r for r, _ in m.check_text(self._card("约 0.55"), "content/economy/insight")}
        self.assertNotIn("DC-09", rules)

    def test_invalid_confidence_warns(self):
        for bad in ("约 70%", "1.5", "2", "-0.2", "很高"):
            rules = {r for r, _ in m.check_text(self._card(bad), "content/economy/insight")}
            self.assertIn("DC-09", rules, bad)

    def test_dc09_nonblocking_even_for_new_report(self):
        self.assertEqual(m._level("DC-09", True), "W")
        self.assertEqual(m._level("DC-09", False), "W")
        self.assertEqual(m._level("DC-01", True), "E")
        self.assertEqual(m._level("DC-01", False), "W")


class TestEvidenceStrengthConsistency(unittest.TestCase):
    """DC-08：证据强度由支撑事实卡 level 唯一推导，并与台账交叉校验。"""

    def test_derive_strength_rules(self):
        V = m._VERIFIED
        self.assertEqual(m.derive_strength([]), "")
        self.assertEqual(m.derive_strength([(V, "A"), (V, "B")]), "强")   # 全部已核验 + 双源
        self.assertEqual(m.derive_strength([(V, "A")]), "中")              # 单源不满足双源
        self.assertEqual(m.derive_strength([(V, "A"), ("部分核验", "B")]), "中")
        self.assertEqual(m.derive_strength([(V, "A"), ("推断", "B")]), "弱")
        self.assertEqual(m.derive_strength([("假设", "A")]), "弱")

    @staticmethod
    def _card(strength, src):
        return ('<div class="decision-card">'
                '<div class="dc-head"><span class="dc-title">DC-X-01 · x</span>'
                f'<span class="ev-mid">证据强度：{strength}</span></div>'
                '<div class="dc-grid">'
                '<div><span class="k">结论：</span>c</div>'
                f'<div><span class="k">证据来源：</span>{src}</div>'
                '<div><span class="k">反向证据：</span>r</div>'
                '</div></div>')

    def test_dc08_flags_strength_mismatch(self):
        m._FC_INDEX = {
            "FC-SEC-001": {"card_id": "FC-SEC-001", "level": "部分核验", "source": "A"},
            "FC-SEC-002": {"card_id": "FC-SEC-002", "level": m._VERIFIED, "source": "B"},
        }
        try:
            rules = {r for r, _ in m.dc08_strength(self._card("强", "[FC-SEC-001] [FC-SEC-002]"), {})}
            self.assertIn("DC-08", rules)
        finally:
            m._FC_INDEX = None

    def test_dc08_flags_ledger_mismatch(self):
        m._FC_INDEX = {}
        try:
            rules = {r for r, _ in m.dc08_strength(self._card("中", "无"), {"DC-X-01": "强"})}
            self.assertIn("DC-08", rules)
        finally:
            m._FC_INDEX = None

    def test_dc08_passes_when_consistent(self):
        m._FC_INDEX = {
            "FC-SEC-001": {"card_id": "FC-SEC-001", "level": m._VERIFIED, "source": "A"},
            "FC-SEC-002": {"card_id": "FC-SEC-002", "level": m._VERIFIED, "source": "B"},
        }
        try:
            self.assertEqual(
                m.dc08_strength(self._card("强", "[FC-SEC-001] [FC-SEC-002]"), {"DC-X-01": "强"}), [])
        finally:
            m._FC_INDEX = None


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
