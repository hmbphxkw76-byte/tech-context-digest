#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""报告全流程编排器（pipeline_runner）。

严格对齐 `engine/docs/report-pipeline-system.md` §1.1 流程图：

    N0 → G0 → N1 → G1 → N2 → G2 → N3 → G3 → N4 → G4 → N5 → G5
    → N6（兜底）→ G6 → N7 → G7 → N8 → G8
    闭环 L1：N8 --心跳/任务清单/复审（异步）--> N1
    闭环 L2：G6 --E 阻断·退回生成--> N4

**薄编排层**：不重写任何校验逻辑。
- 节点层：按 `pipeline_manifest.json` 声明驱动（manual / tool / ci）；
- 门禁层：复用 `optimization_gate.run_checks`（28 项单一入口，同口径）；
- 契约层：`StageResult` / `GateResult` / `PipelineRun`（本模块数据结构）；
- 审计层：`pipeline_audit` 追加留痕。

核心执行逻辑（与流程图一致，无自定义分支）：
    逐节点处理 → 该节点后的门禁校验 → 通过则进入下一节点；
    不通过则按 `gate.on_fail` 精准退回，并携带上下文（门禁输出 / 失败项）。

用法：
    python engine/tools/pipeline_runner.py plan
    python engine/tools/pipeline_runner.py validate
    python engine/tools/pipeline_runner.py gate G4
    python engine/tools/pipeline_runner.py run --from N0 --to N8
    python engine/tools/pipeline_runner.py audit --run <run_id>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = TOOLS_DIR / "pipeline_manifest.json"

DEFAULT_GATE_PERIOD = "2026-12"
DEFAULT_SOURCE_GATE_PERIOD = "2027-01"

# 子进程 wall 上限（秒）：审计四环节（约 160s）与 tool 节点命令不得无限挂起。
DEFAULT_AUDIT_TIMEOUT = 600
DEFAULT_NODE_TIMEOUT = 600
TIMEOUT_EXIT_CODE = 124


# --------------------------------------------------------------------------
# 契约层：数据结构
# --------------------------------------------------------------------------
@dataclass
class StageResult:
    id: str
    name: str
    driver: str                      # manual | tool | ci
    status: str                      # done | manual | external
    detail: str = ""


@dataclass
class GateResult:
    id: str
    name: str
    after: str
    checks: list[str]
    errors: int
    warnings: int
    status: str                      # ok | warn | error | skipped
    blocked: bool
    on_fail: str
    output: list[dict] = field(default_factory=list)
    detail: str = ""                 # 异常 / 审计摘要（可审计）


@dataclass
class PipelineRun:
    run_id: str
    from_node: str
    to_node: str
    outcome: str                     # passed | blocked
    stages: list[StageResult]
    gates: list[GateResult]
    rollback_to: str | None
    audit_path: str


