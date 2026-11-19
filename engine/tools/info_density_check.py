"""信息密度与分层交付门禁（INFORMATION-LAYERING-SPEC v1.0）。

检查规则（新报告缺项 = [E] 阻断；历史报告 = [W] 不阻断）：
    ID-01 分层结构：含决策摘要节；共享 boilerplate 未在正文整段复制
    ID-02 决策摘要长度：≤ 1 屏阈值（约 900 中文字符 / 12 要点，取更严）
    ID-03 信息等级标注：关键信息带四级标记之一
    ID-04 摘要引用约束：决策摘要无「假设乘积」点值（须区间化）
    ID-05 新增信息模块：含「本期新增 / 修正 / 无变化 / 假设核验进度」四要素
    ID-06 指针引用：关键指标以编号 + 指针引用
    ID-07 事实卡片：共享域报告使用 [FC-…] 指针
    ID-08 场景切片：业务配置声明场景；报告含对应切片或指针
    DC-05 版本治理：核验 / 收敛型报告含「读数时点」

退出码：0 通过；1 存在 [E]；2 仅 [W]。

用法：
    python engine/tools/info_density_check.py            # 全量
    python engine/tools/info_density_check.py --file <报告>
    python engine/tools/info_density_check.py --gate-period 2026-12
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, detect_report, iter_business_dirs  # noqa: E402
from gate_period import AUTO  # noqa: E402
from gate_period import resolve as resolve_period

DEFAULT_GATE = AUTO

# 共享 boilerplate 特征（通用基座第四节来源分级规则的完整复述）
_BOILERPLATE_TIERS = ("① 官方一手", "② 行业机构", "③ 挂牌门户", "④ 媒体转述")
_LVL_CLASS_RE = re.compile(r'class="lvl lvl-(verified|partial|inferred|assumption)"')
_LVL_TEXT_RE = re.compile(r"(已核验事实|部分核验|推断|假设)")
_FC_REF_RE = re.compile(r"\[FC-[A-Z]+-\d+\]")
_METRIC_ID_RE = re.compile(r"\b([KPSMGRL]\d{2}|P\d{1,2}|S\d{1,2}|M\d{1,2}|G0\d)\b")
_H2_RE = re.compile(r'<h2 class="sec"[^>]*>(.*?)</h2>', re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
# 注释与 style/script 块不得参与判定：否则 CSS 注释里的「决策卡」「推断」等字样会
# 造成误判（2026-11-18 实测：trends 周报靠 CSS 注释通过 decision_hub_check）。
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_STYLE_RE = re.compile(r"<(style|script)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)
# 摘要内的口径/局限提示块不是结论，其「预校准（ex-ante）」等等级标记不应判为摘要越级
_NOTE_RE = re.compile(r'<div class="(?:note|disc|disclaimer)"[^>]*>.*?</div>', re.DOTALL | re.IGNORECASE)

# 共享事实域（这些业务线的报告必须使用事实卡片指针）
SHARED_FACT_DOMAINS = ("security", "industry-research", "competitive-intelligence")

# 决策摘要节标题特征
_SUMMARY_HEAD_RE = re.compile(r"(决策摘要|执行摘要|结论先行|核心结论|本周要点|摘要)")


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


def _plain(html: str) -> str:
    return _TAG_RE.sub("", html)


def _strip_noise(html: str) -> str:
    """剥离注释与 style/script 块（判定前置，防注释误判）。"""
    return _STYLE_RE.sub("", _COMMENT_RE.sub("", html))


def _section_raw(text: str) -> str:
    """决策摘要节原始片段（标题后至下一个 h2 前），保留 class 标记供等级判定。"""
    matches = list(_H2_RE.finditer(text))
    for i, m in enumerate(matches):
        if _SUMMARY_HEAD_RE.search(_plain(m.group(1))):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[start:end]
    return ""


def _section_text(text: str) -> str:
    """决策摘要节正文（去掉口径/局限提示块后的纯文本）。"""
    return _plain(_NOTE_RE.sub("", _section_raw(text)))


def _has_summary(text: str) -> bool:
    return any(_SUMMARY_HEAD_RE.search(_plain(m.group(1))) for m in _H2_RE.finditer(text))


def _boilerplate_copied(text: str) -> bool:
    return all(t in text for t in _BOILERPLATE_TIERS)


def check_text(text: str, business_line: str = "") -> list[tuple[str, str]]:
    """返回 [(rule_id, 说明)]，仅列不合规项（不含级别）。"""
    out: list[tuple[str, str]] = []
    text = _strip_noise(text)
    plain = _plain(text)

    # ID-01 分层结构
    if not _has_summary(text):
        out.append(("ID-01", "缺决策摘要节（决策摘要 / 执行摘要 / 结论先行 / 核心结论等）"))
    if _boilerplate_copied(text):
        out.append(("ID-01", "正文整段复制共享层来源分级规则（①–④ 四层清单），应改为指针引用"))

    # ID-02 决策摘要长度（≤1 屏：≤900 字或 ≤12 要点，取更严）
    sec_raw = _section_raw(text)
    sec = _plain(_NOTE_RE.sub("", sec_raw))
    if sec:
        n_chars = len(re.sub(r"\s+", "", sec))
        n_points = (len(re.findall(r"<li\b", sec_raw, re.IGNORECASE))
                    or len(re.findall(r"(?m)^\s*(?:\d+[.、]|[-\u2022])", sec)))
        if n_chars > 900 or n_points > 12:
            out.append(("ID-02", f"决策摘要约 {n_chars} 字 / {n_points} 要点，超 1 屏阈值"
                                    f"（≤900 字或 ≤12 要点，取更严）"))

    # ID-03 信息等级标注
    if not (_LVL_CLASS_RE.search(text) or _LVL_TEXT_RE.search(plain)):
        out.append(("ID-03", "未发现信息等级四级标注（已核验 / 部分核验 / 推断 / 假设）"))

    # ID-04 摘要引用约束（仅许已核验 + 部分核验）
    if sec:
        if "假设乘积" in sec and "区间" not in sec:
            out.append(("ID-04", "决策摘要出现「假设乘积」但未区间化（禁止作为确定点值）"))
        # 自算 / 机制自算值须显式标「假设乘积」并区间化（P1-3：不再允许无标注自算点值）
        if "自算" in sec and "假设乘积" not in sec:
            out.append(("ID-04", "决策摘要出现自算值（「自算 / 机制自算」）但未标「假设乘积 + 区间」"
                                "（禁止作为确定点值）"))
        # 结论性要点不得带「推断 / 假设」等级标记（口径/局限提示块除外）。
        # 仅当标记文本确为等级词时才判——信号灯（如「灰灯」）复用 lvl 类不算越级。
        bad = sorted({lbl for cls, lbl in (("inferred", "推断"), ("assumption", "假设"))
                      if re.search(rf'<span class="lvl lvl-{cls}">\s*{lbl}\s*</span>',
                                   _NOTE_RE.sub("", sec_raw))})
        if bad:
            out.append(("ID-04", f"决策摘要结论性要点含「{'、'.join(bad)}」等级标记"
                                f"（摘要仅许已核验 / 部分核验，应下沉证据层并以指针引用）"))

    # ID-05 新增信息模块
    has_delta = ("本期新增" in plain) and ("修正" in plain) and ("无变化" in plain) \
        and ("假设核验" in plain or re.search(r"\d+\s*/\s*\d+", plain))
    if not has_delta:
        out.append(("ID-05", "缺「本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n」统计模块"))

    # ID-06 指针引用
    if not (_FC_REF_RE.search(plain) or _METRIC_ID_RE.search(plain)):
        out.append(("ID-06", "未发现指标编号 / 事实卡片指针引用"))

    # ID-07 事实卡片（共享域）
    if any(d in business_line for d in SHARED_FACT_DOMAINS):
        if not _FC_REF_RE.search(plain):
            out.append(("ID-07", "共享事实域报告未使用 [FC-…] 事实卡片指针"))

    # ID-08 场景切片
    if not any(k in plain for k in ("场景切片", "投资决策", "就业决策", "政策制定")):
        out.append(("ID-08", "未发现场景切片（投资决策 / 就业决策 / 政策制定）声明或切片"))

    # DC-05 版本治理
    if ("核验" in plain and "收敛" in plain) and "读数时点" not in plain:
        out.append(("DC-05", "核验 / 收敛型报告未标注「读数时点」"))
    return out


def iter_targets(only_file: str | None):
    """-> [(relpath, text, period, business_line)]。"""
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


def _period_of(name: str) -> str:
    det = detect_report(name)
    return det[1] if det else ""


# 规则级别：新报告 [E] / 历史 [W]；仅 [W] 的规则
_WARN_ONLY = {"ID-02", "ID-06"}


def run(only_file: str | None, gate: str) -> tuple[int, int, list[str]]:
    gate = resolve_period(gate)
    errors = warnings = 0
    lines = []
    targets = iter_targets(only_file)
    if not targets:
        lines.append("信息密度门禁：未发现报告，跳过")
        return 0, 0, lines
    for rel, text, period, bline in targets:
        findings = check_text(text, bline)
        if not findings:
            continue
        is_new = bool(period) and _period_key(period) >= _period_key(gate)
        for rule, msg in findings:
            if rule in _WARN_ONLY:
                level = "W"
            else:
                level = "E" if is_new else "W"
            if level == "E":
                errors += 1
            else:
                warnings += 1
            tag = "新报告" if is_new else "历史报告"
            lines.append(f"[{level}] {rel}（{tag}，周期 {period or '未识别'}）{rule}：{msg}")
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="信息密度与分层交付门禁")
    ap.add_argument("--file", help="只检查单份报告（仓库相对路径）")
    ap.add_argument("--gate-period", default=DEFAULT_GATE, help="新报告判定周期下限")
    args = ap.parse_args()
    errors, warnings, lines = run(args.file, args.gate_period)
    for line in lines:
        print(line)
    if errors:
        print(f"信息密度门禁失败：{errors} 项错误（新报告缺项），{warnings} 项警告")
        return 1
    if warnings:
        print(f"信息密度门禁：{warnings} 项警告（历史报告 / 非阻断项，不阻断）")
        return 2
    print("信息密度门禁通过：全部新报告分层 / 等级 / 统计模块齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
