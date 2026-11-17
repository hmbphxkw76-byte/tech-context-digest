# -*- coding: utf-8 -*-
"""发布日历结构化采集（release_calendar.py / P1-2）单元测试。"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("release_calendar", ROOT / "engine" / "tools" / "release_calendar.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


class TestParse(unittest.TestCase):
    def test_rows_parsed(self):
        rows = rc.parse_calendar()
        self.assertTrue(rows)
        self.assertIn("来源", rows[0])
        self.assertIn("下次预期窗口", rows[0])

    def test_header_stable(self):
        rows = rc.parse_calendar()
        keys = set(rows[0])
        for k in ("来源", "指标", "频率", "滞后", "下次预期窗口", "入库期限", "责任人"):
            self.assertIn(k, keys)


class TestWindow(unittest.TestCase):
    def test_iso_window(self):
        w = rc.classify_window({"下次预期窗口": "2027-09"})
        self.assertEqual(w["kind"], "iso")
        self.assertEqual(w["date"], "2027-09")

    def test_year_window(self):
        w = rc.classify_window({"下次预期窗口": "2027"})
        self.assertEqual(w["kind"], "year")

    def test_relative_window(self):
        w = rc.classify_window({"下次预期窗口": "次月第 4 周"})
        self.assertEqual(w["kind"], "relative")
        self.assertEqual(w["date"], "")


class TestCoverage(unittest.TestCase):
    def test_p0_coverage_full(self):
        cov = rc.coverage(rc.parse_calendar())
        self.assertEqual(cov["p0_coverage"], 1.0)
        self.assertEqual(cov["field_complete_rate"], 1.0)

    def test_missing_dimension_reported(self):
        cov = rc.coverage([{"来源": "X", "指标": "Y", "频率": "月度",
                            "下次预期窗口": "次月", "入库期限": "5 日"}])
        self.assertTrue(cov["missing_p0"])


class TestDeterminism(unittest.TestCase):
    def test_document_has_no_timestamp(self):
        doc = rc.build_document(rc.parse_calendar())
        text = str(doc)
        self.assertNotIn("2026-11-15T", text)
        self.assertEqual(doc, rc.build_document(rc.parse_calendar()))


if __name__ == "__main__":
    unittest.main()
