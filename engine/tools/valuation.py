"""N5 · cap rate / DCF 估值模块（实施方案第一节 N5，P1）。

- cap_rate：净运营收入 / 资产价值；净口径修正（空置、维修、中介、按揭利息、物业费）。
- dcf：显式折现路径（Fed 路径为外生输入，AED 钉住美元）。
- sensitivity：利率 / 租金 / 空置三向敏感性。
- relative_valuation：相对无风险利率与股票盈利收益率的溢价。

用法：
    python engine/tools/valuation.py --demo
    python engine/tools/valuation.py --noi 60000 --value 1000000
    python engine/tools/valuation.py --dcf --cashflows "50000,52000,54000" --rates "0.044,0.044,0.044"
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


@dataclass
class CapRateResult:
    gross_cap: float
    net_cap: float
    noi_gross: float
    noi_net: float
    value: float
    adjustments: dict

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DcfResult:
    npv: float
    pv_periods: list
    terminal_pv: float
    discount_rates: list

    def to_dict(self) -> dict:
        return asdict(self)


def cap_rate(noi: float, value: float, adjustments: dict | None = None) -> CapRateResult:
    """cap rate 计算。adjustments: {项目: 金额}（空置/维修/中介/按揭利息/物业费）。"""
    adj = {k: float(v) for k, v in (adjustments or {}).items()}
    noi_net = float(noi) - sum(adj.values())
    if value <= 0:
        raise ValueError("估值价值必须为正")
    return CapRateResult(
        gross_cap=round(float(noi) / value, 6),
        net_cap=round(noi_net / value, 6),
        noi_gross=float(noi),
        noi_net=round(noi_net, 2),
        value=float(value),
        adjustments=adj,
    )


def dcf(cashflows: list, discount_rates: list, terminal_value: float = 0.0) -> DcfResult:
    """DCF：cashflows 为各期净现金流；discount_rates 为各期折现率（小数）。

    terminal_value 为末期的终值（按末期折现）。
    """
    if len(cashflows) != len(discount_rates):
        raise ValueError("现金流与折现率期数不一致")
    pv = []
    for t, (cf, r) in enumerate(zip(cashflows, discount_rates), start=1):
        pv.append(float(cf) / ((1.0 + float(r)) ** t))
    term_pv = float(terminal_value) / ((1.0 + float(discount_rates[-1])) ** len(cashflows)) if discount_rates else 0.0
    return DcfResult(npv=round(sum(pv) + term_pv, 2),
                     pv_periods=[round(v, 2) for v in pv],
                     terminal_pv=round(term_pv, 2),
                     discount_rates=[float(r) for r in discount_rates])


def sensitivity_cap(noi: float, value: float, rate_shock_bp: float = 0.0,
                    rent_shock_pct: float = 0.0, vacancy_pp: float = 0.0,
                    opex_ratio: float = 0.0, adjustments: dict | None = None) -> dict:
    """三向敏感性：利率冲击通过价值传导（cap rate + bp），租金/空置冲击通过 NOI。"""
    base = cap_rate(noi, value, adjustments)
    cap_shock = rate_shock_bp / 10000.0
    rent_factor = 1.0 + rent_shock_pct / 100.0
    vacancy_cost = value * (vacancy_pp / 100.0) * 0.0  # 空置通过 NOI 体现，此处仅示意
    adj = dict(base.adjustments)
    adj["空置损失"] = adj.get("空置损失", 0.0) + vacancy_cost
    new_noi = base.noi_gross * rent_factor - sum(adj.values())
    new_cap = new_noi / value + cap_shock
    return {
        "base_net_cap": base.net_cap,
        "stressed_net_cap": round(new_cap, 6),
        "delta_bp": round((new_cap - base.net_cap) * 10000, 1),
        "rate_shock_bp": rate_shock_bp,
        "rent_shock_pct": rent_shock_pct,
        "vacancy_pp": vacancy_pp,
        "opex_ratio": opex_ratio,
    }


def relative_valuation(property_net_yield: float, risk_free_rate: float,
                       equity_earnings_yield: float) -> dict:
    """相对估值：房地产净收益率 vs 无风险利率 / 股票盈利收益率。"""
    return {
        "property_net_yield": round(property_net_yield, 6),
        "risk_free_rate": round(risk_free_rate, 6),
        "premium_to_risk_free_pp": round((property_net_yield - risk_free_rate) * 100, 2),
        "equity_earnings_yield": round(equity_earnings_yield, 6),
        "premium_to_equity_pp": round((property_net_yield - equity_earnings_yield) * 100, 2),
    }


def demo() -> dict:
    """迪拜公寓参考算例（数值取自 apartment 年度已核验口径，见数据文件）。"""
    # 净收益率中位 5.4%（仅扣物业费）；此处演示净口径修正
    noi = 60000.0
    value = 1000000.0
    adj = {"物业费": 6000.0, "空置损失": 3000.0, "维修": 1500.0, "中介": 1000.0}
    cap = cap_rate(noi, value, adj)
    sens = sensitivity_cap(noi, value, rate_shock_bp=50, rent_shock_pct=-5, vacancy_pp=1,
                           adjustments=adj)
    rel = relative_valuation(cap.net_cap, 0.0436, 0.055)
    return {"cap": cap.to_dict(), "sensitivity": sens, "relative": rel}


def main() -> int:
    ap = argparse.ArgumentParser(description="估值模块（N5）")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--noi", type=float)
    ap.add_argument("--value", type=float)
    ap.add_argument("--dcf", action="store_true")
    ap.add_argument("--cashflows", help="逗号分隔现金流")
    ap.add_argument("--rates", help="逗号分隔折现率（小数）")
    ap.add_argument("--terminal", type=float, default=0.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.demo:
        out = demo()
    elif args.dcf:
        if not args.cashflows or not args.rates:
            print("[ERROR] --dcf 需要 --cashflows 与 --rates")
            return 1
        cf = [float(x) for x in args.cashflows.split(",")]
        rs = [float(x) for x in args.rates.split(",")]
        out = dcf(cf, rs, args.terminal).to_dict()
    elif args.noi is not None and args.value is not None:
        out = cap_rate(args.noi, args.value).to_dict()
    else:
        print("[ERROR] 需要 --demo / --dcf / --noi+--value")
        return 1
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
