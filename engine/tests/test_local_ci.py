# -*- coding: utf-8 -*-
"""本地等价 CI（local_ci.py）单元测试。

锁定：检查项登记与运行手册一致、退出码映射、汇总与 JSON / Markdown 输出结构。
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("local_ci", ROOT / "engine" / "tools" / "local_ci.py")
lc = importlib.util.module_from_spec(spec)
sys.modules["local_ci"] = lc
spec.loader.exec_module(lc)

RUNBOOK = ROOT / "engine" / "docs" / "local-ci-runbook.md"


class TestRegistry(unittest.TestCase):
    def test_ids_unique(self):
        ids = [c.id for c in lc.CHECKS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 14)

    def test_runbook_lists_every_check(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        listed = set(re.findall(r"^\| \d+ \| `([a-z0-9_]+)` \|", text, re.M))
        self.assertEqual(listed, {c.id for c in lc.CHECKS})

    def test_remote_only_documented(self):
        text = RUNBOOK.read_text(encoding="utf-8")
        for name, _ in lc.REMOTE_ONLY:
            self.assertIn(f"`{name}`", text)


class TestMapping(unittest.TestCase):
    def test_status_for_exit(self):
        self.assertEqual(lc.status_for_exit(0), "pass")
        self.assertEqual(lc.status_for_exit(2), "warn")
        self.assertEqual(lc.status_for_exit(1), "fail")
        self.assertEqual(lc.status_for_exit(9), "fail")

    def test_overall(self):
        self.assertEqual(lc.overall([]), 0)
        self.assertEqual(lc.overall([{"status": "pass"}]), 0)
        self.assertEqual(lc.overall([{"status": "pass"}, {"status": "warn"}]), 2)
        self.assertEqual(lc.overall([{"status": "warn"}, {"status": "fail"}]), 1)

    def test_select_only_skip(self):
        self.assertEqual([c.id for c in lc.select(lc.CHECKS, "syntax,gate")], ["syntax", "gate"])
        self.assertEqual([c.id for c in lc.select(lc.CHECKS, "", "unittest")][0], "syntax")
        with self.assertRaises(SystemExit):
            lc.select(lc.CHECKS, "nonexistent")


class TestRun(unittest.TestCase):
    def test_run_fast_check(self):
        out = lc.run_check(lc.CHECKS[0], "main")  # syntax
        self.assertEqual(out["status"], "pass", out)
        self.assertEqual(out["id"], "syntax")

    def test_current_branch(self):
        self.assertTrue(lc.current_branch())

    def test_json_document(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = lc.main(["run", "--only", "syntax", "--json"])
        self.assertEqual(code, 0)
        doc = json.loads(buf.getvalue())
        self.assertEqual(doc["schema_version"], lc.SCHEMA_VERSION)
        self.assertEqual(doc["summary"]["total"], 1)
        self.assertEqual(doc["checks"][0]["id"], "syntax")

    def test_markdown_mentions_remote(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            lc.main(["run", "--only", "syntax", "--markdown"])
        text = buf.getvalue()
        self.assertIn("本地等价 CI 结果", text)
        self.assertIn("submit-pr", text)


if __name__ == "__main__":
    unittest.main()