# --------------------------------------------------------------------------
# 清单加载与结构校验
# --------------------------------------------------------------------------
def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _gate_module():
    p = TOOLS_DIR / "optimization_gate.py"
    spec = importlib.util.spec_from_file_location("optimization_gate", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def known_checks() -> set[str]:
    return {c[0] for c in _gate_module().CHECKS}


def node_ids(manifest: dict) -> list[str]:
    return [n["id"] for n in manifest["nodes"]]


def gate_ids(manifest: dict) -> list[str]:
    return [g["id"] for g in manifest["gates"]]


def get_gate(manifest: dict, gate_id: str) -> dict:
    return next(g for g in manifest["gates"] if g["id"] == gate_id)


def gate_after(manifest: dict, node_id: str) -> dict | None:
    for g in manifest["gates"]:
        if g["after"] == node_id:
            return g
    return None


def resolve_checks(manifest: dict, gate: dict) -> list[str]:
    """把 gate.checks（含 '*'）展开为具体门禁名。'*' = 统一门禁全量 28 项。"""
    names = gate.get("checks", [])
    if names == ["*"]:
        return sorted(known_checks())
    return list(names)


def validate_manifest(manifest: dict) -> list[str]:
    """结构校验：返回问题列表（空 = 通过）。"""
    problems: list[str] = []
    nodes = node_ids(manifest)
    gates = gate_ids(manifest)
    if len(nodes) != len(set(nodes)):
        problems.append("节点 id 重复")
    if len(gates) != len(set(gates)):
        problems.append("门禁 id 重复")

    for g in manifest["gates"]:
        if g["after"] not in nodes:
            problems.append(f"{g['id']}.after 指向不存在的节点 {g['after']}")
        if g["on_fail"] not in nodes:
            problems.append(f"{g['id']}.on_fail 指向不存在的节点 {g['on_fail']}")
        for c in g.get("checks", []):
            if c != "*" and c not in known_checks():
                problems.append(f"{g['id']} 引用未知门禁 {c}")

    for lp in manifest.get("loops", []):
        if lp["from"] not in nodes + gates:
            problems.append(f"闭环 {lp['id']}.from 无效：{lp['from']}")
        if lp["to"] not in nodes + gates:
            problems.append(f"闭环 {lp['id']}.to 无效：{lp['to']}")

    # 流程图硬性对齐：两条闭环的触发条件与路径不得改动
    l1 = next((l for l in manifest.get("loops", []) if l["id"] == "L1"), None)
    l2 = next((l for l in manifest.get("loops", []) if l["id"] == "L2"), None)
    if not l1 or (l1["from"], l1["to"], l1["mode"]) != ("N8", "N1", "async"):
        problems.append("闭环 L1 必须为 N8 --异步--> N1")
    if not l2 or (l2["from"], l2["to"], l2["mode"]) != ("G6", "N4", "sync"):
        problems.append("闭环 L2 必须为 G6 --同步--> N4")
    return problems


# --------------------------------------------------------------------------
# 渲染：由清单生成流程图（图与清单同源，保证 100% 对齐）
# --------------------------------------------------------------------------
def render_flow(manifest: dict) -> str:
    lines = ["flowchart TD"]
    for n in manifest["nodes"]:
        lines.append(f'    {n["id"]}["{n["id"]} {n["name"]}"]')
        g = gate_after(manifest, n["id"])
        if g:
            lines.append(f'    {n["id"]} --> {g["id"]}["{g["id"]} {g["name"]}"]')
            nxt = next((x for x in manifest["nodes"] if x["id"] > n["id"]), None)
            if nxt:
                lines.append(f'    {g["id"]} -->|通过| {nxt["id"]}')
    for lp in manifest.get("loops", []):
        label = " / ".join(lp.get("triggers", []))
        lines.append(f'    {lp["from"]} -. "{label}" .-> {lp["to"]}')
    return "\n".join(lines)


# --------------------------------------------------------------------------
# 执行层
# --------------------------------------------------------------------------
def _run_command(cmd: str, timeout: int = DEFAULT_AUDIT_TIMEOUT) -> tuple[int, str]:
    """执行外部命令（如审计四环节），返回 (退出码, 输出)。

    退出码约定（全仓一致）：0=通过，1=错误（阻断），2=警告（不阻断）。
    以字节捕获并按 utf-8 容错解码，兼容 Windows 控制台 GBK 输出。
    timeout 为 wall 上限（秒）；超时按错误（124）处理，不向上崩溃。
    """
    import subprocess
    try:
        r = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, timeout=timeout)
        out = ((r.stdout or b"").decode("utf-8", "replace")
               + (r.stderr or b"").decode("utf-8", "replace"))
        return r.returncode, out
    except subprocess.TimeoutExpired as e:
        partial = e.stdout or e.stderr or b""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", "replace")
        return TIMEOUT_EXIT_CODE, f"[E] 命令执行超时（>{timeout}s）：{cmd}\n{partial}"
    except Exception as e:  # noqa: BLE001
        return 1, f"{type(e).__name__}: {e}"


