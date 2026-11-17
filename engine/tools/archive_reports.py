"""报告归档策略（CI: scheduled-maintenance 的 archive_reports 步骤）。

对每条业务线的 reports/ 按报告类型执行滚动归档：每类只保留最新 N 期，
超出的移动到 reports/archives/（创建于业务目录内，与「报告与归档都在
各项目内部」的约定一致）。基线报告为对比锚，同样只保留最新 3 份。

幂等：重复执行不再移动任何文件。退出码：0 = 成功；1 = 移动失败。
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import detect_report, iter_business_dirs  # noqa: E402

# 每类保留的最新期数（超出部分归档；周报频率高，滚动保留近 12 期）
KEEP = {"monthly": 12, "quarterly": 8, "annual": 5, "baseline": 3, "weekly": 12}


def select_archives(items, keep_map=None):
    """纯函数：给定 [(cycle, period, path)]，返回应归档的 path 列表。

    排序规则：period 降序（同期按路径名），每类保留前 keep 份。
    """
    keep_map = keep_map or KEEP
    by_cycle: dict[str, list] = {}
    for cycle, period, path in items:
        by_cycle.setdefault(cycle, []).append((period, path))
    to_archive: list[Path] = []
    for cycle, entries in by_cycle.items():
        entries.sort(key=lambda e: (e[0], e[1].name), reverse=True)
        keep = keep_map.get(cycle, 12)
        for _, path in entries[keep:]:
            to_archive.append(path)
    return to_archive


def main() -> int:
    moved = 0
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        items = []
        for f in sorted(reports.iterdir()):
            if not f.is_file():
                continue
            det = detect_report(f.name)
            if det:
                items.append((det[0], det[1], f))
        to_archive = select_archives(items)
        if not to_archive:
            continue
        archives = reports / "archives"
        archives.mkdir(exist_ok=True)
        for f in to_archive:
            try:
                shutil.move(str(f), str(archives / f.name))
                print(f"[ARCHIVED] {b.rel}/reports/{f.name} -> archives/")
                moved += 1
            except OSError as e:
                print(f"[ERROR] 归档失败 {f.name}: {e}")
                return 1
    if moved:
        print(f"归档完成：移动 {moved} 份历史报告")
    else:
        print("归档策略检查：无超出保留期数的报告，未移动任何文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
