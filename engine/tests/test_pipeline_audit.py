# -*- coding: utf-8 -*-
"""审计运行流水轮转测试（pipeline_audit.rotate）。

锁定：
- 未超阈值不轮转；
- 超阈值时历史完整迁移到 archive/ 且主文件清空；
- 归档只保留最近 keep 份；
- CLI --rotate 可用。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "tools" / "pipeline_audit.py"


def _load():
    spec = importlib.util.spec_from_file_location("pipeline_audit", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pa = _load()


class _AuditFile(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "pipeline_runs.jsonl"
        self.addCleanup(self._tmp.cleanup)

    def _write(self, n: int):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        rows = [{"schema_version": "1.0", "ts": f"2026-11-16T09:00:{i:02d}+00:00",
                 "run_id": f"r{i}"} for i in range(n)]
        self.path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                             encoding="utf-8")


class TestRotate(_AuditFile):
    def test_below_threshold_no_rotation(self):
        self._write(5)
        rep = pa.rotate(max_records=10, path=self.path)
        self.assertFalse(rep["rotated"])
        self.assertEqual(rep["records"], 5)
        self.assertEqual(len(pa.read_all(self.path)), 5)

    def test_over_threshold_archives_and_clears(self):
        self._write(6)
        rep = pa.rotate(max_records=5, path=self.path)
        self.assertTrue(rep["rotated"])
        self.assertEqual(rep["records"], 6)
        self.assertEqual(pa.read_all(self.path), [])
        archive = self.path.parent / "archive" / rep["archived"]
        self.assertTrue(archive.exists())
        self.assertEqual(len(pa.read_all(archive)), 6, "归档必须完整保留历史")

    def test_prunes_old_archives(self):
        archive_dir = self.path.parent / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        for i in range(6):
            (archive_dir / f"pipeline_runs-2026-11-0{i}T00-00-00+00-00.jsonl").write_text(
                "{}\n", encoding="utf-8")
        self._write(6)
        rep = pa.rotate(max_records=5, keep_archives=2, path=self.path)
        remaining = sorted(p.name for p in archive_dir.glob("pipeline_runs-*.jsonl"))
        self.assertEqual(len(remaining), 2, remaining)
        self.assertEqual(len(rep["pruned"]), 5, rep)

    def test_cli_rotate(self):
        self._write(6)
        r = subprocess.run([sys.executable, str(TOOL), "--rotate",
                            "--max-records", "5", "--path", str(self.path)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("rotated\": true", r.stdout, r.stdout)
        self.assertEqual(pa.read_all(self.path), [])


if __name__ == "__main__":
    unittest.main()
