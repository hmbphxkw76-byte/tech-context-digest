# -*- coding: utf-8 -*-
"""分支命名规范（BRANCH-NAMING-SPEC v1.0）单元测试。

覆盖：会话标识解析与归一化、分支名生成与校验、登记册读写、存量梳理、
pre-push / pre-commit 钩子文件、guard 集成与 CLI 行为。
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
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bn = _load("branch_naming", TOOLS / "branch_naming.py")
rs = _load("repo_sync", TOOLS / "repo_sync.py")

UUID = "5f37e90d-eb60-4247-988a-9207d64048f5"
SHORT = "5f37e90d"


class TestSession(unittest.TestCase):
    def test_normalize_uuid_with_hyphens(self):
        self.assertEqual(bn.normalize_session(UUID), UUID.replace("-", "").lower())

    def test_normalize_lowercases(self):
        self.assertEqual(bn.normalize_session("ABCDEF01-2345-6789-abcd-ef0123456789"),
                         "abcdef0123456789abcdef0123456789")

    def test_normalize_rejects_non_hex(self):
        with self.assertRaises(bn.BranchNamingError):
            bn.normalize_session("not-a-session")

    def test_normalize_rejects_too_short(self):
        with self.assertRaises(bn.BranchNamingError):
            bn.normalize_session("abc1234")

    def test_short_is_first_8_hex(self):
        self.assertEqual(bn.session_short(UUID), SHORT)
        self.assertRegex(bn.session_short(UUID), r"^[0-9a-f]{8}$")

    def test_resolve_env_priority(self):
        full, src = bn.resolve_session(
            {"TECH_CTX_SESSION_ID": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
             "CATPAW_CONVERSATION_ID": UUID}, use_git_config=False)
        self.assertEqual(full, "aaaaaaaabbbbccccddddeeeeeeeeeeee")
        self.assertEqual(src, "env:TECH_CTX_SESSION_ID")

    def test_resolve_falls_back_to_x_ai_session(self):
        full, src = bn.resolve_session({"X_AI_SESSIONID": UUID}, use_git_config=False)
        self.assertEqual(full, UUID.replace("-", ""))
        self.assertEqual(src, "env:X_AI_SESSIONID")

    def test_resolve_invalid_env_fails_without_fallback(self):
        # 显式设置的值非法 → 直接失败，不悄悄换来源
        with self.assertRaises(bn.BranchNamingError):
            bn.resolve_session({"TECH_CTX_SESSION_ID": "bad", "CATPAW_CONVERSATION_ID": UUID},
                               use_git_config=False)

    def test_resolve_missing_raises(self):
        with self.assertRaises(bn.BranchNamingError):
            bn.resolve_session({}, use_git_config=False)

    def test_resolve_from_git_config(self):
        orig = bn._git_config_get
        bn._git_config_get = lambda key: UUID if key == bn.SESSION_GIT_KEY else None
        try:
            full, src = bn.resolve_session({}, use_git_config=True)
        finally:
            bn._git_config_get = orig
        self.assertEqual(full, UUID.replace("-", ""))
        self.assertEqual(src, f"git:{bn.SESSION_GIT_KEY}")


class TestNaming(unittest.TestCase):
    def test_build_branch(self):
        self.assertEqual(bn.build_branch("ci-permissions-fix", UUID),
                         f"task/ci-permissions-fix-{SHORT}")

    def test_build_branch_rejects_bad_slug(self):
        for slug in ("", "Bad_Slug", "a--b", "-lead", "trail-"):
            with self.assertRaises(bn.BranchNamingError, msg=slug):
                bn.build_branch(slug, UUID)

    def test_validate_managed_ok(self):
        ok, why = bn.validate_managed(f"task/x-{SHORT}")
        self.assertTrue(ok, why)

    def test_validate_managed_missing_short(self):
        ok, why = bn.validate_managed("task/ci-permissions-fix")
        self.assertFalse(ok)
        self.assertIn("会话标识", why)

    def test_validate_managed_bad_short_chars(self):
        ok, _ = bn.validate_managed("task/x-zzzzzzzz")
        self.assertFalse(ok)

    def test_validate_managed_short_too_long(self):
        ok, _ = bn.validate_managed(f"task/x-{SHORT}extra")
        self.assertFalse(ok)

    def test_validate_managed_rejects_uppercase(self):
        ok, _ = bn.validate_managed(f"task/X-{SHORT}")
        self.assertFalse(ok)

    def test_non_managed_always_passes(self):
        for name in ("main", "ci/audit", "feature/x", "v1.0"):
            ok, _ = bn.validate_managed(name)
            self.assertTrue(ok, name)

    def test_parse_branch_roundtrip(self):
        parsed = bn.parse_branch(f"task/a-b-c-{SHORT}")
        self.assertEqual(parsed, {"slug": "a-b-c", "session_short": SHORT})
        self.assertIsNone(bn.parse_branch("task/nope"))
        self.assertIsNone(bn.parse_branch("ci/audit"))

    def test_is_managed_and_exempt(self):
        self.assertTrue(bn.is_managed(f"task/x-{SHORT}"))
        self.assertFalse(bn.is_managed("ci/audit"))
        self.assertTrue(bn.is_exempt("main"))
        self.assertTrue(bn.is_exempt("ci/audit"))
        self.assertFalse(bn.is_exempt(f"task/x-{SHORT}"))

    def test_expected_session_short(self):
        self.assertEqual(bn.expected_session_short(f"task/x-{SHORT}"), SHORT)
        self.assertIsNone(bn.expected_session_short("task/x"))


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "branch_registry.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_load_missing_returns_empty(self):
        reg = bn.load_registry(self.path)
        self.assertEqual(reg["schema"], bn.REGISTRY_SCHEMA)
        self.assertEqual(reg["branches"], {})

    def test_register_and_reload(self):
        reg = bn.load_registry(self.path)
        bn.register_branch(reg, f"task/x-{SHORT}", UUID, task="x", note="source=env:X")
        bn.save_registry(reg, self.path)
        again = bn.load_registry(self.path)
        rec = again["branches"][f"task/x-{SHORT}"]
        self.assertEqual(rec["session"], UUID.replace("-", ""))
        self.assertEqual(rec["session_short"], SHORT)
        self.assertEqual(rec["task"], "x")
        self.assertEqual(rec["note"], "source=env:X")

    def test_save_is_deterministic(self):
        reg = bn.load_registry(self.path)
        bn.register_branch(reg, f"task/b-{SHORT}", UUID, task="b")
        bn.register_branch(reg, f"task/a-{SHORT}", UUID, task="a")
        bn.save_registry(reg, self.path)
        first = self.path.read_bytes()
        bn.save_registry(bn.load_registry(self.path), self.path)
        self.assertEqual(first, self.path.read_bytes())

    def test_unregister(self):
        reg = bn.load_registry(self.path)
        bn.register_branch(reg, f"task/x-{SHORT}", UUID)
        bn.unregister_branch(reg, f"task/x-{SHORT}")
        self.assertNotIn(f"task/x-{SHORT}", reg["branches"])

    def test_register_rejects_non_managed(self):
        reg = bn.load_registry(self.path)
        with self.assertRaises(bn.BranchNamingError):
            bn.register_branch(reg, "ci/audit", UUID)

    def test_session_ledger_groups_by_short(self):
        reg = bn.load_registry(self.path)
        bn.register_branch(reg, f"task/a-{SHORT}", UUID, task="a")
        bn.register_branch(reg, f"task/b-{SHORT}", UUID, task="b")
        ledger = bn.session_ledger(reg)
        self.assertEqual(ledger[SHORT], [f"task/a-{SHORT}", f"task/b-{SHORT}"])


class TestAudit(unittest.TestCase):
    def test_audit_splits(self):
        ok, bad, exempt = bn.audit_branches(
            [f"task/good-{SHORT}", "task/bad", "main", "ci/audit"])
        self.assertEqual(ok, [f"task/good-{SHORT}"])
        self.assertEqual(bad, ["task/bad"])
        self.assertEqual(exempt, ["main", "ci/audit"])

    def test_real_repo_base_and_ci_are_exempt(self):
        _, _, exempt = bn.audit_branches(["main", "ci/audit"])
        self.assertEqual(set(exempt), {"main", "ci/audit"})


class TestGuardIntegration(unittest.TestCase):
    def test_guard_push_allows_conforming_task(self):
        blocked, _ = rs.guard_push(
            f"refs/heads/task/x-{SHORT} {'a' * 40} refs/heads/task/x-{SHORT} {'0' * 40}")
        self.assertFalse(blocked)

    def test_guard_push_blocks_malformed_task(self):
        blocked, why = rs.guard_push(f"refs/heads/task/x {'a' * 40} refs/heads/task/x {'0' * 40}")
        self.assertTrue(blocked)
        self.assertIn("命名不合规", why)

    def test_guard_push_still_blocks_main(self):
        blocked, _ = rs.guard_push(f"refs/heads/main {'a' * 40} refs/heads/main {'0' * 40}")
        self.assertTrue(blocked)

    def test_guard_push_allows_system_branch(self):
        blocked, _ = rs.guard_push(f"refs/heads/ci/audit {'a' * 40} refs/heads/ci/audit {'0' * 40}")
        self.assertFalse(blocked)

    def test_push_refuses_malformed_managed_branch(self):
        ok, msg = rs._push(allow_main=False, branch="task/bad", acquire=False)
        self.assertFalse(ok)
        self.assertIn("BRANCH-NAMING-SPEC", msg)

    def test_push_allows_system_branch(self):
        orig = rs.sync
        rs.sync = lambda *a, **k: (True, "mock")
        try:
            ok, msg = rs._push(allow_main=False, branch="ci/audit", acquire=False)
        finally:
            rs.sync = orig
        self.assertNotIn("BRANCH-NAMING-SPEC", msg)

    def test_guard_commit_blocks_malformed_managed(self):
        orig = rs.current_branch
        rs.current_branch = lambda: "task/bad"
        try:
            blocked, why = rs.guard_commit()
        finally:
            rs.current_branch = orig
        self.assertTrue(blocked)
        self.assertIn("命名不合规", why)

    def test_guard_commit_allows_base(self):
        orig = rs.current_branch
        rs.current_branch = lambda: "main"
        try:
            blocked, _ = rs.guard_commit()
        finally:
            rs.current_branch = orig
        self.assertFalse(blocked)


class TestHookFiles(unittest.TestCase):
    def test_hook_files_exist(self):
        for name in ("pre-push", "pre-commit"):
            p = ROOT / ".githooks" / name
            self.assertTrue(p.is_file(), f"缺钩子 {name}")
            self.assertIn("repo_sync.py guard", p.read_text(encoding="utf-8"))

    def test_hook_files_are_tracked(self):
        r = subprocess.run(["git", "ls-files", ".githooks"], cwd=ROOT,
                           capture_output=True, text=True)
        tracked = r.stdout.split()
        self.assertIn(".githooks/pre-push", tracked)
        self.assertIn(".githooks/pre-commit", tracked)

    def test_pre_push_hook_runs_cleanup_first(self):
        text = (ROOT / ".githooks" / "pre-push").read_text(encoding="utf-8")
        self.assertIn("workspace_cleanup.py", text)


class TestCLI(unittest.TestCase):
    def _run(self, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "engine/tools/repo_sync.py", *args],
                              cwd=ROOT, capture_output=True, text=True, input=stdin)

    def test_session_cli(self):
        r = self._run("session")
        self.assertEqual(r.returncode, 0)
        self.assertIn("会话标识：", r.stdout)
        self.assertIn("来源：", r.stdout)

    def test_branch_audit_cli_ok(self):
        r = self._run("branch-audit")
        self.assertEqual(r.returncode, 0)
        self.assertIn("受管合规", r.stdout)

    def test_branches_cli(self):
        r = self._run("branches")
        self.assertEqual(r.returncode, 0)
        self.assertIn("main", r.stdout)

    def test_guard_commit_stage_cli(self):
        r = self._run("guard", "--stage", "commit")
        # 当前检出可能是基座或合规受管分支 → 均应放行
        self.assertEqual(r.returncode, 0)

    def test_guard_cli_blocks_main_via_stdin(self):
        r = self._run("guard", stdin=f"refs/heads/main {'a' * 40} refs/heads/main {'0' * 40}\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("拒绝", r.stderr)

    def test_guard_cli_blocks_malformed_task_via_stdin(self):
        r = self._run("guard", stdin=f"refs/heads/task/bad {'a' * 40} refs/heads/task/bad {'0' * 40}\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("命名不合规", r.stderr)

    def test_hook_install_and_uninstall(self):
        # 先记住原值，测试后恢复（避免改动开发者本克隆的钩子配置）
        original = rs._git("config", "--get", "core.hooksPath").stdout.strip()
        try:
            r = self._run("hook-install")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(rs._git("config", "--get", "core.hooksPath").stdout.strip(), ".githooks")
            r = self._run("hook-uninstall")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotEqual(rs._git("config", "--get", "core.hooksPath").stdout.strip(), ".githooks")
        finally:
            if original:
                rs._git("config", "core.hooksPath", original)
            else:
                rs._git("config", "--unset", "core.hooksPath")


if __name__ == "__main__":
    unittest.main()
