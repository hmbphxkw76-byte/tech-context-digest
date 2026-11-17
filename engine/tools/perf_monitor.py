#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""性能监控与结果缓存（T6）。

依据 engine/report-audits/system-optimization-plan-2026-11-15.md 第四章：
  - 读取 / 更新 perf-status.json（结构化性能记录）；
  - 阈值校验（CI 增幅、门禁 P95、单报告耗时、错误率）；
  - 内容哈希缓存（报告未变则跳过重复语义，保障效率）。

退出码：0 达标；1 用法错误；2 存在超阈值项。

用法：
    python engine/tools/perf_monitor.py check                    # 校验最新 perf-status.json
    python engine/tools/perf_monitor.py update <scenario> --wall-avg 123.4 [--error-rate 0]
    python engine/tools/perf_monitor.py cache-get <path>         # 命中打印 cached，否则 miss
    python engine/tools/perf_monitor.py cache-set <path> --key <k> --value <v>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402

PERF_STATUS = ROOT / "perf-status.json"
CACHE_DIR = ROOT / ".perf-cache"


# ---------------------------------------------------------------- 状态文件

def load_status(path: Path = PERF_STATUS) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_status(payload: dict, path: Path = PERF_STATUS) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_scenario(scenario: str, metrics: dict, path: Path = PERF_STATUS) -> None:
    """按 id 合并 / 追加一个场景指标。"""
    payload = load_status(path)
    scenarios = payload.setdefault("scenarios", [])
    for s in scenarios:
        if s.get("id") == scenario:
            s.update(metrics)
            break
    else:
        metrics = {"id": scenario, **metrics}
        scenarios.append(metrics)
    payload["run"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    save_status(payload, path)


# ---------------------------------------------------------------- 阈值校验

def check_thresholds(payload: dict | None = None) -> list[dict]:
    payload = payload or load_status()
    th = payload.get("thresholds", {})
    scenarios = {s["id"]: s for s in payload.get("scenarios", [])}
    out: list[dict] = []

    def add(level: str, msg: str) -> None:
        out.append({"level": level, "message": msg})

    l0 = scenarios.get("l0_l1_full")
    if l0 and l0.get("wall_ms", {}).get("p95", 0) > th.get("l0_l1_full_p95_ms", 60000):
        add("P0", f"L0/L1 全量门禁 P95 {l0['wall_ms']['p95']}ms 超阈值 {th.get('l0_l1_full_p95_ms')}ms")
    single = scenarios.get("single_report_l1")
    if single and single.get("wall_ms", {}).get("avg", 0) > th.get("single_report_l1_avg_ms", 2000):
        add("P1", f"单报告 L1 平均 {single['wall_ms']['avg']}ms 超阈值 {th.get('single_report_l1_avg_ms')}ms")
    # P-03：strict 审计四环节（audit.yml 关键路径）性能护栏，默认 ≤180000ms。
    strict = scenarios.get("audit_run_strict")
    if strict and strict.get("wall_ms", {}).get("p95", 0) > th.get("audit_strict_p95_ms", 180000):
        add("P0", f"strict 审计 P95 {strict['wall_ms']['p95']}ms 超阈值 {th.get('audit_strict_p95_ms')}ms")
    for s in payload.get("scenarios", []):
        if s.get("error_rate", 0) > th.get("error_rate_max", 0):
            add("P0", f"场景 {s['id']} 错误率 {s['error_rate']:.1%} 超阈值")
    return out


# ---------------------------------------------------------------- 内容哈希缓存

def content_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


class ResultCache:
    """简单的文件系统缓存：key -> {hash, value, ts}。"""

    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.dir = Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def _file(self, key: str) -> Path:
        return self.dir / (hashlib.sha256(key.encode("utf-8")).hexdigest()[:16] + ".json")

    def get(self, key: str, path: Path) -> str | None:
        f = self._file(key)
        if not f.exists():
            return None
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        if rec.get("hash") != content_hash(path):
            return None
        return rec.get("value")

    def set(self, key: str, path: Path, value: str) -> None:
        self._file(key).write_text(json.dumps(
            {"hash": content_hash(path), "value": value,
             "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())},
            ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="性能监控与结果缓存（T6）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    p = sub.add_parser("update"); p.add_argument("scenario")
    p.add_argument("--wall-avg", type=float); p.add_argument("--p95", type=float)
    p.add_argument("--error-rate", type=float); p.add_argument("--throughput", type=float)
    p = sub.add_parser("cache-get"); p.add_argument("path")
    p = sub.add_parser("cache-set"); p.add_argument("path"); p.add_argument("--key", required=True)
    p.add_argument("--value", required=True)
    args = ap.parse_args()

    if args.cmd == "check":
        findings = check_thresholds()
        for f in findings:
            print(f"[{f['level']}] {f['message']}")
        if not findings:
            print("性能阈值校验通过：全部达标")
            return 0
        return 2
    if args.cmd == "update":
        metrics = {}
        if args.wall_avg is not None:
            metrics.setdefault("wall_ms", {})["avg"] = args.wall_avg
        if args.p95 is not None:
            metrics.setdefault("wall_ms", {})["p95"] = args.p95
        if args.error_rate is not None:
            metrics["error_rate"] = args.error_rate
        if args.throughput is not None:
            metrics["throughput_per_sec"] = args.throughput
        update_scenario(args.scenario, metrics)
        print(f"[update] {args.scenario} 已更新 perf-status.json")
        return 0
    if args.cmd == "cache-get":
        v = ResultCache().get("report:" + str(Path(args.path).resolve()), Path(args.path))
        print("cached" if v is not None else "miss")
        return 0 if v is not None else 2
    if args.cmd == "cache-set":
        ResultCache().set("report:" + str(Path(args.path).resolve()), Path(args.path), args.value)
        print("[cache-set] 已写入缓存")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
