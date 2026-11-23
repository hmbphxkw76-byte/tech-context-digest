#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""本地等价 CI（本地优先 · 远程兜底 · 结果分享）。

复刻 .github/workflows 中**本地可跑**的确定性检查（ci.yml / audit.yml /
html-sync.yml / scheduled-maintenance.yml 的检查类步骤），一条命令跑完并汇总。

原则：
  - 本地能跑的，一律本地跑（快、可复跑、无副作用）；
  - 本地环境不具备的才远程跑（自动开 PR / webhook 告警 / GitHub runner 环境 / secrets）；
  - 结果落盘 + Markdown 摘要，随任务 PR 提交或贴 PR 描述，保持可追溯分享。

用法：
    python engine/tools/local_ci.py run                            # 人类可读汇总
    python engine/tools/local_ci.py run --json                     # JSON 到 stdout
    python engine/tools/local_ci.py run --markdown                 # Markdown 摘要
    python engine/tools/local_ci.py run --emit engine/audit/records/local-ci-status.json
    python engine/tools/local_ci.py run --only syntax,gate,page_build
    python engine/tools/local_ci.py list                           # 列出检查项与远程分工

退出码：0 全部通过；2 仅警告（无错误）；1 存在错误项；3 用法 / 执行错误。

本工具是**编排层**，不新增门禁项（统一门禁仍为 optimization_gate 的 32 项）。
规范见 engine/docs/local-ci-runbook.md。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402
from gate_period import resolve as resolve_period  # noqa: E402

SCHEMA_VERSION = "1.0"
EMIT_DEFAULT = ROOT / "engine" / "audit" / "records" / "local-ci-status.json"
CHECK_TIMEOUT = 900  # 单检查项超时（秒）


@dataclass(frozen=True)
class Check:
    """一项本地等价检查。"""

    id: str
    name: str
    ci: str
    cmd: tuple[str, ...]
    note: str = ""

    def cmd_with(self, branch: str) -> tuple[str, ...]:
        """按当前分支替换 `--branch main`（历史审计按实际分支）。"""
        return tuple(branch if a == "main" else a for a in self.cmd)


PY = sys.executable
CHECKS: tuple[Check, ...] = (
    Check("syntax", "语法编译", "ci.syntax", (PY, "-m", "compileall", "-q", "engine")),
    Check("unittest", "单元测试", "ci.test", (PY, "-m", "unittest", "discover", "-s", "engine/tests")),
    Check(
        "gate",
        "统一门禁",
        "ci.validate",
        # 本地不启用 --probe（外网死链探测）：网络不稳定时挂死；该环节归远程。
        (PY, "engine/tools/optimization_gate.py", "--gate-period", "auto",
         "--source-gate-period", "auto"),
    ),
    Check("runner", "端到端编排校验", "ci.validate", (PY, "engine/tools/pipeline_runner.py", "validate")),
    Check("history", "main 首亲历史审计", "ci.history-audit",
          (PY, "engine/tools/git_history_audit.py", "--branch", "main")),
    Check("hub", "HTML 同步校验", "html-sync.validate", (PY, "engine/tools/build_hub.py", "--check")),
    Check("page_build", "页面构建门禁", "门禁.page_build", (PY, "engine/tools/page_build_check.py")),
    Check("fingerprint", "发布指纹校验", "maintenance", (PY, "engine/tools/publish_fingerprint.py", "--check")),
    Check("ledger", "核验台账链校验", "maintenance", (PY, "engine/tools/verification_ledger.py", "verify")),
    Check("audit", "审计四环节", "audit",
          (PY, "engine/audit/scripts/audit_tool.py", "run", "--strict", "--dry-run")),
    Check("audit_status", "审计登记状态", "maintenance", (PY, "engine/audit/scripts/audit_tool.py", "status")),
    Check("l3", "L3 SLA 超期检测", "maintenance", (PY, "engine/audit/scripts/audit_tool.py", "l3-status")),
    Check("compliance", "报告合规校验", "maintenance", (PY, "engine/tools/compliance_check.py", "--check")),
    Check("review", "来源定期复核", "maintenance",
          (PY, "engine/audit/scripts/audit_tool.py", "verify-review", "--period", "auto")),
)

# 本地环境不具备、只能远程跑的环节（不在本地等价集内）。
REMOTE_ONLY: tuple[tuple[str, str], ...] = (
    ("probe", "链接可达率探测（source_check --probe / 门禁 --probe，依赖外网，不稳定）"),
    ("submit-pr", "工作流内门禁通过后立即合并（无需额外凭据）"),
    ("webhook-alert", "外部告警通道（需 webhook 凭据）"),
    ("runner-env", "GitHub runner 环境 / secrets / 服务端保护"),
)


def current_branch() -> str:
    """当前 git 分支（读不到时返回 ``unknown``）。"""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
        )
        return proc.stdout.strip() or "unknown"
    except OSError:
        return "unknown"


def status_for_exit(code: int) -> str:
    """退出码 -> 状态。0 通过 / 2 仅警告 / 其余失败。"""
    if code == 0:
        return "pass"
    if code == 2:
        return "warn"
    return "fail"


