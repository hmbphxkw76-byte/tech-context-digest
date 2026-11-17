#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""审计报告标准化管理工具（AUDIT-MGMT v1.0，engine/audit/）。

子命令：
  inventory                 列出全部纳入管理的报告（业务 + 审计）
  init                      初始化/刷新登记表 audit_registry.json
  structure <report>        L2 结构与要素校验（report-standard.md 十大要素）
  verify <report>           L1 + L2 汇总（L1 调用既有工具链）
  review <report> --stage draft|initial|second|final --reviewer N --decision pass|fix|reject
                            追加审查记录（留痕）
  mark <report>             终审通过后注入「已审计」标识（校验四环节齐备）
  unmark <report>           移除标识
  status [report]           输出登记状态
  sample [--ratio R] [--seed N]   生成定期抽检清单
  accept                    项目级合规率汇总
  l3-status                 L3 SLA 超期检测（每两周覆盖全部正式报告；有超期返回 2 告警）

退出码：0 通过；1 存在不合规；2 用法错误。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT_DIR = ROOT / "engine" / "audit"
RECORDS = AUDIT_DIR / "records"
REGISTRY = RECORDS / "audit_registry.json"
REVIEWS = RECORDS / "reviews"
BACKUPS = RECORDS / "backups"
AUDIT_REPORTS_DIR = ROOT / "engine" / "report-audits"

sys.path.insert(0, str(ROOT / "engine" / "tools"))
from _common import iter_business_dirs, iter_reports  # noqa: E402

STAGES = ("draft", "initial", "second", "final")
STAGE_LABEL = {"draft": "生成", "initial": "初审", "second": "复核", "final": "终审"}
MARK_CLASS = "audit-mark"

# 标识分级（T2）：none 未审计 / pre 预审通过（机器，语义待完成）/ full 已审计（含 L3）
MARK_LEVELS = ("none", "pre", "full")
# mark 只允许注入 pre / full；none 由 unmark 表达（P2-7）
MARK_CHOICES = ("pre", "full")

# L3 宽限期（P0-3）：新报告登记后 N 天内缺语义终审（second/final）不阻断审计 CI，
# 仅告警并注入「预审通过」标识；超期仍缺则 fail-fast 阻断。机器环节（draft/initial）
# 与 machine_final 失败不受宽限，始终阻断。
L3_GRACE_DAYS = 14

# 环节归属：机器环节由 CI 写记录；语义环节（L3）以 Agent 记录为权威，CI 不得覆盖。
MACHINE_STAGES = ("draft", "initial")
SEMANTIC_STAGES = ("second", "final")
MARK_LEVEL_LABEL = {"none": "未审计", "pre": "预审通过（机器）", "full": "已审计"}
MARK_LEVEL_STYLE = {
    "pre": "background:#5b6b7c;color:#fff;",
    "full": "background:#16324f;color:#fff;",
}


# ---------------------------------------------------------------- 报告发现

def collect_reports() -> list[dict]:
    """全部真实业务报告 + 审计报告。category ∈ report / archived / legacy / audit-doc。"""
    out: list[dict] = []
    for ref in iter_reports(include_archives=True, include_legacy=True):
        out.append({
            "path": ref.rel,
            "kind": "business",
            "category": ref.category,
            "business_line": ref.business_line,
            "title": _title_of(ROOT / ref.rel) or Path(ref.rel).name,
        })
    if AUDIT_REPORTS_DIR.is_dir():
        for f in sorted(AUDIT_REPORTS_DIR.glob("*.md")):
            out.append({
                "path": str(f.relative_to(ROOT)).replace("\\", "/"),
                "kind": "audit",
                "category": "audit-doc",
                "business_line": "engine/report-audits",
                "title": _title_of(f) or f.name,
            })
    return out


