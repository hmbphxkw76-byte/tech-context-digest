#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""优化流程统一门禁（optimization_gate）。

把「入口可拦 · 出口可信」优化清单（P0/P1/P2）涉及的全部确定性检查
收敛为**单一入口**，供所有后续阶段复用，避免各工作流各写一套导致口径漂移：

    python engine/tools/optimization_gate.py                      # 全部门禁
    python engine/tools/optimization_gate.py --only source_check,metric_registry
    python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01
    python engine/tools/optimization_gate.py --json
    python engine/tools/optimization_gate.py --list

gate-period 分两级（显式、可分别覆盖，避免单一 flag 语义含糊）：
  - 内容门禁（research_kernel / info_density / fact_card / decision_hub）
    用 --gate-period；
  - 来源登记门禁（source_check）用 --source-gate-period。
两级都遵循「历史报告 [W] 不追溯 / 新报告 [E] 阻断」。

默认值 `auto`（滚动基线，见 gate_period.py）：解析为「当前自然月」，
使新报告判定**不随时间失效**——写死的常量会让「新报告」在若干月后自动变成
「历史」而降级放行。显式传 YYYY-MM / YYYY-Qn / YYYY 可固定口径复现。

退出码（与仓库门禁约定一致）：0 通过；1 存在错误项（阻断）；2 仅警告项（不阻断）。

复用矩阵（后续阶段 → 本入口）：
    ci.yml / scheduled-maintenance.yml / content-update.yml → 步骤调用
    repo_sync run --gate                                      → 提交前调用
    audit.yml（fail-fast）→ audit_tool verify 内已复用 source_check
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_period import AUTO  # noqa: E402
from gate_period import describe as describe_period

ROOT = Path(__file__).resolve().parents[2]
TOOLS = "engine/tools"

# name -> (命令, 是否容忍 exit 2 警告)
# 周期占位符：__GATE__ = 内容门禁周期；__SOURCE_GATE__ = 来源登记门禁周期。
CHECKS: list[tuple[str, list[str], bool]] = [
    ("validate", [sys.executable, f"{TOOLS}/validate.py"], True),
    ("validate_layout", [sys.executable, f"{TOOLS}/validate_layout.py"], True),
    ("lint", [sys.executable, f"{TOOLS}/lint_reports.py"], True),
    ("compliance", [sys.executable, f"{TOOLS}/compliance_check.py", "--check"], True),
    ("classify", [sys.executable, f"{TOOLS}/classify_reports.py", "--check", "--unknown-warn"], True),
    ("period_check", [sys.executable, f"{TOOLS}/period_check.py"], True),
    ("region_topics", [sys.executable, f"{TOOLS}/ensure_region_topics.py", "--check"], True),
    ("links", [sys.executable, f"{TOOLS}/check_links.py"], False),
    ("hub", [sys.executable, f"{TOOLS}/build_hub.py", "--check"], False),
    ("page_build", [sys.executable, f"{TOOLS}/page_build_check.py"], True),
    ("source_check", [sys.executable, f"{TOOLS}/source_check.py", "--gate-period", "__SOURCE_GATE__"], True),
    ("metric_registry", [sys.executable, f"{TOOLS}/metric_registry.py", "check"], False),
    ("metric_audit", [sys.executable, f"{TOOLS}/metric_registry.py", "audit", "--coverage"], True),
    ("release_calendar", [sys.executable, f"{TOOLS}/release_calendar.py", "--check"], True),
    ("publish_fingerprint", [sys.executable, f"{TOOLS}/publish_fingerprint.py", "--check"], True),
    ("semantic_diff", [sys.executable, f"{TOOLS}/semantic_diff.py", "scan"], True),
    ("perf_monitor", [sys.executable, f"{TOOLS}/perf_monitor.py", "check"], True),
    ("research_kernel", [sys.executable, f"{TOOLS}/research_kernel_check.py", "--gate-period", "__GATE__"], True),
    ("info_density", [sys.executable, f"{TOOLS}/info_density_check.py", "--gate-period", "__GATE__"], True),
    ("fact_card", [sys.executable, f"{TOOLS}/fact_card_check.py", "--gate-period", "__GATE__"], True),
    ("decision_hub", [sys.executable, f"{TOOLS}/decision_hub_check.py", "--gate-period", "__GATE__"], True),
    ("blind_spot", [sys.executable, f"{TOOLS}/blind_spot_check.py"], True),
    ("vocab_drift", [sys.executable, f"{TOOLS}/vocab_drift_check.py"], True),
    # 静态检查（Phase 3.1）：默认 [W]，稳定后评 [E]。仅适配退出码，规则见 pyproject.toml。
    ("ruff", [sys.executable, f"{TOOLS}/static_check.py", "ruff"], True),
    ("mypy", [sys.executable, f"{TOOLS}/static_check.py", "mypy"], True),
    # 监测渲染规范机械项（MON-01..05）：规范有、门禁不查缺口接线，默认 [W]。
    ("monitoring_render", [sys.executable, f"{TOOLS}/monitoring_render_check.py"], True),
    # 看板-台账一致与版本治理（LC-01..02 / VG-01..02），默认 [W]。
    ("consistency", [sys.executable, f"{TOOLS}/consistency_check.py"], True),
    # 命名规范全量扫描（NC-01..02），默认 [W]。
    ("naming", [sys.executable, f"{TOOLS}/naming_check.py"], True),
    # 提示词一致性（PC-01..03）：注册表 / 复述规范 / 周期模板齐备，默认 [W]。
    ("prompt_consistency", [sys.executable, f"{TOOLS}/prompt_consistency_check.py"], True),
    # 模型契约（MC-01..05，DC-07 / P1-13）：参数区间 / 假设留痕 / 失败上报，默认 [W]。
    ("model_contract", [sys.executable, f"{TOOLS}/model_contract_check.py"], True),
]

