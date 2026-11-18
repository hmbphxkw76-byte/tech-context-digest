# -*- coding: utf-8 -*-
"""main 首亲历史直推审计（git_history_audit）单元测试。

覆盖：合并放行、PR 引用放行、CI 留痕放行、历史白名单放行、直推违规识别、
max_commits 边界与 CLI 退出码。测试在临时 git 仓库中进行，不依赖真实 main 历史。
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location(
    "git_history_audit", ROOT / "engine" / "tools" / "git_history_audit.py"
)
gha = importlib.util.module_from_spec(spec)
sys.modules["git_history_audit"] = gha
spec.loader.exec_module(gha)


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8"
    )
    if proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} 失败：{proc.stderr}")
    return proc.stdout.strip()


class _TempRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        _git(self.repo, "init", "-q")
        _git(self.repo, "checkout", "-q", "-b", "main")
        _git(self.repo, "config", "user.name", "t")
        _git(self.repo, "config", "user.email", "t@example.com")

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, msg: str) -> str:
        _git(self.repo, "commit", "--allow-empty", "-q", "-m", msg)
        return _git(self.repo, "rev-parse", "HEAD")

    def merge(self, msg: str) -> str:
        # 先在 main 留一条带 PR 引用的种子提交，再造侧分支合并
        self.commit("chore: init (#1)")
        _git(self.repo, "checkout", "-q", "-b", "side")
        self.commit("side commit")
        _git(self.repo, "checkout", "-q", "main")
        _git(self.repo, "merge", "--no-ff", "-q", "-m", msg, "side")
        return _git(self.repo, "rev-parse", "HEAD")


class TestFirstParent(_TempRepo):
    def test_reads_first_parent_only(self):
        self.commit("c1")
        self.merge("Merge pull request #1 from x/y")
        commits = gha.first_parent_commits("main", 50, repo=str(self.repo))
        subjects = [c.subject for c in commits]
        self.assertIn("Merge pull request #1 from x/y", subjects)
        self.assertIn("c1", subjects)
        # 侧分支提交不属首亲
        self.assertNotIn("side commit", subjects)

    def test_max_commits_zero_rejected(self):
        with self.assertRaises(gha.AuditError):
            gha.first_parent_commits("main", 0, repo=str(self.repo))


class TestAudit(_TempRepo):
    def test_merge_and_pr_ref_allowed(self):
        self.merge("Merge pull request #1 from x/y")
        self.commit("feat: squash (#2)")
        result = gha.audit("main", 50, repo=str(self.repo))
        self.assertTrue(result.ok, result.violations)
        self.assertEqual(result.allowed_merge, 1)
        self.assertEqual(result.allowed_pr_ref, 2)  # init (#1) + squash (#2)

    def test_ci_mark_allowed(self):
        self.merge("Merge pull request #1 from x/y")
        self.commit("chore: 自动同步 HTML（由 CI 生成）")
        result = gha.audit("main", 50, repo=str(self.repo))
        self.assertTrue(result.ok)
        self.assertEqual(result.allowed_ci, 1)

    def test_historical_allow_allowed(self):
        sha = self.commit("初始化")
        result = gha.audit("main", 50, allow_shas=(sha,), repo=str(self.repo))
        self.assertTrue(result.ok)
        self.assertEqual(result.allowed_historical, 1)

    def test_direct_commit_violation(self):
        sha = self.commit("直接改 main")
        result = gha.audit("main", 50, repo=str(self.repo))
        self.assertFalse(result.ok)
        self.assertEqual(len(result.violations), 1)
        self.assertEqual(result.violations[0].sha, sha)
        self.assertIn("直接改 main", result.violations[0].subject)

    def test_default_historical_allow(self):
        # 真实仓库的两条历史直接提交应被默认白名单覆盖
        self.assertEqual(len(gha.HISTORICAL_ALLOW), 2)
        for sha in gha.HISTORICAL_ALLOW:
            self.assertEqual(len(sha), 40)

    def test_to_dict_shape(self):
        self.commit("c1")
        d = gha.audit("main", 50, repo=str(self.repo)).to_dict()
        self.assertEqual(d["spec"], gha.SPEC_ID)
        self.assertIn("allowed", d)
        self.assertIn("violations", d)


class TestCli(_TempRepo):
    def test_exit_code_on_violation(self):
        self.commit("直接改 main")
        rc = gha.main(["--branch", "main", "--repo", str(self.repo),
                       "--max-commits", "50"])
        self.assertEqual(rc, 1)

    def test_exit_code_ok(self):
        self.merge("Merge pull request #1 from x/y")
        rc = gha.main(["--branch", "main", "--repo", str(self.repo),
                       "--max-commits", "50"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
