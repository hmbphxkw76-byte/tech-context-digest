"""报告自动归位（CI: scheduled-maintenance / content-update 的 classify 步骤）。

扫描散落在业务目录之外（仓库根、engine/templates/ 等）的报告文件，
按**双校验**判定归属业务线：

  信号一（地区/物业类型）：文件名包含目标业务线的 region 或 property_type 线索；
  信号二（类型节拍）：文件名周期与目标业务线 `{{REPORT_TYPE}}` 声明类型的
                        节拍白名单（`_common.TYPE_CADENCE`）一致。

两个信号都命中且候选唯一才自动归位；只命中其一或候选不唯一 -> UNKNOWN（人工确认），
避免「按地区词误搬」的分类逻辑错误。类型声明结构化（`{{REPORT_TYPE}}`）优先，
缺声明时回落继承声明引用（`_common.parse_report_type`）。

用法：
    python engine/tools/classify_reports.py --apply --unknown-warn
    python engine/tools/classify_reports.py --check --unknown-warn
    python engine/tools/classify_reports.py --explain

退出码：
    0 = 无错位报告
    1 = 存在可自动归位的错位（--check 模式），或 --apply 移动失败
    2 = 存在无法判定归属的报告（--unknown-warn 时不阻断）
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    TEMPLATE_DIR, business_report_type, detect_report, detect_report_loose, iter_business_dirs, load_layout, type_cadence, ROOT,
)


def strays() -> list[Path]:
    """收集业务目录之外的报告文件（仓库根一级 + engine/templates/）。"""
    out: list[Path] = []
    for f in sorted(ROOT.iterdir()):
        if f.is_file() and detect_report(f.name):
            out.append(f)
    tpl = TEMPLATE_DIR
    if tpl.is_dir():
        for f in sorted(tpl.rglob("*")):
            if f.is_file() and detect_report(f.name):
                out.append(f)
    return out


def owner_signals(name: str) -> dict:
    """双校验信号 -> dict。

    信号一（地区/细分）：先按 property_type 精匹配，无命中时回落 region 单命中；
    文件名出现的地区必须与候选业务线 region 一致（地区一致性）。
    信号二（类型节拍）：文件名周期与候选类型节拍白名单一致。
    """
    lower = name.lower()
    businesses = iter_business_dirs()
    # 地区线索取自「region 白名单 + 各业务线 region 段」（category-first 下 region
    # 位于 category 之后，由 Business.region 按维度序列取出），避免新结构下漏检。
    region_tokens = set(load_layout().regions) | {b.region for b in businesses if b.segments}
    regions_in_name = [r for r in sorted(region_tokens) if r.lower() in lower]

    def region_ok(b) -> bool:
        return (not regions_in_name) or (b.region in regions_in_name)

    prop_hits = [b for b in businesses if region_ok(b) and b.property_type.lower() in lower]
    reg_hits = [b for b in businesses if region_ok(b) and b.region.lower() in lower]
    if len(prop_hits) == 1:
        candidates, signal = prop_hits, "property"
    elif not prop_hits and len(reg_hits) == 1:
        candidates, signal = reg_hits, "region"
    else:
        candidates, signal = [], "none"

    det = detect_report(name) or detect_report_loose(name)
    cycle = det[0] if det else None
    owner = None
    cadence = None
    cycle_ok = None
    if len(candidates) == 1:
        b = candidates[0]
        type_id, _structured, _note = business_report_type(b)
        cadence = type_cadence(type_id)
        if cadence is None:
            cycle_ok = True  # 未注册类型不做节拍校验
            owner = b
        elif cycle is None:
            cycle_ok = False  # 项目制命名无法校验节拍 -> 需人工
        else:
            cycle_ok = cycle in cadence
            owner = b if cycle_ok else None
    return {
        "regions_in_name": regions_in_name,
        "region_hits": [b.rel for b in reg_hits],
        "property_hits": [b.rel for b in prop_hits],
        "signal": signal,
        "candidates": [b.rel for b in candidates],
        "region_hit": len(candidates) == 1,
        "cycle": cycle,
        "cadence": list(cadence) if cadence else None,
        "cycle_ok": cycle_ok,
        "owner": owner.rel if owner else None,
    }


def owner_of(name: str):
    """按双校验判定唯一归属业务线；不唯一 / 只命中单信号返回 None。"""
    return next((b for b in iter_business_dirs() if b.rel == owner_signals(name)["owner"]), None)


def main() -> int:
    ap = argparse.ArgumentParser(description="报告自动归位（双校验）")
    ap.add_argument("--apply", action="store_true", help="执行移动（缺省仅报告）")
    ap.add_argument("--check", action="store_true", help="只检查：存在可自动归位项时退出码 1")
    ap.add_argument("--unknown-warn", action="store_true", help="无法判定归属时仅告警（退出码 2）")
    ap.add_argument("--explain", action="store_true", help="输出逐份双校验信号明细")
    args = ap.parse_args()

    files = strays()
    movable: list[tuple[Path, Path]] = []
    unknown: list[Path] = []
    for f in files:
        target = owner_of(f.name)
        if target is None:
            unknown.append(f)
        else:
            movable.append((f, target.path / "reports" / f.name))
        if args.explain:
            sig = owner_signals(f.name)
            print(f"[SIGNALS] {f.relative_to(ROOT)}: {sig}")

    for f in unknown:
        print(f"[UNKNOWN] {f.relative_to(ROOT)}: 无法判定归属业务线（双校验未同时命中）")
    for src, dst in movable:
        print(f"[MISPLACED] {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")

    if args.apply:
        failed = 0
        for src, dst in movable:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f"[MOVED] {src.name} -> {dst.relative_to(ROOT)}")
            except OSError as e:
                print(f"[ERROR] 移动失败 {src.name}: {e}")
                failed += 1
        if failed:
            return 1
        if unknown and args.unknown_warn:
            return 2
        return 0

    if movable:
        hint = "运行 python engine/tools/classify_reports.py --apply 自动归位" if args.check else ""
        print(f"存在 {len(movable)} 份可自动归位的错位报告 {hint}")
        return 1
    if unknown and args.unknown_warn:
        print(f"存在 {len(unknown)} 份需人工确认归属的报告（不阻断）")
        return 2
    print("报告归位检查通过：无错位报告")
    return 0


if __name__ == "__main__":
    sys.exit(main())
