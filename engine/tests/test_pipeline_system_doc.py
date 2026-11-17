# -*- coding: utf-8 -*-
"""体系说明文档与两级 gate-period 一致性测试（REPORT-PIPELINE-SYSTEM v1.2）。

锁定内容与代码事实源一致：
- `engine/docs/report-pipeline-system.md` 存在、含完整 Mermaid 流程图、覆盖 N0–N8 全链路节点；
- **门禁左移**：主链各阶段配就地门禁 G0–G8，G0–G5 左移到 N6 之前，N6 为兜底；
- 文档门禁清单数量与 `optimization_gate.CHECKS` 一致（新增门禁须同步文档）；
- 两级 gate-period（内容 2026-12 / 来源 2027-01）在文档与代码中显式声明且接线正确。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "engine" / "docs" / "report-pipeline-system.md"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location(
        "optimization_gate", ROOT / "engine" / "tools" / "optimization_gate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPipelineSystemDoc(unittest.TestCase):
    """体系说明文档完整性。"""

    def setUp(self):
        self.assertTrue(DOC.exists(), f"体系说明文档缺失：{DOC.relative_to(ROOT)}")
        self.text = DOC.read_text(encoding="utf-8")

    def test_mermaid_flowcharts_present(self):
        blocks = re.findall(r"```mermaid\n(.*?)```", self.text, re.DOTALL)
        self.assertGreaterEqual(len(blocks), 3, "至少需要 3 个 Mermaid 流程图")
        for b in blocks:
            self.assertRegex(b.strip(), r"^(flowchart|graph)\b", "Mermaid 块须为流程图")

    def test_all_pipeline_nodes_covered(self):
        for n in range(0, 9):
            self.assertIn(f"N{n} ", self.text, f"缺全链路节点 N{n}")

    def test_gate_count_matches_code(self):
        mod = _load_gate_module()
        names = [c[0] for c in mod.CHECKS]
        self.assertEqual(len(names), 21, "门禁清单数量变化须同步体系文档")
        self.assertIn("21 项", self.text)
        for name in names:
            self.assertIn(name, self.text, f"文档门禁清单缺 {name}")

    def test_two_level_gate_period_declared(self):
        for kw in ("2026-12", "2027-01", "--gate-period", "--source-gate-period"):
            self.assertIn(kw, self.text)

    def test_five_defense_lines_declared(self):
        for kw in ("L0", "四门禁", "统一门禁", "审计四环节", "发布留痕"):
            self.assertIn(kw, self.text)

    def test_gates_shifted_left(self):
        """门禁左移：主链各阶段配就地门禁 G0–G8，G0–G5 在 N6 之前，N6 为兜底。"""
        self.assertIn("左移", self.text)
        self.assertIn("兜底", self.text)
        for g in range(0, 9):
            self.assertIn(f"G{g}", self.text, f"缺就地门禁 G{g}")
        blocks = re.findall(r"```mermaid\n(.*?)```", self.text, re.DOTALL)
        main = blocks[0]
        self.assertIn("flowchart TD", main)
        self.assertLess(main.index("G5"), main.index("N6"),
                        "G0–G5 应左移到 N6 之前（门禁左移）")


class TestGatePeriodWiring(unittest.TestCase):
    """两级 gate-period 接线（optimization_gate）。"""

    def test_placeholders_and_defaults(self):
        mod = _load_gate_module()
        self.assertEqual(mod.DEFAULT_GATE_PERIOD, "2026-12")
        self.assertEqual(mod.DEFAULT_SOURCE_GATE_PERIOD, "2027-01")
        by_name = {n: cmd for n, cmd, _w in mod.CHECKS}
        self.assertIn("__SOURCE_GATE__", by_name["source_check"])
        for gate in ("research_kernel", "info_density", "fact_card", "decision_hub"):
            self.assertIn("__GATE__", by_name[gate])

    def test_resolve_checks_propagates_both_periods(self):
        mod = _load_gate_module()
        resolved = dict(mod.resolve_checks(["source_check", "info_density"],
                                          gate_period="2030-01", source_gate_period="2031-01"))
        self.assertIn("2031-01", resolved["source_check"])
        self.assertNotIn("__SOURCE_GATE__", resolved["source_check"])
        self.assertIn("2030-01", resolved["info_density"])
        self.assertNotIn("__GATE__", resolved["info_density"])

    def test_cli_accepts_source_gate_period(self):
        r = subprocess.run([sys.executable, "engine/tools/optimization_gate.py",
                            "--only", "metric_registry", "--source-gate-period", "2026-12"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
