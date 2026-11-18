# -*- coding: utf-8 -*-
"""模型契约门禁测试（MODEL-CONTRACT-CHECK v1.0 / DC-07 / P1-13）。"""
from __future__ import annotations

import importlib.util
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


mc = _load("model_contract_check", "engine/tools/model_contract_check.py")


class TestModelContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transmission = _load("transmission", "engine/tools/transmission.py")
        cls.valuation = _load("valuation", "engine/tools/valuation.py")
        cls.stress = _load("stress_test", "engine/tools/stress_test.py")

    def test_no_warnings_on_current_models(self):
        warns = (mc.mc01_transmission(self.transmission)
                 + mc.mc02_stress_elasticities(self.stress)
                 + mc.mc03_stress_scenario(self.stress)
                 + mc.mc04_assumption_metadata(
                     {"transmission": self.transmission, "stress_test": self.stress,
                      "valuation": self.valuation})
                 + mc.mc05_failure_reporting(self.transmission, self.valuation))
        self.assertEqual(warns, [])

    def test_valuation_results_carry_assumptions(self):
        cap = self.valuation.cap_rate(60000.0, 1000000.0, {"物业费": 6000.0})
        self.assertTrue(cap.to_dict()["assumptions"])
        dcf = self.valuation.dcf([50000.0, 52000.0], [0.044, 0.044])
        self.assertTrue(dcf.to_dict()["assumptions"])

    def test_failure_reporting_raises(self):
        with self.assertRaises(Exception):
            self.transmission.estimate_chain("no-such-chain", [])
        with self.assertRaises(Exception):
            self.valuation.cap_rate(100.0, -1.0)
        with self.assertRaises(Exception):
            self.valuation.dcf([1.0, 2.0], [0.1])


if __name__ == "__main__":
    unittest.main()
