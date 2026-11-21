# -*- coding: utf-8 -*-
"""报告周期校验测试（period_check）。

锁定：
- `abs_month` 对月 / 季 / 年 / 周周期的绝对月序换算；
- `run()` 对「落款周期晚于当前自然月」的报告判 [E]，对当期 / 历史放行；
- 默认基准为 `auto`（当前自然月），显式周期可固定口径复现。
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load():
    spec = importlib.util.spec_from_file_location(
        "period_check", ROOT / "engine" / "tools" / "period_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestAbsMonth(unittest.TestCase):
    def test_month(self):
        self.assertEqual(_load().abs_month("2026-11"), 2026 * 12 + 10)

    def test_quarter_anchors_first_month(self):
        self.assertEqual(_load().abs_month("2026-Q3"), 2026 * 12 + 6)

    def test_year_anchors_january(self):
        self.assertEqual(_load().abs_month("2026"), 2026 * 12)

    def test_weekly_uses_calendar_month(self):
        self.assertEqual(_load().abs_month("2026-11-27"), 2026 * 12 + 10)

    def test_invalid_returns_none(self):
        self.assertIsNone(_load().abs_month("not-a-period"))
        self.assertIsNone(_load().abs_month(""))


class TestRun(unittest.TestCase):
    mod = _load()

    def setUp(self):
        self._orig_iter = self.mod.iter_reports

    def tearDown(self):
        self.mod.iter_reports = self._orig_iter

    def _fake(self, rel, cycle, period):
        from _common import ReportRef
        return [ReportRef(rel=rel, business_line="content/x", cycle=cycle,
                          period=period, category="report")]

    def test_future_report_is_error(self):
        self.mod.iter_reports = lambda: self._fake("content/x/reports/2026-12_monthly.html",
                                                  "monthly", "2026-12")
        errors, warnings, lines = self.mod.run("2026-11")
        self.assertEqual(len(errors), 1)
        self.assertIn("2026-12", errors[0])
        self.assertIn("2026-11", errors[0])

    def test_current_and_past_pass(self):
        self.mod.iter_reports = lambda: (
            self._fake("content/x/reports/2026-11_monthly.html", "monthly", "2026-11")
            + self._fake("content/x/reports/2026-Q3_quarterly.html", "quarterly", "2026-Q3")
            + self._fake("content/x/reports/2026_annual.html", "annual", "2026")
        )
        errors, warnings, lines = self.mod.run("2026-11")
        self.assertEqual(errors, [])
        self.assertEqual(lines, [])

    def test_default_basis_is_auto(self):
        self.mod.iter_reports = lambda: []
        errors, _warnings, _lines = self.mod.run()
        self.assertEqual(errors, [])

    def test_unparseable_period_skipped(self):
        self.mod.iter_reports = lambda: self._fake("content/x/reports/weird.html",
                                                  "monthly", "")
        errors, _warnings, _lines = self.mod.run("2026-11")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
