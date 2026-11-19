"""决策交付门禁（DECISION-DELIVERY-SPEC v1.0）。

检查：
    DC-01 决策卡字段：结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度（decision-hub 强制）
    DC-02 行动协议：触发条件 + 阈值 + 责任角色 + 时限 + 可观测验证指标，且三档优先级
    DC-03 场景切片：投资决策 / 就业决策 / 政策制定
    DC-04 ex-ante 标注：信号灯 / 阈值处含「预校准（ex-ante）」
    DC-08 证据强度一致性：决策卡「证据强度」与支撑事实卡 level 推导结果一致，且与台账一致

新报告缺项 = [E]；历史报告 = [W]。退出码 0/1/2。

用法：
    python engine/tools/decision_hub_check.py
    python engine/tools/decision_hub_check.py --gate-period 2026-12
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, detect_report, iter_business_dirs  # noqa: E402
from gate_period import AUTO  # noqa: E402
from gate_period import resolve as resolve_period

DEFAULT_GATE = AUTO
# 跨研究线决策层业务线目录段（content/economy/insight）
HUB_LINE = "insight"

_PROTOCOL_KEYS = ("触发条件", "阈值", "责任角色", "时限", "验证指标")
_PRIO_KEYS = ("立即行动", "持续观察", "仅记录存档")
_SLICE_KEYS = ("投资决策", "就业决策", "政策制定")
_CARD_KEYS = ("结论", "证据强度", "触发条件", "反向证据", "信息充分度")
# 卡片级必备字段：决策卡块内必须出现的三个（触发条件 / 信息充分度允许位于
# dc-head 或报告其他章节，故不做卡片级强制）
_CARD_LEVEL_KEYS = ("结论", "证据强度", "反向证据")
_CARD_FIELD_RE = re.compile(r'<span class="k">([^<]+)：</span>(.*?)</div>', re.DOTALL)
_CARD_HEAD_RE = re.compile(
    r'<span class="dc-title">([^<]+)</span><span class="ev-\w+">证据强度：(\S+?)</span>')
_FC_REF_RE = re.compile(r"\[FC-[A-Z]+-\d+\]")
_LEDGER_RELPATH = "data/processed/economy/insight/decision_cards.json"
_VERIFIED = "已核验事实"
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_STYLE_RE = re.compile(r"<(style|script)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
_CARD_RE = re.compile(r'<div class="decision-card"')
_ACTION_RE = re.compile(r'<div class="a-head"')
_TAG_RE = re.compile(r"<[^>]+>")


def _period_key(period: str) -> tuple:
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", period)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{4})-(\d{2})", period)
    if m:
        return (int(m.group(1)), int(m.group(2)), 0)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", period)
    if m:
        return (int(m.group(1)), int(m.group(2)) * 3, 0)
    m = re.fullmatch(r"(\d{4})", period)
    if m:
        return (int(m.group(1)), 12, 31)
    return (0, 0, 0)


def _period_of(name: str) -> str:
    det = detect_report(name)
    return det[1] if det else ""


def _strip_noise(html: str) -> str:
    """剥离注释与 style/script（防注释误判：trends 周报曾在 CSS 注释中写「决策卡」）。"""
    return _STYLE_RE.sub("", _COMMENT_RE.sub("", html))


def _blocks(text: str, start_re: re.Pattern) -> list[str]:
    """按起始标记切分出各卡片 / 行动项块（到下一个同类起始或文末）。"""
    ms = list(start_re.finditer(text))
    return [text[m.start(): ms[i + 1].start() if i + 1 < len(ms) else len(text)]
            for i, m in enumerate(ms)]


def check_text(text: str, business_line: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    text = _strip_noise(text)
    is_hub = HUB_LINE in business_line

    # DC-01 决策卡（decision-hub 强制；其他报告含「决策卡」字样时同样检查）
    if is_hub or "决策卡" in text:
        missing = [k for k in _CARD_KEYS if k not in text]
        if missing:
            out.append(("DC-01", f"决策卡缺字段：{'、'.join(missing)}"))
        # 卡片级逐卡校验：每张 decision-card 必须具备结论 / 证据强度 / 反向证据
        cards = _blocks(text, _CARD_RE)
        if cards:
            bad = [i + 1 for i, c in enumerate(cards)
                   if any(k not in _TAG_RE.sub("", c) for k in _CARD_LEVEL_KEYS)]
            if bad:
                out.append(("DC-01", f"第 {'、'.join(map(str, bad))} 张决策卡缺卡片级字段"
                                    f"（{'、'.join(_CARD_LEVEL_KEYS)}）"))

    # DC-02 行动协议（含「可执行启示 / 行动 / 行动项」的报告）
    if any(k in text for k in ("可执行启示", "行动项", "行动协议", "立即行动", "持续观察")):
        missing = [k for k in _PROTOCOL_KEYS if k not in text]
        if missing:
            out.append(("DC-02", f"行动协议缺要素：{'、'.join(missing)}"))
        # 逐条行动项校验：每个 a-head 块须含五要素
        acts = _blocks(text, _ACTION_RE)
        if acts:
            bad = [i + 1 for i, a in enumerate(acts)
                   if any(k not in _TAG_RE.sub("", a) for k in _PROTOCOL_KEYS)]
            if bad:
                out.append(("DC-02", f"第 {'、'.join(map(str, bad))} 条行动项缺要素"
                                    f"（{'、'.join(_PROTOCOL_KEYS)}）"))
            # 阈值须可观测：数值 / 区间 / 日期（P1-4：定性表述不可自动判定）
            thr_bad = []
            for i, a in enumerate(acts):
                m = re.search(r"阈值：</b>\s*([^<]*)", a)
                if m and not re.search(r"\d", m.group(1)):
                    thr_bad.append(i + 1)
            if thr_bad:
                out.append(("DC-02", f"第 {'、'.join(map(str, thr_bad))} 条行动项阈值为定性表述"
                                    f"（须为数值 / 区间 / 日期）"))
        if not all(k in text for k in _PRIO_KEYS):
            out.append(("DC-02", "行动项未按三档优先级（立即行动 / 持续观察 / 仅记录存档）划分"))

    # DC-03 场景切片
    if is_hub or "场景切片" in text:
        hit = [k for k in _SLICE_KEYS if k in text]
        if is_hub:
            missing = [k for k in _SLICE_KEYS if k not in text]
            if missing:
                out.append(("DC-03", f"决策仪表盘场景切片缺：{'、'.join(missing)}"))
        elif not hit:
            out.append(("DC-03", "未声明任何场景切片（投资决策 / 就业决策 / 政策制定）"))

    # DC-04 ex-ante 标注（含信号灯 / 阈值的报告）
    if ("信号灯" in text or "阈值" in text) and "预校准" not in text and "ex-ante" not in text:
        out.append(("DC-04", "信号灯 / 阈值处缺「预校准（ex-ante）」标注"))
    return out


_FC_INDEX: dict | None = None


def fact_card_index() -> dict:
    """事实卡片索引（card_id → 卡片），来自 engine/fact_cards/*.json。"""
    global _FC_INDEX
    if _FC_INDEX is None:
        idx: dict = {}
        fcdir = ROOT / "engine" / "fact_cards"
        if fcdir.is_dir():
            for f in sorted(fcdir.glob("*.json")):
                try:
                    data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
                except (OSError, ValueError):
                    continue
                for c in data.get("cards", []):
                    if c.get("card_id"):
                        idx[c["card_id"]] = c
        _FC_INDEX = idx
    return _FC_INDEX


def derive_strength(entries: list[tuple[str, str]]) -> str:
    """由支撑卡 (level, source) 推导证据强度。

    强 = 关键事实全部「已核验事实」且来源 ≥ 2（双源）；
    弱 = 含「推断 / 假设」；其余（主体已核验）= 中。
    """
    if not entries:
        return ""
    if any(lv in ("推断", "假设") for lv, _s in entries):
        return "弱"
    if all(lv == _VERIFIED for lv, _s in entries) and len({s for _lv, s in entries}) >= 2:
        return "强"
    return "中"


def load_ledger() -> dict:
    """决策卡台账 card_id → evidence_strength。"""
    p = ROOT / _LEDGER_RELPATH
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {}
    return {c.get("card_id"): c.get("evidence_strength", "") for c in data.get("cards", [])}


def dc08_strength(text: str, ledger: dict) -> list[tuple[str, str]]:
    """DC-08：报告决策卡「证据强度」与支撑卡等级推导结果、台账三方一致。

    支撑卡 = 决策卡「证据来源」字段中引用的事实卡片；未引用支撑卡的决策卡
    （如无事实卡底座的业务线）不参与推导，仅做台账一致性校验。
    """
    out: list[tuple[str, str]] = []
    idx = fact_card_index()
    for blk in _blocks(text, _CARD_RE):
        head = _CARD_HEAD_RE.search(blk)
        if not head:
            continue
        card_id = head.group(1).split("·")[0].strip()
        stated = head.group(2)
        fields = {k: v for k, v in _CARD_FIELD_RE.findall(blk)}
        entries = []
        for ref in dict.fromkeys(_FC_REF_RE.findall(fields.get("证据来源", ""))):
            c = idx.get(ref[1:-1])
            if c:
                entries.append((c.get("level", ""), c.get("source", "")))
        if entries:
            expected = derive_strength(entries)
            if expected and expected != stated:
                out.append(("DC-08", f"{card_id} 证据强度标「{stated}」，"
                                        f"据支撑卡等级应为「{expected}」"))
        if card_id in ledger and ledger[card_id] and ledger[card_id] != stated:
            out.append(("DC-08", f"{card_id} 报告标「{stated}」与台账 "
                                    f"{_LEDGER_RELPATH} 的「{ledger[card_id]}」不一致"))
    return out


def iter_targets(only_file: str | None):
    if only_file:
        p = ROOT / only_file
        return [(p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8", errors="replace"),
                 _period_of(p.name), "")]
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            out.append((f"{b.rel}/reports/{f.name}",
                        f.read_text(encoding="utf-8", errors="replace"),
                        _period_of(f.name), b.rel))
    return out


def run(only_file: str | None, gate: str) -> tuple[int, int, list[str]]:
    gate = resolve_period(gate)
    errors = warnings = 0
    lines = []
    targets = iter_targets(only_file)
    if not targets:
        lines.append("决策交付门禁：未发现报告，跳过")
        return 0, 0, lines
    ledger = load_ledger()
    for rel, text, period, bline in targets:
        findings = check_text(text, bline)
        if HUB_LINE in bline:
            findings = findings + dc08_strength(text, ledger)
        if not findings:
            continue
        is_new = bool(period) and _period_key(period) >= _period_key(gate)
        for rule, msg in findings:
            level = "E" if is_new else "W"
            if level == "E":
                errors += 1
            else:
                warnings += 1
            tag = "新报告" if is_new else "历史报告"
            lines.append(f"[{level}] {rel}（{tag}，周期 {period or '未识别'}）{rule}：{msg}")
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="决策交付门禁")
    ap.add_argument("--file")
    ap.add_argument("--gate-period", default=DEFAULT_GATE)
    args = ap.parse_args()
    errors, warnings, lines = run(args.file, args.gate_period)
    for line in lines:
        print(line)
    if errors:
        print(f"决策交付门禁失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"决策交付门禁：{warnings} 项历史报告警告（不阻断）")
        return 2
    print("决策交付门禁通过：决策卡 / 行动协议 / 场景切片 / ex-ante 齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
