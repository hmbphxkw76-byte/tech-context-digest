#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""性能基线压测（T6 / T0 基线）。

依据 engine/report-audits/system-optimization-plan-2026-11-15.md 第四章：
按既定场景、并发参数与采样时长执行，输出核心指标（吞吐量 / 响应时间 / 错误率 /
资源占用），结构化写入 perf-status.json，作为后续对比基准。

场景与并发口径：
  - 门禁类：concurrency=1（与 CI 串行一致），warmup 1 轮 + samples 5 轮；
  - 单报告类：samples 10 轮（样本小、波动大）；
  - 审计类：samples 3 轮（较慢）；
  - 并行吞吐：concurrency=4，度量多报告并发校验的吞吐与加速比。

退出码：0 正常；1 压测执行异常；2 存在场景错误率 > 0（仅提示，不阻断基线落盘）。

用法：
    python engine/tools/perf_bench.py                 # 全场景，写 perf-status.json
    python engine/tools/perf_bench.py --out <path>    # 指定输出
    python engine/tools/perf_bench.py --samples 3     # 缩减采样轮次
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_business_dirs  # noqa: E402

SCHEMA_VERSION = "1.0"
DEFAULT_OUT = ROOT / "perf-status.json"

# 代表性单报告（用于单报告场景）
SAMPLE_REPORT = "content/economy/dubai/apartment/reports/2026-11_monthly.html"


def _py() -> str:
    return sys.executable or "python"


def _cmd(*parts: str) -> list[str]:
    return [_py(), *parts]


# 场景定义 ---------------------------------------------------------------

def _l0_l1_seq() -> list[str]:
    """L0/L1 全量门禁（串行，与 ci.yml 同口径）。"""
    return [
        _cmd("engine/tools/validate.py"),
        _cmd("engine/tools/validate_layout.py"),
        _cmd("engine/tools/lint_reports.py"),
        _cmd("engine/tools/compliance_check.py", "--check"),
        _cmd("engine/tools/classify_reports.py", "--check"),
        _cmd("engine/tools/check_links.py"),
        _cmd("engine/tools/page_build_check.py", "--quiet"),
        _cmd("engine/tools/research_kernel_check.py"),
        _cmd("engine/tools/source_check.py", "--quiet"),
    ]


def _single_report_seq() -> list[str]:
    return [
        _cmd("engine/tools/compliance_check.py", "--file", SAMPLE_REPORT),
        _cmd("engine/tools/source_check.py", "--file", SAMPLE_REPORT, "--quiet"),
    ]


SCENARIOS = [
    {"id": "l0_l1_full", "desc": "L0/L1 全量门禁（串行）", "kind": "seq",
     "steps": _l0_l1_seq(), "concurrency": 1, "warmup": 1, "samples": 5,
     "unit": "全量仓库", "n_units": 1},
    {"id": "single_report_l1", "desc": "单报告 L1（合规 + 来源校验）", "kind": "seq",
     "steps": _single_report_seq(), "concurrency": 1, "warmup": 1, "samples": 10,
     "unit": "单份报告", "n_units": 1},
    {"id": "source_check_full", "desc": "来源登记校验（全量）", "kind": "cmd",
     "cmd": _cmd("engine/tools/source_check.py", "--quiet"), "concurrency": 1,
     "warmup": 1, "samples": 5, "unit": "全量仓库", "n_units": 1},
    {"id": "build_hub_check", "desc": "汇总页一致性校验", "kind": "cmd",
     "cmd": _cmd("engine/tools/build_hub.py", "--check"), "concurrency": 1,
     "warmup": 1, "samples": 5, "unit": "全量仓库", "n_units": 1},
    {"id": "audit_run_default", "desc": "审计四环节（默认模式，dry-run）", "kind": "cmd",
     "cmd": _cmd("engine/audit/scripts/audit_tool.py", "run", "--dry-run"),
     "concurrency": 1, "warmup": 0, "samples": 3, "unit": "全量正式报告", "n_units": 11,
     "acceptable_rc": [0, 1, 2]},
    {"id": "audit_run_strict", "desc": "审计四环节（strict 模式，dry-run）", "kind": "cmd",
     "cmd": _cmd("engine/audit/scripts/audit_tool.py", "run", "--strict", "--dry-run"),
     "concurrency": 1, "warmup": 0, "samples": 3, "unit": "全量正式报告", "n_units": 11,
     "acceptable_rc": [0, 1, 2]},
]


# 测量工具 ---------------------------------------------------------------

def _run_cmd(cmd: list[str]) -> tuple[float, float, int]:
    """运行命令 -> (wall_ms, cpu_ms, returncode)。"""
    t0 = time.perf_counter()
    c0 = time.process_time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    wall = (time.perf_counter() - t0) * 1000.0
    cpu = (time.process_time() - c0) * 1000.0
    return wall, cpu, rc


