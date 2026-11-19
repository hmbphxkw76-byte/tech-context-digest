"""报告模板合规校验（CI: ci.yml 阻断式校验关卡 / scheduled-maintenance 定期合规审计）。

依据 engine/templates/compliance-rules.json（已注册类型（当前 13+）的结构骨架规则），
对业务线 reports/*.html 逐份校验：
- 结构完整性：h2 节数与类型模板骨架一致（缺失=错误阻断；超额=警告，业务固化锚需人工确认）；
  已编号节（id="sN"）必须 s1..sN 连续且有序
- 必填字段：<title> 非空、周期报告（月/季/年）顶部导航（基线缺失降为警告）
- 内容格式：导航/正文锚点 href="#x" 必须存在对应 id（无断头锚点）

报告类型自动识别：读取业务线 prompts/business-config.md 继承声明中的
engine/templates/<类型ID>/ 引用；命名不识别的报告按警告处理（与 validate.py 口径一致）。

退出码：0 = 通过；1 = 存在错误项（CI 阻断合并）；2 = 仅警告项 / 审计发现不匹配项。

用法：
    python engine/tools/compliance_check.py                # 全量校验（CI 关卡）
    python engine/tools/compliance_check.py --file <路径>   # 校验单份报告
    python engine/tools/compliance_check.py --list-types   # 列出已注册类型与模板引用入口
    python engine/tools/compliance_check.py --scaffold <类型ID> [周期]   # 模板自动填充引导
    python engine/tools/compliance_check.py --audit        # 历史报告合规审计（写报告，不阻断）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import AUDIT_DIR, ROOT, TEMPLATE_DIR, detect_report, iter_business_dirs  # noqa: E402

RULES_PATH = TEMPLATE_DIR / "compliance-rules.json"

H2_RE = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.DOTALL)
H2_ID_RE = re.compile(r"<h2\b[^>]*\bid=\"(s\d+)\"")
ID_ATTR_RE = re.compile(r"\bid=\"([^\"]+)\"")
HREF_ANCHOR_RE = re.compile(r"href=\"#([^\"]+)\"")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.DOTALL)
TYPE_REF_RE = re.compile(r"engine/templates/([a-z0-9]+(?:-[a-z0-9]+)*)/")


def load_rules() -> dict:
    """读取合规规则文件；缺失或非法时报错退出。"""
    try:
        data = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[ERROR] 缺少合规规则文件: {RULES_PATH.relative_to(ROOT)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] 合规规则文件非法 JSON: {e}")
        sys.exit(1)
    return data


def detect_type(config_text: str):
    """从业务配置继承声明识别报告类型 -> 类型 ID；无引用返回 None。"""
    m = TYPE_REF_RE.search(config_text)
    return m.group(1) if m else None


def cycle_rule(rules: dict, type_id: str, cycle: str, brel: str = ""):
    """查 (类型, 周期) 规则。业务级覆盖优先（business_overrides）；否则按类型规则，
    周期未单独登记时按「结构逐字继承基线」回落到基线节数。

    返回 (rule_dict, inherited)；类型未注册返回 (None, False)。
    """
    t = rules["types"].get(type_id)
    if not t:
        return None, False
    ovr = rules.get("business_overrides", {}).get(brel)
    if ovr and cycle in ovr:
        r = dict(ovr[cycle])
        r.setdefault("inherited", False)
        r.setdefault("nav", cycle in rules.get("common", {}).get("nav_required_cycles", ()))
        return r, False
    r = dict(t.get("cycles", {}).get(cycle) or {})
    if not r:
        base = t["cycles"]["baseline"]
        r = {"sections": base["sections"], "nav": base.get("nav", False), "inherited": True}
    r.setdefault("nav", cycle in rules.get("common", {}).get("nav_required_cycles", ()))
    return r, r.get("inherited", False)


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def check_report(text: str, rule: dict, common: dict) -> list[tuple[str, str]]:
    """对单份 HTML 按 (类型, 周期) 规则校验 -> [(level, message), ...]，level in {'E','W'}。

    纯函数，供 tests/ 直接调用。rule = cycle_rule() 输出；common = 规则文件 common 节。
    """
    issues: list[tuple[str, str]] = []
    expected = rule["sections"]

    # 结构完整性：h2 节数
    h2s = H2_RE.findall(text)
    n = len(h2s)
    if n < expected:
        issues.append(("E", f"结构不完整：h2 节数 {n} 少于模板骨架 {expected} 节（缺失即阻断）"))
    elif n > expected:
        issues.append(
            ("W", f"h2 节数 {n} 超出模板骨架 {expected} 节（如为业务固化锚请人工确认，"
                  f"否则须对齐类型模板 {rule.get('template', '')}）")
        )

    # 已编号节的连续性：id="sN" 必须恰为 s1..sN 且按出现顺序
    ids = H2_ID_RE.findall(text)
    if ids:
        want = [f"s{i}" for i in range(1, len(ids) + 1)]
        if ids != want:
            issues.append(("E", f"章节编号不连续或不有序：实际 {','.join(ids)}，期望 {','.join(want)}"))

    # 必填字段：title / 顶部导航
    title = TITLE_RE.search(text)
    if common.get("require_title") and (not title or not strip_tags(title.group(1)).strip()):
        issues.append(("E", "缺少 <title> 或标题为空（必填字段）"))
    if rule.get("nav") and not re.search(r'<nav\b[^>]*aria-label="报告导航"', text):
        issues.append(("E", "周期报告缺少顶部导航 <nav aria-label=\"报告导航\">（通用规范第 5 节强制）"))
    elif not rule.get("nav") and not re.search(r"<nav\b", text):
        issues.append(("W", "基线报告缺少简化锚点导航 <nav>（建议补充，不阻断）"))

    # 内容格式：锚点无断链
    if common.get("anchor_check"):
        all_ids = set(ID_ATTR_RE.findall(text))
        broken = sorted({a for a in HREF_ANCHOR_RE.findall(text) if a not in all_ids})
        if broken:
            issues.append(("E", f"存在断头锚点（href=\"#…\" 无对应 id）: {', '.join(broken)}"))

    return issues


def type_of_business(b) -> tuple[str, str | None]:
    """识别业务线报告类型 -> (类型 ID, 警告说明)；识别成功时说明为 None。"""
    config = b.path / "prompts" / "business-config.md"
    if not config.exists():
        return "", f"{b.rel}: 缺少 prompts/business-config.md，无法自动识别报告类型"
    text = config.read_text(encoding="utf-8", errors="replace")
    type_id = detect_type(text) or ""
    if not type_id:
        return "", f"{b.rel}: business-config.md 继承声明未引用 engine/templates/<类型ID>/"
    return type_id, None


def _business_rel_of(path: Path) -> str:
    """向上找到含 prompts/business-config.md 的业务线目录，返回其仓库相对路径。"""
    for parent in path.parents:
        if (parent / "prompts" / "business-config.md").exists():
            return parent.relative_to(ROOT).as_posix()
    return ""


def collect_targets(only_file: str | None):
    """收集待校验报告 -> [(relpath, text, type_id, cycle, note, brel)]。note 为警告性说明（可为 None）。"""
    out: list[tuple[str, str, str, str, str | None, str]] = []
    if only_file:
        p = ROOT / only_file
        text = p.read_text(encoding="utf-8", errors="replace")
        cycle = detect_report(p.name)
        type_id = ""
        brel = _business_rel_of(p)
        if brel:
            cfg = ROOT / brel / "prompts" / "business-config.md"
            type_id = detect_type(cfg.read_text(encoding="utf-8", errors="replace")) or ""
        out.append(
            (p.relative_to(ROOT).as_posix(), text, type_id, cycle[0] if cycle else "",
             None if cycle else "文件名不符合报告命名约定，无法识别周期（按警告处理）", brel)
        )
        return out
    for b in iter_business_dirs():
        type_id, note = type_of_business(b)
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            detected = detect_report(f.name)
            note_f = note
            cycle = ""
            if detected:
                cycle = detected[0]
            else:
                extra = "文件名不符合报告命名约定，无法识别周期（按警告处理）"
                note_f = f"{note}；{extra}" if note else extra
            out.append((f"{b.rel}/reports/{f.name}", f.read_text(encoding="utf-8", errors="replace"),
                        type_id, cycle, note_f, b.rel))
    return out


def run_check(only_file: str | None) -> tuple[int, int, list[str]]:
    """执行全量校验 -> (errors, warnings, 输出行)。"""
    rules = load_rules()
    common = rules.get("common", {})
    targets = collect_targets(only_file)
    errors = warnings = 0
    lines: list[str] = []
    if not targets:
        lines.append("合规校验：未发现报告 HTML，跳过")
        return 0, 0, lines
    for rel, text, type_id, cycle, note, brel in targets:
        if note:
            lines.append(f"[W] {rel}: {note}")
            warnings += 1
        if not type_id:
            if not note:
                lines.append(f"[W] {rel}: 报告类型未注册，跳过结构校验")
                warnings += 1
            continue
        rule, inherited = cycle_rule(rules, type_id, cycle or "baseline", brel)
        if rule is None:
            lines.append(f"[W] {rel}: 类型 {type_id} 未在 compliance-rules.json 登记，跳过结构校验")
            warnings += 1
            continue
        if inherited:
            lines.append(f"[INFO] {rel}: 周期「{cycle}」未单独登记，按基线骨架（结构逐字继承）校验")
        for level, msg in check_report(text, rule, common):
            lines.append(f"[{level}] {rel}: [{type_id}/{cycle or '未识别周期'}] {msg}")
            if level == "E":
                errors += 1
            else:
                warnings += 1
    return errors, warnings, lines


def run_audit(outdir: Path) -> tuple[int, int, int, Path]:
    """历史报告合规审计 -> (总数, 合规数, 违规报告数, 审计报告路径)。"""
    _errors, _warnings, lines = run_check(None)  # 仅取渲染行；明细统计由下方逐报告重算
    rules = load_rules()
    targets = collect_targets(None)
    total = len(targets)
    # 违规报告数：按报告维度统计（含警告）
    violated = 0
    for _rel, _text, type_id, cycle, note, brel in targets:
        bad = bool(note) or not type_id
        if type_id and not bad:
            rule, _ = cycle_rule(rules, type_id, cycle or "baseline", brel)
            bad = bool(check_report(_text, rule, rules.get("common", {})))
        if bad:
            violated += 1
    compliant = total - violated

    outdir.mkdir(exist_ok=True)
    audit_path = outdir / "compliance-audit.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rate = f"{compliant / total * 100:.0f}%" if total else "N/A"
    # 逐报告明细（即使全部匹配也列出，保证审计报告内容完整、可复核）。
    detail_lines = []
    for rel, text, type_id, cycle, note, brel in targets:
        bad = bool(note) or not type_id
        if type_id and not bad:
            rule, _ = cycle_rule(rules, type_id, cycle or "baseline", brel)
            bad = bool(check_report(text, rule, rules.get("common", {})))
        status = "不符合 ⚠️" if bad else "匹配 ✅"
        detail_lines.append(
            f"- {status}  `{rel}`  （类型 `{type_id or '未注册'}` / 周期 `{cycle or '未识别'}`）")
    body = [
        "# 报告合规性审计（历史报告 × 类型模板匹配度）",
        "",
        f"- **审计时间**：{now}",
        f"- **审计范围**：全部业务线 reports/*.html（共 {total} 份）",
        f"- **匹配度**：{compliant}/{total}（{rate}）报告与对应类型模板规则完全匹配",
"- **规则来源**：[compliance-rules.json](../templates/compliance-rules.json)"
            "（已注册类型结构骨架，与 [template-registry.md](../templates/template-registry.md) 登记一致）",
        f"- **结论**：{'全部合规 ✅' if violated == 0 else f'{violated} 份报告存在不符合项，需整改 ⚠️'}",
        "",
        "## 明细",
        "",
        *detail_lines,
        "",
    ]
    if lines:
        body += ["## 不符合项明细", "", "```", *lines, "```", ""]
    audit_path.write_text("\n".join(body), encoding="utf-8")
    return total, compliant, violated, audit_path


def run_scaffold(type_id: str, cycle: str | None) -> int:
    """模板自动填充引导：输出骨架、模板引用入口与合规自检要点。"""
    rules = load_rules()
    t = rules["types"].get(type_id)
    if not t:
        print(f"[ERROR] 未注册的报告类型: {type_id}（用 --list-types 查看已注册类型）")
        return 1
    cycles = t.get("cycles", {})
    if cycle is None:
        cycle = "baseline" if "baseline" in cycles else next(iter(cycles))
    if cycle not in cycles:
        print(f"[ERROR] 类型 {type_id} 无周期「{cycle}」；可用周期: {', '.join(cycles)}")
        return 1
    rule, _inherited = cycle_rule(rules, type_id, cycle)
    titles = rule.get("section_titles") or t.get("section_titles") or []
    n = rule["sections"]
    print(f"# {t['name']}（{type_id}）· 周期：{cycle} — 模板自动填充引导\n")
    print(f"标准模板引用入口：engine/templates/{type_id}/{rule.get('template', '（结构逐字继承基线）')}")
    print("渲染规范：engine/templates/monitoring-common-spec.md（跨类型最低渲染标准）\n")
    print(f"## 报告结构骨架（{n} 节固定顺序，不得增删节、调整顺序）\n")
    for i, title in enumerate(titles, start=1):
        print(f"| {i} | {title} | id=\"s{i}\" |" if titles and len(titles) == n
              else f"{i}. {title}")
    print("\n## 填充与合规自检要点\n")
    print("- 节标题可按业务细化措辞，但节数、顺序、编号（id=\"s1\"..\"s%d\"）不得改变" % n)
    print("- 顶部导航 <nav class=\"report-nav\" aria-label=\"报告导航\">：锚点标签与节标题逐字一致"
          if rule.get("nav") else "- 基线报告保留简化锚点导航（<nav aria-label=\"报告导航\">）")
    print("- <title> 非空；全部锚点 href=\"#x\" 必须有对应 id")
    print("- 表格 / 图表 / 来源链接格式见 monitoring-common-spec.md 第 2–5 节")
    print("\n完成后自检：python engine/tools/compliance_check.py --file <报告路径>")
    return 0


def run_list_types() -> int:
    rules = load_rules()
    print("已注册报告类型（规则与 template-registry.md 第二节登记一致）：\n")
    for tid, t in rules["types"].items():
        cycles = ", ".join(t.get("cycles", {}))
        print(f"- {tid}（{t['name']}）：周期 {cycles}；模板入口 {t['template_dir']}")
    print("\n模板自动填充引导：python engine/tools/compliance_check.py --scaffold <类型ID> [周期]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="报告模板合规校验")
    ap.add_argument("--check", action="store_true", help="全量校验（缺省行为，参数仅为显式声明）")
    ap.add_argument("--file", help="只校验单份报告（仓库相对路径）")
    ap.add_argument("--audit", action="store_true", help="历史报告合规审计（写审计报告，不阻断）")
    ap.add_argument("--audit-out", default=str(AUDIT_DIR), help="审计报告输出目录")
    ap.add_argument("--scaffold", nargs="+", metavar="参数",
                    help="模板自动填充引导：--scaffold <类型ID> [周期]")
    ap.add_argument("--list-types", action="store_true", help="列出已注册类型与模板引用入口")
    args = ap.parse_args()

    if args.list_types:
        return run_list_types()
    if args.scaffold:
        if not 1 <= len(args.scaffold) <= 2:
            print("[ERROR] --scaffold 用法：--scaffold <类型ID> [周期]")
            return 1
        return run_scaffold(args.scaffold[0], args.scaffold[1] if len(args.scaffold) > 1 else None)
    if args.audit:
        total, compliant, violated, path = run_audit(Path(args.audit_out))
        print(f"合规审计完成：{compliant}/{total} 份报告与类型模板完全匹配（匹配度 "
              f"{compliant / total * 100:.0f}%）；审计报告已写入 {path.relative_to(ROOT)}")
        if violated:
            print(f"审计发现 {violated} 份报告存在不符合项（见明细，不阻断）")
            return 2
        return 0

    errors, warnings, lines = run_check(args.file)
    for line in lines:
        print(line)
    if errors:
        print(f"模板合规校验失败：{errors} 项错误，{warnings} 项警告（错误项阻断合并）")
        return 1
    if warnings:
        print(f"模板合规校验存在 {warnings} 项警告（无错误，不阻断）")
        return 2
    print("模板合规校验通过：全部报告与对应类型模板规则一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
