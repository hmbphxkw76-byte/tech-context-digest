#!/usr/bin/env python3
"""A-03 真值核对辅助工具（候选差异清单，**不计分**）。

用法：
    python engine/tools/a03_truth_check.py            # 打印候选差异
    python engine/tools/a03_truth_check.py --json     # JSON 输出

背景：A-03「数值一致率」自动抽取无法区分「指标值 / 阈值 / 统计周期」，
直接判分将产生伪差异。本工具只产出候选差异供人工核验，不改变 A-03 指标值。
自动判分待登记册结构化「最新值 + 周期 + 来源」字段后再实施。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_coverage as mc  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="A-03 真值核对（候选差异清单，不计分）")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args()

    res = mc.a03_truth_candidates()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    if res.get("error"):
        print(f"[A-03 真值核对] 登记册不可读：{res.get('registry')}")
        return 1
    print(f"[A-03 真值核对] 登记册：{res['registry']}")
    print(f"可比对 {res['compared']} 项：一致 {res['same']} / 差异 {res['diff']}"
          f"；不可比 {res['uncomparable']} 项")
    if not res["diffs"]:
        print("无候选差异。")
        return 0
    print("\n候选差异（需人工判读，可能为阈值 / 周期差异）：")
    for d in res["diffs"]:
        print(f"  - {d['report']} | {d['indicator']}：报告 {d['report_value']}"
              f" vs 登记册 {d['registry_value']}（登记册周期 {d['registry_period']}）")
    print("\n⚠️ 本清单不计入 A-03 指标值。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
