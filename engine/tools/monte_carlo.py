"""N8 · 蒙特卡洛模拟模块（实施方案第一节 N8，P2）。

用概率分布替代「悲观/基准/乐观」三档：对驱动变量抽样，经传导弹性映射到目标，
输出 P10/P50/P90 与 VaR(95%)/ES(95%)。固定随机种子，结果可复现。

用法：
    python engine/tools/monte_carlo.py --demo
    python engine/tools/monte_carlo.py --drivers "EIBOR_3M:0.5:0.1" --el "EIBOR_3M:-0.8" --n 10000
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import mean, percentile, std  # noqa: E402


@dataclass
class MCResult:
    n: int
    seed: int
    percentiles: dict
    var_95: float
    es_95: float
    mean: float
    std: float
    target: str

    def to_dict(self) -> dict:
        return asdict(self)


def simulate(drivers: dict, elasticities: list, n: int = 10000, seed: int = 42,
             target: str = "VOLUME_YOY") -> MCResult:
    """drivers: {名: (均值, 标准差)}；elasticities: [(驱动名, eta), ...]。

    目标 = Σ eta_i · driver_i（线性传导，单位：目标百分比）。
    """
    if n <= 0:
        raise ValueError("模拟次数必须为正")
    rng = random.Random(seed)
    samples = []
    for _ in range(n):
        total = 0.0
        for name, eta in elasticities:
            if name not in drivers:
                raise ValueError(f"缺少驱动分布: {name}")
            mu, sd = drivers[name]
            total += eta * rng.gauss(mu, sd)
        samples.append(total)
    samples.sort()
    p10 = percentile(samples, 10)
    p50 = percentile(samples, 50)
    p90 = percentile(samples, 90)
    var = percentile(samples, 5)
    tail = [x for x in samples if x <= var]
    es = mean(tail) if tail else var
    return MCResult(
        n=n, seed=seed,
        percentiles={"P10": round(p10, 3), "P50": round(p50, 3), "P90": round(p90, 3)},
        var_95=round(var, 3), es_95=round(es, 3),
        mean=round(mean(samples), 3), std=round(std(samples), 3),
        target=target,
    )


def demo() -> dict:
    drivers = {"rate_shock": (0.0, 0.4), "demand_shock": (0.0, 2.0)}
    elasticities = [("rate_shock", -0.8), ("demand_shock", 0.6)]
    return simulate(drivers, elasticities, n=10000, seed=42).to_dict()


def _parse_driver(s: str):
    # 名:均值:标准差
    parts = s.split(":")
    if len(parts) != 3:
        raise ValueError(f"驱动格式应为 名:均值:标准差: {s}")
    return parts[0], (float(parts[1]), float(parts[2]))


def _parse_el(s: str):
    name, eta = s.split(":")
    return name, float(eta)


def main() -> int:
    ap = argparse.ArgumentParser(description="蒙特卡洛（N8）")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--drivers", action="append", help="名:均值:标准差（可多次）")
    ap.add_argument("--el", action="append", help="驱动名:弹性（可多次）")
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--target", default="VOLUME_YOY")
    args = ap.parse_args()
    try:
        if args.demo:
            out = demo()
        else:
            if not args.drivers or not args.el:
                print("[ERROR] 需要 --drivers 与 --el（或 --demo）")
                return 1
            drivers = {k: v for k, v in (_parse_driver(s) for s in args.drivers)}
            els = [_parse_el(s) for s in args.el]
            out = simulate(drivers, els, n=args.n, seed=args.seed, target=args.target).to_dict()
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
