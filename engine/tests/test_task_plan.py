# -*- coding: utf-8 -*-
"""任务计划工件生成器测试（task_plan / MAINLINE-ADOPTION-PHASE1）。

锁定：
- `init` 生成 plan.json / tasks.json / risks.json / task-start.md 四件套；
- schema 固定（schema_version / slug / title / nodes / gates / artifacts / reuse / reports）；
- `reports` 关联报告 rel 去重 + 字典序，写入 plan.json 与 task-start.md「## 关联报告」；
- 确定性：重复生成字节一致，`check` 可重放；
- N0.5「任务计划」子节点映射存在，主体 N0–N8 保留。
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("task_plan", ROOT / "engine" / "tools" / "task_plan.py")
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)


class TestTaskPlan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._orig_dir = tp.TASKS_DIR
        tp.TASKS_DIR = Path(self.tmp.name)

    def tearDown(self):
        tp.TASKS_DIR = self._orig_dir
        self.tmp.cleanup()

    def _init(self, slug="demo-task"):
        return tp.write_artifacts(
            slug,
            tp.build_plan(slug, "示例任务"),
            tp.parse_tasks(["T-01:第一步", "T-02:第二步"]),
            tp.parse_risks(["R-01:风险一:缓解一"]),
        )

    def test_init_writes_four_artifacts(self):
        written = self._init()
        self.assertEqual([p.name for p in written],
                         ["plan.json", "tasks.json", "risks.json", "task-start.md"])
        for p in written:
            self.assertTrue(p.exists())

    def test_plan_schema_fixed(self):
        self._init()
        plan, tasks, risks = tp.load_artifacts("demo-task")
        self.assertEqual(plan["schema_version"], tp.SCHEMA_VERSION)
        self.assertEqual(plan["slug"], "demo-task")
        self.assertEqual(plan["title"], "示例任务")
        self.assertEqual(plan["gates"], [f"G{i}" for i in range(0, 9)])
        self.assertIn("plan", plan["artifacts"])
        self.assertIn("gate", plan["reuse"])
        ids = [n["id"] for n in plan["nodes"]]
        self.assertIn("N0.5", ids)
        for i in range(0, 9):
            self.assertIn(f"N{i}", ids)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(len(risks), 1)

    def test_deterministic_bytes(self):
        self._init()
        first = {p.name: p.read_text(encoding="utf-8")
                 for p in sorted(tp.plan_dir("demo-task").iterdir())}
        self._init()
        second = {p.name: p.read_text(encoding="utf-8")
                  for p in sorted(tp.plan_dir("demo-task").iterdir())}
        self.assertEqual(first, second)

    def test_check_passes_and_detects_tamper(self):
        self._init()
        self.assertEqual(tp.check("demo-task"), [])
        p = tp.plan_dir("demo-task") / "tasks.json"
        p.write_text("{}\n", encoding="utf-8")
        problems = tp.check("demo-task")
        self.assertTrue(any("不一致" in x or "缺" in x or "schema" in x for x in problems), problems)

    def test_check_missing_artifacts(self):
        problems = tp.check("missing-task")
        self.assertTrue(problems)

    def test_validate_artifacts_catches_slug_mismatch(self):
        plan = tp.build_plan("a", "t")
        problems = tp.validate_artifacts("b", plan, [], [])
        self.assertTrue(any("slug" in x for x in problems))

    def test_parse_tasks_and_risks(self):
        tasks = tp.parse_tasks(["T-1:标题"])
        self.assertEqual(tasks[0]["status"], "pending")
        risks = tp.parse_risks(["R-1:描述:缓解"])
        self.assertEqual(risks[0]["mitigation"], "缓解")

    def test_slug_validation(self):
        self.assertFalse(tp.validate_slug("Bad_Slug")[0])
        self.assertTrue(tp.validate_slug("phase1-task-loop")[0])

    def test_plan_has_reports_field(self):
        self.assertEqual(tp.build_plan("demo-task", "示例任务")["reports"], [])

    def test_normalize_reports_sorted_unique(self):
        self.assertEqual(tp.normalize_reports(["b/x.md", "a/y.md", "b/x.md"]),
                         ["a/y.md", "b/x.md"])
        self.assertEqual(tp.normalize_reports(None), [])
        self.assertEqual(tp.normalize_reports(["  ", "a/y.md"]), ["a/y.md"])

    def test_init_writes_reports_and_start_section(self):
        plan = tp.build_plan("demo-task", "示例任务")
        plan["reports"] = tp.normalize_reports(["b/x.md", "a/y.md"])
        tp.write_artifacts("demo-task", plan, tp.parse_tasks([]), tp.parse_risks([]))
        loaded, _, _ = tp.load_artifacts("demo-task")
        self.assertEqual(loaded["reports"], ["a/y.md", "b/x.md"])
        start = (tp.plan_dir("demo-task") / "task-start.md").read_text(encoding="utf-8")
        self.assertIn("## 关联报告", start)
        self.assertIn("- `a/y.md`", start)
        self.assertIn("- `b/x.md`", start)
        self.assertEqual(tp.check("demo-task"), [])

    def test_start_md_empty_reports_fixed_text(self):
        tp.write_artifacts("demo-task", tp.build_plan("demo-task", "示例任务"),
                           tp.parse_tasks([]), tp.parse_risks([]))
        start = (tp.plan_dir("demo-task") / "task-start.md").read_text(encoding="utf-8")
        self.assertIn("- 无（手工/工具类任务）", start)

    def test_validate_reports_rejects_dup_non_string_and_non_list(self):
        plan = tp.build_plan("demo-task", "示例任务")
        plan["reports"] = ["a", "a"]
        self.assertTrue(any("重复" in x for x in tp.validate_artifacts("demo-task", plan, [], [])))
        plan["reports"] = ["a", 3]
        self.assertTrue(any("非字符串" in x for x in tp.validate_artifacts("demo-task", plan, [], [])))
        plan["reports"] = "not-a-list"
        self.assertTrue(any("列表" in x for x in tp.validate_artifacts("demo-task", plan, [], [])))


if __name__ == "__main__":
    unittest.main()
