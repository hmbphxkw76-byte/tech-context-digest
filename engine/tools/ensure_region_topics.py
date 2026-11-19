"""结构补全（幂等）（CI: scheduled-maintenance / ci.yml 的 ensure_region_topics 步骤）。

扫描全部业务线目录（content/<theme>/<维度段...>/，维度顺序见 layout.json），补齐标准子目录
prompts/、reports/，并校验集中数据目录 data/processed/<theme>/<维度段...>/ 存在
（--check 模式只报告不创建）。

退出码：0 = 结构齐全（或已补齐）；2 = 存在缺失项（警告，不阻断）。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs, processed_data_dir  # noqa: E402

REQUIRED_SUBDIRS = ("prompts", "reports")


def main() -> int:
    ap = argparse.ArgumentParser(description="业务线结构补全（幂等）")
    ap.add_argument("--check", action="store_true", help="只检查不创建")
    args = ap.parse_args()

    businesses = iter_business_dirs()
    if not businesses:
        print("未识别到业务线目录，跳过结构补全")
        return 0

    missing_all: list[str] = []
    for b in businesses:
        missing = [s for s in REQUIRED_SUBDIRS if not (b.path / s).is_dir()]
        config_missing = not (b.path / "prompts" / "business-config.md").exists()
        for sub in missing:
            if args.check:
                print(f"[WARN] {b.rel}: 缺少 {sub}/ 目录")
            else:
                (b.path / sub).mkdir(parents=True, exist_ok=True)
                print(f"[FIXED] {b.rel}: 已创建 {sub}/ 目录")
            missing_all.append(f"{b.rel}/{sub}")
        if config_missing:
            print(f"[WARN] {b.rel}: 缺少 prompts/business-config.md（业务单一事实源）")
            missing_all.append(f"{b.rel}/prompts/business-config.md")
        data_dir = processed_data_dir(b.rel)
        if not data_dir.is_dir():
            print(f"[WARN] {b.rel}: 缺少集中数据目录 {data_dir.relative_to(ROOT).as_posix()}/")
            missing_all.append(f"{b.rel}:data")

    if missing_all and args.check:
        print(f"结构补全检查：{len(missing_all)} 项缺失（不阻断，定时维护将自动补齐）")
        return 2
    if missing_all:
        print(f"结构补全完成：补齐 {len(missing_all)} 项")
    else:
        print("结构补全检查通过：全部业务线结构齐全")
    return 0


if __name__ == "__main__":
    if ROOT.is_dir():
        sys.exit(main())
    sys.exit(1)