def _title_of(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------- 登记表

def load_registry() -> dict:
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {"schema_version": "1.0", "reports": {}}


def save_registry(reg: dict) -> None:
    RECORDS.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stale_paths(reports: dict) -> list[str]:
    """登记路径在磁盘上不存在的失效条目（P-01）。

    业务报告被删除 / 迁移后，登记册残留旧路径会损害审计留痕可信度；
    本函数为唯一判定入口，供 status（告警）与 prune（清理）复用。
    """
    return sorted(rel for rel in reports if not (ROOT / rel).exists())


# ---------------------------------------------------------------- 证据索引

def _rel_or_empty(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/") if path.exists() else ""


def build_evidence(rel: str, entry: dict | None = None) -> dict:
    """汇总单份报告的完成前证据索引（P-02 / 吸收项 ③）。

    关联四类证据：任务计划工件（plan/tasks/risks）、统一门禁入口、审计记录（reviews）、
    登记状态。只做**指针汇聚**，不重算校验结论（校验仍由 optimization_gate / audit_tool 承载）。
    """
    entry = entry or {}
    plans: list[dict] = []
    tasks_root = RECORDS / "tasks"
    bl = entry.get("business_line", "")
    if tasks_root.is_dir():
        for d in sorted(tasks_root.iterdir()):
            if not d.is_dir():
                continue
            plan_fp = d / "plan.json"
            tasks_fp = d / "tasks.json"
            risks_fp = d / "risks.json"
            if not plan_fp.exists():
                continue
            try:
                plan = json.loads(plan_fp.read_text(encoding="utf-8"))
                tasks = json.loads(tasks_fp.read_text(encoding="utf-8")) if tasks_fp.exists() else []
                risks = json.loads(risks_fp.read_text(encoding="utf-8")) if risks_fp.exists() else []
            except (OSError, json.JSONDecodeError):
                continue
            # 兜底文本排除 reports 字段，保持「原有语义」：否则业务线前缀会命中同线全部报告。
            plan_blob = json.dumps([{k: v for k, v in plan.items() if k != "reports"}, tasks],
                                   ensure_ascii=False)
            # 主判据：plan.reports 显式关联（task_plan init --report 写入，确定性）。
            # 兜底：既有 plan/tasks/risks 文本包含 rel 或业务线（兼容历史工件）。
            matched = rel in plan.get("reports", []) \
                or rel in json.dumps([plan, tasks, risks], ensure_ascii=False) \
                or (bool(bl) and bl in plan_blob)
            if matched:
                plans.append({
                    "slug": d.name,
                    "plan": _rel_or_empty(plan_fp),
                    "tasks": _rel_or_empty(tasks_fp),
                    "risks": _rel_or_empty(risks_fp),
                    "reports": plan.get("reports", []),
                    "task_count": len(tasks),
                    "risk_count": len(risks),
                })
    review = _review_file(rel)
    return {
        "report": rel,
        "business_line": entry.get("business_line", ""),
        "plans": plans,
        "gate": {"entry": "engine/tools/optimization_gate.py", "probe": True},
        "audit": {
            "review": _rel_or_empty(review),
            "status": entry.get("status", ""),
            "stages": entry.get("stages", {}),
            "mark_level": entry.get("mark_level", "none"),
            "audit_id": entry.get("audit_id", ""),
        },
    }


def cmd_init(_args) -> int:
    reg = load_registry()
    reports = reg.setdefault("reports", {})
    today = _dt.date.today().isoformat()
    for r in collect_reports():
        rec = reports.get(r["path"], {})
        rec.setdefault("title", r["title"])
        rec.setdefault("kind", r["kind"])
        rec.setdefault("category", r["category"])
        rec.setdefault("business_line", r["business_line"])
        rec.setdefault("status", "draft")
        rec.setdefault("stages", {s: False for s in STAGES})
        rec.setdefault("mark", False)
        # L3 宽限期起点（P0-3）：新登记取当日；既有登记缺字段时补当日（统一进入宽限）。
        rec.setdefault("first_seen_at", today)
        # 兼容旧登记：已注入标识但无 mark_level 的，视为 full
        if rec.get("mark") and not rec.get("mark_level"):
            rec["mark_level"] = "full"
        rec["evidence"] = build_evidence(r["path"], rec)
        reports[r["path"]] = rec
    save_registry(reg)
    print(f"[init] 登记 {len(reports)} 份报告 → {REGISTRY.relative_to(ROOT)}")
    return 0


def cmd_inventory(_args) -> int:
    reps = collect_reports()
    reg = load_registry()["reports"]
    print(f"{'报告':<62} {'类别':<8} {'状态':<10} {'标识'}")
    for r in reps:
        st = reg.get(r["path"], {}).get("status", "未登记")
        mk = "已审计" if reg.get(r["path"], {}).get("mark") else "-"
        print(f"{r['path']:<62} {r['kind']:<8} {st:<10} {mk}")
    print(f"\n合计 {len(reps)} 份（业务 {sum(1 for r in reps if r['kind']=='business')} / 审计 {sum(1 for r in reps if r['kind']=='audit')}）")
    return 0


# ---------------------------------------------------------------- L2 结构要素

def structure_check(path: Path, kind: str) -> tuple[list[str], list[str]]:
    """-> ([E1..E10 缺失], [警告])。启发式校验，边界情形需人工确认。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    is_html = path.suffix.lower() == ".html"
    missing: list[str] = []
    warn: list[str] = []

    def need(tag: str, cond: bool) -> None:
        if not cond:
            missing.append(tag)

    # E1 标题与类型标识
    need("E1 标题与类型标识", bool(re.search(r"<title\b", text, re.I)) or bool(re.search(r"^#\s+", text, re.M)))
    # E2 报告概况（数据截止/基线日期 + 版本/日期）
    has_cutoff = ("数据截止" in text) or ("截止" in text) or ("基线日期" in text) or bool(re.search(r"\d{4}-\d{2}-\d{2}", text))
    has_ver = ("版本" in text) or bool(re.search(r"v\d+\.\d+", text))
    need("E2 报告概况", has_cutoff and has_ver)
    # E3 结论先行 / 审计结论
    if kind == "audit":
        need("E3 审计结论", ("审计意见" in text) or ("审计结论" in text) or bool(re.search(r"^#+.*结论", text, re.M)))
    else:
        need("E3 结论先行", ("执行摘要" in text) or ("结论先行" in text)
             or bool(re.search(r'<h2[^>]*>[^<]*(?:结论|要点|摘要)', text))
             or bool(re.search(r"^#+.*(?:结论|要点|摘要)", text, re.M)))
    # E4 编制基础与依据
    need("E4 编制基础与依据", ("口径" in text and ("方法" in text or "依据" in text or "指标" in text)))
    # E5 正文结构
    n_sec = len(re.findall(r'<h2[^>]*class="[^"]*\bsec\b', text)) if is_html else len(re.findall(r"^##\s+", text, re.M))
    need("E5 正文结构", n_sec >= 5)
    # E6 来源与引用
    need("E6 来源与引用", ("来源" in text) or ("参考" in text) or ("source" in low))
    # E7 数据一致性
    need("E7 数据一致性", ("口径" in text) or ("单位" in text))
    # E8 局限与风险
    need("E8 局限与风险", any(k in text for k in ("局限", "风险", "盲区", "遗留", "不确定性")))
    # E9 修正记录
    need("E9 修正记录", any(k in text for k in ("已修正事实清单", "修正记录", "本期无修正", "修复记录", "已修正项", "修正项", "勘误")))
    # E10 签发要素（版本 + 日期；审计标识为终审后追加，见 audit-mark.md）
    has_date = ("日期" in text) or ("基线日期" in text) or bool(re.search(r"\d{4}-\d{2}-\d{2}", text))
    has_ver2 = ("版本" in text) or bool(re.search(r"v\d+\.\d+", text))
    need("E10 签发要素", has_ver2 and has_date)

    # 硬性表述项（警告级）
    if re.search(r"(崩盘|绝对的|一定|必然)", text):
        warn.append("H1 疑似绝对化断言（需人工确认）")
    if not re.search(r"\d+(?:\.\d+)?\s*(?:AED|USD|\$|亿|万|%)", text):
        warn.append("H2 未见带单位量级（需人工确认）")
    return missing, warn


def cmd_structure(args) -> int:
    path = _resolve(args.report)
    if path is None:
        return 2
    kind = "audit" if path.suffix.lower() == ".md" else "business"
    missing, warn = structure_check(path, kind)
    total = 10
    ok = total - len(missing)
    print(f"[structure] {path.relative_to(ROOT)}  要素完整率 {ok}/{total}")
    for m in missing:
        print(f"  [缺失] {m}")
    for w in warn:
        print(f"  [警告] {w}")
    if kind == "audit":
        passed = ok == total
    else:
        passed = ok >= 9
    print("判定：" + ("通过" if passed else "不通过"))
    return 0 if passed else 1


def _resolve(report: str) -> Path | None:
    p = (ROOT / report)
    if p.exists():
        return p
    for cand in collect_reports():
        if cand["path"] == report or cand["path"].endswith("/" + report):
            return ROOT / cand["path"]
    print(f"[ERROR] 未找到报告：{report}", file=sys.stderr)
    return None


# ---------------------------------------------------------------- L1

def cmd_verify(args) -> int:
    """L1 + L2 汇总。

    L1 复用统一门禁单一入口（`optimization_gate.run_checks`，含 `--probe`），
    与 ci.yml / audit.yml 同口径；不再分项调用各工具（P1-2 去重，
    见 report-pipeline-system.md §七「校验一律复用统一入口，不得另写检查命令」）。
    """
    path = _resolve(args.report)
    if path is None:
        return 2
    kind = "audit" if path.suffix.lower() == ".md" else "business"
    missing, warn = structure_check(path, kind)
    print(f"[L2] 要素完整率 {10 - len(missing)}/10" + (f"，缺失：{'; '.join(missing)}" if missing else ""))
    for w in warn:
        print(f"  [警告] {w}")
    # L1：统一门禁单一入口（全库口径，含 probe）
    try:
        import optimization_gate  # type: ignore
        rep = optimization_gate.run_checks(quiet=True, probe=True)
    except Exception as e:  # noqa: BLE001
        print(f"[L1] 统一门禁执行异常：{type(e).__name__}: {e}")
        return 1
    l1_fail = []
    for c in rep.get("checks", []):
        if c.get("status") == "error":
            l1_fail.append(c["name"])
            print(f"[L1] {c['name']}: exit={c.get('code')}（错误）")
    n_warn = sum(1 for c in rep.get("checks", []) if c.get("status") == "warn")
    print(f"[L1] 统一门禁：{len(rep.get('checks', []))} 项；错误 {len(l1_fail)}；警告 {n_warn}")
    print(f"[verify] L1 失败项：{l1_fail or '无'}；L2 缺失：{missing or '无'}")
    return 1 if l1_fail or missing else 0


# ---------------------------------------------------------------- 审查留痕

def cmd_review(args) -> int:
    path = _resolve(args.report)
    if path is None:
        return 2
    if args.stage not in STAGES:
        print(f"[ERROR] stage 须为 {STAGES}", file=sys.stderr)
        return 2
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    REVIEWS.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", rel).strip("-") + ".json"
    fp = REVIEWS / slug
    rec = json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else {"report": rel, "reviews": []}
    findings = [{"id": f"F-{i+1:03d}", "severity": "P1", "desc": d} for i, d in enumerate(args.finding or [])]
    rec["reviews"].append({
        "stage": args.stage,
        "reviewer": args.reviewer,
        "timestamp": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "decision": args.decision,
        "findings": findings,
        "evidence": args.evidence or "",
        "levels": ["L1", "L2"] if args.stage in ("draft", "initial") else ["L3"],
    })
    fp.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 同步登记表 stages
    reg = load_registry()
    entry = reg["reports"].setdefault(rel, {"title": _title_of(path), "kind": "audit" if path.suffix.lower() == ".md" else "business",
                                            "business_line": "engine/report-audits", "status": "draft",
                                            "stages": {s: False for s in STAGES}, "mark": False})
    entry["stages"][args.stage] = args.decision == "pass"
    if args.stage == "initial" and args.decision == "pass":
        entry["status"] = "in-review"
    if args.stage == "final" and args.decision == "pass":
        entry["status"] = "audited"
        entry["audited_at"] = rec["reviews"][-1]["timestamp"]
    if args.decision == "reject":
        entry["status"] = "rejected"
    save_registry(reg)
    print(f"[review] {rel} · {STAGE_LABEL[args.stage]} · {args.decision} · 记录 {fp.name}")
    return 0


# ---------------------------------------------------------------- 标识

def _badge_html(audit_id: str, date: str, done: int, level: str = "full") -> str:
    """生成标识横幅。level=full 用 canonical navy；pre 用灰色并显式标注语义待完成。"""
    style = MARK_LEVEL_STYLE.get(level, MARK_LEVEL_STYLE["full"])
    if level == "pre":
        badge, meta = "预审通过（机器）", f"语义复核待完成 · {date} · 审查链 {done}/4 · {audit_id}"
    else:
        badge, meta = "已审计", f"终审通过 · {date} · 审查链 {done}/4 · {audit_id}"
    return (
        f'<div class="{MARK_CLASS}" data-audit-id="{audit_id}" data-mark-level="{level}" '
        f'style="{style}font:600 13px/1.6 system-ui,-apple-system,\'Segoe UI\',sans-serif;'
        'padding:8px 16px;text-align:center;letter-spacing:.02em">'
        f'<span class="audit-badge">{badge}</span>'
        f'<span class="audit-meta">{meta}</span>'
        f'</div>\n'
    )


def cmd_mark(args) -> int:
    path = _resolve(args.report)
    if path is None:
        return 2
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    reg = load_registry()
    entry = reg["reports"].get(rel)
    if not entry:
        print(f"[ERROR] 未登记：{rel}（先执行 init）", file=sys.stderr)
        return 2
    level = getattr(args, "level", "full")
    if level not in MARK_CHOICES:
        print(f"[ERROR] level 须为 {MARK_LEVELS}", file=sys.stderr)
        return 2
    stages = entry.get("stages", {})
    if level == "full" and not all(stages.get(s) for s in STAGES):
        print(f"[ERROR] 四环节未齐备，拒绝注入『已审计』标识：{rel}", file=sys.stderr)
        return 1
    if level == "pre" and not (stages.get("draft") and stages.get("initial")):
        print(f"[ERROR] 生成/初审未通过，拒绝注入『预审通过』标识：{rel}", file=sys.stderr)
        return 1
    audit_id = entry.get("audit_id") or _next_audit_id(reg)
    entry["audit_id"] = audit_id
    entry["mark_level"] = level
    entry["mark"] = True
    entry["status"] = "audited" if level == "full" else "in-review"
    entry.setdefault("audited_at", _dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    date = entry["audited_at"][:10]

    BACKUPS.mkdir(parents=True, exist_ok=True)
    bak = BACKUPS / (path.name + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)

    text = path.read_text(encoding="utf-8")
    done = sum(1 for s in STAGES if entry.get("stages", {}).get(s))
    if path.suffix.lower() == ".html":
        badge = _badge_html(audit_id, date, done, level)
        if f'class="{MARK_CLASS}"' in text:
            text = re.sub(r'<div class="audit-mark".*?</div>', badge.rstrip("\n"), text, count=1, flags=re.S)
        else:
            m = re.search(r"<body[^>]*>", text, re.I)
            if not m:
                print("[ERROR] 未找到 <body>", file=sys.stderr)
                return 2
            text = text[: m.end()] + "\n" + badge + text[m.end():]
    else:
        if level == "pre":
            badge = (f"> **【预审通过（机器）】** 语义复核待完成 · {date} · "
                    f"审查链 {done}/4 · 登记编号 {audit_id}\n\n")
        else:
            badge = (f"> **【已审计】** 终审通过 · 签发日期 {date} · "
                    f"审查链 {done}/4 · 登记编号 {audit_id}\n\n")
        if "【已审计】" in text or "【预审通过（机器）】" in text:
            text = re.sub(r"> \*\*【(?:已审计|预审通过（机器）)】\*\*.*?\n\n", badge, text, count=1, flags=re.S)
        else:
            m = re.search(r"^#\s+.*$", text, re.M)
            pos = m.end() if m else 0
            text = text[:pos] + "\n\n" + badge + text[pos:]
    path.write_text(text, encoding="utf-8")
    save_registry(reg)
    print(f"[mark] {rel} · {audit_id}")
    return 0


def cmd_unmark(args) -> int:
    path = _resolve(args.report)
    if path is None:
        return 2
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".html":
        text = re.sub(r'\n?<div class="audit-mark".*?</div>\n?', "\n", text, count=1, flags=re.S)
    else:
        text = re.sub(r"> \*\*【(?:已审计|预审通过（机器）)】\*\*.*?\n\n", "", text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")
    reg = load_registry()
    if rel in reg["reports"]:
        reg["reports"][rel]["mark"] = False
        reg["reports"][rel]["mark_level"] = "none"
        reg["reports"][rel]["status"] = "in-review"
        save_registry(reg)
    print(f"[unmark] {rel}")
    return 0


def _age_days(entry: dict) -> int | None:
    """登记天数（first_seen_at → 今日）；缺失 / 非法返回 None。"""
    ts = str(entry.get("first_seen_at", "") or "")
    if not ts:
        return None
    try:
        d = _dt.date.fromisoformat(ts[:10])
    except ValueError:
        return None
    return (_dt.date.today() - d).days


def in_grace(entry: dict, days: int = L3_GRACE_DAYS) -> bool:
    """是否处于 L3 宽限期（新报告 N 天内缺语义终审不阻断）。"""
    age = _age_days(entry)
    return age is not None and age <= days


def agent_stage_pass(rel: str, stage: str) -> bool:
    """是否存在由 Agent（非 ci-bot）完成的该环节 pass 记录（P0-2）。

    语义环节（second/final）以 Agent 记录为权威：只要 Agent 已 pass，
    CI 不得覆盖该记录，也不得据自身机器判定把语义环节降级。
    """
    rec = _last_stage(rel, stage)
    return bool(rec and rec.get("decision") == "pass"
                and rec.get("reviewer") not in ("ci-bot", ""))


def _next_audit_id(reg: dict) -> str:
    today = _dt.date.today().isoformat()
    n = sum(1 for r in reg["reports"].values() if str(r.get("audit_id", "")).startswith(f"AUD-{today}"))
    return f"AUD-{today}-{n + 1:03d}"


def cmd_index(_args) -> int:
    """刷新登记册 evidence 字段（吸收项 ③）。"""
    reg = load_registry()
    for rel, rec in reg.get("reports", {}).items():
        rec["evidence"] = build_evidence(rel, rec)
    save_registry(reg)
    print(f"[index] 已刷新 {len(reg.get('reports', {}))} 条登记的证据索引")
    return 0


def cmd_evidence(args) -> int:
    """打印单份报告的证据索引 JSON（实时计算）。"""
    path = _resolve(args.report)
    if path is None:
        return 2
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    entry = load_registry().get("reports", {}).get(rel, {})
    print(json.dumps(build_evidence(rel, entry), ensure_ascii=False, indent=2))
    return 0


def cmd_prune(_args) -> int:
    """移除登记路径不存在的失效条目（P-01）。幂等：无失效条目时不写盘。"""
    reg = load_registry()
    reports = reg.get("reports", {})
    stale = stale_paths(reports)
    for rel in stale:
        reports.pop(rel, None)
    if stale:
        save_registry(reg)
    print(f"[prune] 移除失效登记 {len(stale)} 条"
          + (f"：{', '.join(stale)}" if stale else "（无失效条目）"))
    return 0


def cmd_status(args) -> int:
    reg = load_registry()["reports"]
    if args.report:
        rel = str(_resolve(args.report).relative_to(ROOT)).replace("\\", "/") if _resolve(args.report) else args.report
        e = reg.get(rel)
        if not e:
            print(f"未登记：{rel}")
            return 1
        if not (ROOT / rel).exists():
            print(f"[STALE] 登记路径不存在：{rel}")
            return 2
        print(json.dumps({rel: e}, ensure_ascii=False, indent=2))
        return 0
    print(f"{'报告':<62} {'状态':<10} {'审查链':<10} {'标识'}")
    mark_label = {"full": "已审计", "pre": "预审通过", "none": "-"}
    for rel, e in sorted(reg.items()):
        done = sum(1 for s in STAGES if e.get("stages", {}).get(s))
        level = e.get("mark_level") if e.get("mark") else "none"
        print(f"{rel:<62} {e.get('status','-'):<10} {done}/4       {mark_label.get(level, '-')}")
    stale = stale_paths(reg)
    with_ev = sum(1 for e in reg.values() if e.get("evidence"))
    print(f"\n登记 {len(reg)} 条；失效条目（stale）：{len(stale)}；含证据索引：{with_ev}")
    for rel in stale:
        print(f"  [STALE] {rel}（登记路径不存在）")
    return 2 if stale else 0


# ---------------------------------------------------------------- 抽检与验收

def _review_file(rel: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", rel).strip("-") + ".json"
    return REVIEWS / slug


def _last_stage(rel: str, stage: str) -> dict | None:
    fp = _review_file(rel)
    if not fp.exists():
        return None
    rec = json.loads(fp.read_text(encoding="utf-8"))
    for r in reversed(rec.get("reviews", [])):
        if r.get("stage") == stage:
            return r
    return None


def _run_gate(probe: bool = True) -> dict:
    """调用优化流程统一门禁（optimization_gate）-> {ok, detail, errors, warnings}。

    P0-1：audit 与 ci 使用同一入口、同一 gate-period、同一 probe 策略，
    判定口径完全一致；machine_final 不再只做结构启发式。
    """
    try:
        import optimization_gate  # type: ignore
    except Exception as e:  # pragma: no cover
        return {"ok": False, "detail": f"optimization_gate 不可用：{e}", "errors": 1, "warnings": 0}
    try:
        rep = optimization_gate.run_checks(quiet=True, probe=probe)
    except Exception as e:  # pragma: no cover
        return {"ok": False, "detail": f"optimization_gate 执行异常：{e}", "errors": 1, "warnings": 0}
    errs = [c["name"] for c in rep.get("checks", []) if c.get("status") == "error"]
    detail = f"门禁错误 {len(errs)} 项" + (f"：{', '.join(errs[:5])}" if errs else "")
    return {"ok": not errs, "detail": detail, "errors": len(errs),
            "warnings": sum(1 for c in rep.get("checks", []) if c.get("status") == "warn")}


def _machine_final(path: Path, gate: dict | None = None) -> tuple[bool, str]:
    """机器终审（T2 / P0-1）：L2 结构 + 标题 + 锚点 + 统一门禁真实结果。

    gate 为 None 时回退到结构校验（单测 / 无工具环境兼容）；
    cmd_run --strict 传入 _run_gate()，确保 audit 与 ci 判定一致、不依赖关键词命中。
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    missing, _ = structure_check(path, "business")
    ok_l2 = len(missing) <= 1
    ok_title = bool(re.search(r"<title[^>]*>\s*\S", text, re.I))
    ids = set(re.findall(r'\bid="([^"]+)"', text))
    broken = sorted({a for a in re.findall(r'href="#([^"]+)"', text) if a not in ids})
    ok_anchor = not broken
    detail = f"L2 {10 - len(missing)}/10；标题 {'OK' if ok_title else '缺'}；断头锚点 {len(broken)}"
    ok_struct = ok_l2 and ok_title and ok_anchor
    if gate is None:
        return ok_struct, detail
    return (ok_struct and bool(gate.get("ok"))), f"{detail}；{gate.get('detail', '')}"


def _semantic_final(rel: str) -> tuple[bool, str]:
    """语义终审（T2）：须存在由 Agent（非 ci-bot）完成的 second 复核 pass 记录。

    只认领非 ci-bot 的 second 记录：机器环节（cmd_run）可能追加 ci-bot 的 second
    留痕，不得让它遮蔽 Agent 的 L3 语义复核（否则 fail-fast 会把已复核报告误判为待修）。
    """
    rec = _review_file(rel)
    if not rec.exists():
        return False, "无 second 复核记录"
    data = json.loads(rec.read_text(encoding="utf-8"))
    for r in reversed(data.get("reviews", [])):
        if r.get("stage") == "second" and r.get("reviewer") not in ("ci-bot", ""):
            ok = r.get("decision") == "pass"
            return bool(ok), f"reviewer={r.get('reviewer')} decision={r.get('decision')}"
    return False, "无 Agent second 复核记录（仅机器留痕）"


# ---------------------------------------------------------------- L3 SLA 超期检测

def _review_fp(reviews_dir: Path, rel: str) -> Path:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", rel).strip("-") + ".json"
    return Path(reviews_dir) / slug


def _last_agent_semantic_date(rel: str, reviews_dir: Path) -> _dt.date | None:
    """最后一条 Agent（非 ci-bot）second/final pass 记录的日期；无则 None。"""
    fp = _review_fp(reviews_dir, rel)
    if not fp.exists():
        return None
    try:
        data = json.loads(fp.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    ts = ""
    for r in data.get("reviews", []):
        if (r.get("stage") in SEMANTIC_STAGES
                and r.get("reviewer") not in ("ci-bot", "")
                and r.get("decision") == "pass"
                and r.get("timestamp")):
            ts = r["timestamp"]
    if not ts:
        return None
    try:
        return _dt.datetime.fromisoformat(ts).date()
    except ValueError:
        return None


def l3_overdue(reports: dict, reviews_dir: Path,
               today: _dt.date | str | None = None) -> list[dict]:
    """L3 SLA 超期检测（R3）：正式报告中距上次 Agent 语义终审超过 L3_GRACE_DAYS 的清单。

    基准：records/reviews/<slug>.json 中最后一条 Agent（非 ci-bot）second/final pass
    的 timestamp；缺失时回退登记的 first_seen_at。纯读、幂等、不写盘、无时间戳。
    """
    if today is None:
        today_d = _dt.date.today()
    elif isinstance(today, str):
        today_d = _dt.date.fromisoformat(today)
    else:
        today_d = today
    out: list[dict] = []
    for rel, entry in sorted(reports.items()):
        if entry.get("category") != "report":
            continue
        last = _last_agent_semantic_date(rel, reviews_dir)
        if last is not None:
            basis, base, last_iso = "review", last, last.isoformat()
        else:
            fs = str(entry.get("first_seen_at", "") or "")
            if not fs:
                continue
            try:
                base = _dt.date.fromisoformat(fs[:10])
            except ValueError:
                continue
            basis, last_iso = "first_seen_at", None
        days = (today_d - base).days
        if days > L3_GRACE_DAYS:
            out.append({"report": rel, "basis": basis,
                        "last_agent_review": last_iso, "days": days})
    return out


def cmd_l3_status(_args) -> int:
    """打印 L3 SLA 超期清单与计数；有超期返回 2（告警），无则 0。"""
    reg = load_registry()["reports"]
    overdue = l3_overdue(reg, REVIEWS)
    print(f"L3 SLA 超期检测：{len(overdue)} 份超期（阈值 {L3_GRACE_DAYS} 天）")
    for o in overdue:
        print(f"  [OVERDUE] {o['report']}  基准 {o['basis']}  距上次 Agent 语义终审 {o['days']} 天")
    if overdue:
        return 2
    print("无超期：全部正式报告均在 L3 SLA 内")
    return 0


def cmd_run(args) -> int:
    """确定性执行四环节（CI 用）。

    默认模式（向后兼容）：L2 + 来源/口径关键词。
    --strict 模式（T2）：final 由 machine_final + semantic_final 共同判定。

    P0-1：--strict 下 machine_final 消费 optimization_gate 真实结果（与 ci 同口径）。
    P0-2：语义环节（second/final）以 Agent 记录为权威，ci-bot 不得覆盖 Agent 的 pass。
    P0-3：新报告在 L3 宽限期（L3_GRACE_DAYS）内缺语义终审只告警（返回 2）；
          超期缺失或 machine_final 失败才 fail-fast 阻断（返回 1）。
    """
    cmd_init(None)
    reg = load_registry()
    reps = [r for r in collect_reports() if r["category"] == "report"]
    strict = getattr(args, "strict", False)
    # P0-1：统一门禁只跑一次（全量），结果注入每份报告的 machine_final。
    gate = _run_gate() if (strict and not getattr(args, "no_gate", False)) else None
    n_pass = n_block = n_grace = 0
    for r in reps:
        path = ROOT / r["path"]
        entry = reg["reports"].get(r["path"], {})
        grace = in_grace(entry)
        missing, _warn = structure_check(path, "business")
        text = path.read_text(encoding="utf-8", errors="replace")
        ok_l2 = len(missing) <= 1
        ok_src = ("来源" in text) or ("参考" in text)
        ok_cons = ("口径" in text)
        hard_fail = soft_fail = False
        if strict:
            m_ok, m_detail = _machine_final(path, gate)
            s_ok, s_detail = _semantic_final(r["path"])
            # P0-2：语义环节以 Agent 记录为权威，CI 机器判定不得降级 Agent 已 pass 的 second
            agent_second = agent_stage_pass(r["path"], "second")
            second_ok = (ok_src and ok_cons and m_ok) or agent_second
            results = {
                "draft": ok_l2,
                "initial": ok_l2,
                "second": second_ok,
                "final": m_ok and s_ok,
            }
            hard_fail = not m_ok
            soft_fail = not s_ok
            ev = (f"[strict] {m_detail}；来源可追溯 {'OK' if ok_src else '缺'}；"
                  f"口径一致 {'OK' if ok_cons else '缺'}；语义终审 {s_detail}")
        else:
            results = {
                "draft": ok_l2,
                "initial": ok_l2,
                "second": ok_src and ok_cons,
                "final": ok_l2 and ok_src and ok_cons,
            }
            hard_fail = not all(results.values())
            ev = (f"L2 要素 {10 - len(missing)}/10；来源可追溯 {'OK' if ok_src else '缺'}；"
                  f"口径一致 {'OK' if ok_cons else '缺'}；语义深度复核由 Agent 定期执行"
                  f"（关键词判定，非 A1–A8；建议启用 --strict）")
        # P0-3：机器环节失败始终阻断；语义缺失仅在 L3 宽限期外阻断
        blocking = hard_fail or (soft_fail and not grace)
        if not args.dry_run:
            for stage, ok in results.items():
                # second 为 Agent L3 语义复核阶段，机器不写留痕（避免 ci-bot 记录遮蔽 Agent 复核）
                if stage == "second" and strict:
                    continue
                decision = "pass" if ok else "fix"
                prev = _last_stage(r["path"], stage)
                if prev and prev.get("decision") == decision and prev.get("evidence") == ev:
                    continue  # 幂等：同结论不重复留痕
                ns = argparse.Namespace(report=r["path"], stage=stage, reviewer="ci-bot",
                                        decision=decision, finding=None, evidence=ev)
                cmd_review(ns)
            if strict:
                if results["final"]:
                    cmd_mark(argparse.Namespace(report=r["path"], level="full"))
                elif results["second"]:
                    cmd_mark(argparse.Namespace(report=r["path"], level="pre"))
            elif all(results.values()):
                cmd_mark(argparse.Namespace(report=r["path"], level="full"))
        n_pass += 1 if all(results.values()) else 0
        n_block += 1 if blocking else 0
        n_grace += 1 if (strict and soft_fail and not hard_fail and grace) else 0
        if blocking:
            flag = "BLOCK"
        elif strict and soft_fail and not hard_fail and grace:
            flag = "GRACE"
        elif all(results.values()):
            flag = "PASS"
        else:
            flag = "FIX"
        print(f"[{flag}] {r['path']}  {ev}")
    tail = ("（dry-run，未写记录）" if args.dry_run else "") + (" [strict]" if strict else "")
    if n_block:
        print(f"\n[run] 覆盖 {len(reps)} 份正式报告，通过 {n_pass}，阻断 {n_block}"
              f"（machine_final 失败或 L3 超宽限期缺失）{tail}")
        return 1
    if n_grace:
        print(f"\n[run] 覆盖 {len(reps)} 份正式报告，通过 {n_pass}，"
              f"宽限期内待 L3 {n_grace}（不阻断）{tail}")
        return 2
    print(f"\n[run] 覆盖 {len(reps)} 份正式报告，全部通过 {tail}")
    return 0


def cmd_sample(args) -> int:
    reg = load_registry()
    reps = [r for r in collect_reports() if r["path"] in reg["reports"]]
    # 分层：高风险（新业务线/审计类）100%，其余按比例
    high = [r for r in reps if r["kind"] == "audit" or reg["reports"][r["path"]]["business_line"] in
            ("content/tech/competitive-intelligence/dubai", "content/tech/industry-research/dubai")]
    rest = [r for r in reps if r not in high]
    rng = random.Random(args.seed)
    k = max(1, round(len(rest) * args.ratio))
    picked = high + rng.sample(rest, min(k, len(rest)))
    print(f"[sample] 总体 {len(reps)} · 抽取 {len(picked)}（高风险 {len(high)} 全抽 + 随机 {len(picked) - len(high)}）· ratio={args.ratio} seed={args.seed}")
    for r in picked:
        print("  " + r["path"])
    return 0


def cmd_accept(_args) -> int:
    reg = load_registry()
    reps = reg["reports"]
    # 指标单一事实源（T3 / P1-5）：audit 验收消费 metrics-dictionary，与 ci 的
    # optimization_gate metric_audit 同口径，避免双维护阈值。
    try:
        sys.path.insert(0, str(ROOT / "engine" / "tools"))
        import metric_registry  # type: ignore
        mrep = metric_registry.check_all_metrics(metric_registry.load_dictionary())
        dict_issues = mrep.get("issues", [])
        print(f"指标单一事实源：{len(mrep['metrics'])} 项；兜底 {mrep['fallback_count']} 项；"
              f"不达标 {len(mrep['failures'])} 项；问题 {len(dict_issues)} 项")
        for it in dict_issues[:5]:
            print(f"  [DICT] {it}")
    except Exception as e:  # pragma: no cover
        print(f"[DICT] 指标字典校验不可用：{e}")
    total = len(reps)
    if not total:
        print("[accept] 登记表为空")
        return 1
    all_reps = collect_reports()
    formal = [r for r in all_reps if r["category"] == "report"]
    audited = [r for r in formal if reps.get(r["path"], {}).get("status") == "audited"]
    complete = [r for r in formal if all(reps.get(r["path"], {}).get("stages", {}).get(s) for s in STAGES)]
    marked = [r for r in formal if reps.get(r["path"], {}).get("mark")]
    def _consistent(e: dict) -> bool:
        # full ↔ audited；pre ↔ in-review（预审通过本就对应未完成终审）
        return ((e.get("mark_level") == "full" and e.get("status") == "audited")
                or (e.get("mark_level") == "pre" and e.get("status") == "in-review"))

    consistent = [r for r in marked if _consistent(reps.get(r["path"], {}))]
    pre = [r for r in marked if reps.get(r["path"], {}).get("mark_level") == "pre"]
    full = [r for r in marked if reps.get(r["path"], {}).get("mark_level") == "full"]
    other = [r for r in all_reps if r["category"] != "report"]
    print(f"登记覆盖率（全量）：{total}/{len(all_reps)} = {total / max(1, len(all_reps)):.1%}")
    print(f"正式报告流程完备率：{len(complete)}/{len(formal)} = {len(complete) / max(1, len(formal)):.1%}（阈值 ≥95%）")
    print(f"正式报告已审计率：{len(audited)}/{len(formal)} = {len(audited) / max(1, len(formal)):.1%}")
    print(f"标识分级：已审计（full）{len(full)} · 预审通过（pre）{len(pre)} · 其他 {len(marked) - len(full) - len(pre)}")
    print(f"标识一致率：{len(consistent)}/{len(marked) or 1} = {len(consistent) / (len(marked) or 1):.1%}（阈值 100%）")
    print(f"其他登记（归档/审计文档）：{len(other)} 份（登记管理，不适用完整四环节）")
    return 0


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="审计报告标准化管理工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inventory")
    sub.add_parser("init")
    sub.add_parser("prune", help="移除登记路径不存在的失效条目（stale）")
    sub.add_parser("index", help="刷新登记册 evidence 字段（证据索引）")
    p = sub.add_parser("evidence", help="打印单份报告的证据索引 JSON")
    p.add_argument("report")
    p = sub.add_parser("structure"); p.add_argument("report")
    p = sub.add_parser("verify"); p.add_argument("report")
    p = sub.add_parser("review")
    p.add_argument("report"); p.add_argument("--stage", required=True); p.add_argument("--reviewer", default="agent")
    p.add_argument("--decision", choices=["pass", "fix", "reject"], default="pass")
    p.add_argument("--finding", action="append"); p.add_argument("--evidence", default="")
    p = sub.add_parser("mark"); p.add_argument("report"); p.add_argument("--level", choices=MARK_CHOICES, default="full")
    p = sub.add_parser("unmark"); p.add_argument("report")
    p = sub.add_parser("status"); p.add_argument("report", nargs="?")
    p = sub.add_parser("sample"); p.add_argument("--ratio", type=float, default=0.2); p.add_argument("--seed", type=int, default=20261114)
    sub.add_parser("accept")
    sub.add_parser("l3-status", help="L3 SLA 超期检测（每两周覆盖全部正式报告）")
    p = sub.add_parser("run"); p.add_argument("--dry-run", action="store_true"); p.add_argument("--strict", action="store_true")
    p.add_argument("--no-gate", action="store_true",
                   help="严格模式下不内部重跑统一门禁（由调用方统一执行，避免重复）")
    args = ap.parse_args()
    return {
        "inventory": cmd_inventory, "init": cmd_init, "prune": cmd_prune,
        "index": cmd_index, "evidence": cmd_evidence,
        "structure": cmd_structure, "verify": cmd_verify,
        "review": cmd_review, "mark": cmd_mark, "unmark": cmd_unmark, "status": cmd_status,
        "sample": cmd_sample, "accept": cmd_accept, "run": cmd_run,
        "l3-status": cmd_l3_status,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
