#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""本地 mainline 一键闭环（薄封装，只编排不重写校验）。

吸收 mainline 阶段 5：`plan → unittest → optimization_gate --probe → repo_sync push → repo_sync pr`。

**复用纪律（《方案》治理标准 3）**：本模块**不重写任何校验逻辑**，只按顺序调用既有入口：
- 计划校验：`task_plan.py check`（工件即门禁输入）；
- 单测：`unittest discover`；
- 统一门禁：`optimization_gate.py --probe`（与 ci / audit 同口径）；
- 提交 / PR：`repo_sync.py push` / `pr`（统一网关）。

用法：
    python engine/tools/local_mainline.py run --slug <slug> --title <PR 标题> \
        [--body <PR 正文>] [--dry-run]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# 滚动基线（auto = 当前自然月 + 1）：新报告判定不随时间失效，见 gate_period.py
GATE_PERIOD = "auto"
SOURCE_GATE_PERIOD = "auto"

DEFAULT_BODY = (
    "由 `local_mainline.py` 一键闭环生成：计划工件校验 → unittest → "
    "optimization_gate --probe → repo_sync push → repo_sync pr。\n\n"
    "复用入口：统一门禁 `optimization_gate.py`；提交网关 `repo_sync.py`。"
)


def build_steps(slug: str, title: str, body: str) -> list[tuple[str, list[str]]]:
    """-> [(步骤名, 命令)]，顺序即 mainline 阶段 5 的闭环顺序。"""
    return [
        ("plan", [sys.executable, "engine/tools/task_plan.py", "check", "--slug", slug]),
        ("unittest", [sys.executable, "-m", "unittest", "discover",
                      "-s", "engine/tests", "-p", "test_*.py"]),
        ("gate", [sys.executable, "engine/tools/optimization_gate.py",
                  "--gate-period", GATE_PERIOD,
                  "--source-gate-period", SOURCE_GATE_PERIOD, "--probe"]),
        ("push", [sys.executable, "engine/tools/repo_sync.py", "push"]),
        ("pr", [sys.executable, "engine/tools/repo_sync.py", "pr",
                "--title", title, "--body", body, "--queue"]),
    ]


def run(slug: str, title: str, body: str = DEFAULT_BODY,
        dry_run: bool = False) -> int:
    steps = build_steps(slug, title, body)
    for name, cmd in steps:
        print(f"[step] {name}: {' '.join(cmd)}")
        if dry_run:
            continue
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            print(f"[FAIL] {name} 退出码 {r.returncode}（闭环中止）")
            return r.returncode
    if dry_run:
        print("[dry-run] 一键闭环步骤已列出，未执行")
        return 0
    print("[OK] 本地 mainline 一键闭环完成")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="本地 mainline 一键闭环（薄封装，只编排）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--slug", required=True, help="任务 slug（对应 engine/audit/records/tasks/<slug>/）")
    p.add_argument("--title", required=True, help="PR 标题")
    p.add_argument("--body", default=DEFAULT_BODY, help="PR 正文")
    p.add_argument("--dry-run", action="store_true", help="只打印步骤，不执行")
    args = ap.parse_args()
    return run(args.slug, args.title, args.body, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
