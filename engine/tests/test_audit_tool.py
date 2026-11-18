# -*- coding: utf-8 -*-
"""审计标准化管理工具（engine/audit/scripts/audit_tool.py）单元测试。"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import re
import tempfile
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
        from _common import iter_business_dirs, iter_business_reports
        reps = audit_tool.collect_reports()
        for b in iter_business_dirs():
            # 已接入但尚未产出报告的业务线（P1-9 四主题就绪化）不参与报告登记校验
            if not iter_business_reports(b):
                continue
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


class TestStaleDetection(unittest.TestCase):
    """P-01：登记路径不存在 = 失效条目（stale）。"""

    def test_stale_paths_detects_missing(self):
        existing = "engine/report-audits/release-calendar.md"
        self.assertTrue((ROOT / existing).exists())
        reps = {existing: {}, "content/does-not-exist.html": {}}
        self.assertEqual(audit_tool.stale_paths(reps), ["content/does-not-exist.html"])

    def test_registry_has_no_stale_after_prune(self):
        reg = audit_tool.load_registry()["reports"]
        self.assertEqual(audit_tool.stale_paths(reg), [])

    def test_prune_is_idempotent(self):
        before = len(audit_tool.load_registry()["reports"])
        self.assertEqual(audit_tool.cmd_prune(None), 0)
        self.assertEqual(audit_tool.cmd_prune(None), 0)
        self.assertEqual(len(audit_tool.load_registry()["reports"]), before)


class TestEvidenceIndex(unittest.TestCase):
    """吸收项 ③：完成前审计证据索引。"""

    REL = "content/economy/dubai/apartment/reports/2026-11_monthly.html"

    def test_build_evidence_keys(self):
        entry = audit_tool.load_registry()["reports"][self.REL]
        ev = audit_tool.build_evidence(self.REL, entry)
        self.assertEqual(ev["report"], self.REL)
        self.assertEqual(ev["business_line"], "content/economy/dubai/apartment")
        self.assertIn("plans", ev)
        self.assertEqual(ev["gate"]["entry"], "engine/tools/optimization_gate.py")
        self.assertTrue((ROOT / ev["audit"]["review"]).exists())
        self.assertIn(ev["audit"]["status"], {"in-review", "audited", "draft", "rejected"})
        self.assertEqual(ev["audit"]["mark_level"], "full")

    def test_registry_entries_have_evidence(self):
        reg = audit_tool.load_registry()["reports"]
        for rel, rec in reg.items():
            self.assertIn("evidence", rec, rel)
            self.assertEqual(rec["evidence"]["report"], rel)

    def test_cmd_evidence_prints_json(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit_tool.cmd_evidence(argparse.Namespace(report=self.REL))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(buf.getvalue())["report"], self.REL)

    def test_cmd_index_idempotent(self):
        before = json.dumps(audit_tool.load_registry()["reports"], sort_keys=True, ensure_ascii=False)
        self.assertEqual(audit_tool.cmd_index(None), 0)
        after = json.dumps(audit_tool.load_registry()["reports"], sort_keys=True, ensure_ascii=False)
        self.assertEqual(before, after)

    def test_plans_linked_via_report_reports_field(self):
        """吸收项 ③：plan.reports 显式关联 → evidence.plans 非空（真实工件驱动，非硬编码）。"""
        rel = "engine/report-audits/mainline-adoption-coverage-matrix.md"
        entry = audit_tool.load_registry()["reports"].get(rel, {})
        ev = audit_tool.build_evidence(rel, entry)
        slugs = [p["slug"] for p in ev["plans"]]
        self.assertIn("fix-alignment", slugs)
        for p in ev["plans"]:
            self.assertIn(rel, p["reports"])


class TestL3Overdue(unittest.TestCase):
    """R3 / L3 SLA：超期检测纯函数（确定性，today 显式注入）。"""

    REL = "content/economy/dubai/apartment/reports/2026-11_monthly.html"

    @staticmethod
    def _write_review(d, rel, reviews):
        slug = re.sub(r"[^A-Za-z0-9]+", "-", rel).strip("-") + ".json"
        (Path(d) / slug).write_text(
            json.dumps({"report": rel, "reviews": reviews}, ensure_ascii=False), encoding="utf-8")

    def test_no_agent_review_and_old_first_seen_is_overdue(self):
        with tempfile.TemporaryDirectory() as d:
            reports = {self.REL: {"category": "report", "first_seen_at": "2026-01-01"}}
            out = audit_tool.l3_overdue(reports, Path(d), today="2026-11-17")
            self.assertEqual(len(out), 1)
            self.assertEqual(out[0]["report"], self.REL)
            self.assertEqual(out[0]["basis"], "first_seen_at")

    def test_recent_agent_review_not_overdue(self):
        with tempfile.TemporaryDirectory() as d:
            self._write_review(d, self.REL, [
                {"stage": "second", "reviewer": "agent", "decision": "pass",
                 "timestamp": "2026-11-10T12:00:00+00:00"},
            ])
            reports = {self.REL: {"category": "report", "first_seen_at": "2026-01-01"}}
            self.assertEqual(audit_tool.l3_overdue(reports, Path(d), today="2026-11-17"), [])

    def test_final_stage_agent_review_counts(self):
        with tempfile.TemporaryDirectory() as d:
            self._write_review(d, self.REL, [
                {"stage": "final", "reviewer": "agent", "decision": "pass",
                 "timestamp": "2026-11-01T12:00:00+00:00"},
            ])
            reports = {self.REL: {"category": "report", "first_seen_at": "2026-01-01"}}
            self.assertEqual(audit_tool.l3_overdue(reports, Path(d), today="2026-11-15"), [])
            out = audit_tool.l3_overdue(reports, Path(d), today="2026-11-16")
            self.assertEqual(len(out), 1)
            self.assertEqual(out[0]["basis"], "review")

    def test_ci_bot_review_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            self._write_review(d, self.REL, [
                {"stage": "second", "reviewer": "ci-bot", "decision": "pass",
                 "timestamp": "2026-11-10T12:00:00+00:00"},
            ])
            reports = {self.REL: {"category": "report", "first_seen_at": "2026-01-01"}}
            out = audit_tool.l3_overdue(reports, Path(d), today="2026-11-17")
            self.assertEqual(len(out), 1)
            self.assertEqual(out[0]["basis"], "first_seen_at")

    def test_non_report_category_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            reports = {self.REL: {"category": "audit-doc", "first_seen_at": "2026-01-01"}}
            self.assertEqual(audit_tool.l3_overdue(reports, Path(d), today="2026-11-17"), [])

    def test_last_appended_agent_review_wins(self):
        # reviews 按时间序追加，最后一条 Agent pass 为基准。
        with tempfile.TemporaryDirectory() as d:
            self._write_review(d, self.REL, [
                {"stage": "final", "reviewer": "agent", "decision": "pass",
                 "timestamp": "2026-11-01T12:00:00+00:00"},
                {"stage": "second", "reviewer": "agent", "decision": "pass",
                 "timestamp": "2026-11-16T12:00:00+00:00"},
            ])
            reports = {self.REL: {"category": "report", "first_seen_at": "2026-01-01"}}
            self.assertEqual(audit_tool.l3_overdue(reports, Path(d), today="2026-11-17"), [])


if __name__ == "__main__":
    unittest.main()
