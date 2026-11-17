# -*- coding: utf-8 -*-
"""自动化状态记录测试（automation_status）。

锁定：占位 / 本机 URL 不得写入状态文件，避免假记录污染活跃度统计。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "tools" / "automation_status.py"


def _load():
    spec = importlib.util.spec_from_file_location("automation_status", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPlaceholderGuard(unittest.TestCase):
    def setUp(self):
        self.pa = _load()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_file = Path(self._tmp.name) / "automation-status.json"
        self.pa.STATUS_FILE = self.tmp_file

    def test_detects_placeholder_hosts(self):
        for u in ("https://example.local/run/1", "http://localhost/x",
                  "http://127.0.0.1/run", "https://example.com/a"):
            self.assertTrue(self.pa.is_placeholder_url(u), u)
        for u in ("https://github.com/o/r/actions/runs/1", ""):
            self.assertFalse(self.pa.is_placeholder_url(u), u)

    def test_record_skips_placeholder(self):
        rc = self.pa.record("maintenance", "failure", "https://example.local/run/1")
        self.assertEqual(rc, 0)
        self.assertFalse(self.tmp_file.exists(), "占位记录不应落盘")

    def test_record_accepts_real_url(self):
        url = "https://github.com/o/r/actions/runs/1"
        self.pa.record("maintenance", "success", url)
        data = json.loads(self.tmp_file.read_text(encoding="utf-8"))
        self.assertEqual(data["records"][-1]["run_url"], url)
        self.assertEqual(data["records"][-1]["phase"], "maintenance")


if __name__ == "__main__":
    unittest.main()
