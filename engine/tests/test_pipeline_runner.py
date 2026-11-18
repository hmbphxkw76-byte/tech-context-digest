# -*- coding: utf-8 -*-
"""报告全流程编排器测试（pipeline_runner / pipeline_audit）。

锁定内容与清单、流程图一致：
- `pipeline_manifest.json`：N0–N8 九节点、G0–G8 九门禁、两条闭环（L1 N8→N1 异步、L2 G6→N4 同步）；
- 门禁 checks 必须是 `optimization_gate.CHECKS` 的子集（'*' = 全量 27 项）；
- 编排路由：通过则下一节点，E 阻断则按 `on_fail` 精准退回（G6 → N4）；
- 审计：追加式留痕，可按 run_id 还原。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))

import pipeline_audit  # noqa: E402
import pipeline_runner as pr  # noqa: E402

MANIFEST = pr.load_manifest()
REAL_CHECK_NAMES = [c[0] for c in pr._gate_module().CHECKS]


class _FakeGateModule:
    """替代表单执行：按预设结果返回 run_checks 字典。"""

    CHECKS = [(n, [], True) for n in REAL_CHECK_NAMES]

    def __init__(self, results: dict[str, str]):
        self.results = results

    def run_checks(self, names=None, gate_period=None, source_gate_period=None,
                   quiet=True, probe=False):
        errors = warnings = 0
        checks = []
        for n in names or []:
            st = self.results.get(n, "ok")
            if st == "error":
                errors += 1
            elif st == "warn":
                warnings += 1
            checks.append({"name": n, "status": st})
        return {"checks": checks, "errors": errors, "warnings": warnings}


class TestManifestGraph(unittest.TestCase):
    """清单图结构 = 流程图。"""

    def test_nine_nodes_and_gates(self):
        self.assertEqual(pr.node_ids(MANIFEST),
                         [f"N{i}" for i in range(0, 9)])
        self.assertEqual(pr.gate_ids(MANIFEST),
                         [f"G{i}" for i in range(0, 9)])

    def test_each_node_has_exactly_one_gate(self):
        afters = [g["after"] for g in MANIFEST["gates"]]
        self.assertEqual(sorted(afters), [f"N{i}" for i in range(0, 9)])
        for n in pr.node_ids(MANIFEST):
            self.assertIsNotNone(pr.gate_after(MANIFEST, n), f"{n} 缺门禁")

    def test_gate_checks_subset_of_unified_gate(self):
        for g in MANIFEST["gates"]:
            for c in g["checks"]:
                if c == "*":
                    continue
                self.assertIn(c, REAL_CHECK_NAMES, f"{g['id']} 引用未知门禁 {c}")

    def test_star_expands_to_all_23(self):
        g6 = pr.get_gate(MANIFEST, "G6")
        self.assertEqual(g6["checks"], ["*"])
        self.assertEqual(len(pr.resolve_checks(MANIFEST, g6)), len(REAL_CHECK_NAMES))

    def test_loops_exact(self):
        l1 = next(l for l in MANIFEST["loops"] if l["id"] == "L1")
        l2 = next(l for l in MANIFEST["loops"] if l["id"] == "L2")
        self.assertEqual((l1["from"], l1["to"], l1["mode"]), ("N8", "N1", "async"))
        self.assertEqual((l2["from"], l2["to"], l2["mode"]), ("G6", "N4", "sync"))

    def test_validate_manifest_ok(self):
        self.assertEqual(pr.validate_manifest(MANIFEST), [])

    def test_render_flow_matches_manifest(self):
        flow = pr.render_flow(MANIFEST)
        self.assertTrue(flow.startswith("flowchart TD"))
        for nid in pr.node_ids(MANIFEST):
            self.assertIn(nid, flow)
        for gid in pr.gate_ids(MANIFEST):
            self.assertIn(gid, flow)
        self.assertIn("N8", flow)
        self.assertIn("G6", flow)


class TestGateExecution(unittest.TestCase):
    """门禁执行复用统一入口。"""

    def test_run_gate_ok(self):
        fake = _FakeGateModule({})
        with mock.patch.object(pr, "_gate_module", return_value=fake):
            g = pr.run_gate(MANIFEST, "G0")
        self.assertEqual(g.status, "ok")
        self.assertFalse(g.blocked)
        self.assertEqual(g.checks, ["validate_layout", "validate", "region_topics"])

    def test_run_gate_blocked(self):
        fake = _FakeGateModule({"info_density": "error"})
        with mock.patch.object(pr, "_gate_module", return_value=fake):
            g = pr.run_gate(MANIFEST, "G4")
        self.assertEqual(g.status, "error")
        self.assertTrue(g.blocked)
        self.assertEqual(g.on_fail, "N4")

    def test_run_gate_skipped_when_no_checks(self):
        g = pr.run_gate(MANIFEST, "G8")
        self.assertEqual(g.status, "skipped")
        self.assertFalse(g.blocked)

    def test_run_gate_exception_blocked(self):
        """门禁工具抛错 → 计为 1 个 error（阻断），不向上崩溃。"""
        class _Boom:
            CHECKS = [(n, [], True) for n in REAL_CHECK_NAMES]

            def run_checks(self, **kwargs):
                raise RuntimeError("boom")

        with mock.patch.object(pr, "_gate_module", return_value=_Boom()):
            g = pr.run_gate(MANIFEST, "G4")
        self.assertEqual(g.status, "error")
        self.assertTrue(g.blocked)
        self.assertIn("boom", g.detail)

    def test_g6_audit_failure_blocks(self):
        """G6 审计四环节失败 → 阻断（退回 N4）。"""
        fake = _FakeGateModule({})
        with mock.patch.object(pr, "_gate_module", return_value=fake), \
             mock.patch.object(pr, "_run_command", return_value=(1, "audit failed")):
            g = pr.run_gate(MANIFEST, "G6")
        self.assertTrue(g.blocked)
        self.assertEqual(g.on_fail, "N4")
        self.assertIn("审计", g.detail)


class TestProbeSemantics(unittest.TestCase):
    """P-04 / 0.3：probe 语义必须尊重清单 gate.probe 字段（缺省不覆盖）。"""

    class _Fake:
        CHECKS = [(n, [], True) for n in REAL_CHECK_NAMES]

        def __init__(self):
            self.probe = None

        def run_checks(self, names=None, gate_period=None, source_gate_period=None,
                       quiet=True, probe=False):
            self.probe = probe
            return {"checks": [], "errors": 0, "warnings": 0}

    def test_manifest_probe_true_respected(self):
        fake = self._Fake()
        with mock.patch.object(pr, "_gate_module", return_value=fake):
            pr.run_gate(MANIFEST, "G2", probe=None)   # G2 probe:true
        self.assertIs(True, fake.probe)

    def test_manifest_probe_false_respected(self):
        fake = self._Fake()
        with mock.patch.object(pr, "_gate_module", return_value=fake):
            pr.run_gate(MANIFEST, "G0", probe=None)   # G0 probe:false
        self.assertIs(False, fake.probe)

    def test_probe_override(self):
        fake = self._Fake()
        with mock.patch.object(pr, "_gate_module", return_value=fake):
            pr.run_gate(MANIFEST, "G0", probe=True)
            self.assertIs(True, fake.probe)
            pr.run_gate(MANIFEST, "G2", probe=False)
            self.assertIs(False, fake.probe)

    @staticmethod
    def _gate_result():
        return pr.GateResult(id="G2", name="分级 / 双源 / 死链校验", after="N2",
                            checks=["source_check"], errors=0, warnings=0,
                            status="ok", blocked=False, on_fail="N2")

    def test_cli_gate_probe_default_is_none(self):
        with mock.patch.object(pr, "run_gate", return_value=self._gate_result()) as rg, \
             mock.patch.object(sys, "argv", ["pipeline_runner.py", "gate", "G2"]):
            pr.main()
        self.assertIsNone(rg.call_args.kwargs["probe"])

    def test_cli_gate_probe_flags(self):
        for flag, expected in (("--probe", True), ("--no-probe", False)):
            with mock.patch.object(pr, "run_gate", return_value=self._gate_result()) as rg, \
                 mock.patch.object(sys, "argv", ["pipeline_runner.py", "gate", "G2", flag]):
                pr.main()
            self.assertIs(expected, rg.call_args.kwargs["probe"])


class TestPipelineRouting(unittest.TestCase):
    """核心执行逻辑：通过则下一节点，E 阻断则精准退回。"""

    def test_full_pass(self):
        fake = _FakeGateModule({})
        with mock.patch.object(pr, "_gate_module", return_value=fake), \
             mock.patch.object(pr, "_run_command", return_value=(0, "")):
            run = pr.run_pipeline(MANIFEST, audit=False)
        self.assertEqual(run.outcome, "passed")
        self.assertIsNone(run.rollback_to)
        self.assertEqual(len(run.stages), 9)
        self.assertEqual(len(run.gates), 9)

    def test_g6_block_rolls_back_to_n4(self):
        # G6 = 全量 27 项；metric_audit 仅属 G6（G0–G5/G7 不含），确保阻断发生在 G6
        self.assertNotIn("metric_audit", pr.get_gate(MANIFEST, "G0")["checks"])
        fake = _FakeGateModule({"metric_audit": "error"})
        with mock.patch.object(pr, "_gate_module", return_value=fake), \
             mock.patch.object(pr, "_run_command", return_value=(0, "")):
            run = pr.run_pipeline(MANIFEST, audit=False)
        self.assertEqual(run.outcome, "blocked")
        self.assertEqual(run.rollback_to, "N4")
        # 阻断发生在 N6 的门禁，故 N7 / N8 不应被执行
        self.assertEqual([s.id for s in run.stages], [f"N{i}" for i in range(0, 7)])
        self.assertEqual(run.gates[-1].id, "G6")

    def test_g0_block_stops_at_n0(self):
        fake = _FakeGateModule({"validate_layout": "error"})
        with mock.patch.object(pr, "_gate_module", return_value=fake):
            run = pr.run_pipeline(MANIFEST, audit=False)
        self.assertEqual(run.outcome, "blocked")
        self.assertEqual(run.rollback_to, "N0")
        self.assertEqual([s.id for s in run.stages], ["N0"])


class TestSubprocessBounds(unittest.TestCase):
    """子进程 wall 上限：挂起不得无限阻塞编排。"""

    def test_run_command_timeout(self):
        cmd = f'{sys.executable} -c "import time; time.sleep(5)"'
        rc, out = pr._run_command(cmd, timeout=1)
        self.assertEqual(rc, pr.TIMEOUT_EXIT_CODE)
        self.assertIn("超时", out)

    def test_run_node_command_timeout(self):
        cmd = f'{sys.executable} -c "import time; time.sleep(5)"'
        st = pr.run_node(MANIFEST, "N3", command=cmd, timeout=1)
        self.assertEqual(st.status, "error")
        self.assertIn("超时", st.detail)


class TestAudit(unittest.TestCase):
    """审计留痕：只追加、可还原。"""

    def test_append_and_read_run(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "runs.jsonl"
            rec = pipeline_audit.append({"run_id": "r1", "kind": "run_start"}, path=path)
            pipeline_audit.append({"run_id": "r1", "kind": "gate", "id": "G0"}, path=path)
            pipeline_audit.append({"run_id": "r2", "kind": "run_start"}, path=path)
            self.assertEqual(rec["schema_version"], "1.0")
            self.assertIn("ts", rec)
            rows = pipeline_audit.read_run("r1", path=path)
            self.assertEqual([r["kind"] for r in rows], ["run_start", "gate"])
            self.assertEqual(len(pipeline_audit.read_all(path)), 3)


if __name__ == "__main__":
    unittest.main()
