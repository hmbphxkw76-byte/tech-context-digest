#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-03 真值核对辅助工具（**不计分**）。

用法：
    python engine/tools/a03_truth_check.py                # sidecar 版（一致/差异/不可比）
    python engine/tools/a03_truth_check.py --candidates    # 旧版候选差异清单
    python engine/tools/a03_truth_check.py --json

背景：A-03「数值一致率」自动抽取无法区分「指标值 / 阈值 / 统计周期」，
直接判分将产生伪差异。sidecar 版读 `indicator_latest.json`（结构化最新值 /
周期 / 来源），把多口径 / 区间 / 不等式分类为不可比，仍只产出明细供人工核验，
不改变 A-03 指标值。旧版 `a03_truth_candidates` 保留于 `--candidates`。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_coverage as mc  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="A-03 真值核对（辅助，不计分）")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    ap.add_argument("--candidates", action="store_true",
                    help="使用旧版候选差异清单（读 xlsx 登记册）")
    args = ap.parse_args()

    if args.candidates:
        res = mc.a03_truth_candidates()
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return 0
        if res.get("error"):
            print(f"[A-03 真值核对] 登记册不可读：{res.get('registry')}")
            return 1
        print(f"[A-03 真值核对·候选] 登记册：{res['registry']}")
        print(f"可比对 {res['compared']} 项：一致 {res['same']} / 差异 {res['diff']}"
              f"；不可比 {res['uncomparable']} 项")
        for d in res["diffs"]:
            print(f"  - {d['report']} | {d['indicator']}：报告 {d['report_value']}"
                  f" vs 登记册 {d['registry_value']}（登记册周期 {d['registry_period']}）")
        print("\n⚠️ 本清单不计入 A-03 指标值。")
        return 0

    res = mc.a03_truth_check()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    if res.get("error"):
        print(f"[A-03 真值核对] sidecar 不可读：{res.get('sidecar')}")
        return 1
    print(f"[A-03 真值核对·sidecar] {res['sidecar']}")
    print(f"可比对 {res['compared']} 项：一致 {res['same']} / 差异 {res['diff']}"
          f"；不可比 {res['uncomparable']} 项")
    for r in res["records"]:
        if r["verdict"] == "一致":
            continue
        print(f"  - [{r['verdict']}] {r['report']} | {r['indicator']}："
              f"报告 {r['report_value']} vs 登记册 {r['sidecar_value']}"
              f"（周期 {r['period']}，来源 {r['source']}）— {r['reason']}")
    print("\n⚠️ 本清单不计入 A-03 指标值。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
