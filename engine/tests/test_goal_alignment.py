# -*- coding: utf-8 -*-
"""目标对齐 P0 增量测试（IGI 度量 / 滚动 gate-period / 语义门禁 / 词库漂移）。

锁定：
- `gate_period.resolve` 的滚动基线语义（auto = 当前自然月 + 1；显式周期原样；非法回落）；
- `info_gap_metrics.compute` 产出 IGI-01..08 且合成口径自洽；
- `info_density_check` ID-04 只对**结论性**推断/假设判定（提示块与 CSS 注释不误报）；
- `decision_hub_check` 剥离注释后判定（CSS 注释里的「决策卡」不再蒙混过关）；
- `vocab_drift_check` 三类检查可检出（区块不成对 / 空词库 / 规范形未命中）。
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gate_period = _load("gate_period", "engine/tools/gate_period.py")
info_gap = _load("info_gap_metrics", "engine/tools/info_gap_metrics.py")
info_density = _load("info_density_check", "engine/tools/info_density_check.py")
decision_hub = _load("decision_hub_check", "engine/tools/decision_hub_check.py")
vocab_drift = _load("vocab_drift_check", "engine/tools/vocab_drift_check.py")


class TestGatePeriod(unittest.TestCase):
    def test_auto_is_next_month(self):
        self.assertEqual(gate_period.resolve("auto", today=date(2026, 11, 18)), "2026-12")
        self.assertEqual(gate_period.resolve("auto", today=date(2026, 12, 31)), "2027-01")

    def test_explicit_period_passthrough(self):
        for p in ("2026-12", "2026-Q3", "2026", "2026-11-13"):
            self.assertEqual(gate_period.resolve(p, today=date(2026, 11, 18)), p)

    def test_invalid_falls_back_to_rolling(self):
        """非法周期不得让门禁静默失效——回落滚动基线。"""
        self.assertEqual(gate_period.resolve("not-a-period", today=date(2026, 11, 18)), "2026-12")

    def test_none_is_auto(self):
        self.assertEqual(gate_period.resolve(None, today=date(2026, 11, 18)), "2026-12")


class TestInfoGapMetrics(unittest.TestCase):
    def test_compute_returns_eight_metrics(self):
        rep = info_gap.compute(today=date(2026, 11, 18))
        vals = rep["values"]
        for i in range(1, 9):
            self.assertIn(f"IGI-0{i}", vals)
            self.assertGreaterEqual(vals[f"IGI-0{i}"], 0.0)
            self.assertLessEqual(vals[f"IGI-0{i}"], 1.0)

    def test_synthetic_index_is_weighted_gap(self):
        rep = info_gap.compute(today=date(2026, 11, 18))
        vals = rep["values"]
        gap = sum(info_gap.WEIGHTS[m] * (1 - vals[m]) for m in info_gap.WEIGHTS)
        self.assertAlmostEqual(vals["IGI-08"], round(1 - gap, 4), places=4)

    def test_theme_coverage_reflects_actual_state(self):
        """实测口径：当前仅 economy / tech 有业务线 → 2/6。"""
        v, detail = info_gap.igi_01_theme_coverage()
        self.assertEqual(v, round(2 / 6, 4))
        self.assertEqual(set(detail["covered"]), {"economy", "tech"})


class TestInfoDensitySemantics(unittest.TestCase):
    _BASE = ('<h2 class="sec" id="s1">一、决策摘要</h2>{body}'
             '<h2 class="sec" id="s2">二、证据</h2>')

    def test_summary_inference_is_flagged(self):
        body = '<ol><li>判断 X。<span class="lvl lvl-inferred">推断</span> '
        body += '<span class="fact-ref">[FC-IND-001]</span></li></ol>'
        findings = dict(info_density.check_text(self._BASE.format(body=body)))
        self.assertIn("ID-04", findings)

    def test_note_block_and_lamp_are_not_flagged(self):
        """口径提示块与信号灯复用 lvl 类不算摘要越级（防误报）。"""
        body = ('<div class="note">当前信号灯为<span class="lvl lvl-assumption">预校准（ex-ante）</span>。</div>'
                '<ol><li>K13 <span class="lvl lvl-assumption">灰灯</span>。</li></ol>')
        findings = dict(info_density.check_text(self._BASE.format(body=body)))
        self.assertNotIn("ID-04", findings)

    def test_css_comment_does_not_trigger(self):
        """CSS 注释里的「决策卡」等字样不得参与判定。"""
        html = '<style>.lvl-inferred{color:red}/* 决策卡 */</style>' + self._BASE.format(body="<p>x</p>")
        findings = dict(info_density.check_text(html))
        self.assertNotIn("ID-04", findings)

    def test_summary_length_uses_or_not_and(self):
        body = "<p>" + "字" * 950 + "</p>"
        findings = dict(info_density.check_text(self._BASE.format(body=body)))
        self.assertIn("ID-02", findings)


class TestDecisionHubSemantics(unittest.TestCase):
    def test_css_comment_decision_card_does_not_pass(self):
        """trends 周报式陷阱：决策卡只写在 CSS 注释里 → 不得误判为通过。"""
        html = "<style>/* 决策卡 */</style><h2 class=\"sec\">一、本周要点</h2><p>正文</p>"
        findings = decision_hub.check_text(html, "economy/trends")
        # 剥离注释后「决策卡」不再存在 → DC-01 根本不应被触发
        self.assertEqual(findings, [])

    def test_per_card_field_check(self):
        good = ('<div class="decision-card"><div class="dc-grid">'
                '<div><span class="k">结论：</span>A</div>'
                '<div><span class="k">证据强度：</span>强</div>'
                '<div><span class="k">反向证据：</span>B</div></div></div>')
        bad = ('<div class="decision-card"><div class="dc-grid">'
               '<div><span class="k">结论：</span>A</div></div></div>')
        html_good = ('<h3>决策卡</h3>' + good + '<h3>决策卡</h3>' + bad)
        findings = dict(decision_hub.check_text(html_good, ""))
        self.assertIn("DC-01", findings)
        self.assertTrue(any("第 2 张决策卡" in m for m in findings.values()))


class TestVocabDrift(unittest.TestCase):
    def test_pair_issue_detects_mismatch(self):
        """合成用例：BEGIN/END 数量不等必须可检出；当前仓库处于成对状态。"""
        self.assertIsNotNone(vocab_drift.pair_issue("<!-- VOCAB-SYNC:BEGIN topic=x -->"))
        self.assertIsNone(vocab_drift.pair_issue(
            "<!-- VOCAB-SYNC:BEGIN topic=x -->a<!-- VOCAB-SYNC:END -->"))
        self.assertEqual([r for r, _ in vocab_drift.check_sync_blocks()], [])

    def test_empty_theme_detected(self):
        findings = dict(vocab_drift.check_theme_terms())
        self.assertIn("VD-02", findings)

    def test_canonical_form_drift_detected(self):
        findings = dict(vocab_drift.check_canonical_forms())
        self.assertIn("VD-03", findings)

    def test_load_terms_counts_rows(self):
        forms, n = vocab_drift.load_terms("economy")
        self.assertGreater(n, 0)
        self.assertGreaterEqual(len(forms), n)


if __name__ == "__main__":
    unittest.main()