# 两级 gate-period 默认值（见模块 docstring）：auto = 滚动基线（当前自然月）
DEFAULT_GATE_PERIOD = AUTO
DEFAULT_SOURCE_GATE_PERIOD = AUTO

# 单项门禁 wall 上限（秒）：任一检查挂起（如网络探测）不得无限阻塞统一入口。
# 探测类（source_check --probe）实测可达数分钟，故上限取宽松值，只拦真正挂死。
DEFAULT_CHECK_TIMEOUT = 900
TIMEOUT_EXIT_CODE = 124


def resolve_checks(names: list[str] | None = None, gate_period: str = DEFAULT_GATE_PERIOD,
                   source_gate_period: str = DEFAULT_SOURCE_GATE_PERIOD) -> list[tuple[str, list[str]]]:
    """-> [(name, 解析后的命令)]（周期占位符 __GATE__ / __SOURCE_GATE__ 已替换）。

    纯函数，供单测直接断言两级 gate-period 的接线。
    """
    selected = [c for c in CHECKS if not names or c[0] in names]
    out: list[tuple[str, list[str]]] = []
    for name, cmd, _warn in selected:
        cmd = [source_gate_period if a == "__SOURCE_GATE__"
               else gate_period if a == "__GATE__" else a for a in cmd]
        out.append((name, cmd))
    return out


