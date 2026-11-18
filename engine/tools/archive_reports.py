"""报告与源稿归档策略（CI: scheduled-maintenance 的 archive_reports 步骤）。

对每条业务线的 reports/ 与 sources/ 按报告类型执行滚动归档：每类只保留最新 N 期，
超出的移动到对应目录的 archives/（创建于业务目录内，与「报告与归档都在
各项目内部」的约定一致）。保留期数与展示窗口同源（CYCLE_WINDOWS）：
月 18 / 季 8 / 年 5 / 基线 3 / 周报 12。基线报告为对比锚，同样只保留最新 3 份。
sources/legacy/ 为存档，不参与轮转。

幂等：重复执行不再移动任何文件。退出码：0 = 成功；1 = 移动失败。
"""
from __future__ import annotations

import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import CYCLE_WINDOWS, detect_report, iter_business_dirs  # noqa: E402

# 每类保留的最新期数（超出部分归档；周报频率高，滚动保留近 12 期）。
# 与展示窗口同源（CYCLE_WINDOWS，REPORT-CYCLE-WINDOWS-SPEC v1.0）：
# monthly 18 个月 = 18 期；quarterly 24 个月 = 8 期；annual 60 个月 = 5 期。
KEEP = {
    "monthly": CYCLE_WINDOWS["monthly"]["retention"],
    "quarterly": CYCLE_WINDOWS["quarterly"]["retention"] // 3,
    "annual": CYCLE_WINDOWS["annual"]["retention"] // 12,
    "baseline": 3,
    "weekly": 12,
}

# 审计文档轮转（Phase 3.2）：`engine/report-audits/` 根只保留最近 12 个月，
# 更早的移入 `archives/`；无日期后缀的账本型文档不轮转。
AUDIT_DOCS = Path(__file__).resolve().parents[2] / "engine" / "report-audits"
AUDIT_ARCHIVE = AUDIT_DOCS / "archives"
AUDIT_KEEP_MONTHS = 12
AUDIT_DATE_RE = re.compile(r"-(\d{4})-(\d{2})-(\d{2})\.md$")


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


def select_audit_docs(root: Path | None = None, keep_months: int = AUDIT_KEEP_MONTHS,
                      today: date | None = None) -> list[Path]:
    """纯函数：返回应轮转到 `archives/` 的审计文档（早于最近 keep_months 个月）。

    仅识别 `<slug>-YYYY-MM-DD.md` 命名；无日期后缀的账本型文档（如覆盖矩阵）不轮转。
    `today` 显式传入以保证确定性（测试可重放）。
    """
    root = AUDIT_DOCS if root is None else root
    today = today or date.today()
    out: list[Path] = []
    if not root.is_dir():
        return out
    for f in sorted(root.glob("*.md")):
        m = AUDIT_DATE_RE.search(f.name)
        if not m:
            continue
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            continue
        months = (today.year - d.year) * 12 + (today.month - d.month)
        if months >= keep_months:
            out.append(f)
    return out


def rotate_audit_docs(root: Path | None = None, keep_months: int = AUDIT_KEEP_MONTHS,
                      today: date | None = None) -> int:
    """轮转审计文档：超出保留期的移入 `archives/`。幂等。退出码 0/1。"""
    root = AUDIT_DOCS if root is None else root
    files = select_audit_docs(root, keep_months, today)
    if not files:
        print(f"审计文档轮转：无超出保留期（最近 {keep_months} 个月）的文档，未移动")
        return 0
    archive = root / "archives"
    archive.mkdir(parents=True, exist_ok=True)
    for f in files:
        try:
            shutil.move(str(f), str(archive / f.name))
            print(f"[ARCHIVED] engine/report-audits/{f.name} -> archives/")
        except OSError as e:
            print(f"[ERROR] 轮转失败 {f.name}: {e}")
            return 1
    print(f"审计文档轮转：移动 {len(files)} 份文档")
    return 0


def archive_cycle_dir(root: Path, label: str) -> int:
    """归档单个周期目录（reports/ 或 sources/），返回移动数量。"""
    if not root.is_dir():
        return 0
    items = []
    for f in sorted(root.iterdir()):
        if not f.is_file():
            continue
        det = detect_report(f.name)
        if det:
            items.append((det[0], det[1], f))
    to_archive = select_archives(items)
    if not to_archive:
        return 0
    archives = root / "archives"
    archives.mkdir(exist_ok=True)
    moved = 0
    for f in to_archive:
        try:
            shutil.move(str(f), str(archives / f.name))
            print(f"[ARCHIVED] {label}/{f.name} -> archives/")
            moved += 1
        except OSError as e:
            print(f"[ERROR] 归档失败 {f.name}: {e}")
            return 1
    return moved


def main() -> int:
    if "--audit-docs" in sys.argv[1:]:
        return rotate_audit_docs()
    moved = 0
    for b in iter_business_dirs():
        for sub in ("reports", "sources"):
            moved += archive_cycle_dir(b.path / sub, f"{b.rel}/{sub}")
    if moved:
        print(f"归档完成：移动 {moved} 份历史报告 / 源稿")
    else:
        print("归档策略检查：无超出保留期数的报告 / 源稿，未移动任何文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
