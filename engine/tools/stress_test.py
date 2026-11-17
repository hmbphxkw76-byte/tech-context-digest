"""N7 · 压力测试模块（实施方案第一节 N7，P2）。

尾部情景库（油价突破 / 霍尔木兹关闭 / 资本外流 / LTV 收紧 / 兑现率塌陷），
用传导弹性把冲击传导至成交量 / 价格 / 收益率 / 估值，输出尾部损失区间（非点值）。

弹性缺省值为经验估计（见 ELASTICITIES），实施时应由 transmission.py 的本地估计替换。

用法：
    python engine/tools/stress_test.py --list
    python engine/tools/stress_test.py --run --json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# 经验弹性（Δ目标%/Δ驱动%），未经本地回测，仅供情景推演
ELASTICITIES = {
    "rate_to_volume": {"eta": -0.80, "ci": (-1.30, -0.30), "target": "VOLUME_YOY"},
    "supply_to_rent": {"eta": -0.40, "ci": (-0.70, -0.10), "target": "RENT_YOY"},
    "demand_to_price": {"eta": 0.60, "ci": (0.20, 1.00), "target": "PRICE_YOY"},
    "sentiment_to_volume": {"eta": 0.70, "ci": (0.30, 1.10), "target": "VOLUME_YOY"},
}

# 情景 → 驱动冲击（驱动名: 变动，单位见 drive_unit）
SCENARIOS = [
    {"id": "S1", "name": "油价突破", "trigger": "Brent > 100 美元持续 1 季",
     "shocks": {"rate_to_volume": -0.5, "demand_to_price": -2.0}},
    {"id": "S2", "name": "霍尔木兹关闭", "trigger": "海峡通行中断 > 30 日",
     "shocks": {"rate_to_volume": -1.0, "demand_to_price": -6.0, "sentiment_to_volume": -15.0}},
    {"id": "S3", "name": "资本外流", "trigger": "FDI 同比转负且连续 2 季",
     "shocks": {"demand_to_price": -4.0, "sentiment_to_volume": -10.0}},
    {"id": "S4", "name": "LTV 大幅收紧", "trigger": "LTV -10pp 生效",
     "shocks": {"rate_to_volume": -0.8, "demand_to_price": -3.0}},
    {"id": "S5", "name": "兑现率塌陷", "trigger": "交付兑现率 <35% 且次年计划 ≥150,000 套",
     "shocks": {"supply_to_rent": -3.0, "demand_to_price": -2.0}},
]


@dataclass
class ScenarioResult:
    id: str
    name: str
    trigger: str
    impacts: dict = field(default_factory=dict)
    loss_range: dict = field(default_factory=dict)
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def run_scenario(scenario: dict, elasticities: dict | None = None) -> ScenarioResult:
    """把单一情景的驱动冲击传导至目标，输出区间。"""
    elas = elasticities or ELASTICITIES
    impacts, loss = {}, {}
    for drive, shock in scenario.get("shocks", {}).items():
        spec = elas.get(drive)
        if not spec:
            continue
        target = spec["target"]
        eta = spec["eta"]
        lo, hi = spec.get("ci", (eta, eta))
        impacts[target] = round(eta * shock, 2)
        # 冲击可正可负：乘完再排序，保证 loss_range 为 [低, 高]
        loss[target] = sorted([round(min(lo, hi) * shock, 2), round(max(lo, hi) * shock, 2)])
    return ScenarioResult(
        id=scenario["id"], name=scenario["name"], trigger=scenario["trigger"],
        impacts=impacts, loss_range=loss,
        note="弹性为经验估计，未经本地回测；区间来自弹性 CI",
    )


def run_all(elasticities: dict | None = None) -> list[ScenarioResult]:
    return [run_scenario(s, elasticities) for s in SCENARIOS]


def main() -> int:
    ap = argparse.ArgumentParser(description="压力测试（N7）")
    ap.add_argument("--list", action="store_true", help="列出情景库")
    ap.add_argument("--run", action="store_true", help="运行全部情景")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.list:
        for s in SCENARIOS:
            print(f"{s['id']} {s['name']}｜触发：{s['trigger']}｜冲击：{s['shocks']}")
        return 0
    if args.run:
        results = run_all()
        if args.json:
            print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"{r.id} {r.name}: 目标影响={r.impacts} 损失区间={r.loss_range}")
        return 0
    print("[ERROR] 需要 --list 或 --run")
    return 1


if __name__ == "__main__":
    sys.exit(main())
