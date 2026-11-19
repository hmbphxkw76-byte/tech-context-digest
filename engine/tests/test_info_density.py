# -*- coding: utf-8 -*-
"""信息密度与分层交付门禁（INFORMATION-LAYERING-SPEC v1.0）单元测试。

覆盖 info_density_check：ID-01–ID-08、DC-05 判定，周期比较，共享事实域规则。
运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import info_density_check as m  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

GOOD = """
<html><body>
<h2 class="sec" id="s1">一、决策摘要</h2>
<p>本期读数时点：2026-11-15。<span class="lvl lvl-verified">已核验</span></p>
<div class="delta-strip" data-module="delta">
  <div class="d add"><div class="n">3</div><div class="l">本期新增</div></div>
  <div class="d fix"><div class="n">0</div><div class="l">修正</div></div>
  <div class="d same"><div class="n">12</div><div class="l">无变化</div></div>
  <div class="d hyp"><div class="n">4/15</div><div class="l">假设核验进度</div></div>
</div>
<p>场景切片：主场景 投资决策；次场景 政策制定。</p>
<p>指标指针：K01、RL-01。</p>
</body></html>
"""


class TestInfoDensity(unittest.TestCase):
    def test_good_report_has_no_findings(self):
        self.assertEqual(m.check_text(GOOD), [])

    def test_missing_summary_flagged(self):
        text = "<h2 class='sec'>一、指标台账</h2><p>本期新增 1 条。</p>"
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("ID-01", rules)

    def test_missing_delta_module_flagged(self):
        text = ("<h2 class='sec'>一、决策摘要</h2><p>已核验</p>"
                "<p>场景切片：投资决策。</p>")
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("ID-05", rules)

    def test_missing_level_annotation_flagged(self):
        text = ('<h2 class="sec">一、决策摘要</h2>'
                '<p>本期新增 1 条；修正 0 条；无变化 1 条；核验进度 1/2。</p>'
                '<p>场景切片：投资决策。</p>')
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("ID-03", rules)

    def test_assumption_product_without_interval_flagged(self):
        text = ('<h2 class="sec">一、决策摘要</h2>'
                '<p>规模 52.5 亿（假设乘积）。</p>'
                '<p>本期新增 1 条；修正 0 条；无变化 1 条；核验进度 1/2。</p>'
                '<p>场景切片：投资决策。</p>')
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("ID-04", rules)

    def test_assumption_product_with_interval_passes(self):
        text = ('<h2 class="sec">一、决策摘要</h2>'
                '<p>规模区间 50–55 亿（假设乘积，区间）。</p>'
                '<p>本期新增 1 条；修正 0 条；无变化 1 条；核验进度 1/2。</p>'
                '<p>场景切片：投资决策。</p>')
        rules = {r for r, _ in m.check_text(text)}
        self.assertNotIn("ID-04", rules)

    def test_self_computed_without_label_flagged(self):
        """P1-3：摘要内的自算 / 机制自算值未标「假设乘积 + 区间」须告警。"""
        text = ('<h2 class="sec">一、决策摘要</h2>'
                '<p>月供由 10,447 升至 10,992（机制自算）。</p>'
                '<p>本期新增 1 条；修正 0 条；无变化 1 条；核验进度 1/2。</p>'
                '<p>场景切片：投资决策。</p>')
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("ID-04", rules)

    def test_self_computed_with_label_passes(self):
        text = ('<h2 class="sec">一、决策摘要</h2>'
                '<p>月供区间 10,447–10,992（假设乘积，区间）。</p>'
                '<p>本期新增 1 条；修正 0 条；无变化 1 条；核验进度 1/2。</p>'
                '<p>场景切片：投资决策。</p>')
        rules = {r for r, _ in m.check_text(text)}
        self.assertNotIn("ID-04", rules)

    def test_shared_domain_requires_fact_card(self):
        text = ("<h2 class='sec'>一、决策摘要</h2><p>已核验</p>"
                "<p>本期新增 1 / 修正 0 / 无变化 1 / 假设核验进度 1/2。</p>"
                "<p>场景切片：投资决策。</p>")
        rules = {r for r, _ in m.check_text(text, "content/tech/security/dubai")}
        self.assertIn("ID-07", rules)
        rules2 = {r for r, _ in m.check_text(text, "content/economy/dubai/apartment")}
        self.assertNotIn("ID-07", rules2)

    def test_reading_time_for_verification_run(self):
        text = ("<h2 class='sec'>一、决策摘要</h2><p>已核验</p>"
                "<p>本期为核验 / 收敛型运行。</p>"
                "<p>本期新增 1 / 修正 0 / 无变化 1 / 假设核验进度 1/2。</p>"
                "<p>场景切片：投资决策。</p>")
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("DC-05", rules)

    def test_boilerplate_copy_flagged(self):
        text = ("<h2 class='sec'>一、决策摘要</h2><p>已核验</p>"
                "<p>① 官方一手 ② 行业机构 ③ 挂牌门户 ④ 媒体转述</p>"
                "<p>本期新增 1 / 修正 0 / 无变化 1 / 假设核验进度 1/2。</p>"
                "<p>场景切片：投资决策。</p>")
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("ID-01", rules)

    def test_period_key_ordering(self):
        k = m._period_key
        self.assertLess(k("2026-11"), k("2026-12"))
        self.assertLess(k("2026-Q3"), k("2026-12"))
        self.assertLess(k("2026-11-13"), k("2026-12"))
        self.assertGreaterEqual(k("2026-12-01"), k("2026-12"))

    def test_decision_hub_report_passes(self):
        p = ROOT / "content/economy/insight/reports/2026-12_baseline_report.html"
        if not p.exists():
            self.skipTest("decision-hub 报告不存在")
        errors, warnings, lines = m.run(str(p.relative_to(ROOT)), "2026-12")
        self.assertEqual(errors, 0, lines)


class TestId02RollingGate(unittest.TestCase):
    """P1-4：ID-02 由 WARN_ONLY 改为滚动 gate-period（新报告 [E] / 历史 [W]）。"""

    @staticmethod
    def _long_summary() -> str:
        return ("<h2 class=\"sec\">一、决策摘要</h2>"
                "<p><span class=\"lvl lvl-verified\">已核验</span> "
                "本期新增 1；修正 0；无变化 1；假设核验进度 1/2。"
                "场景切片：投资决策。指标指针：K01。</p>"
                "<p>" + "填充" * 500 + "</p>")

    def test_id02_not_warn_only(self):
        self.assertNotIn("ID-02", m._WARN_ONLY)
        self.assertEqual(m._level_for("ID-02", True), "E")
        self.assertEqual(m._level_for("ID-02", False), "W")

    def test_id06_stays_warn_only(self):
        self.assertIn("ID-06", m._WARN_ONLY)
        self.assertEqual(m._level_for("ID-06", True), "W")

    def test_long_summary_flagged(self):
        rules = {r for r, _ in m.check_text(self._long_summary())}
        self.assertIn("ID-02", rules)

    def test_new_report_error_historical_warning(self):
        text = self._long_summary()
        with mock.patch.object(m, "iter_targets",
                               return_value=[("x.html", text, "2026-12", "")]):
            errors, warnings, lines = m.run(None, "2026-12")
        self.assertEqual(errors, 1, lines)
        self.assertIn("ID-02", " ".join(lines))
        with mock.patch.object(m, "iter_targets",
                               return_value=[("x.html", text, "2026-11", "")]):
            errors, warnings, lines = m.run(None, "2026-12")
        self.assertEqual(errors, 0, lines)
        self.assertEqual(warnings, 1, lines)


if __name__ == "__main__":
    unittest.main()
