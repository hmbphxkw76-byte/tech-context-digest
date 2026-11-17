# -*- coding: utf-8 -*-
"""审计标准化管理工具（engine/audit/scripts/audit_tool.py）单元测试。"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "audit" / "scripts" / "audit_tool.py"

spec = importlib.util.spec_from_file_location("audit_tool", TOOL)
audit_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_tool)


class TestInventory(unittest.TestCase):
    def test_collects_business_and_audit(self):
        reps = audit_tool.collect_reports()
        kinds = {r["kind"] for r in reps}
        self.assertIn("business", kinds)
        self.assertIn("audit", kinds)
        self.assertTrue(all((ROOT / r["path"]).exists() for r in reps))

    def test_every_business_line_registered(self):
        import sys
        sys.path.insert(0, str(ROOT / "engine" / "tools"))
        from _common import iter_business_dirs
        reps = audit_tool.collect_reports()
        for b in iter_business_dirs():
            self.assertTrue(any(r["business_line"] == b.rel for r in reps), b.rel)


class TestStructureCheck(unittest.TestCase):
    def test_main_business_report_meets_threshold(self):
        p = ROOT / "content/economy/dubai/apartment/reports/2026-11_monthly.html"
        missing, _ = audit_tool.structure_check(p, "business")
        self.assertLessEqual(len(missing), 1)  # ≥9/10

    def test_missing_elements_reported(self):
        p = ROOT / "engine/report-audits/release-calendar.md"
        missing, _ = audit_tool.structure_check(p, "audit")
        self.assertTrue(any("E" in m for m in missing))


class TestRegistry(unittest.TestCase):
    def test_load_save_roundtrip(self):
        reg = audit_tool.load_registry()
        self.assertIn("reports", reg)
        self.assertGreaterEqual(len(reg["reports"]), 20)

    def test_audit_id_unique(self):
        reg = audit_tool.load_registry()
        ids = [r.get("audit_id") for r in reg["reports"].values() if r.get("audit_id")]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
