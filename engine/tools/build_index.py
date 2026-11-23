"""全局报告索引（CI: scheduled-maintenance 的 build_index 步骤）。

汇总全部业务线 reports/ 下的报告，生成仓库根 INDEX.md
（content-update 工作流提交该文件，其「最近生成」时间戳用作活跃度心跳）。

退出码：0 = 成功；1 = 写入失败。
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, SITE_BRAND, iter_business_dirs, iter_business_reports, report_title  # noqa: E402

CYCLE_LABEL = {"monthly": "月度", "quarterly": "季度", "annual": "年度", "baseline": "基线", "weekly": "周报"}


def collect_entries():
    """-> [(business_rel, cycle, period, relpath, title, mtime_iso)]，period 降序。

    发现口径与 hub / audit 统一（iter_business_reports：reports/*.html 为正式，
    不含 archives / legacy）。
    """
    entries = []
    for b in iter_business_dirs():
        for ref in iter_business_reports(b):
            f = ROOT / ref.rel
            text = f.read_text(encoding="utf-8", errors="replace")
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            entries.append((b.rel, ref.cycle, ref.period, ref.rel, report_title(text), mtime))
    entries.sort(key=lambda e: (e[0], e[2]), reverse=True)
    return entries


def render_index(entries, now_iso: str) -> str:
    lines = [
        f"# {SITE_BRAND} 报告索引",
        "",
        f"> 最近生成：{now_iso}（由 engine/tools/build_index.py 自动维护）",
    ]
    if not entries:
        lines += ["", "暂无已产出报告。"]
        return "\n".join(lines) + "\n"
    current = None
    for rel, cycle, period, path, title, mtime in entries:
        if rel != current:
            current = rel
            lines += ["", f"## {rel}", "", "| 类型 | 周期 | 报告 | 标题 | 更新时间 (UTC) |", "|---|---|---|---|---|"]
        label = CYCLE_LABEL.get(cycle, cycle)
        name = Path(path).name
        lines.append(f"| {label} | {period} | [{name}]({path}) | {title or '—'} | {mtime:%Y-%m-%d %H:%M} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    entries = collect_entries()
    now_iso = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = render_index(entries, now_iso)
    try:
        (ROOT / "INDEX.md").write_text(text, encoding="utf-8")
    except OSError as e:
        print(f"[ERROR] 写入 INDEX.md 失败: {e}")
        return 1
    print(f"索引已生成：INDEX.md（{sum(1 for _ in entries)} 份报告，{len({e[0] for e in entries})} 条业务线）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
