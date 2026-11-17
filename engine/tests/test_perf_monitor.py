# -*- coding: utf-8 -*-
"""性能监控与缓存（perf_monitor / T6）单元测试。"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("perf_monitor", ROOT / "engine" / "tools" / "perf_monitor.py")
pm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)


class TestThresholds(unittest.TestCase):
    def _payload(self, p95=2546.0, single=247.0, err=0.0, strict_p95=81521.0):
        return {
            "thresholds": {"l0_l1_full_p95_ms": 60000.0, "single_report_l1_avg_ms": 2000.0,
                           "audit_strict_p95_ms": 180000.0, "error_rate_max": 0.0},
            "scenarios": [
                {"id": "l0_l1_full", "wall_ms": {"p95": p95}, "error_rate": err},
                {"id": "single_report_l1", "wall_ms": {"avg": single}, "error_rate": 0.0},
                {"id": "audit_run_strict", "wall_ms": {"p95": strict_p95}, "error_rate": 0.0},
            ],
        }

    def test_pass(self):
        self.assertEqual(pm.check_thresholds(self._payload()), [])

    def test_p95_exceeds(self):
        f = pm.check_thresholds(self._payload(p95=70000.0))
        self.assertTrue(any("P95" in x["message"] for x in f))

    def test_error_rate_exceeds(self):
        f = pm.check_thresholds(self._payload(err=0.02))
        self.assertTrue(any("错误率" in x["message"] for x in f))

    def test_audit_strict_p95_exceeds(self):
        """P-03：strict 审计 P95 超阈值 → P0。"""
        f = pm.check_thresholds(self._payload(strict_p95=181000.0))
        self.assertTrue(any("strict 审计" in x["message"] and x["level"] == "P0" for x in f), f)

    def test_audit_strict_threshold_declared_in_status(self):
        """perf-status.json 必须声明 audit_strict_p95_ms 阈值。"""
        import json
        th = json.loads((ROOT / "perf-status.json").read_text(encoding="utf-8"))["thresholds"]
        self.assertIn("audit_strict_p95_ms", th)
        self.assertLessEqual(th["audit_strict_p95_ms"], 180000.0)


class TestUpdateAndCache(unittest.TestCase):
    def test_update_scenario(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "perf.json"
            pm.save_status({"schema_version": "1.0", "scenarios": [], "thresholds": {}}, p)
            pm.update_scenario("x", {"wall_ms": {"avg": 10.0}}, p)
            self.assertEqual(pm.load_status(p)["scenarios"][0]["wall_ms"]["avg"], 10.0)

    def test_cache_hit_and_invalidation(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "r.html"
            f.write_text("v1", encoding="utf-8")
            c = pm.ResultCache(cache_dir=Path(d) / "cache")
            c.set("k", f, "cached")
            self.assertEqual(c.get("k", f), "cached")
            f.write_text("v2", encoding="utf-8")
            self.assertIsNone(c.get("k", f))


if __name__ == "__main__":
    unittest.main()
