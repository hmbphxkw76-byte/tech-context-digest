# -*- coding: utf-8 -*-
"""体系说明文档与两级 gate-period 一致性测试（REPORT-PIPELINE-SYSTEM v1.2）。

锁定内容与代码事实源一致：
- `engine/docs/report-pipeline-system.md` 存在、含完整 Mermaid 流程图、覆盖 N0–N8 全链路节点；
- **门禁左移**：主链各阶段配就地门禁 G0–G8，G0–G5 左移到 N6 之前，N6 为兜底；
- 文档门禁清单数量与 `optimization_gate.CHECKS` 一致（新增门禁须同步文档）；
- 两级 gate-period（内容 / 来源）在文档与代码中显式声明且接线正确；
  默认 `auto`（滚动基线 = 当前自然月），不写死周期。

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

# 现行（非历史时点）文件：门禁数量口径必须为 32 项（报告层核验接入后）。
# 历史时点报告（report-audits/*-2026-11-15/16.md）与 engine/quality/** 的
# 「21 项量化指标」为另一套口径，不在扫描范围。
GATE_COUNT_FILES = [
    ROOT / "AGENTS.md",
    ROOT / "engine" / "audit" / "verification.md",
    ROOT / "engine" / "tools" / "pipeline_runner.py",
    ROOT / "engine" / "tools" / "README.md",
    ROOT / "engine" / "tests" / "test_pipeline_runner.py",
]
GATE_COUNT_FILES += sorted((ROOT / "engine" / "docs").glob("*.md"))
GATE_COUNT_FILES += sorted((ROOT / "engine" / "report-audits").glob("mainline-adoption-*.md"))

# 声明门禁数量的现行文件（这些必须显式写「23 项」）。
GATE_COUNT_DECLARING = [
    ROOT / "AGENTS.md",
    ROOT / "engine" / "audit" / "verification.md",
    ROOT / "engine" / "tools" / "pipeline_runner.py",
    ROOT / "engine" / "tools" / "README.md",
    ROOT / "engine" / "tests" / "test_pipeline_runner.py",
    ROOT / "engine" / "docs" / "report-pipeline-system.md",
    ROOT / "engine" / "docs" / "architecture-and-pipeline-design.md",
    ROOT / "engine" / "docs" / "architecture-development-standard.md",
    ROOT / "engine" / "docs" / "end-to-end-coverage.md",
    ROOT / "engine" / "docs" / "page-build-governance.md",
    ROOT / "engine" / "docs" / "process-vs-infrastructure-governance.md",
    ROOT / "engine" / "docs" / "report-pipeline-implementation-plan.md",
    ROOT / "engine" / "report-audits" / "mainline-adoption-assessment-2026-11-17.md",
]


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
        self.assertEqual(len(names), 32, "门禁清单数量变化须同步体系文档")
        self.assertIn("32 项", self.text)
        for name in names:
            self.assertIn(name, self.text, f"文档门禁清单缺 {name}")

    def test_two_level_gate_period_declared(self):
        for kw in ("auto", "滚动", "--gate-period", "--source-gate-period"):
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


class TestGateCountConsistency(unittest.TestCase):
    """P-07 / M6：现行文档/代码不得残留陈述性「21 项 / 21 门禁」门禁口径（现为 32 项）。

    合法表述显式放行：历史基线（「基线 21 项」）与更正记录（「由 21 项更正为 23 项」）。
    扫描范围沿用 GATE_COUNT_FILES（已排除历史时点报告与 engine/quality/**）。
    """

    FORBIDDEN = re.compile(
        r"21\s*项"
        r"|21\s*门禁"
        r"|门禁\s*21\s*项"
    )
    # 合法历史 / 基线 / 更正表述：先剥离再匹配，避免误伤。
    ALLOWED = re.compile(
        r"基线\s*21\s*项?"
        r"|由\s*21\s*项?\s*更正为"
    )

    def _offender(self, text: str) -> str | None:
        m = self.FORBIDDEN.search(self.ALLOWED.sub("", text))
        return m.group(0) if m else None

    def test_no_stale_gate_count_in_current_docs(self):
        offenders = {}
        for f in GATE_COUNT_FILES:
            text = f.read_text(encoding="utf-8")
            hit = self._offender(text)
            if hit:
                offenders[str(f.relative_to(ROOT))] = hit
        self.assertEqual(offenders, {}, f"现行文件残留 21 项门禁口径：{offenders}")

    def test_forbidden_pattern_catches_stale_wording(self):
        """反恒真：FORBIDDEN 必须真的能命中陈述性残留，否则扫描无意义。"""
        for sample in ("统一门禁 21 项", "21 门禁", "门禁 21 项", "全量 21 项"):
            self.assertIsNotNone(self._offender(sample), f"未命中陈述性残留：{sample}")

    def test_allowed_baseline_wording_is_permitted(self):
        """合法基线 / 更正表述不得误报。"""
        for sample in ("基线 21 项", "（基线 21 项，Phase 3.1 起 30 项）",
                       "由 21 项更正为 30 项", "由 21 更正为 24"):
            self.assertIsNone(self._offender(sample), f"合法表述被误报：{sample}")

    def test_gate_count_declarations_are_30(self):
        mod = _load_gate_module()
        self.assertEqual(len(mod.CHECKS), 32)
        for f in GATE_COUNT_DECLARING:
            text = f.read_text(encoding="utf-8")
            self.assertIn("32 项", text, f"{f.relative_to(ROOT)} 未声明 32 项门禁")


class TestGatePeriodWiring(unittest.TestCase):
    """两级 gate-period 接线（optimization_gate）。"""

    def test_placeholders_and_defaults(self):
        mod = _load_gate_module()
        # 默认为滚动基线 auto；解析结果 = 当前自然月（不随时间失效）
        self.assertEqual(mod.DEFAULT_GATE_PERIOD, "auto")
        self.assertEqual(mod.DEFAULT_SOURCE_GATE_PERIOD, "auto")
        from gate_period import resolve
        self.assertEqual(resolve(mod.DEFAULT_GATE_PERIOD), resolve("auto"))
        self.assertNotEqual(resolve("auto"), "auto")
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
