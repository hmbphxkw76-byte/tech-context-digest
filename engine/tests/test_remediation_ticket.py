# -*- coding: utf-8 -*-
"""闭环修正工单测试（remediation_ticket）。

锁定：
- 触发判定（门禁 [E] / 活跃度超阈值）；
- 工单必含「失败项明细 / 责任归属周期 / 可直接执行的复跑命令」；
- 两级 gate-period 在复跑命令中正确渲染；
- 责任周期推导（含回退当前周期）。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "tools" / "remediation_ticket.py"


def _load():
    spec = importlib.util.spec_from_file_location("remediation_ticket", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestRemediationTicket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def test_summarize_extracts_locations_and_key_lines(self):
        out = ("前缀行\n"
               "[ERROR] content/economy/dubai/apartment/reports/2026-11-monthly.html:42 未登记外部 URL\n"
               "尾行\n")
        s = self.mod.summarize(out)
        self.assertIn("content/economy/dubai/apartment/reports/2026-11-monthly.html:42", s["locations"])
        self.assertTrue(any("未登记外部 URL" in l for l in s["summary"]))

    def test_extract_failures_only_errors(self):
        rep = {"checks": [
            {"name": "a", "status": "error", "output": "[ERROR] x\n"},
            {"name": "b", "status": "warn", "output": "[WARN] y\n"},
        ], "errors": 1}
        fs = self.mod.extract_failures(rep)
        self.assertEqual([f["name"] for f in fs], ["a"])

    def test_derive_period_latest(self):
        now = datetime(2026, 11, 15, tzinfo=timezone.utc)
        period, basis = self.mod.derive_period(
            ["见 2026-09 与 2026-12 报告", "另见 2026-Q3"], now)
        self.assertEqual(period, "2026-12")
        self.assertIn("2026-12", basis)

    def test_derive_period_quarter(self):
        now = datetime(2026, 11, 15, tzinfo=timezone.utc)
        period, _ = self.mod.derive_period(["问题在 2026-Q4"], now)
        self.assertEqual(period, "2026-Q4")

    def test_derive_period_fallback(self):
        now = datetime(2026, 11, 15, tzinfo=timezone.utc)
        period, basis = self.mod.derive_period(["无周期标识"], now)
        self.assertEqual(period, "2026-11")  # default_period：非季首月
        self.assertIn("回退", basis)

    def test_check_command_two_level_periods(self):
        c = self.mod.check_command("source_check", "2030-01", "2031-01")
        self.assertIn("2031-01", c)
        self.assertNotIn("__SOURCE_GATE__", c)
        c2 = self.mod.check_command("info_density", "2030-01", "2031-01")
        self.assertIn("2030-01", c2)
        self.assertNotIn("__GATE__", c2)

    def test_render_body_required_sections(self):
        data = {
            "reasons": ["gate-error"],
            "period": "2026-11",
            "period_basis": "测试",
            "gate": {"errors": 1, "warnings": 0,
                     "failures": [{"name": "source_check",
                                   "summary": ["[ERROR] x"], "locations": ["a.html:1"]}]},
            "activity": {"days": None, "threshold": 45, "stale": False},
            "commands": ["python engine/tools/optimization_gate.py --gate-period 2026-12 "
                         "--source-gate-period 2027-01 --probe"],
        }
        body = self.mod.render_body(data)
        for kw in ("## 触发原因", "## 失败项明细", "## 责任归属周期",
                   "## 可直接执行的复跑命令", "## 标准修复流程", "## 闭环要求",
                   "source_check", "a.html:1", "2026-11", "--probe"):
            self.assertIn(kw, body)

    def test_detect_triggered_and_not(self):
        now = datetime(2026, 11, 15, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "gate.json"
            p.write_text(json.dumps(
                {"checks": [{"name": "lint", "status": "error", "output": "[ERROR] 2026-10 x"}],
                 "errors": 1, "warnings": 0}), encoding="utf-8")
            hit = self.mod.detect(str(p), "2026-12", "2027-01", 9999, False, now)
            self.assertTrue(hit["triggered"])
            self.assertIn("gate-error", hit["reasons"])
            self.assertEqual(hit["period"], "2026-10")

            p.write_text(json.dumps({"checks": [], "errors": 0, "warnings": 2}),
                         encoding="utf-8")
            miss = self.mod.detect(str(p), "2026-12", "2027-01", 9999, False, now)
            self.assertFalse(miss["triggered"])
            self.assertEqual(miss["reasons"], [])

    def test_detect_activity_stale(self):
        now = datetime(2026, 11, 15, tzinfo=timezone.utc)
        orig = self.mod.read_activity
        self.mod.read_activity = lambda t: {"days": 50, "threshold": t, "stale": True}
        try:
            with tempfile.TemporaryDirectory() as td:
                p = Path(td) / "g.json"
                p.write_text(json.dumps({"checks": [], "errors": 0, "warnings": 0}),
                             encoding="utf-8")
                d = self.mod.detect(str(p), "2026-12", "2027-01", 45, False, now)
                self.assertTrue(d["triggered"])
                self.assertIn("activity-stale", d["reasons"])
                self.assertIn("50 天", d["body"])
        finally:
            self.mod.read_activity = orig

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "g.json"
            p.write_text(json.dumps(
                {"checks": [{"name": "lint", "status": "error", "output": "[ERROR] x"}],
                 "errors": 1, "warnings": 0}), encoding="utf-8")
            r = subprocess.run([sys.executable, str(TOOL), "detect",
                                "--gate-json", str(p), "--activity-threshold", "9999",
                                "--porcelain"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("triggered=true", r.stdout)

            p.write_text(json.dumps({"checks": [], "errors": 0, "warnings": 0}),
                         encoding="utf-8")
            r2 = subprocess.run([sys.executable, str(TOOL), "detect",
                                 "--gate-json", str(p), "--activity-threshold", "9999",
                                 "--porcelain"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r2.returncode, 2, r2.stdout + r2.stderr)
            self.assertIn("triggered=false", r2.stdout)


if __name__ == "__main__":
    unittest.main()
