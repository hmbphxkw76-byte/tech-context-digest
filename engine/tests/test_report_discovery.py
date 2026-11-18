# -*- coding: utf-8 -*-
"""统一报告发现（T5）单元测试：_common.iter_reports 与 hub/audit 口径一致。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

from _common import iter_business_dirs, iter_business_reports, iter_reports  # noqa: E402


class TestDiscoveryCategories(unittest.TestCase):
    def test_default_is_formal_only(self):
        refs = iter_reports()
        self.assertTrue(refs)
        self.assertTrue(all(r.category == "report" for r in refs))

    def test_archives_excluded_by_default(self):
        all_refs = iter_reports(include_archives=True, include_legacy=True)
        formal = {r.rel for r in iter_reports()}
        archived = [r for r in all_refs if r.category == "archived"]
        # 归档若存在，必须被默认口径排除
        self.assertTrue(all(r.rel not in formal for r in archived))

    def test_legacy_not_published(self):
        formal = {r.rel for r in iter_reports()}
        legacy = {r.rel for r in iter_reports(include_legacy=True) if r.category == "legacy"}
        # 2026-11-17 全量重生成已清理 reports/legacy/（tech-debt-ledger B12–B14），
        # 存档机制保留：legacy 允许为空，但一旦存在必须全部未发布。
        self.assertTrue(all(rel not in formal for rel in legacy))

    def test_every_business_line_represented(self):
        for b in iter_business_dirs():
            refs = iter_business_reports(b)
            reports_dir = b.path / "reports"
            # 仅对实际含有报告文件的业务线要求可被发现；空目录（仅 .gitkeep 占位）
            # 对应「已接入、未产出」状态（P1-9 四主题就绪化），不参与本项校验。
            has_report_files = (
                any(f.is_file() and not f.name.startswith(".") for f in reports_dir.iterdir())
                if reports_dir.is_dir() else False
            )
            if has_report_files:
                self.assertTrue(refs, b.rel)

    def test_period_parsed_for_named_reports(self):
        for r in iter_reports():
            self.assertTrue(r.cycle, r.rel)
            self.assertTrue(r.period, r.rel)


class TestHubAuditParity(unittest.TestCase):
    def test_hub_formal_equals_audit_formal(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "audit_tool", ROOT / "engine" / "audit" / "scripts" / "audit_tool.py")
        audit_tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(audit_tool)
        hub_formal = {r.rel for r in iter_reports()}
        audit_formal = {r["path"] for r in audit_tool.collect_reports()
                        if r["kind"] == "business" and r["category"] == "report"}
        self.assertEqual(hub_formal, audit_formal)


if __name__ == "__main__":
    unittest.main()
