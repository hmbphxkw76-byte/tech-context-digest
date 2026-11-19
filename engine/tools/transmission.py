"""N4 · 传导弹性模块（实施方案第一节 N4，P1；OLS + VAR 双方法）。

四链（利率 / 供给 / 需求 / 情绪）弹性估计：
    η = (ΔY/Y) / (ΔX/X) ≈ beta * mean(X) / mean(Y)

OLS：对每个滞后阶 l 拟合 y_t = a + b·x_{t-l}，按 AIC 选阶；输出 η + 时滞 + 95% CI。
VAR：多元序列按 BIC 选阶，脉冲响应累计给出 η；OLS 与 VAR 并列，冲突时标注。

纯标准库实现（见 _quant.py）；小样本 CI 较宽，输出须如实标注。

用法：
    python engine/tools/transmission.py --input <csv> --chain all --json
    列名见 CHAINS 定义（如 EIBOR_3M,VOLUME_YOY）。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import (  # noqa: E402
    mean,
    ols,
    read_csv_records,
    to_float,
    var_fit,
    var_irf,
    var_select_order,
)

# 链 → (自变量, 因变量, VAR 冲击变量序号名)
CHAINS = {
    "rate": {"x": "EIBOR_3M", "y": "VOLUME_YOY", "label": "利率→成交量"},
    "supply": {"x": "COMPLETIONS_YOY", "y": "RENT_YOY", "label": "供给→租金"},
    "demand": {"x": "FDI_YOY", "y": "PRICE_YOY", "label": "需求→价格"},
    "sentiment": {"x": "SEARCH_INDEX", "y": "VOLUME_YOY", "label": "情绪→成交量"},
}


@dataclass
class Elasticity:
    chain: str
    method: str
    x: str
    y: str
    eta: float | None
    lag: int
    ci_low: float | None = None
    ci_high: float | None = None
    p_value: float | None = None
    r2: float | None = None
    n: int = 0
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _series(records: list[dict], name: str) -> list[float]:
    return [to_float(r.get(name)) for r in records]


def estimate_ols(y: list[float], x: list[float], max_lag: int = 4,
                 chain: str = "") -> Elasticity:
    """OLS 弹性估计（对 0..max_lag 滞后按 AIC 选阶）。"""
    n = len(y)
    if n != len(x) or n < 6:
        return Elasticity(chain, "OLS", "x", "y", None, -1, n=n,
                          note="样本不足（<6）")
    best = None
    for lag in range(0, min(max_lag, n - 4) + 1):
        xs = x[: n - lag] if lag else x
        ys = y[lag:]
        m = len(ys)
        if m < 5:
            continue
        X = [[1.0, float(v)] for v in xs]
        try:
            fit = ols(X, ys)
        except ValueError:
            continue
        ssr = sum(e * e for e in fit["resid"])
        aic = m * math.log(ssr / m) + 2 * fit["k"] if ssr > 0 else float("-inf")
        if best is None or aic < best["aic"]:
            best = {"aic": aic, "lag": lag, "fit": fit, "m": m}
    if best is None:
        return Elasticity(chain, "OLS", "x", "y", None, -1, n=n, note="无法拟合")
    fit = best["fit"]
    beta, se = fit["beta"][1], fit["se"][1]
    mx, my = mean(x), mean(y)
    scale = mx / my if my else 0.0
    eta = beta * scale
    lo, hi = sorted(((beta - 1.96 * se) * scale, (beta + 1.96 * se) * scale))
    note = "" if fit["p"][1] < 0.1 else "p≥0.1（不显著）"
    if my <= 0:
        note = (note + "；" if note else "") + "因变量均值≤0，均值处弹性不可靠，建议改用对数规格"
    return Elasticity(
        chain, "OLS", "x", "y", round(eta, 4), best["lag"],
        round(lo, 4), round(hi, 4), round(fit["p"][1], 4),
        round(fit["r2"], 4), best["m"], note,
    )


def estimate_var(series: dict[str, list[float]], max_p: int = 4,
                 chain: str = "") -> Elasticity:
    """VAR 弹性：对 x 冲击，累计 h 期响应换算弹性。"""
    names = list(series.keys())
    if len(names) < 2:
        return Elasticity(chain, "VAR", "", "", None, -1, note="变量不足")
    T = min(len(v) for v in series.values())
    if T < 8:
        return Elasticity(chain, "VAR", "", "", None, -1, n=T, note="样本不足（<8）")
    Y = [[to_float(series[nm][t]) for nm in names] for t in range(T)]
    try:
        p = var_select_order(Y, max_p)
        fit = var_fit(Y, p)
    except ValueError as e:
        return Elasticity(chain, "VAR", "", "", None, -1, n=T, note=str(e))
    irf = var_irf(fit["coef"], fit["m"], p, steps=6)
    # 对第一个变量的单位冲击，累计第 2 期响应
    cum = sum(row[0] for row in irf[:3])
    my = mean([row[0] for row in Y])
    eta = cum / my if my else None
    return Elasticity(chain, "VAR", names[0], names[1] if len(names) > 1 else "",
                     round(eta, 4) if eta is not None else None, p,
                     n=T, note="VAR 脉冲响应累计（未正交化）")


def estimate_chain(chain: str, records: list[dict]) -> list[Elasticity]:
    spec = CHAINS.get(chain)
    if not spec:
        raise ValueError(f"未知链条: {chain}")
    y = _series(records, spec["y"])
    x = _series(records, spec["x"])
    out = [estimate_ols(y, x, chain=chain)]
    var_series = {spec["x"]: x, spec["y"]: y}
    out.append(estimate_var(var_series, chain=chain))
    for e in out:
        e.x, e.y = spec["x"], spec["y"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="传导弹性估计（N4）")
    ap.add_argument("--input", required=True, help="时间序列 CSV（含链所需列）")
    ap.add_argument("--chain", default="all", help="rate|supply|demand|sentiment|all")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    p = Path(args.input)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / args.input
    if not p.exists():
        print(f"[ERROR] 输入不存在: {p}")
        return 1
    records = read_csv_records(p)
    chains = list(CHAINS) if args.chain == "all" else [args.chain]
    results: list[Elasticity] = []
    for c in chains:
        try:
            results.extend(estimate_chain(c, records))
        except ValueError as e:
            print(f"[ERROR] {c}: {e}")
            return 1
    if args.json:
        print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"{r.chain}/{r.method}: eta={r.eta} lag={r.lag} "
                  f"CI=[{r.ci_low},{r.ci_high}] n={r.n} {r.note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
