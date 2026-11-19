#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A-03 真值核对与计分。

用法：
    python engine/tools/a03_truth_check.py                # 结构化登记册版（一致/差异/不可比 + A-03 组合值）
    python engine/tools/a03_truth_check.py --candidates    # 旧版候选差异清单
    python engine/tools/a03_truth_check.py --json

背景：A-03「数值一致率」计分 = 0.5 × 真值核对一致率 + 0.5 × 代理一致率。
真值核对读 `engine/tools/indicator-truth-registry.json`（R01–R09，字段：指标编号 /
最新值 / 周期 / 来源 URL / 核验状态），与 apartment 报告显式数值对比对；多口径 /
区间 / 不等式归不可比。代理一致率见 `metric_coverage.a03_numeric_consistency`。
可比项为 0 时回退代理并显式标注；代理与真值均为机械口径，不得当作语义达标。
旧版 `a03_truth_candidates` 保留于 `--candidates`。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metric_coverage as mc  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="A-03 真值核对与计分")
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
        print("\n⚠️ 候选清单为旧版辅助口径，不计入 A-03 指标值。")
        return 0

    value, detail = mc.a03_combined()
    truth = mc.a03_truth_check()
    if args.json:
        print(json.dumps({"a03_value": value, "a03_detail": detail, "truth": truth},
                         ensure_ascii=False, indent=2))
        return 0
    if truth.get("error"):
        print(f"[A-03 真值核对] 登记册不可读：{truth.get('sidecar')}")
        return 1
    print(f"[A-03 数值一致率·组合] {value:.4f}（{detail}）")
    print(f"[A-03 真值核对] {truth['sidecar']}")
    print(f"可比对 {truth['compared']} 项：一致 {truth['same']} / 差异 {truth['diff']}"
          f"；不可比 {truth['uncomparable']} 项")
    for r in truth["records"]:
        if r["verdict"] == "一致":
            continue
        print(f"  - [{r['verdict']}] {r['report']} | {r['indicator']}："
              f"报告 {r['report_value']} vs 登记册 {r['sidecar_value']}"
              f"（周期 {r['period']}，来源 {r['source']}，核验 {r['verification_status']}）"
              f"— {r['reason']}")
    print("\n⚠️ 组合值为机械口径（真值核对 + 代理），不得当作语义达标。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