def run_gate(manifest: dict, gate_id: str, gate_period: str = DEFAULT_GATE_PERIOD,
             source_gate_period: str = DEFAULT_SOURCE_GATE_PERIOD,
             probe: bool | None = None, quiet: bool = True) -> GateResult:
    """执行单个门禁：统一入口检查 + （可选）审计四环节。

    异常处理：统一门禁检查抛错或审计命令退出码 1 计为 1 个 error（阻断）；
    审计命令退出码 2（警告）计为 warning，不阻断。不向上崩溃。
    """
    gate = get_gate(manifest, gate_id)
    checks = resolve_checks(manifest, gate)
    use_probe = gate.get("probe", False) if probe is None else probe
    errors = warnings = 0
    output: list[dict] = []
    detail = ""

    if checks:
        try:
            rep = _gate_module().run_checks(names=checks, gate_period=gate_period,
                                            source_gate_period=source_gate_period,
                                            quiet=quiet, probe=use_probe)
            errors, warnings, output = rep["errors"], rep["warnings"], list(rep["checks"])
        except Exception as e:  # noqa: BLE001
            errors += 1
            output.append({"name": "gate_exception", "status": "error",
                           "items": [f"{type(e).__name__}: {e}"]})
            detail = f"门禁执行异常：{type(e).__name__}: {e}"

    audit_cmd = (gate.get("audit") or {}).get("command")
    if audit_cmd:
        rc, out = _run_command(audit_cmd)
        st = "ok" if rc == 0 else ("warn" if rc == 2 else "error")
        output.append({"name": "audit_tool", "status": st, "items": [out[-2000:]]})
        if st == "error":
            errors += 1
            detail = (detail + "；" if detail else "") + "审计四环节未通过"
        elif st == "warn":
            warnings += 1

    if not checks and not audit_cmd:
        status = "skipped"
    else:
        status = "error" if errors else ("warn" if warnings else "ok")
    return GateResult(id=gate_id, name=gate["name"], after=gate["after"], checks=checks,
                      errors=errors, warnings=warnings, status=status,
                      blocked=errors > 0, on_fail=gate["on_fail"],
                      output=output, detail=detail)


def run_node(manifest: dict, node_id: str, command: str | None = None,
             timeout: int = DEFAULT_NODE_TIMEOUT) -> StageResult:
    """节点处理。manual / ci 由 Agent / CI 完成并登记；tool 节点可经 command 执行。"""
    node = next(n for n in manifest["nodes"] if n["id"] == node_id)
    driver = node.get("driver", "manual")
    if command:
        import subprocess
        try:
            r = subprocess.run(command, shell=True, cwd=ROOT, capture_output=True,
                               text=True, timeout=timeout)
            status = "done" if r.returncode == 0 else "error"
            detail = (r.stdout or "") + (r.stderr or "")
        except subprocess.TimeoutExpired:
            status = "error"
            detail = f"[E] 节点命令执行超时（>{timeout}s）：{command}"
        return StageResult(id=node_id, name=node["name"], driver=driver,
                           status=status, detail=detail[-2000:])
    status = {"manual": "manual", "ci": "external"}.get(driver, "done")
    return StageResult(id=node_id, name=node["name"], driver=driver, status=status,
                       detail=f"driver={driver}；工具：{', '.join(node.get('tools', []))}")


