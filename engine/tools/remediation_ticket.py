#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""闭环修正工单（remediation_ticket）。

触发条件（任一）：
  1. 统一门禁存在 [E]（optimization_gate 退出码 1）；
  2. 活跃度超阈值（automation_status activity 距上次记录 > 阈值）。

产出**标准化修正工单**：失败项明细 + 责任归属周期 + 可直接执行的复跑命令，
由工作流经 `.github/actions/remediation-ticket` 复合动作创建为 GitHub Issue（幂等）。
本工具**只建工单，不提交代码**——代码提交仍走 task/<slug> + PR 协议。

用法：
    python engine/tools/remediation_ticket.py detect --probe \
        --gate-period 2026-12 --source-gate-period 2027-01 \
        --activity-threshold 45 \
        --out .automation-tmp/remediation.json \
        --body-out .automation-tmp/remediation.md
    python engine/tools/remediation_ticket.py detect --gate-json gate.json --porcelain

退出码：0 = 触发（需建工单）；2 = 未触发；1 = 运行错误。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import optimization_gate  # noqa: E402
from update_planner import default_period  # noqa: E402

GATE_SCRIPT = TOOLS / "optimization_gate.py"
ACTIVITY_SCRIPT = TOOLS / "automation_status.py"

# 失败摘要关键词（门禁输出行）
KEY_RE = re.compile(r"\[E\]|\[ERROR\]|错误|缺失|未通过|失败|阻断|不通过|INVALID|FAIL", re.I)
# 位置（文件:行）
LOC_RE = re.compile(r"([\w./\\-]+\.(?:html|md|json|py|yml|yaml|txt)):(\d+)")
# 周期标识（YYYY-MM / YYYY-Qn）
PERIOD_RE = re.compile(r"\b(\d{4})(?:-(\d{2})|-Q([1-4]))\b")


def run_gate(gate_period: str, source_gate_period: str, probe: bool) -> dict:
    """运行统一门禁 -> 解析 JSON 报告；解析失败时回退为原始输出。"""
    cmd = [sys.executable, str(GATE_SCRIPT), "--json",
           "--gate-period", gate_period, "--source-gate-period", source_gate_period]
    if probe:
        cmd.append("--probe")
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        doc = json.loads(r.stdout)
    except (json.JSONDecodeError, TypeError):
        return {"checks": [], "errors": 0, "warnings": 0,
                "parse_error": (r.stdout or "") + (r.stderr or "")}
    doc.setdefault("parse_error", "")
    return doc


def read_activity(threshold: int) -> dict:
    """读取活跃度 -> {days, threshold, stale}；无记录返回 days=None。"""
    r = subprocess.run([sys.executable, str(ACTIVITY_SCRIPT), "activity",
                        "--threshold", str(threshold), "--porcelain"],
                       capture_output=True, text=True)
    out = (r.stdout or "").strip()
    if not out.isdigit():
        return {"days": None, "threshold": threshold, "stale": False}
    days = int(out)
    return {"days": days, "threshold": threshold, "stale": days > threshold}


def summarize(output: str, max_lines: int = 4) -> dict:
    """从门禁输出提取失败摘要与位置。"""
    lines = [line.strip() for line in (output or "").splitlines() if line.strip()]
    key = [line for line in lines if KEY_RE.search(line)]
    picked = (key or lines)[-max_lines:]
    locs: list[str] = []
    for m in LOC_RE.finditer(output or ""):
        loc = f"{m.group(1)}:{m.group(2)}"
        if loc not in locs:
            locs.append(loc)
    return {"summary": picked, "locations": locs[:5]}


def extract_failures(gate_report: dict) -> list[dict]:
    failures = []
    for c in gate_report.get("checks", []):
        if c.get("status") == "error":
            s = summarize(c.get("output", ""))
            failures.append({"name": c.get("name", "?"), **s})
    return failures


def derive_period(texts: list[str], now: datetime) -> tuple[str, str]:
    """从失败输出推断责任归属周期 -> (period, 依据)。无则回退当前周期。"""
    candidates: list[tuple[tuple[int, int], str, str]] = []
    for t in texts:
        for m in PERIOD_RE.finditer(t or ""):
            y = int(m.group(1))
            if m.group(2):
                mo = int(m.group(2))
                if 1 <= mo <= 12:
                    candidates.append(((y, mo), f"{y}-{mo:02d}", m.group(0)))
            elif m.group(3):
                q = int(m.group(3))
                candidates.append(((y, q * 3), f"{y}-Q{q}", m.group(0)))
    if candidates:
        key, label, token = max(candidates, key=lambda x: x[0])
        return label, f"失败输出中出现周期标识 `{token}`"
    return default_period(now), "失败输出未含周期标识，回退当前周期"


def check_command(name: str, gate_period: str, source_gate_period: str) -> str | None:
    """单个门禁的可直接执行复跑命令。"""
    resolved = dict(optimization_gate.resolve_checks(
        [name], gate_period, source_gate_period))
    cmd = resolved.get(name)
    if not cmd:
        return None
    return " ".join(["python", *cmd[1:]])


def build_commands(failures: list[dict], gate_period: str, source_gate_period: str) -> list[str]:
    cmds = [f"python engine/tools/optimization_gate.py --gate-period {gate_period} "
            f"--source-gate-period {source_gate_period} --probe"]
    for f in failures:
        c = check_command(f["name"], gate_period, source_gate_period)
        if c:
            cmds.append(c)
    return cmds


