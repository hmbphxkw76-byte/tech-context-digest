# -*- coding: utf-8 -*-
"""审计出口可信（audit_tool.py / T2）单元测试：标识分级与终审拆分。"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "audit" / "scripts" / "audit_tool.py"

spec = importlib.util.spec_from_file_location("audit_tool", TOOL)
audit_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_tool)


class TestMarkLevels(unittest.TestCase):
    def test_levels_defined(self):
        self.assertEqual(audit_tool.MARK_LEVELS, ("none", "pre", "full"))

    def test_badge_full_uses_navy(self):
        html = audit_tool._badge_html("AUD-1", "2026-11-15", 4, "full")
        self.assertIn("#16324f", html)
        self.assertIn("已审计", html)
        self.assertIn('data-mark-level="full"', html)

    def test_badge_pre_is_grey_and_explicit(self):
        html = audit_tool._badge_html("AUD-1", "2026-11-15", 3, "pre")
        self.assertIn("#5b6b7c", html)
        self.assertIn("预审通过", html)
        self.assertIn("语义复核待完成", html)
        self.assertNotIn("终审通过", html)


class TestMachineFinal(unittest.TestCase):
    def test_real_report_passes_machine_final(self):
        p = ROOT / "content/economy/dubai/apartment/reports/2026-11_monthly.html"
        ok, detail = audit_tool._machine_final(p)
        self.assertTrue(ok, detail)

    def test_broken_anchor_fails(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.html"
            p.write_text('<html><head><title>t</title></head><body>'
                         '<a href="#missing">x</a></body></html>', encoding="utf-8")
            ok, detail = audit_tool._machine_final(p)
            self.assertFalse(ok)
            self.assertIn("断头锚点 1", detail)


class TestSemanticFinal(unittest.TestCase):
    def test_missing_record_is_false(self):
        ok, detail = audit_tool._semantic_final("no/such/report.html")
        self.assertFalse(ok)
        self.assertIn("无 second", detail)


class TestRunStrictDryRun(unittest.TestCase):
    def test_strict_dry_run_does_not_write(self):
        import argparse
        orig = audit_tool.cmd_init
        audit_tool.cmd_init = lambda _a: None  # 避免 dry-run 写登记表
        try:
            ns = argparse.Namespace(dry_run=True, strict=True, no_gate=True)
            rc = audit_tool.cmd_run(ns)  # dry-run 只计算不写记录；不应抛异常
            # rc=2 为 P0-3 宽限期（新报告缺语义终审只告警、不阻断）的合法返回值：
            # 仓库中存在 fix / 待 L3 报告时 cmd_run --strict 返回 2，不属异常。
            self.assertIn(rc, (0, 1, 2))
        finally:
            audit_tool.cmd_init = orig


class TestSemanticFinalIgnoresCiBot(unittest.TestCase):
    """机器 second 留痕不得遮蔽 Agent 的 L3 语义复核（fail-fast 回归）。"""

    def _patch_review_file(self, reviews):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            fp = Path(d) / "r.json"
            fp.write_text(json.dumps({"report": "x", "reviews": reviews}, ensure_ascii=False),
                           encoding="utf-8")
            orig = audit_tool._review_file
            audit_tool._review_file = lambda _rel: fp
            try:
                yield_ok, detail = audit_tool._semantic_final("x")
            finally:
                audit_tool._review_file = orig
        return yield_ok, detail

    def test_ci_bot_after_agent_does_not_shadow(self):
        reviews = [
            {"stage": "second", "reviewer": "agent", "decision": "pass"},
            {"stage": "second", "reviewer": "ci-bot", "decision": "pass"},
        ]
        ok, detail = self._patch_review_file(reviews)
        self.assertTrue(ok, detail)
        self.assertIn("reviewer=agent", detail)

    def test_only_ci_bot_is_false(self):
        reviews = [{"stage": "second", "reviewer": "ci-bot", "decision": "pass"}]
        ok, detail = self._patch_review_file(reviews)
        self.assertFalse(ok)
        self.assertIn("无 Agent second", detail)


class TestRunStrictDoesNotWriteSecond(unittest.TestCase):
    def test_machine_does_not_record_second_stage(self):
        import argparse
        written = []
        orig_init, orig_review, orig_mark, orig_last = (
            audit_tool.cmd_init, audit_tool.cmd_review, audit_tool.cmd_mark, audit_tool._last_stage)
        audit_tool.cmd_init = lambda _a: None
        audit_tool.cmd_review = lambda ns: written.append(ns.stage)
        audit_tool.cmd_mark = lambda ns: None
        audit_tool._last_stage = lambda *a: None  # 关闭幂等跳过，强制走写留痕分支
        try:
            rc = audit_tool.cmd_run(argparse.Namespace(dry_run=False, strict=True, no_gate=True))
            # rc=2 为 P0-3 宽限期合法返回值（存在待 L3 / fix 报告时返回 2）。
            self.assertIn(rc, (0, 1, 2))
        finally:
            audit_tool.cmd_init = orig_init
            audit_tool.cmd_review = orig_review
            audit_tool.cmd_mark = orig_mark
            audit_tool._last_stage = orig_last
        # second 为 Agent L3 语义复核阶段，机器不得写留痕
        self.assertNotIn("second", written)
        self.assertIn("final", written)


class TestGracePeriod(unittest.TestCase):
    """P0-3：新报告 L3 宽限期——宽限内缺语义终审只告警（rc=2），超期阻断（rc=1）。"""

    def test_age_and_grace_boundary(self):
        import datetime as dt
        today = dt.date.today()
        self.assertIsNone(audit_tool._age_days({}))
        self.assertTrue(audit_tool.in_grace({"first_seen_at": today.isoformat()}))
        self.assertTrue(audit_tool.in_grace(
            {"first_seen_at": (today - dt.timedelta(days=audit_tool.L3_GRACE_DAYS)).isoformat()}))
        self.assertFalse(audit_tool.in_grace(
            {"first_seen_at": (today - dt.timedelta(days=audit_tool.L3_GRACE_DAYS + 1)).isoformat()}))
        self.assertFalse(audit_tool.in_grace({"first_seen_at": "not-a-date"}))

    def _run_with_grace(self, grace):
        import argparse
        import datetime as dt
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            report = Path(d) / "r.html"
            report.write_text("<html><head><title>t</title></head><body>来源 口径</body></html>",
                              encoding="utf-8")
            orig = (audit_tool.cmd_init, audit_tool.load_registry, audit_tool.collect_reports,
                    audit_tool.structure_check, audit_tool._machine_final, audit_tool._semantic_final,
                    audit_tool.agent_stage_pass, audit_tool.cmd_review, audit_tool.cmd_mark,
                    audit_tool._last_stage)
            first_seen = dt.date.today().isoformat() if grace else "2026-01-01"
            audit_tool.cmd_init = lambda _a: None
            audit_tool.load_registry = lambda: {"reports": {str(report): {"first_seen_at": first_seen}}}
            audit_tool.collect_reports = lambda: [{"path": str(report), "category": "report"}]
            audit_tool.structure_check = lambda *a: ([], [])
            audit_tool._machine_final = lambda p, gate=None: (True, "L2 10/10")
            audit_tool._semantic_final = lambda rel: (False, "无 Agent second 复核记录")
            audit_tool.agent_stage_pass = lambda *a: False
            audit_tool.cmd_review = lambda ns: None
            audit_tool.cmd_mark = lambda ns: None
            audit_tool._last_stage = lambda *a: None
            try:
                return audit_tool.cmd_run(argparse.Namespace(dry_run=True, strict=True, no_gate=True))
            finally:
                (audit_tool.cmd_init, audit_tool.load_registry, audit_tool.collect_reports,
                 audit_tool.structure_check, audit_tool._machine_final, audit_tool._semantic_final,
                 audit_tool.agent_stage_pass, audit_tool.cmd_review, audit_tool.cmd_mark,
                 audit_tool._last_stage) = orig

    def test_grace_returns_warn(self):
        self.assertEqual(self._run_with_grace(True), 2)

    def test_overdue_returns_block(self):
        self.assertEqual(self._run_with_grace(False), 1)


if __name__ == "__main__":
    unittest.main()