def run_pipeline(manifest: dict, from_node: str = "N0", to_node: str = "N8",
                 gate_period: str = DEFAULT_GATE_PERIOD,
                 source_gate_period: str = DEFAULT_SOURCE_GATE_PERIOD,
                 audit=True, probe: bool | None = None) -> PipelineRun:
    """按流程图串行执行：节点 → 门禁 → 通过则下一节点 / 不通过则精准退回。"""
    import pipeline_audit  # noqa: PLW0406（同目录模块）

    ids = node_ids(manifest)
    start, end = ids.index(from_node), ids.index(to_node)
    run_id = uuid.uuid4().hex[:12]
    stages: list[StageResult] = []
    gates: list[GateResult] = []
    rollback_to: str | None = None
    outcome = "passed"

    if audit:
        pipeline_audit.append({"run_id": run_id, "kind": "run_start",
                               "from": from_node, "to": to_node,
                               "gate_period": gate_period,
                               "source_gate_period": source_gate_period})

    for node_id in ids[start:end + 1]:
        st = run_node(manifest, node_id)
        stages.append(st)
        if audit:
            pipeline_audit.append({"run_id": run_id, "kind": "stage", **asdict(st)})

        gate = gate_after(manifest, node_id)
        if gate is None:
            continue
        g = run_gate(manifest, gate["id"], gate_period, source_gate_period, probe=probe)
        gates.append(g)
        if audit:
            pipeline_audit.append({"run_id": run_id, "kind": "gate", **asdict(g)})

        if g.blocked:
            outcome = "blocked"
            rollback_to = g.on_fail
            if audit:
                pipeline_audit.append({"run_id": run_id, "kind": "route",
                                       "from": g.id, "to": rollback_to,
                                       "reason": "E 阻断", "checks": g.checks,
                                       "errors": g.errors})
            break

    if audit and outcome == "passed":
        l1 = next((l for l in manifest.get("loops", []) if l["id"] == "L1"), None)
        if l1:
            pipeline_audit.append({"run_id": run_id, "kind": "loop", "id": l1["id"],
                                   "from": l1["from"], "to": l1["to"],
                                   "mode": l1["mode"], "triggers": l1.get("triggers", [])})

    if audit:
        pipeline_audit.append({"run_id": run_id, "kind": "run_end",
                               "outcome": outcome, "rollback_to": rollback_to})

    return PipelineRun(run_id=run_id, from_node=from_node, to_node=to_node,
                       outcome=outcome, stages=stages, gates=gates,
                       rollback_to=rollback_to, audit_path=str(pipeline_audit.AUDIT_PATH))


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="报告全流程编排器（严格对齐 §1.1 流程图）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("plan", help="由清单渲染流程图")
    sub.add_parser("validate", help="校验清单结构")

    g = sub.add_parser("gate", help="执行单个门禁")
    g.add_argument("gate_id")
    g.add_argument("--gate-period", default=DEFAULT_GATE_PERIOD)
    g.add_argument("--source-gate-period", default=DEFAULT_SOURCE_GATE_PERIOD)
    g.add_argument("--probe", action=argparse.BooleanOptionalAction, default=None,
                   help="source_check 是否启用 URL 探测；缺省（不传）尊重清单 gate.probe 字段")

    r = sub.add_parser("run", help="按流程图串行执行")
    r.add_argument("--from", dest="from_node", default="N0")
    r.add_argument("--to", dest="to_node", default="N8")
    r.add_argument("--gate-period", default=DEFAULT_GATE_PERIOD)
    r.add_argument("--source-gate-period", default=DEFAULT_SOURCE_GATE_PERIOD)
    r.add_argument("--no-audit", action="store_true")
    r.add_argument("--probe", action=argparse.BooleanOptionalAction, default=None,
                   help="覆盖清单 probe 语义；缺省（不传）尊重清单 gate.probe 字段")

    a = sub.add_parser("audit", help="查询审计留痕")
    a.add_argument("--run", dest="run_id")
    a.add_argument("--tail", type=int, default=20)

    args = ap.parse_args()
    manifest = load_manifest()

    if args.cmd == "plan":
        print(render_flow(manifest))
        return 0

    if args.cmd == "validate":
        problems = validate_manifest(manifest)
        if problems:
            for p in problems:
                print(f"[E] {p}")
            return 1
        print(f"[OK] 清单结构校验通过：{len(node_ids(manifest))} 节点 / "
              f"{len(gate_ids(manifest))} 门禁 / {len(manifest.get('loops', []))} 闭环")
        return 0

    if args.cmd == "gate":
        res = run_gate(manifest, args.gate_id, args.gate_period,
                       args.source_gate_period, probe=args.probe)
        print(json.dumps(asdict(res), ensure_ascii=False, indent=2))
        return 1 if res.blocked else 0

    if args.cmd == "run":
        run = run_pipeline(manifest, args.from_node, args.to_node,
                           args.gate_period, args.source_gate_period,
                           audit=not args.no_audit, probe=args.probe)
        print(json.dumps({k: v for k, v in asdict(run).items() if k != "audit_path"},
                         ensure_ascii=False, indent=2, default=str))
        print(f"[audit] {run.audit_path}（run_id={run.run_id}）")
        if run.outcome == "blocked":
            print(f"[BLOCKED] 门禁未通过，按流程图退回 {run.rollback_to}")
            return 1
        print("[PASSED] 全流程通过")
        return 0

    if args.cmd == "audit":
        import pipeline_audit
        if args.run_id:
            for row in pipeline_audit.read_run(args.run_id):
                print(json.dumps(row, ensure_ascii=False))
        else:
            for row in pipeline_audit.tail(args.tail):
                print(json.dumps(row, ensure_ascii=False))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
