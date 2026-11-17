# -*- coding: utf-8 -*-
"""流程复用一致性测试（PROCESS-REUSE-MANIFEST v1.3）。

确认「信息分层与决策交付」优化流程被后续每个阶段一致复用：
  - 四门禁接入 ci / html-sync / content-update / scheduled-maintenance；
  - 复用清单文档存在且覆盖四门禁与两份规范；
  - 全部 business-config 与类型模板声明强制项；
  - AGENTS.md 固化硬性约束。
另确认 P0/P1/P2 优化清单的统一门禁入口（optimization_gate.py）被所有阶段复用。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / ".github" / "workflows"

GATES = (
    "info_density_check.py",
    "fact_card_check.py",
    "decision_hub_check.py",
    "blind_spot_check.py",
)
WORKFLOWS = ("ci.yml", "html-sync.yml", "content-update.yml", "scheduled-maintenance.yml")


class TestProcessReuse(unittest.TestCase):
    def test_all_workflows_reuse_four_gates(self):
        # P1-2：四门禁由 optimization_gate 统一承载，各阶段只调统一入口，不得分项重复。
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "optimization_gate", ROOT / "engine" / "tools" / "optimization_gate.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        blob = " ".join(" ".join(cmd) for _n, cmd, _w in mod.CHECKS)
        for gate in GATES:
            self.assertIn(gate, blob, f"统一入口缺少 {gate}")
        for wf in WORKFLOWS:
            text = (WF / wf).read_text(encoding="utf-8")
            self.assertIn("optimization_gate.py", text, f"{wf} 未调用统一入口")
            for gate in GATES:
                self.assertNotIn(f"python engine/tools/{gate}", text,
                                 f"{wf} 分项重复调用 {gate}（应统一入口）")

    def test_manifest_exists_and_covers_gates(self):
        p = ROOT / "engine/docs/report-process-reuse.md"
        self.assertTrue(p.exists())
        text = p.read_text(encoding="utf-8")
        for gate in GATES:
            self.assertIn(gate.replace(".py", ""), text)
        self.assertIn("information-layering-spec.md", text)
        self.assertIn("decision-delivery-spec.md", text)

    def test_agents_md_hard_constraint(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("信息分层与决策交付（硬性约束", text)
        for gate in GATES:
            self.assertIn(gate, text)

    def test_every_business_config_declares_mandatory_section(self):
        configs = sorted(ROOT.glob("*/**/prompts/business-config.md"))
        self.assertGreaterEqual(len(configs), 7)
        for c in configs:
            text = c.read_text(encoding="utf-8")
            self.assertIn("信息分层与决策交付", text, f"{c} 缺强制项声明")

    def test_type_templates_declare_mandatory_block(self):
        templates = sorted((ROOT / "engine/templates").glob("*/prompt-*-template.md"))
        self.assertGreaterEqual(len(templates), 16)
        for t in templates:
            text = t.read_text(encoding="utf-8")
            self.assertIn("信息分层与决策交付", text, f"{t} 缺强制项")

    def test_specs_are_single_source(self):
        base = ROOT / "engine/templates"
        self.assertTrue((base / "information-layering-spec.md").exists())
        self.assertTrue((base / "decision-delivery-spec.md").exists())
        # 通用基座必须指针到两份规范
        generic = (base / "prompt-generic-base.md").read_text(encoding="utf-8")
        self.assertIn("information-layering-spec.md", generic)
        self.assertIn("decision-delivery-spec.md", generic)


class TestOptimizationGateReuse(unittest.TestCase):
    """P0/P1/P2 优化清单统一门禁的复用一致性。"""

    def test_all_stages_invoke_unified_gate(self):
        for wf in WORKFLOWS:
            text = (WF / wf).read_text(encoding="utf-8")
            self.assertIn("optimization_gate.py", text, f"{wf} 未复用统一门禁")

    def test_audit_stage_fail_fast(self):
        text = (WF / "audit.yml").read_text(encoding="utf-8")
        self.assertIn("audit_tool.py run --strict", text)
        self.assertIn("::error::审计四环节未通过", text)
        # 不得回潮为「告警后放行」
        self.assertNotIn("::warning::存在待修报告", text)
        self.assertNotIn("::warning::存在待修", text)

    def test_gate_check_scripts_exist(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "optimization_gate", ROOT / "engine" / "tools" / "optimization_gate.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        names = [n for n, _c, _w in mod.CHECKS]
        self.assertEqual(len(names), len(set(names)))
        for _name, cmd, _warn in mod.CHECKS:
            script = next((a for a in cmd if a.startswith("engine/tools/") and a.endswith(".py")), None)
            self.assertIsNotNone(script, cmd)
            self.assertTrue((ROOT / script).exists(), f"门禁脚本缺失：{script}")

    def test_gate_subset_runs(self):
        import subprocess
        r = subprocess.run([sys.executable, "engine/tools/optimization_gate.py",
                            "--only", "metric_registry,release_calendar"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_gate_unknown_check_rejected(self):
        import subprocess
        r = subprocess.run([sys.executable, "engine/tools/optimization_gate.py",
                            "--only", "bogus_gate"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)

    def test_task_loop_declared(self):
        """Phase 1.3：任务级闭环硬性约束与 N0.5 映射已声明。"""
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("任务级闭环", agents)
        self.assertIn("task_plan.py", agents)
        self.assertIn("local_mainline.py", agents)
        doc = (ROOT / "engine" / "docs" / "report-pipeline-system.md").read_text(encoding="utf-8")
        self.assertIn("N0.5", doc)
        self.assertIn("任务计划", doc)

    def test_ci_runs_pipeline_runner_validate(self):
        """Phase 0.4 方案 A：ci.yml 必须执行端到端编排校验（声明-实现一致）。"""
        text = (WF / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("pipeline_runner.py validate", text)

    def test_repo_sync_exposes_gate(self):
        text = (ROOT / "engine" / "tools" / "repo_sync.py").read_text(encoding="utf-8")
        self.assertIn("--gate", text)
        self.assertIn("optimization_gate.py", text)

    def test_gate_timeout_is_bounded(self):
        """单项门禁挂起 → 超时按错误处理（退出码 124），不无限阻塞。"""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "optimization_gate", ROOT / "engine" / "tools" / "optimization_gate.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertGreater(mod.DEFAULT_CHECK_TIMEOUT, 0)
        old = mod.CHECKS
        mod.CHECKS = [("sleepy", [sys.executable, "-c", "import time; time.sleep(5)"], True)]
        try:
            rep = mod.run_checks(names=["sleepy"], timeout=1, quiet=True)
        finally:
            mod.CHECKS = old
        self.assertEqual(rep["errors"], 1)
        self.assertEqual(rep["checks"][0]["code"], mod.TIMEOUT_EXIT_CODE)
        self.assertIn("超时", rep["checks"][0]["output"])


if __name__ == "__main__":
    unittest.main()
