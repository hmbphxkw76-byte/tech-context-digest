# -*- coding: utf-8 -*-
"""报告层信息核验门禁测试（INFORMATION-VERIFICATION-SPEC v1.0 报告层一致性）。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from report_verification_check import (  # noqa: E402
    _decision_blocks,
    _norm_url,
    iter_report_units,
    run,
)

GATE = "2026-11"
SRC = {
    "verified.example.com/a": [("verified", "content/x/y", "S-1")],
    "media.example.com/b": [("media_unverified", "content/x/y", "S-2")],
    "unver.example.com/c": [("unverifiable", "content/x/y", "S-3")],
}


def _report(period: str, body: str) -> list[tuple[str, str, str]]:
    return [(f"content/x/y/reports/{period}_monthly.html", period, body)]


class TestHelpers(unittest.TestCase):
    def test_norm_url(self):
        self.assertEqual(_norm_url("HTTPS://WWW.Example.com/a/"),
                         "example.com/a")
        self.assertEqual(_norm_url(""), "")

    def test_decision_blocks_nested_div(self):
        text = ('<div class="decision-summary"><h3>决策摘要</h3><ul>'
                '<li><span class="lvl lvl-verified">已核验</span>x</li>'
                '</ul></div><p>after</p>')
        spans = _decision_blocks(text)
        self.assertEqual(len(spans), 1)
        self.assertIn("决策摘要", text[spans[0][0]:spans[0][1]])
        self.assertNotIn("after", text[spans[0][0]:spans[0][1]])

    def test_units_exclude_generic_div(self):
        text = ('<div class="tblwrap"><tr><td><span class="lvl lvl-verified">已核验</span>'
                '</td></tr></div>')
        units = iter_report_units(text)
        self.assertEqual(len(units), 1)
        self.assertIn("<tr", units[0][0])


class TestRV01DecisionSummary(unittest.TestCase):
    def test_inferred_in_decision_summary_is_error(self):
        body = ('<div class="decision-summary"><ul><li>'
                '<span class="lvl lvl-inferred">推断</span>结论</li></ul></div>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)
        self.assertTrue(any("RV-01" in x for x in lines))

    def test_unverifiable_link_in_decision_summary_is_error(self):
        body = ('<div class="decision-summary"><ul><li>'
                '<span class="lvl lvl-verified">已核验</span>'
                '<a href="https://unver.example.com/c">来源</a></li></ul></div>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        # RV-01（决策摘要纯净）与 RV-02（未核验呈现）同时命中，均为真实违规。
        self.assertEqual(errors, 2)
        self.assertTrue(any("RV-01" in x for x in lines))
        self.assertTrue(any("RV-02" in x for x in lines))

    def test_clean_decision_summary_passes(self):
        body = ('<div class="decision-summary"><ul><li>'
                '<span class="lvl lvl-verified">已核验</span>'
                '<a href="https://verified.example.com/a">来源</a></li></ul></div>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 0)


class TestRV02UnverifiedPresentation(unittest.TestCase):
    def test_verified_claim_on_unverifiable_source(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '<a href="https://unver.example.com/c">来源</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)
        self.assertTrue(any("RV-02" in x for x in lines))

    def test_verified_claim_on_media_source_only(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '<a href="https://media.example.com/b">来源</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)
        self.assertTrue(any("RV-02" in x for x in lines))

    def test_verified_claim_with_verified_source_passes(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '<a href="https://verified.example.com/a">来源</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 0)

    def test_partial_claim_on_media_source_passes(self):
        body = ('<tr><td><span class="lvl lvl-partial">部分核验</span>'
                '<a href="https://media.example.com/b">来源</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 0)

    def test_partial_claim_on_unverifiable_source_is_error(self):
        body = ('<tr><td><span class="lvl lvl-partial">部分核验</span>'
                '<a href="https://unver.example.com/c">来源</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)

    def test_unverifiable_link_with_verified_backstop_passes(self):
        """单元内同时有已核验来源支撑时，不判不一致（避免误报）。"""
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '<a href="https://verified.example.com/a">A</a>'
                '<a href="https://unver.example.com/c">B</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 0)


class TestRV03StatusText(unittest.TestCase):
    def test_unverified_text_with_verified_level(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '机构 · 2026Q3 · 未核验</td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)
        self.assertTrue(any("RV-03" in x for x in lines))

    def test_partial_text_with_verified_level(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '机构 · 2026Q3 · 部分核验</td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)

    def test_matching_text_passes(self):
        body = ('<tr><td><span class="lvl lvl-partial">部分核验</span>'
                '机构 · 2026Q3 · 部分核验</td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-11", body))
        self.assertEqual(errors, 0)


class TestGatePeriod(unittest.TestCase):
    def test_historical_report_is_warning(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '<a href="https://unver.example.com/c">来源</a></td></tr>')
        errors, warnings, lines, _ = run(GATE, SRC, _report("2026-10", body))
        self.assertEqual(errors, 0)
        self.assertEqual(warnings, 1)
        self.assertTrue(any("历史不追溯" in x for x in lines))

    def test_period_boundary(self):
        body = ('<tr><td><span class="lvl lvl-verified">已核验</span>'
                '<a href="https://unver.example.com/c">来源</a></td></tr>')
        errors, _, _, _ = run("2026-11", SRC, _report("2026-11", body))
        self.assertEqual(errors, 1)
        errors, _, _, _ = run("2026-12", SRC, _report("2026-11", body))
        self.assertEqual(errors, 0)


if __name__ == "__main__":
    unittest.main()