def run_checks(names: list[str] | None = None, gate_period: str = DEFAULT_GATE_PERIOD,
               source_gate_period: str = DEFAULT_SOURCE_GATE_PERIOD,
               quiet: bool = False, probe: bool = False,
               timeout: int = DEFAULT_CHECK_TIMEOUT) -> dict:
    """顺序执行门禁 -> 报告字典（确定性，无时间戳）。

    probe=True 时给 source_check 追加 --probe（R6 死链真阻断，与 ci/audit 同口径）。
    timeout 为单项 wall 上限（秒）；超时按错误处理（退出码 124），不向上崩溃。
    """
    results = []
    errors = warnings = 0
    for name, cmd in resolve_checks(names, gate_period, source_gate_period):
        warn_ok = next(w for n, _c, w in CHECKS if n == name)
        if probe and name == "source_check" and "--probe" not in cmd:
            # lenient（CI 口径）：明确 4xx/5xx 死链阻断，网络超时/反爬仅告警
            cmd = [*cmd, "--probe", "--probe-lenient"]
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
            code = r.returncode
            out = (r.stdout or "") + (r.stderr or "")
        except subprocess.TimeoutExpired as e:
            code = TIMEOUT_EXIT_CODE
            partial = e.stdout or e.stderr or ""
            if isinstance(partial, bytes):
                partial = partial.decode("utf-8", "replace")
            out = (f"[E] 门禁执行超时（>{timeout}s）：{' '.join(cmd)}\n" + partial)
        if code == 0:
            status = "ok"
        elif code == 2 and warn_ok:
            status = "warn"
            warnings += 1
        else:
            status = "error"
            errors += 1
        results.append({"name": name, "code": code, "status": status, "output": out})
        if not quiet:
            tail = [ln for ln in out.strip().splitlines() if ln.strip()][-3:]
            print(f"[{status.upper():<5}] {name} (exit {code})")
            for ln in tail:
                print(f"         {ln}")
    return {"checks": results, "errors": errors, "warnings": warnings}


def main() -> int:
    ap = argparse.ArgumentParser(description="优化流程统一门禁（单一入口）")
    ap.add_argument("--only", help="只跑指定门禁（逗号分隔）")
    ap.add_argument("--gate-period", default=DEFAULT_GATE_PERIOD,
                    help="内容门禁（研究内核/信息分层/事实卡片/决策交付）新报告判定周期下限；"
                         "默认 auto = 滚动基线（当前月 + 1），可显式传 YYYY-MM / YYYY-Qn / YYYY")
    ap.add_argument("--source-gate-period", default=DEFAULT_SOURCE_GATE_PERIOD,
                    help="来源登记门禁（source_check）新报告判定周期下限；默认 auto = 滚动基线")
    ap.add_argument("--json", action="store_true", help="输出 JSON 报告")
    ap.add_argument("--list", action="store_true", help="列出门禁清单")
    ap.add_argument("--quiet", action="store_true", help="仅输出汇总")
    ap.add_argument("--probe", action="store_true",
                    help="source_check 启用外部 URL 探测（R6 死链真阻断，与 ci/audit 同口径）")
    ap.add_argument("--timeout", type=int, default=DEFAULT_CHECK_TIMEOUT,
                    help=f"单项门禁 wall 上限（秒，默认 {DEFAULT_CHECK_TIMEOUT}；超时按错误处理）")
    args = ap.parse_args()

    if args.list:
        for name, cmd, warn_ok in CHECKS:
            ph = next((a for a in cmd if a in ("__GATE__", "__SOURCE_GATE__")), "")
            period = {"__GATE__": args.gate_period,
                      "__SOURCE_GATE__": args.source_gate_period}.get(ph, "-")
            shown = describe_period(period) if period != "-" else "-"
            print(f"{name:<18} warn_ok={warn_ok}  gate={shown:<16}  {' '.join(cmd)}")
        return 0

    names = [s.strip() for s in args.only.split(",")] if args.only else None
    if names:
        known = {c[0] for c in CHECKS}
        unknown = [n for n in names if n not in known]
        if unknown:
            print(f"[ERROR] 未知门禁：{', '.join(unknown)}（--list 查看清单）")
            return 1

    rep = run_checks(names, gate_period=args.gate_period,
                     source_gate_period=args.source_gate_period,
                     quiet=args.quiet or args.json, probe=args.probe,
                     timeout=args.timeout)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        if rep["errors"]:
            return 1
        return 2 if rep["warnings"] else 0
    if args.quiet:
        print(f"[SUMMARY] errors={rep['errors']} warnings={rep['warnings']}")
    if rep["errors"]:
        print(f"优化流程门禁失败：{rep['errors']} 项错误（阻断）")
        return 1
    if rep["warnings"]:
        print(f"优化流程门禁：{rep['warnings']} 项警告（不阻断）")
        return 2
    print("优化流程门禁通过：全部门禁 0 错误")
    return 0


if __name__ == "__main__":
    sys.exit(main())
