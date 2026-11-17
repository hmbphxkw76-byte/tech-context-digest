#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""任务计划工件生成器（task_plan）。

吸收 mainline 阶段 2「计划与准备」：为每次任务生成 `plan.json` / `tasks.json` /
`risks.json` 与任务启动文件，落 `engine/audit/records/tasks/<slug>/`，
补齐 P-05「任务级闭环工件缺失」。

设计约束（《方案》配套治理标准 1–3）：
- **工件即门禁输入**：无 `plan.json` 不得执行 `repo_sync run --gate`；
- **单一事实源**：工件 schema 只在本模块定义，其余位置只指针；
- **确定性**：无时间戳 / 无随机数，重复生成字节一致（`--check` 可重放）；
- **复用**：不重写任何校验，只生成工件。

用法：
    python engine/tools/task_plan.py init --slug <slug> --title <title> \
        [--task "T-1:标题"]... [--risk "R-1:描述:缓解"]... [--from main]
    python engine/tools/task_plan.py show --slug <slug>
    python engine/tools/task_plan.py check --slug <slug>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS_DIR = ROOT / "engine" / "audit" / "records" / "tasks"
SCHEMA_VERSION = "1.0"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SPEC_ID = "MAINLINE-ADOPTION-PHASE1"

# 与 N0–N8 体系的映射：N0.5 为本次吸收新增的「任务计划」子节点，其余主体保留。
NODE_MAP: list[tuple[str, str, str]] = [
    ("N0", "需求与配置", "business-config / layout.json 维度注册"),
    ("N0.5", "任务计划（mainline 阶段 2 吸收）", "plan.json / tasks.json / risks.json / task-start.md"),
    ("N1", "信息采集", "source_registry / 台账 / 发布日历"),
    ("N2", "信息筛选与分级", "四层分级 + 双源 + 死链"),
    ("N3", "信息分类", "类型 / 维度 / 归位"),
    ("N4", "内容生成", "四层提示词继承 + 量化模型"),
    ("N5", "渲染与交付", "canonical 样式 + 自包含 HTML"),
    ("N6", "质量校验与审计", "统一门禁 + 审计四环节"),
    ("N7", "发布 / 索引 / 归档", "hub / INDEX / 指纹 / 归档"),
    ("N8", "运维与监控", "CI 工作流 + 告警"),
]
GATE_IDS = [f"G{i}" for i in range(0, 9)]
REUSE = {
    "gate": "engine/tools/optimization_gate.py",
    "commit": "engine/tools/repo_sync.py",
    "orchestrator": "engine/tools/pipeline_runner.py",
    "audit": "engine/audit/scripts/audit_tool.py",
    "local_mainline": "engine/tools/local_mainline.py",
}
ARTIFACT_NAMES = ("plan.json", "tasks.json", "risks.json", "task-start.md")


# ---------------------------------------------------------------- 路径

def plan_dir(slug: str) -> Path:
    return TASKS_DIR / slug


def plan_path(slug: str) -> Path:
    return plan_dir(slug) / "plan.json"


def validate_slug(slug: str) -> tuple[bool, str]:
    if not slug:
        return False, "slug 为空"
    if not SLUG_RE.match(slug):
        return False, f"slug {slug!r} 需为 kebab-case（小写字母 / 数字 / 单连字符）"
    return True, ""


# ---------------------------------------------------------------- 纯渲染

def build_plan(slug: str, title: str, source: str = "main") -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "spec": SPEC_ID,
        "slug": slug,
        "title": title,
        "source": source,
        "nodes": [{"id": n, "name": name, "note": note} for n, name, note in NODE_MAP],
        "gates": list(GATE_IDS),
        "artifacts": {
            "dir": f"engine/audit/records/tasks/{slug}",
            "plan": f"engine/audit/records/tasks/{slug}/plan.json",
            "tasks": f"engine/audit/records/tasks/{slug}/tasks.json",
            "risks": f"engine/audit/records/tasks/{slug}/risks.json",
            "start": f"engine/audit/records/tasks/{slug}/task-start.md",
        },
        "reuse": dict(REUSE),
    }


