# -*- coding: utf-8 -*-
"""工作区标准化清理测试（WORKSPACE-CLEANUP v1.0）。

锁定：
- 缓存 / 临时 / 构建产物被清除，普通文件保留；
- **受 git 跟踪的路径一律跳过**（安全硬性约束）；
- dry-run 不删、verify 有残留即 exit 1；
- 输出确定性（重复执行一致）；
- --deep 才清理虚拟环境。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "tools" / "workspace_cleanup.py"


def _load():
    spec = importlib.util.spec_from_file_location("workspace_cleanup", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wc = _load()


class _Workspace(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _make(self, rel: str, content: str = "x") -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def _git_track(self, rel: str):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True,
                       capture_output=True)
        subprocess.run(["git", "add", "--", rel], cwd=self.root, check=True,
                       capture_output=True)


class TestCleanRemovesJunk(_Workspace):
    def test_removes_cache_temp_and_build(self):
        self._make("__pycache__/a.pyc")
        self._make("engine/__pycache__/b.pyc")
        self._make(".pytest_cache/CACHEDIR.TAG")
        self._make(".automation-tmp/remediation.json")
        self._make(".screenshots/a.png")
        self._make("build/out.bin")
        self._make("dist/pkg.tar")
        self._make("report.html.tmp")
        self._make("engine/tools/.coverage")
        self._make("engine/tools/keep.py", "print('keep')")

        rep = wc.clean(self.root)
        self.assertEqual(rep["failed"], [])
        self.assertTrue((self.root / "engine/tools/keep.py").exists())
        self.assertFalse((self.root / "__pycache__").exists())
        self.assertFalse((self.root / ".automation-tmp").exists())
        self.assertFalse((self.root / "build").exists())
        self.assertFalse((self.root / "report.html.tmp").exists())
        self.assertFalse((self.root / "engine/tools/.coverage").exists())

    def test_deep_removes_venv_only_when_requested(self):
        self._make(".venv/Lib/site-packages/x")
        shallow = wc.clean(self.root, deep=False)
        self.assertEqual(shallow["removed"], 0)
        self.assertTrue((self.root / ".venv").exists())
        deep = wc.clean(self.root, deep=True)
        self.assertGreaterEqual(deep["removed"], 1)
        self.assertFalse((self.root / ".venv").exists())

    def test_idempotent(self):
        self._make("__pycache__/a.pyc")
        first = wc.clean(self.root)
        second = wc.clean(self.root)
        self.assertEqual(first["removed"], 1)
        self.assertEqual(second["removed"], 0)

    def test_dry_run_removes_nothing(self):
        self._make("__pycache__/a.pyc")
        rep = wc.clean(self.root, dry_run=True)
        self.assertEqual(rep["removed"], 1)
        self.assertTrue((self.root / "__pycache__").exists())


class TestTrackedProtection(_Workspace):
    def test_tracked_file_matching_junk_suffix_is_kept(self):
        self._make("keep.pyc")
        self._make("__pycache__/junk.pyc")
        self._git_track("keep.pyc")

        rep = wc.clean(self.root)
        self.assertTrue((self.root / "keep.pyc").exists(), "受跟踪文件被误删")
        self.assertFalse((self.root / "__pycache__").exists())
        self.assertNotIn("keep.pyc", rep["targets"])

    def test_tracked_file_inside_junk_named_dir_is_kept(self):
        # 极端情形：被跟踪文件位于名为 build 的目录内 → 整个目录跳过
        self._make("build/keep.txt")
        self._git_track("build/keep.txt")
        wc.clean(self.root)
        self.assertTrue((self.root / "build" / "keep.txt").exists())


class TestVerifyAndCli(_Workspace):
    def test_verify_detects_residue(self):
        self._make("__pycache__/a.pyc")
        r = subprocess.run([sys.executable, str(TOOL), "--mode", "verify",
                            "--root", str(self.root)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("残留", r.stdout)

    def test_verify_clean_workspace_passes(self):
        self._make("keep.py")
        r = subprocess.run([sys.executable, str(TOOL), "--mode", "verify",
                            "--root", str(self.root)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_cli_clean_and_json_deterministic(self):
        self._make("__pycache__/a.pyc")
        self._make(".automation-tmp/b.json")
        r1 = subprocess.run([sys.executable, str(TOOL), "--json", "--root", str(self.root)],
                            capture_output=True, text=True)
        self.assertEqual(r1.returncode, 0, r1.stderr)
        # 幂等：第二次应无残留可清
        r2 = subprocess.run([sys.executable, str(TOOL), "--json", "--root", str(self.root)],
                            capture_output=True, text=True)
        self.assertIn('"removed": 0', r2.stdout)

    def test_cli_missing_root_errors(self):
        r = subprocess.run([sys.executable, str(TOOL), "--root", str(self.root / "nope")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