def _run_seq(steps: list[list[str]]) -> tuple[float, float, int]:
    """顺序执行多条命令，取总耗时；任一非 0/2 视为错误（2=警告可接受）。"""
    t0 = time.perf_counter()
    c0 = time.process_time()
    rc = 0
    for cmd in steps:
        _w, _c, r = _run_cmd(cmd)
        if r not in (0, 2):
            rc = r
            break
    wall = (time.perf_counter() - t0) * 1000.0
    cpu = (time.process_time() - c0) * 1000.0
    return wall, cpu, rc


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (pct / 100.0)
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def _measure(scn: dict, samples: int) -> dict:
    """执行一个场景 -> 指标字典。"""
    walls: list[float] = []
    cpus: list[float] = []
    errors = 0
    runs = 0
    acceptable = tuple(scn.get("acceptable_rc", (0, 2)))

    def one() -> tuple[float, float, int]:
        if scn["kind"] == "seq":
            return _run_seq(scn["steps"])
        return _run_cmd(scn["cmd"])

    # 预热
    for _ in range(scn.get("warmup", 0)):
        one()
    # 采样
    n = max(1, samples)
    for _ in range(n):
        w, c, rc = one()
        runs += 1
        walls.append(w)
        cpus.append(c)
        if rc not in acceptable:
            errors += 1

    avg = statistics.fmean(walls) if walls else 0.0
    n_units = scn.get("n_units", 1)
    return {
        "id": scn["id"],
        "desc": scn["desc"],
        "kind": scn["kind"],
        "concurrency": scn.get("concurrency", 1),
        "acceptable_rc": list(acceptable),
        "runs": runs,
        "errors": errors,
        "error_rate": round(errors / runs, 4) if runs else 0.0,
        "wall_ms": {
            "avg": round(avg, 2),
            "p50": round(_percentile(walls, 50), 2),
            "p95": round(_percentile(walls, 95), 2),
            "max": round(max(walls), 2) if walls else 0.0,
            "min": round(min(walls), 2) if walls else 0.0,
        },
        "cpu_ms": {"avg": round(statistics.fmean(cpus), 2) if cpus else 0.0},
        "throughput_per_sec": round((n_units * runs) / (sum(walls) / 1000.0), 3) if walls and sum(walls) > 0 else 0.0,
        "unit": scn.get("unit", " run"),
    }


def _parallel_scenario(workers: int = 4, samples: int = 3) -> dict:
    """多报告并行来源校验：度量并发吞吐与相对串行的加速比。"""
    rels: list[str] = []
    for b in iter_business_dirs():
        reports = b.path / "reports"
        if not reports.is_dir():
            continue
        for f in sorted(reports.glob("*.html")):
            rels.append(f"{b.rel}/reports/{f.name}")

    def one_report(rel: str) -> int:
        return _run_cmd(_cmd("engine/tools/source_check.py", "--file", rel, "--quiet"))[2]

    # 串行基线
    t0 = time.perf_counter()
    for rel in rels:
        one_report(rel)
    serial = (time.perf_counter() - t0) * 1000.0

    walls: list[float] = []
    errors = 0
    runs = 0
    for _ in range(max(1, samples)):
        t0 = time.perf_counter()
        with cf.ThreadPoolExecutor(max_workers=workers) as ex:
            rcs = list(ex.map(one_report, rels))
        walls.append((time.perf_counter() - t0) * 1000.0)
        runs += 1
        errors += sum(1 for r in rcs if r not in (0, 2))

    avg = statistics.fmean(walls) if walls else 0.0
    n = len(rels)
    return {
        "id": "parallel_source_check",
        "desc": f"多报告并行来源校验（concurrency={workers}）",
        "kind": "parallel",
        "concurrency": workers,
        "runs": runs,
        "errors": errors,
        "error_rate": round(errors / (runs * n), 4) if runs and n else 0.0,
        "wall_ms": {"avg": round(avg, 2), "p50": round(_percentile(walls, 50), 2),
                    "p95": round(_percentile(walls, 95), 2),
                    "max": round(max(walls), 2) if walls else 0.0,
                    "min": round(min(walls), 2) if walls else 0.0},
        "cpu_ms": {"avg": 0.0},
        "throughput_per_sec": round((n * runs) / (sum(walls) / 1000.0), 3) if walls and sum(walls) > 0 else 0.0,
        "unit": f"{n} 份报告",
        "serial_wall_ms": round(serial, 2),
        "speedup": round(serial / avg, 2) if avg > 0 else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="性能基线压测（T0）")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--samples", type=int, default=5, help="门禁类采样轮次")
    ap.add_argument("--skip-parallel", action="store_true")
    args = ap.parse_args()

    results: list[dict] = []
    for scn in SCENARIOS:
        n = 3 if scn["id"].startswith("audit_run") else (10 if scn["id"] == "single_report_l1" else args.samples)
        results.append(_measure(scn, n))
        m = results[-1]
        print(f"[{m['id']}] avg={m['wall_ms']['avg']}ms p95={m['wall_ms']['p95']}ms "
              f"err={m['error_rate']:.1%} thr={m['throughput_per_sec']}/s")

    if not args.skip_parallel:
        p = _parallel_scenario()
        results.append(p)
        print(f"[{p['id']}] avg={p['wall_ms']['avg']}ms speedup={p['speedup']}x err={p['error_rate']:.1%}")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "run": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "baseline": True,
        "environment": {
            "concurrency_default": 1,
            "warmup": 1,
            "samples": args.samples,
        },
        "metrics": ["throughput_per_sec", "wall_ms.avg/p50/p95/max", "error_rate", "cpu_ms.avg"],
        "scenarios": results,
        "thresholds": {
            "ci_total_increase_pct": 10.0,
            "l0_l1_full_p95_ms": 60000.0,
            "single_report_l1_avg_ms": 2000.0,
            "error_rate_max": 0.0,
        },
    }

    out = Path(args.out)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n[perf] 基线已写入 {out.relative_to(ROOT)}（场景 {len(results)} 个）")
    any_err = any(r["error_rate"] > 0 for r in results)
    return 2 if any_err else 0


if __name__ == "__main__":
    sys.exit(main())
