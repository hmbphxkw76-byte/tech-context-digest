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
        self.assertIn("--auto", text)
        self.assertIn("inputs.token", text)
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

    def test_workflows_pass_token(self):
        for name in FOUR:
            text = (WF / name).read_text(encoding="utf-8")
            self.assertIn("secrets.CI_PR_TOKEN", text, f"{name} 未传入 CI_PR_TOKEN")

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
