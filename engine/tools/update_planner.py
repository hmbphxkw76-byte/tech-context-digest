"""内容更新任务清单（CI: content-update 的「生成任务清单」步骤）。

按业务线与周期判断应执行的任务，输出 tasks.md（人读）与 tasks.json
（--porcelain，供创建 Issue 的脚本判断是否为空）。

用法（与 content-update.yml 一致）：
    python engine/tools/update_planner.py --porcelain --pending-only \
        [--project content/economy/dubai/apartment] [--period 2026-11] > tasks.json
    python engine/tools/update_planner.py --pending-only [--project ...] [--period ...] > tasks.md

周周期：`--period YYYY-MM-DD` 只为具备 weekly 提示词的業務线派发（周报）。

周期规则（与 _common.tasks_for_period 一致）：
    月度期 YYYY-MM  -> 月度任务；季首月追加季度任务；1 月追加上一自然年年度任务
    季度期 YYYY-Qn  -> 季度任务
    年度期 YYYY     -> 年度任务
任务状态：输出文件已存在于业务 reports/ 则为 done，否则 pending。
条件节拍：提示词含 `<!-- report-output: none -->` 时不派任务（见 _common.prompt_produces_report）。

退出码：0 = 正常（含空清单）；2 = 参数错误（项目 / 周期无法识别）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    ROOT,
    Business,
    baseline_year_month,
    expected_output,
    iter_business_dirs,
    parse_period,
    prompt_file_candidates,
    prompt_produces_report,
    tasks_for_period,
)

CALENDAR_JSON = ROOT / "engine" / "report-audits" / "release-calendar.json"
WEEK_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def calendar_summary() -> str:
    """读取结构化发布日历（P1-6）-> 任务清单摘要段落；缺失返回空串。"""
    if not CALENDAR_JSON.exists():
        return ""
    try:
        doc = json.loads(CALENDAR_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    s = doc.get("summary", {})
    missing = s.get("missing_p0") or []
    lines = [
        "",
        "## 发布日历摘要（结构化采集 · P1-6）",
        f"- 日历行数 {s.get('rows', 0)}；字段完整率 {s.get('field_complete_rate', 0):.1%}；"
        f"P0 维度覆盖 {s.get('p0_covered', 0)}/{s.get('p0_dimensions', 0)}",
    ]
    if missing:
        lines.append(f"- 未覆盖 P0 维度：{', '.join(missing)}（需补录发布日历）")
    return "\n".join(lines)

CYCLE_LABEL = {"monthly": "月度", "quarterly": "季度", "annual": "年度",
               "baseline": "基线", "weekly": "周报"}


def default_period(now: datetime) -> str:
    """与 content-update.yml 的「计算周期标识」逻辑一致：季首月用季度标识。"""
    month = now.month
    year = now.year
    if month in (1, 4, 7, 10):
        return f"{year}-Q{(month - 1) // 3 + 1}"
    return f"{year}-{month:02d}"


def build_weekly_tasks(y: int, mo: int, d: int, businesses: list[Business]) -> list[dict]:
    """周周期（YYYY-MM-DD）任务：仅为具备 weekly 提示词的業務线派发。

    周报落盘名为 `<YYYY-MM-DD>_weekly.html`（见 `_common.WEEKLY_RE`）；
    `_common.expected_output` 无 weekly 分支，故此处直接构造文件名。
    """
    tasks = []
    prompt_names = prompt_file_candidates("weekly")
    for b in businesses:
        base_ym = baseline_year_month(b)
        if base_ym and (y, mo) < base_ym:
            continue
        prompt_path = next(
            (b.path / "prompts" / name for name in prompt_names
             if (b.path / "prompts" / name).exists()),
            None,
        )
        if prompt_path is None or not prompt_produces_report(prompt_path):
            continue
        output = f"{y}-{mo:02d}-{d:02d}_weekly.html"
        tasks.append(
            {
                "project": b.rel,
                "cycle": "weekly",
                "cycle_label": CYCLE_LABEL["weekly"],
                "period": f"{y}-{mo:02d}-{d:02d}",
                "prompt": f"{b.rel}/prompts/{prompt_path.name}",
                "output": f"{b.rel}/reports/{output}",
                "status": "done" if (b.path / "reports" / output).exists() else "pending",
            }
        )
    return tasks


def build_tasks(period: str, businesses: list[Business]) -> list[dict]:
    m = WEEK_RE.fullmatch(period)
    if m:
        return build_weekly_tasks(int(m.group(1)), int(m.group(2)),
                                  int(m.group(3)), businesses)
    try:
        cycle, y, n = parse_period(period)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        raise SystemExit(2)
    tasks = []
    for b in businesses:
        base_ym = baseline_year_month(b)
        for rc, ry, rn in tasks_for_period(cycle, y, n):
            # 不派发早于业务线基线的周期任务（新建立业务线不应被派历史任务）。
            task_ym = (ry, 12 if rc == "annual" else (rn * 3 if rc == "quarterly" else rn))
            if base_ym and task_ym < base_ym:
                continue
            # 业务线只为已建立周期提示词的周期生成任务（节拍设计由业务 prompts/ 实际内容决定），
            # 避免「周报型 / 事件触发型」业务线被硬派月度 / 季度 / 年度任务。
            # 文件名支持类型特有别名（如 prompt-annual-refresh.md）。
            prompt_path = next(
                (b.path / "prompts" / name for name in prompt_file_candidates(rc) if (b.path / "prompts" / name).exists()),
                None,
            )
            if prompt_path is None:
                continue
            # 条件节拍 / 核验型轻运行（提示词声明 `<!-- report-output: none -->`）
            # 不产出报告文件，故不派发任务（如 security 的月度核验）。
            if not prompt_produces_report(prompt_path):
                continue
            output = expected_output(rc, ry, rn)
            prompt_rel = f"{b.rel}/prompts/{prompt_path.name}"
            status = "done" if (b.path / "reports" / output).exists() else "pending"
            tasks.append(
                {
                    "project": b.rel,
                    "cycle": rc,
                    "cycle_label": CYCLE_LABEL[rc],
                    "period": f"{ry}" + (f"-Q{rn}" if rc == "quarterly" else (f"-{rn:02d}" if rc == "monthly" else "")),
                    "prompt": prompt_rel,
                    "output": f"{b.rel}/reports/{output}",
                    "status": status,
                }
            )
    return tasks


def blindspot_summary(now: datetime) -> str:
    """盲区阻塞跟踪（S2）：未消号项与责任周期，过期项显式标注。

    数据源为盲区台账（单一事实源，只读）；月周期与周周期共用，供 content-update
    月度对账与 Issue 清单使用。
    """
    try:
        import blind_spot_check
    except ImportError:
        return ""
    if not blind_spot_check.LEDGER.exists():
        return ""
    rows = [r for r in blind_spot_check.parse_rows(
        blind_spot_check.LEDGER.read_text(encoding="utf-8")) if len(r) >= 9]
    open_rows = [r for r in rows if r[7] in ("open", "in_progress")]
    if not open_rows:
        return ""
    cur = f"{now.year}-{now.month:02d}"
    overdue = [r for r in open_rows if r[5] < cur]
    lines = [
        "",
        "## 盲区阻塞跟踪（S2 · 未消号项）",
        f"- 未消号 {len(open_rows)} 项；责任周期已过期 {len(overdue)} 项"
        "（须消号或更新责任周期）",
    ]
    for r in open_rows:
        flag = " **[责任周期已过期]**" if r[5] < cur else ""
        lines.append(f"- {r[0]} {r[1]}（{r[2]}，责任周期 {r[5]}，{r[7]}）{flag}")
    return "\n".join(lines)


def render_md(tasks: list[dict], period: str, now: datetime) -> str:
    lines = [f"## 内容更新任务清单（{period}）", ""]
    for t in tasks:
        mark = "x" if t["status"] == "done" else " "
        state = "已产出" if t["status"] == "done" else "待产出"
        lines.append(
            f"- [{mark}] {t['project']} · {t['cycle_label']} {t['period']}"
            f" — 提示词 `{t['prompt']}` · 输出 `{t['output']}`（{state}）"
        )
    lines.append("")
    lines.append(calendar_summary())
    lines.append(blindspot_summary(now))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="内容更新任务清单生成")
    ap.add_argument("--project", default="", help="限定业务线（如 content/economy/dubai/apartment），缺省全部")
    ap.add_argument("--period", default="", help="周期标识（YYYY-MM / YYYY-Qn / YYYY / YYYY-MM-DD 周周期），缺省按当前 UTC 日期")
    ap.add_argument("--pending-only", action="store_true", help="仅输出未完成任务")
    ap.add_argument("--porcelain", action="store_true", help="输出 JSON 数组")
    args = ap.parse_args()

    businesses = iter_business_dirs()
    if args.project:
        target = args.project.strip("/")
        businesses = [b for b in businesses if b.rel == target]
        if not businesses:
            print(f"[ERROR] 未找到业务线目录: {target}", file=sys.stderr)
            return 2

    period = args.period or default_period(datetime.now(tz=timezone.utc))
    if not WEEK_RE.fullmatch(period):
        try:
            parse_period(period)
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 2

    tasks = build_tasks(period, businesses)
    if args.pending_only:
        tasks = [t for t in tasks if t["status"] == "pending"]

    if args.porcelain:
        print(json.dumps(tasks, ensure_ascii=False))
    else:
        print(render_md(tasks, period, datetime.now(tz=timezone.utc)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
