# -*- coding: utf-8 -*-
"""多会话统一提交网关（repo_sync）单元测试：锁与直推守卫（不触发真实推送）。"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("repo_sync", ROOT / "engine" / "tools" / "repo_sync.py")
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)


class TestLock(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lock = Path(self.tmp.name) / "sync.lock"
        self._orig = rs.LOCK_PATH
        rs.LOCK_PATH = self.lock

    def tearDown(self):
        rs.LOCK_PATH = self._orig
        self.tmp.cleanup()

    def test_acquire_and_release(self):
        token = rs.acquire_lock("t1")
        self.assertTrue(self.lock.exists())
        rs.release_lock()
        self.assertFalse(self.lock.exists())
        self.assertEqual(token, f"t1-{rs.os.getpid()}")

    def test_second_acquire_times_out(self):
        rs.acquire_lock("holder-a")
        t0 = time.time()
        with self.assertRaises(rs.SyncError):
            rs.acquire_lock("holder-b", timeout=1)
        self.assertLess(time.time() - t0, 10)

    def test_stale_lock_reclaimed(self):
        self.lock.write_text(json.dumps({"pid": 999999, "ts": time.time() - 3600,
                                         "holder": "dead"}), encoding="utf-8")
        token = rs.acquire_lock("new", timeout=1)
        self.assertTrue(token.startswith("new-"))


class TestGuard(unittest.TestCase):
    def test_push_main_refused_without_allow(self):
        ok, msg = rs._push(allow_main=False, branch="main", acquire=False)
        self.assertFalse(ok)
        self.assertIn("拒绝直接推送", msg)

    def test_push_non_main_not_guarded(self):
        # 非 main 分支不会被守卫拒绝（mock sync，避免真实网络）
        orig = rs.sync
        rs.sync = lambda *a, **k: (True, "mock")
        try:
            ok, msg = rs._push(allow_main=False, branch="task/x-5f37e90d", acquire=False)
        finally:
            rs.sync = orig
        self.assertNotIn("拒绝直接推送", msg)

    def test_guard_cli_blocks_on_main(self):
        r = subprocess.run([sys.executable, "engine/tools/repo_sync.py", "guard"],
                           cwd=ROOT, capture_output=True, text=True)
        # 当前检出在 main → 应被阻断（退出码 1）
        if rs.current_branch() == "main":
            self.assertEqual(r.returncode, 1)
            self.assertIn("拒绝", r.stderr)
        else:
            self.assertEqual(r.returncode, 0)

    def test_parse_push_refs_normal_and_delete(self):
        text = ("refs/heads/main " + "a" * 40 + " refs/heads/main " + "0" * 40 + "\n"
                "(delete) " + "0" * 40 + " refs/heads/task/x " + "b" * 40 + "\n")
        refs = rs.parse_push_refs(text)
        self.assertEqual(len(refs), 2)
        self.assertEqual(refs[0][2], "refs/heads/main")
        self.assertEqual(refs[1][0], "(delete)")

    def test_guard_push_blocks_main_ref(self):
        blocked, why = rs.guard_push(f"refs/heads/main {'a' * 40} refs/heads/main {'0' * 40}")
        self.assertTrue(blocked)
        self.assertIn("refs/heads/main", why)

    def test_guard_push_blocks_main_pushed_from_task_branch(self):
        # 站在 task 分支上显式推 main 也必须阻断（旧实现只看当前分支，会放行）
        blocked, _ = rs.guard_push(f"refs/heads/main {'a' * 40} refs/heads/main {'b' * 40}")
        self.assertTrue(blocked)

    def test_guard_push_allows_main_delete(self):
        blocked, _ = rs.guard_push(f"(delete) {'0' * 40} refs/heads/main {'b' * 40}")
        self.assertFalse(blocked)

    def test_guard_push_allows_task_branch(self):
        blocked, _ = rs.guard_push(f"refs/heads/task/x-5f37e90d {'a' * 40} refs/heads/task/x-5f37e90d {'0' * 40}")
        self.assertFalse(blocked)

    def test_guard_push_blocks_malformed_task_branch(self):
        # 受管分支缺会话标识 → 推送阻断（BRANCH-NAMING-SPEC）
        blocked, why = rs.guard_push(f"refs/heads/task/x {'a' * 40} refs/heads/task/x {'0' * 40}")
        self.assertTrue(blocked)
        self.assertIn("命名不合规", why)

    def test_guard_push_fallback_to_current_branch(self):
        # 无 refspec 上下文（手动调用）→ 回退当前分支判定
        blocked, _ = rs.guard_push("")
        self.assertEqual(blocked, rs.current_branch() == "main")

    def test_gitlab_remote_blocked(self):
        blocked, why = rs.gitlab_remote_blocked(
            ["git@github.com:o/r.git", "https://gitlab.com/o/r.git"])
        self.assertTrue(blocked)
        self.assertIn("gitlab.com", why)

    def test_gitlab_remote_case_insensitive(self):
        blocked, _ = rs.gitlab_remote_blocked(["https://GitLab.example.com/o/r.git"])
        self.assertTrue(blocked)

    def test_gitlab_remote_allows_github(self):
        blocked, _ = rs.gitlab_remote_blocked(
            ["git@github.com:o/r.git", "https://github.com/o/r.git"])
        self.assertFalse(blocked)

    def test_current_repo_has_no_gitlab_remote(self):
        # 用户硬性约束：本仓库不得配置 GitLab 远端
        blocked, why = rs.gitlab_remote_blocked()
        self.assertFalse(blocked, why)

    def test_guard_cli_reads_stdin(self):
        r = subprocess.run([sys.executable, "engine/tools/repo_sync.py", "guard"],
                           cwd=ROOT, capture_output=True, text=True,
                           input=f"refs/heads/main {'a' * 40} refs/heads/main {'0' * 40}\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("拒绝", r.stderr)

    def test_guard_cli_allows_branch_delete_stdin(self):
        # 在 main 上删除远端分支不应被守卫误拦
        r = subprocess.run([sys.executable, "engine/tools/repo_sync.py", "guard"],
                           cwd=ROOT, capture_output=True, text=True,
                           input=f"(delete) {'0' * 40} refs/heads/task/x-5f37e90d {'b' * 40}\n")
        self.assertEqual(r.returncode, 0)

    def test_status_cli_ok(self):
        r = subprocess.run([sys.executable, "engine/tools/repo_sync.py", "status"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("分支：", r.stdout)


class TestTaskPlanGate(unittest.TestCase):
    """治理标准 1：受管 task/* 分支 `run --gate` 前必须有任务计划。"""

    def test_non_managed_branch_not_required(self):
        ok, _ = rs.require_task_plan(branch="main", root=Path("/nonexistent"))
        self.assertTrue(ok)

    def test_managed_branch_missing_plan(self):
        with tempfile.TemporaryDirectory() as d:
            ok, msg = rs.require_task_plan(branch="task/x-00000000", root=Path(d))
            self.assertFalse(ok)
            self.assertIn("缺任务计划", msg)

    def test_managed_branch_plan_present(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "engine/audit/records/tasks/x"
            p.mkdir(parents=True)
            (p / "plan.json").write_text("{}\n", encoding="utf-8")
            ok, msg = rs.require_task_plan(branch="task/x-00000000", root=Path(d))
            self.assertTrue(ok)
            self.assertIn("任务计划就绪", msg)

    def test_run_refuses_without_plan(self):
        from contextlib import contextmanager

        @contextmanager
        def fake_locked(holder=""):
            yield "tok"

        orig_locked, orig_req = rs.locked, rs.require_task_plan
        rs.locked = fake_locked
        rs.require_task_plan = lambda *a, **k: (False, "缺任务计划")
        try:
            ok, msg = rs.run(["a"], "m", gate=True)
        finally:
            rs.locked, rs.require_task_plan = orig_locked, orig_req
        self.assertFalse(ok)
        self.assertIn("工件即门禁输入", msg)

    def test_run_allow_no_plan_override(self):
        from contextlib import contextmanager

        @contextmanager
        def fake_locked(holder=""):
            yield "tok"

        orig_locked = rs.locked
        orig_req = rs.require_task_plan
        orig_run = rs.subprocess.run
        orig_git = rs._git
        rs.locked = fake_locked
        rs.require_task_plan = lambda *a, **k: (False, "缺任务计划")
        rs.subprocess.run = lambda *a, **k: subprocess.CompletedProcess(a, 0, "", "")
        rs._git = lambda *a, **k: subprocess.CompletedProcess(a, 1, "", "no match")
        try:
            ok, msg = rs.run(["a"], "m", gate=True, allow_no_plan=True)
        finally:
            rs.locked, rs.require_task_plan, rs.subprocess.run, rs._git = (
                orig_locked, orig_req, orig_run, orig_git)
        # 计划缺失但显式放行后，会继续走门禁（此处 mock 门禁退出码 0，随后因无变更 / add 等失败，
        # 关键断言是「未在计划校验处被拒绝」）。
        self.assertNotIn("工件即门禁输入", msg)


if __name__ == "__main__":
    unittest.main()