def _last_line(text: str) -> str:
    for line in reversed(text.strip().splitlines()):
        if line.strip():
            return line.strip()
    return ""


def run_check(check: Check, branch: str) -> dict:
    """执行单项检查，返回结果字典（确定性：不含时间戳 / 时长）。"""
    try:
        proc = subprocess.run(
            list(check.cmd_with(branch)),
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=CHECK_TIMEOUT,
        )
        code, output = proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        code, output = 1, f"超时（>{CHECK_TIMEOUT}s）"
    except OSError as exc:  # 命令无法启动
        code, output = 1, f"无法执行：{exc}"
    return {
        "id": check.id,
        "name": check.name,
        "ci": check.ci,
        "exit_code": code,
        "status": status_for_exit(code),
        "summary": _last_line(output),
    }


def select(checks: tuple[Check, ...], only: str = "", skip: str = "") -> tuple[Check, ...]:
    ids = {c.id for c in checks}
    want = [s.strip() for s in only.split(",") if s.strip()]
    drop = {s.strip() for s in skip.split(",") if s.strip()}
    unknown = (set(want) | drop) - ids
    if unknown:
        raise SystemExit(f"未知检查项：{sorted(unknown)}；可用：{sorted(ids)}")
    out = [c for c in checks if c.id in set(want)] if want else list(checks)
    return tuple(c for c in out if c.id not in drop)


def overall(results: list[dict]) -> int:
    if any(r["status"] == "fail" for r in results):
        return 1
    if any(r["status"] == "warn" for r in results):
        return 2
    return 0


def build_document(results: list[dict], branch: str, period: str) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "comment": "本地等价 CI 结果（确定性，无时间戳）。由 local_ci.py run --emit 生成。",
        "branch": branch,
        "gate_period": period,
        "checks": results,
        "summary": {
            "total": len(results),
            "pass": sum(1 for r in results if r["status"] == "pass"),
            "warn": sum(1 for r in results if r["status"] == "warn"),
            "fail": sum(1 for r in results if r["status"] == "fail"),
        },
    }


def render_text(results: list[dict], branch: str, period: str) -> str:
    lines = [f"本地等价 CI（本地优先 · 远程兜底）· 分支 {branch} · gate-period {period}"]
    for r in results:
        mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[r["status"]]
        tail = f" — {r['summary']}" if r["summary"] else ""
        lines.append(f"  [{mark}] {r['id']:<13} {r['name']}（{r['ci']}）{tail}")
    s = build_document(results, branch, period)["summary"]
    lines.append(f"汇总：{s['total']} 项，通过 {s['pass']} / 警告 {s['warn']} / 失败 {s['fail']}")
    return "\n".join(lines)


def render_markdown(results: list[dict], branch: str, period: str) -> str:
    s = build_document(results, branch, period)["summary"]
    lines = [
        "## 本地等价 CI 结果",
        "",
        f"- 分支：`{branch}`；gate-period：`{period}`",
        f"- 汇总：**{s['total']} 项，通过 {s['pass']} / 警告 {s['warn']} / 失败 {s['fail']}**",
        "",
        "| # | 检查 | 对应 CI | 状态 | 摘要 |",
        "|---|---|---|---|---|",
    ]
    for i, r in enumerate(results, 1):
        mark = {"pass": "✅ 通过", "warn": "⚠️ 警告", "fail": "❌ 失败"}[r["status"]]
        lines.append(f"| {i} | {r['name']} (`{r['id']}`) | {r['ci']} | {mark} | {r['summary']} |")
    lines += [
        "",
        "### 本地未覆盖（仅远程）",
        "",
    ]
    for name, desc in REMOTE_ONLY:
        lines.append(f"- `{name}`：{desc}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="本地等价 CI（本地优先 · 远程兜底）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="跑检查集")
    run.add_argument("--only", default="", help="只跑指定 id（逗号分隔）")
    run.add_argument("--skip", default="", help="跳过指定 id（逗号分隔）")
    run.add_argument("--json", action="store_true", help="JSON 输出到 stdout")
    run.add_argument("--markdown", action="store_true", help="Markdown 输出到 stdout")
    run.add_argument("--emit", default="", help="结果 JSON 落盘路径")
    sub.add_parser("list", help="列出检查项与远程分工")
    args = ap.parse_args(argv)

    if args.cmd == "list":
        print("本地等价检查：")
        for c in CHECKS:
            print(f"  {c.id:<13} {c.name}（{c.ci}）")
        print("仅远程：")
        for name, desc in REMOTE_ONLY:
            print(f"  {name:<13} {desc}")
        return 0

    try:
        chosen = select(CHECKS, args.only, args.skip)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 3

    branch = current_branch()
    period = resolve_period("auto")
    results = [run_check(c, branch) for c in chosen]

    if args.json:
        print(json.dumps(build_document(results, branch, period), ensure_ascii=False, indent=2))
    elif args.markdown:
        print(render_markdown(results, branch, period))
    else:
        print(render_text(results, branch, period))

    if args.emit:
        out = Path(args.emit)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(build_document(results, branch, period), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if not args.json and not args.markdown:
            print(f"结果已落盘：{out}")

    return overall(results)


if __name__ == "__main__":
    sys.exit(main())