def render_body(data: dict) -> str:
    reasons = data["reasons"]
    period = data["period"]
    period_basis = data["period_basis"]
    failures = data["gate"]["failures"]
    activity = data["activity"]
    cmds = data["commands"]

    lines = ["## 触发原因", ""]
    if "gate-error" in reasons:
        lines.append(f"- **门禁 [E] 未通过**：{len(failures)} 项失败（见下表）。")
    if "activity-stale" in reasons:
        days = activity.get("days")
        lines.append(f"- **活跃度超阈值**：距上次自动化记录 {days} 天（阈值 {activity['threshold']} 天）。")
    lines.append("")

    lines += ["## 失败项明细", ""]
    if failures:
        lines += ["| # | 门禁 | 摘要 | 位置 |", "|---|---|---|---|"]
        for i, f in enumerate(failures, 1):
            summary = "<br>".join(f["summary"]) or "—"
            loc = ", ".join(f["locations"]) or "—"
            lines.append(f"| {i} | `{f['name']}` | {summary} | {loc} |")
    else:
        lines.append("（无门禁失败项）")
    lines.append("")

    lines += ["## 责任归属周期", "",
              f"- **{period}**（{period_basis}）",
              "- 修复产出应归档到该周期；若为跨期结构性问题，请在本工单下说明并另开任务。",
              ""]

    lines += ["## 可直接执行的复跑命令", "", "```bash"]
    lines += cmds
    lines += ["# 修复后按协议提交（不直推 main）",
              'python engine/tools/repo_sync.py run --message "fix: 修正门禁失败项 '
              f'({period})" --paths <变更路径> --gate',
              "```", ""]

    lines += ["## 标准修复流程", "",
              "1. 逐项处理上表失败项（对照对应规范与单一事实源）；",
              "2. 运行「复跑命令」确认 `[E]` 归零（`[W]` 历史降级不阻断）；",
              "3. 按 `task/<slug>` 分支提交并开 PR（`repo_sync.py run --gate`），严禁直推 `main`；",
              "4. 工单关闭时回填：实际修复项、复跑结果、PR 链接。",
              "",
              "## 闭环要求", "",
              "- 本工单由 `.github/actions/remediation-ticket` 自动生成（幂等：同标题 open 工单不重复创建）；",
              "- 代码提交仍走既有 PR 协议，本机制不改变提交流程；",
              "- 处理完成后请关闭工单，活跃度与门禁状态将在下次维护运行时自动复核。",
              ""]
    return "\n".join(lines)


def detect(gate_json: str | None, gate_period: str, source_gate_period: str,
           activity_threshold: int, probe: bool, now: datetime) -> dict:
    if gate_json:
        gate_report = json.loads(Path(gate_json).read_text(encoding="utf-8"))
    else:
        gate_report = run_gate(gate_period, source_gate_period, probe)

    activity = read_activity(activity_threshold)
    failures = extract_failures(gate_report)
    gate_errors = int(gate_report.get("errors", len(failures)))
    reasons = []
    if gate_errors > 0:
        reasons.append("gate-error")
    if activity["stale"]:
        reasons.append("activity-stale")

    period, basis = derive_period([f"{f['name']}\n" + "\n".join(f["summary"]) for f in failures]
                                  + [gate_report.get("parse_error", "")], now)
    cmds = build_commands(failures, gate_period, source_gate_period)

    data = {
        "triggered": bool(reasons),
        "reasons": reasons,
        "period": period,
        "period_basis": basis,
        "gate": {"errors": gate_errors, "warnings": int(gate_report.get("warnings", 0)),
                 "failures": failures},
        "activity": activity,
        "commands": cmds,
    }
    data["body"] = render_body(data)
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="闭环修正工单生成（门禁 [E] / 活跃度超阈值）")
    sub = ap.add_subparsers(dest="command", required=True)
    d = sub.add_parser("detect", help="检测并生成标准化修正工单")
    d.add_argument("--gate-json", help="读取已有门禁 JSON（缺省则运行 optimization_gate）")
    d.add_argument("--gate-period", default=optimization_gate.DEFAULT_GATE_PERIOD)
    d.add_argument("--source-gate-period", default=optimization_gate.DEFAULT_SOURCE_GATE_PERIOD)
    d.add_argument("--activity-threshold", type=int, default=45)
    d.add_argument("--probe", action="store_true", help="运行门禁时启用外部 URL 探测")
    d.add_argument("--now", help="覆盖当前时间（ISO，仅测试用）")
    d.add_argument("--out", help="写入 JSON 报告")
    d.add_argument("--body-out", help="写入工单 Markdown 正文")
    d.add_argument("--porcelain", action="store_true", help="仅输出 triggered=true|false")
    args = ap.parse_args()

    now = (datetime.fromisoformat(args.now) if args.now
           else datetime.now(tz=timezone.utc))
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    try:
        data = detect(args.gate_json, args.gate_period, args.source_gate_period,
                      args.activity_threshold, args.probe, now)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[ERROR] 检测失败：{e}", file=sys.stderr)
        return 1

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(
            json.dumps({k: v for k, v in data.items() if k != "body"},
                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.body_out:
        Path(args.body_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.body_out).write_text(data["body"], encoding="utf-8")

    if args.porcelain:
        print(f"triggered={'true' if data['triggered'] else 'false'}")
        print(f"period={data['period']}")
        print(f"reasons={','.join(data['reasons']) or '-'}")
    else:
        print(f"触发={data['triggered']} 原因={data['reasons']} 周期={data['period']}")
        print(data["body"])
    return 0 if data["triggered"] else 2


if __name__ == "__main__":
    sys.exit(main())
