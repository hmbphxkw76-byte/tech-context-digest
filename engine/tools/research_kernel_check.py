"""研究内核质量门禁（实施方案第三节 M4）。

对报告检查四项研究内核必填（新报告缺项 = [E] 阻断；历史报告缺项 = [W] 不阻断）：
    ① 周期定位：含「周期定位」或「周期阶段」
    ② 传导量化：同时含「弹性」与「时滞」
    ③ 政策入模：含「政策乘数」，或同时含「政策」与「入模」
    ④ 盲区列示：含「未核验」或「盲区」

新报告判定：报告周期（文件名）>= 门禁周期（缺省 2026-12，即机制上线后新产出）。历史报告只警告。

退出码：0 通过；1 存在 [E]；2 仅 [W]。

用法：
    python engine/tools/research_kernel_check.py            # 全量
    python engine/tools/research_kernel_check.py --file <报告>
    python engine/tools/research_kernel_check.py --gate-period 2026-11
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, detect_report, iter_business_dirs  # noqa: E402

DEFAULT_GATE = "2026-12"

RULES = (
    ("周期定位", lambda t: ("周期定位" in t) or ("周期阶段" in t)),
    ("传导量化", lambda t: ("弹性" in t) and ("时滞" in t)),
    ("政策入模", lambda t: ("政策乘数" in t) or (("政策" in t) and ("入模" in t))),
    ("盲区列示", lambda t: ("未核验" in t) or ("盲区" in t)),
)


def _period_of(name: str) -> str:
    det = detect_report(name)
    return det[1] if det else ""


def _period_key(period: str) -> tuple:
    """周期字符串 → 可比较元组（季/年归一到月末，避免字典序误判）。"""
    import re

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


def check_text(text: str) -> list[str]:
    """返回缺失的内核项名称列表。"""
    return [name for name, ok in RULES if not ok(text)]


def iter_targets(only_file: str | None):
    """-> [(relpath, text, period)]。"""
    if only_file:
        p = ROOT / only_file
        return [(p.relative_to(ROOT).as_posix(), p.read_text(encoding="utf-8", errors="replace"),
                 _period_of(p.name))]
    out = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            out.append((f"{b.rel}/reports/{f.name}",
                        f.read_text(encoding="utf-8", errors="replace"), _period_of(f.name)))
    return out


def run(only_file: str | None, gate: str) -> tuple[int, int, list[str]]:
    errors = warnings = 0
    lines = []
    targets = iter_targets(only_file)
    if not targets:
        lines.append("研究内核门禁：未发现报告，跳过")
        return 0, 0, lines
    for rel, text, period in targets:
        missing = check_text(text)
        if not missing:
            continue
        is_new = bool(period) and _period_key(period) >= _period_key(gate)
        level = "E" if is_new else "W"
        if is_new:
            errors += 1
        else:
            warnings += 1
        tag = "新报告" if is_new else "历史报告"
        lines.append(f"[{level}] {rel}（{tag}，周期 {period or '未识别'}）缺失内核项："
                     f"{'、'.join(missing)}")
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="研究内核质量门禁（M4）")
    ap.add_argument("--file", help="只检查单份报告（仓库相对路径）")
    ap.add_argument("--gate-period", default=DEFAULT_GATE, help="新报告判定周期下限")
    args = ap.parse_args()
    errors, warnings, lines = run(args.file, args.gate_period)
    for line in lines:
        print(line)
    if errors:
        print(f"研究内核门禁失败：{errors} 项错误（新报告缺内核项），{warnings} 项警告")
        return 1
    if warnings:
        print(f"研究内核门禁：{warnings} 项历史报告警告（不阻断）")
        return 2
    print("研究内核门禁通过：全部新报告四项内核项齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
