# -*- coding: utf-8 -*-
"""静态检查适配层测试（static_check / Phase 3.1）。

锁定退出码语义：0 干净；2 非阻断发现（warn）；1 执行错误；工具缺失 → 2。
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "engine" / "tools" / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sc = _load("static_check", "static_check.py")


class TestStaticCheckExitCodes(unittest.TestCase):
    def test_clean_is_zero(self):
        with mock.patch.object(sc.shutil, "which", return_value="ruff"), \
             mock.patch.object(sc.subprocess, "run",
                               return_value=mock.Mock(returncode=0, stdout="", stderr="")):
            self.assertEqual(sc.ruff(), 0)

    def test_findings_are_warn(self):
        with mock.patch.object(sc.shutil, "which", return_value="ruff"), \
             mock.patch.object(sc.subprocess, "run",
                               return_value=mock.Mock(returncode=1, stdout="finding", stderr="")):
            self.assertEqual(sc.ruff(), 2)

    def test_missing_tool_is_warn(self):
        with mock.patch.object(sc.shutil, "which", return_value=None):
            self.assertEqual(sc.ruff(), 2)

    def test_execution_error_is_error(self):
        with mock.patch.object(sc.shutil, "which", return_value="ruff"), \
             mock.patch.object(sc.subprocess, "run",
                               return_value=mock.Mock(returncode=2, stdout="", stderr="boom")):
            self.assertEqual(sc.ruff(), 1)

    def test_mypy_missing_module_is_warn(self):
        with mock.patch.object(sc.subprocess, "run",
                               return_value=mock.Mock(returncode=1, stdout="No module named mypy", stderr="")):
            self.assertEqual(sc.mypy(), 2)

    def test_mypy_findings_are_warn(self):
        with mock.patch.object(sc.subprocess, "run",
                               return_value=mock.Mock(returncode=1, stdout="error: x", stderr="")):
            self.assertEqual(sc.mypy(), 2)


class TestGateWiring(unittest.TestCase):
    def test_gate_includes_static_checks(self):
        mod = _load("optimization_gate", "optimization_gate.py")
        names = [c[0] for c in mod.CHECKS]
        self.assertIn("ruff", names)
        self.assertIn("mypy", names)
        self.assertIn("monitoring_render", names)
        self.assertIn("prompt_consistency", names)
        self.assertIn("model_contract", names)
        self.assertIn("verification_ledger", names)
        self.assertEqual(len(names), 31)
        warn_ok = {n: w for n, _c, w in mod.CHECKS}
        self.assertTrue(warn_ok["ruff"])
        self.assertTrue(warn_ok["mypy"])


if __name__ == "__main__":
    unittest.main()