def parse_tasks(items: list[str] | None) -> list[dict]:
    out: list[dict] = []
    for i, raw in enumerate(items or [], 1):
        parts = (raw or "").split(":", 1)
        tid = parts[0].strip() or f"T-{i:02d}"
        title = parts[1].strip() if len(parts) > 1 else ""
        out.append({"id": tid, "title": title, "phase": "", "depends_on": [],
                    "acceptance": "", "status": "pending"})
    return out


def parse_risks(items: list[str] | None) -> list[dict]:
    out: list[dict] = []
    for i, raw in enumerate(items or [], 1):
        parts = (raw or "").split(":")
        rid = parts[0].strip() or f"R-{i:02d}"
        desc = parts[1].strip() if len(parts) > 1 else ""
        mit = parts[2].strip() if len(parts) > 2 else ""
        out.append({"id": rid, "description": desc, "mitigation": mit, "owner": ""})
    return out


def render_plan(plan: dict) -> str:
    return json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_tasks(tasks: list[dict]) -> str:
    return json.dumps(tasks, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_risks(risks: list[dict]) -> str:
    return json.dumps(risks, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_start_md(slug: str, plan: dict, tasks: list[dict], risks: list[dict]) -> str:
    lines = [
        f"# 任务启动 · {plan['title']}",
        "",
        f"- slug：`{slug}`",
        f"- 起点：`{plan['source']}`；分支：`task/{slug}-<session8>`（见 `branch_registry.json`）",
        f"- 计划工件目录：`engine/audit/records/` 下的 `tasks/{slug}/`",
        "  - `plan.json`（计划与 N0–N8 映射）",
        "  - `tasks.json`（任务分解）",
        "  - `risks.json`（风险登记）",
        "  - `task-start.md`（本文件）",
        "",
        "## 体系映射（主体保留，增量吸收）",
        "",
        "| 节点 | 名称 | 说明 |",
        "|---|---|---|",
    ]
    for n, name, note in NODE_MAP:
        lines.append(f"| {n} | {name} | {note} |")
    lines += [
        "",
        "## 复用入口（不得另写一套校验）",
        "",
        f"- 统一门禁：`python {REUSE['gate']} --gate-period 2026-12 --source-gate-period 2027-01 --probe`",
        f"- 提交网关：`python {REUSE['commit']} run --message ... --paths ... --gate`",
        f"- 端到端编排：`python {REUSE['orchestrator']} validate`",
        f"- 一键闭环：`python {REUSE['local_mainline']} run --slug {slug} --title ...`",
        "",
        f"## 任务清单（{len(tasks)} 项，详见 tasks.json）",
        "",
    ]
    for t in tasks:
        lines.append(f"- [{t['status']}] {t['id']} {t['title']}")
    lines += [
        "",
        f"## 风险登记（{len(risks)} 项，详见 risks.json）",
        "",
    ]
    for r in risks:
        lines.append(f"- {r['id']} {r['description']}"
                     + (f"（缓解：{r['mitigation']}）" if r.get("mitigation") else ""))
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- 校验 / 读写

def validate_artifacts(slug: str, plan: dict, tasks: list[dict], risks: list[dict]) -> list[str]:
    problems: list[str] = []
    ok, why = validate_slug(slug)
    if not ok:
        problems.append(why)
    if plan.get("slug") != slug:
        problems.append(f"plan.slug={plan.get('slug')!r} 与目录 slug={slug!r} 不一致")
    if plan.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"plan.schema_version 须为 {SCHEMA_VERSION}")
    if not str(plan.get("title", "")).strip():
        problems.append("plan.title 为空")
    ids = [t.get("id") for t in tasks]
    if len(ids) != len(set(ids)):
        problems.append("tasks.id 重复")
    for t in tasks:
        if not t.get("id") or not str(t.get("title", "")).strip():
            problems.append(f"task 缺 id/title：{t}")
    rids = [r.get("id") for r in risks]
    if len(rids) != len(set(rids)):
        problems.append("risks.id 重复")
    for r in risks:
        if not r.get("id") or not str(r.get("description", "")).strip():
            problems.append(f"risk 缺 id/description：{r}")
    return problems


def load_artifacts(slug: str) -> tuple[dict, list[dict], list[dict]]:
    d = plan_dir(slug)
    plan = json.loads((d / "plan.json").read_text(encoding="utf-8"))
    tasks = json.loads((d / "tasks.json").read_text(encoding="utf-8"))
    risks = json.loads((d / "risks.json").read_text(encoding="utf-8"))
    return plan, tasks, risks


def write_artifacts(slug: str, plan: dict, tasks: list[dict], risks: list[dict]) -> list[Path]:
    d = plan_dir(slug)
    d.mkdir(parents=True, exist_ok=True)
    contents = {
        "plan.json": render_plan(plan),
        "tasks.json": render_tasks(tasks),
        "risks.json": render_risks(risks),
        "task-start.md": render_start_md(slug, plan, tasks, risks),
    }
    written: list[Path] = []
    for name in ARTIFACT_NAMES:
        p = d / name
        p.write_text(contents[name], encoding="utf-8")
        written.append(p)
    return written


def check(slug: str) -> list[str]:
    """重放校验：磁盘工件存在且与纯渲染结果字节一致（确定性）。"""
    problems: list[str] = []
    d = plan_dir(slug)
    for name in ARTIFACT_NAMES:
        if not (d / name).exists():
            problems.append(f"缺工件：{d / name}")
    if problems:
        return problems
    try:
        plan, tasks, risks = load_artifacts(slug)
    except (OSError, json.JSONDecodeError) as e:
        return [f"工件读取失败：{e}"]
    problems += validate_artifacts(slug, plan, tasks, risks)
    expected = {
        "plan.json": render_plan(plan),
        "tasks.json": render_tasks(tasks),
        "risks.json": render_risks(risks),
        "task-start.md": render_start_md(slug, plan, tasks, risks),
    }
    for name, text in expected.items():
        actual = (d / name).read_text(encoding="utf-8")
        if actual != text:
            problems.append(f"{name} 与确定性渲染结果不一致（非可重放）")
    return problems


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="任务计划工件生成器（plan/tasks/risks + 任务启动文件）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="生成 / 覆盖任务计划工件")
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--task", action="append", default=[], help="任务：\"T-1:标题\"")
    p.add_argument("--risk", action="append", default=[], help="风险：\"R-1:描述:缓解\"")
    p.add_argument("--from", dest="source", default="main", help="起点 ref（默认 main）")

    p = sub.add_parser("show", help="打印 plan.json")
    p.add_argument("--slug", required=True)

    p = sub.add_parser("check", help="重放校验工件确定性 / schema")
    p.add_argument("--slug", required=True)

    args = ap.parse_args()

    if args.cmd == "init":
        ok, why = validate_slug(args.slug)
        if not ok:
            print(f"[ERROR] {why}", file=sys.stderr)
            return 2
        plan = build_plan(args.slug, args.title, args.source)
        tasks = parse_tasks(args.task)
        risks = parse_risks(args.risk)
        problems = validate_artifacts(args.slug, plan, tasks, risks)
        if problems:
            for p in problems:
                print(f"[ERROR] {p}", file=sys.stderr)
            return 1
        written = write_artifacts(args.slug, plan, tasks, risks)
        print(f"[init] slug={args.slug} 任务 {len(tasks)} 项 / 风险 {len(risks)} 项")
        for p in written:
            print(f"  {p.relative_to(ROOT)}")
        return 0

    if args.cmd == "show":
        plan, tasks, risks = load_artifacts(args.slug)
        print(render_plan(plan), end="")
        return 0

    if args.cmd == "check":
        problems = check(args.slug)
        if problems:
            for p in problems:
                print(f"[E] {p}")
            return 1
        print(f"[OK] 工件 schema / 确定性校验通过：{plan_dir(args.slug).relative_to(ROOT)}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
