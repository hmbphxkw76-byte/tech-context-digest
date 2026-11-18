# -*- coding: utf-8 -*-
"""本地 mainline 一键闭环测试（local_mainline）。

锁定复用纪律：只编排，不重写校验；顺序为 plan → unittest → 统一门禁 → push → pr。
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("local_mainline", ROOT / "engine" / "tools" / "local_mainline.py")
lm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lm)


class TestSteps(unittest.TestCase):
    def test_order_and_reuse(self):
        steps = lm.build_steps("demo", "标题", "正文")
        names = [n for n, _ in steps]
        self.assertEqual(names, ["plan", "unittest", "gate", "push", "pr"])
        gate_cmd = steps[2][1]
        self.assertIn("engine/tools/optimization_gate.py", gate_cmd)
        self.assertIn("--probe", gate_cmd)
        # 滚动基线：gate-period 传 auto（不写死周期，避免随时间失效）
        self.assertIn("auto", gate_cmd)
        self.assertIn("engine/tools/repo_sync.py", steps[3][1])
        self.assertIn("engine/tools/repo_sync.py", steps[4][1])

    def test_no_reimplemented_checks(self):
        src = (ROOT / "engine" / "tools" / "local_mainline.py").read_text(encoding="utf-8")
        self.assertNotIn("def run_checks", src)
        self.assertNotIn("def check_thresholds", src)


class TestRun(unittest.TestCase):
    def _fake_run(self, fail_at=None):
        calls = []

        def _run(cmd, cwd=None):
            calls.append(cmd)
            rc = 1 if (fail_at is not None and len(calls) == fail_at) else 0
            return mock.Mock(returncode=rc)

        return _run, calls

    def test_run_all_steps(self):
        _run, calls = self._fake_run()
        with mock.patch.object(lm.subprocess, "run", side_effect=_run):
            rc = lm.run("demo", "标题", "正文")
        self.assertEqual(rc, 0)
        self.assertEqual(len(calls), 5)

    def test_run_stops_on_failure(self):
        _run, calls = self._fake_run(fail_at=3)  # gate 失败
        with mock.patch.object(lm.subprocess, "run", side_effect=_run):
            rc = lm.run("demo", "标题", "正文")
        self.assertEqual(rc, 1)
        self.assertEqual(len(calls), 3)  # push / pr 未执行

    def test_dry_run_executes_nothing(self):
        with mock.patch.object(lm.subprocess, "run") as r:
            rc = lm.run("demo", "标题", "正文", dry_run=True)
        self.assertEqual(rc, 0)
        r.assert_not_called()

    def test_main_cli_dry_run(self):
        # 回归：main() 必须用 add_subparsers（曾误用 add_parser 导致 CLI 崩溃）。
        with mock.patch.object(lm.subprocess, "run") as r, \
             mock.patch.object(sys, "argv", ["local_mainline.py", "run", "--slug", "demo",
                                           "--title", "标题", "--dry-run"]):
            rc = lm.main()
        self.assertEqual(rc, 0)
        r.assert_not_called()


if __name__ == "__main__":
    unittest.main()
