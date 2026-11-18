# -*- coding: utf-8 -*-
"""发布指纹（publish_fingerprint.py / P2-2）单元测试。"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("publish_fingerprint", ROOT / "engine" / "tools" / "publish_fingerprint.py")
pf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pf)


class TestFingerprint(unittest.TestCase):
    def test_sha256_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.html"
            p.write_text("<html>x</html>", encoding="utf-8")
            self.assertEqual(pf.fingerprint_file(p), pf.fingerprint_file(p))
            self.assertEqual(len(pf.fingerprint_file(p)), 64)

    def test_crlf_normalized_cross_platform(self):
        """CRLF 与 LF 版本必须同指纹（Windows 工作区 / CI 一致性）。"""
        with tempfile.TemporaryDirectory() as d:
            a = Path(d) / "a.html"
            b = Path(d) / "b.html"
            a.write_bytes(b"<html>x</html>\n")
            b.write_bytes(b"<html>x</html>\r\n")
            self.assertEqual(pf.fingerprint_file(a), pf.fingerprint_file(b))

    def test_duplicates_grouping(self):
        fps = {"a.html": "h1", "b.html": "h1", "c.html": "h2"}
        self.assertEqual(pf.duplicates(fps), [["a.html", "b.html"]])

    def test_diff(self):
        store = {"a": "h1", "b": "h2", "c": "h3"}
        current = {"a": "h1", "b": "h9", "d": "h4"}
        d = pf.diff(store, current)
        self.assertEqual(d["new"], ["d"])
        self.assertEqual(d["changed"], ["b"])
        self.assertEqual(d["removed"], ["c"])

    def test_collect_formal_reports(self):
        fps = pf.collect()
        self.assertTrue(fps)
        self.assertTrue(all(len(h) == 64 for h in fps.values()))


class TestStoreRoundtrip(unittest.TestCase):
    def test_emit_and_load(self):
        with tempfile.TemporaryDirectory() as d:
            store = Path(d) / "fps.json"
            store.write_text('{"schema_version": "1.0", "fingerprints": {"a.html": "h1"}}\n',
                             encoding="utf-8")
            self.assertEqual(pf.load_store(store), {"a.html": "h1"})

    def test_load_missing(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(pf.load_store(Path(d) / "none.json"), {})


if __name__ == "__main__":
    unittest.main()
