# -*- coding: utf-8 -*-
"""CI 协作隔离回归测试（T：CI 改为开 PR + 自动合并，不再直推 main）。"""
from __future__ import annotations

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / ".github" / "workflows"
ACTION = ROOT / ".github" / "actions" / "submit-pr" / "action.yml"
FOUR = ("audit.yml", "html-sync.yml", "content-update.yml", "scheduled-maintenance.yml")


class TestCIUsesPRs(unittest.TestCase):
    def test_composite_action_exists(self):
        self.assertTrue(ACTION.exists(), "缺少 .github/actions/submit-pr/action.yml")
        data = yaml.safe_load(ACTION.read_text(encoding="utf-8"))
        self.assertEqual(data["runs"]["using"], "composite")
        text = ACTION.read_text(encoding="utf-8")
        self.assertIn("gh pr create", text)
        self.assertIn("gh pr merge", text)
        self.assertIn("inputs.token", text)
        # 无凭据模式：不再用 --auto（bot PR 不触发 pull_request，--auto 会永卡 BLOCKED）
        self.assertNotIn("--auto", text)
        # 推送前必须刷新 CI 分支远端跟踪引用，避免 --force-with-lease 因 stale info 失败
        self.assertIn("refs/remotes/origin/$BRANCH", text)

    def test_no_direct_push_in_workflows(self):
        for name in FOUR:
            text = (WF / name).read_text(encoding="utf-8")
            self.assertNotIn("git push", text, f"{name} 仍存在 git push（应改走 submit-pr）")

    def test_workflows_have_pr_permission(self):
        for name in FOUR:
            data = yaml.safe_load((WF / name).read_text(encoding="utf-8"))
            perms = data.get("permissions", {}) or {}
            self.assertIn("pull-requests", perms, f"{name} 缺少 pull-requests 权限")

    def test_workflows_use_submit_pr(self):
        for name in FOUR:
            text = (WF / name).read_text(encoding="utf-8")
            self.assertIn("submit-pr", text, f"{name} 未复用 submit-pr 动作")

    def test_composite_action_merges_immediately(self):
        """无 PAT 模式：门禁通过后 gh pr merge --merge（门禁内移至调用工作流）。"""
        data = yaml.safe_load(ACTION.read_text(encoding="utf-8"))
        self.assertEqual(data["inputs"]["merge"]["default"], "true")
        text = ACTION.read_text(encoding="utf-8")
        self.assertIn("gh pr merge", text)
        self.assertIn("--merge", text)

    def test_workflows_do_not_use_user_token(self):
        """无凭据模式：工作流不得引用用户 token（仅 PAT / GitHub App 才需）。"""
        for name in FOUR:
            text = (WF / name).read_text(encoding="utf-8")
            self.assertNotIn("CI_PR_TOKEN", text, f"{name} 仍引用 CI_PR_TOKEN")
            # 合并后清理被门禁的空跑运行（action_required）需 actions: write
            self.assertIn("actions: write", text, f"{name} 缺少 actions: write")

    def test_checkout_workflows_have_contents_permission(self):
        # 声明 permissions 块后，未列出的 scope 一律降为 none：缺 contents 会让
        # actions/checkout 在私有仓库上 fetch 失败（remote: Repository not found）。
        for path in sorted(WF.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            if "actions/checkout@" not in text:
                continue
            perms = (yaml.safe_load(text).get("permissions") or {})
            self.assertIn(
                "contents",
                perms,
                f"{path.name} 使用 actions/checkout，但 permissions 缺 contents（read/write 均可）",
            )


if __name__ == "__main__":
    unittest.main()
