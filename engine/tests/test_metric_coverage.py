# -*- coding: utf-8 -*-
"""指标实测覆盖测试（METRIC-COVERAGE v1.0，批次 B）。

锁定：
- `metric_coverage.measure()` 覆盖字典全部 38 项，且 TOOL 指标全部为 measured / probe；
- 覆盖率报告把未接线项显式列为 gap（不静默跳过）；
- `metric_registry audit --coverage` 输出覆盖与缺口。
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mc = _load("metric_coverage", "engine/tools/metric_coverage.py")


class TestCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.meas = mc.measure()
        cls.rep = mc.coverage_report(cls.meas)

    def test_all_dictionary_metrics_present(self):
        dictionary = json.loads((TOOLS / "metrics-dictionary.json").read_text(encoding="utf-8"))
        ids = {m["metric_id"] for m in dictionary["metrics"]}
        self.assertEqual(set(self.meas), ids)

    def test_tool_metrics_are_measured_or_probe(self):
        dictionary = json.loads((TOOLS / "metrics-dictionary.json").read_text(encoding="utf-8"))
        tool_ids = {m["metric_id"] for m in dictionary["metrics"]
                    if m["detected_by"] == "TOOL"}
        bad = {mid for mid in tool_ids if self.meas[mid]["status"] not in ("measured", "probe")}
        self.assertEqual(bad, set(), f"TOOL 指标未接线：{bad}")

    def test_igi_values_match_info_gap(self):
        ig = _load("info_gap_metrics", "engine/tools/info_gap_metrics.py")
        vals = ig.compute()["values"]
        for mid, v in vals.items():
            self.assertAlmostEqual(self.meas[mid]["value"], v, places=4)

    def test_gaps_are_explicit(self):
        self.assertIn("A-05", self.rep["gaps"])  # 需网络探测
        self.assertTrue(all(self.meas[mid]["status"] in ("fallback", "probe")
                            for mid in self.rep["gaps"]))

    def test_llm_metrics_are_not_faked(self):
        dictionary = json.loads((TOOLS / "metrics-dictionary.json").read_text(encoding="utf-8"))
        llm_ids = {m["metric_id"] for m in dictionary["metrics"] if m["detected_by"] == "LLM"}
        for mid in llm_ids:
            self.assertEqual(self.meas[mid]["status"], "llm")
            self.assertIsNone(self.meas[mid]["value"])

    def test_audit_coverage_cli(self):
        r = subprocess.run([sys.executable, "engine/tools/metric_registry.py",
                            "audit", "--coverage"], cwd=ROOT, capture_output=True, text=True)
        self.assertIn("[coverage]", r.stdout)
        self.assertIn("[gap]", r.stdout)


if __name__ == "__main__":
    unittest.main()
