#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""模型契约门禁（MODEL-CONTRACT-CHECK v1.0，DC-07 / P1-13）。

把量化模型（transmission / valuation / stress_test）的「参数区间 + 假设 + 失败上报」
从单测提升为统一门禁检查项，纳入 `optimization_gate`。

  MC-01 参数区间（[W]）：transmission 弹性结果须含置信区间字段（ci_low / ci_high）。
  MC-02 参数区间（[W]）：stress_test 经验弹性表每项须含 ci 区间。
  MC-03 区间输出（[W]）：stress_test 情景结果须含 loss_range（损失区间）。
  MC-04 假设留痕（[W]）：模型结果 to_dict 须含假设 / 口径字段（note / assumptions /
        loss_range / ci* 之一）；缺失即视为契约不完整。
  MC-05 失败上报（[W]）：非法输入须显式 raise（不得静默返回 None / 吞异常）。

退出码：0 = 通过；1 = 存在 [E]；2 = 仅 [W]。
用法：python engine/tools/model_contract_check.py [--quiet]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

INTERVAL_KEYS = ("ci_low", "ci_high", "loss_range", "ci")
ASSUMPTION_KEYS = ("note", "assumptions", "assumption", "caliber", "loss_range")


def _load(name: str, rel: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ROOT = Path(__file__).resolve().parents[2]


def mc01_transmission(transmission) -> list[str]:
    warns: list[str] = []
    keys = set(transmission.Elasticity("rate", "ols", "x", "y", 0.1, 1).to_dict())
    if not {"ci_low", "ci_high"} <= keys:
        warns.append("MC-01 transmission 弹性结果缺置信区间字段（ci_low / ci_high）")
    return warns


def mc02_stress_elasticities(stress) -> list[str]:
    warns: list[str] = []
    for name, e in stress.ELASTICITIES.items():
        if "ci" not in e or not isinstance(e["ci"], (list, tuple)) or len(e["ci"]) != 2:
            warns.append(f"MC-02 stress_test 弹性 {name} 缺 ci 区间")
    return warns


def mc03_stress_scenario(stress) -> list[str]:
    warns: list[str] = []
    keys = set(stress.ScenarioResult("S1", "n", "t").to_dict())
    if "loss_range" not in keys:
        warns.append("MC-03 stress_test 情景结果缺损失区间字段（loss_range）")
    return warns


def mc04_assumption_metadata(modules: dict) -> list[str]:
    warns: list[str] = []
    for name, mod in modules.items():
        for cls_name in ("Elasticity", "ScenarioResult", "CapRateResult", "DcfResult"):
            cls = getattr(mod, cls_name, None)
            if cls is None:
                continue
            try:
                inst = cls.__new__(cls)
                keys = set(inst.__dict__) | set(getattr(cls, "__dataclass_fields__", {}))
            except Exception:
                keys = set(getattr(cls, "__dataclass_fields__", {}))
            if not any(k in keys for k in ASSUMPTION_KEYS):
                warns.append(f"MC-04 {name}.{cls_name} 结果缺假设 / 口径字段（note / assumptions 等）")
    return warns


def mc05_failure_reporting(transmission, valuation) -> list[str]:
    warns: list[str] = []
    try:
        transmission.estimate_chain("no-such-chain", [])
        warns.append("MC-05 transmission 未知链条未显式 raise")
    except Exception:
        pass
    try:
        valuation.cap_rate(100.0, -1.0)
        warns.append("MC-05 valuation 非正价值未显式 raise")
    except Exception:
        pass
    try:
        valuation.dcf([1.0, 2.0], [0.1])
        warns.append("MC-05 valuation 期数不一致未显式 raise")
    except Exception:
        pass
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description="模型契约门禁")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    transmission = _load("transmission", "engine/tools/transmission.py")
    valuation = _load("valuation", "engine/tools/valuation.py")
    stress = _load("stress_test", "engine/tools/stress_test.py")
    warns = (mc01_transmission(transmission) + mc02_stress_elasticities(stress)
             + mc03_stress_scenario(stress)
             + mc04_assumption_metadata({"transmission": transmission, "stress_test": stress,
                                         "valuation": valuation})
             + mc05_failure_reporting(transmission, valuation))
    for w in warns:
        print(f"[W] {w}")
    if not args.quiet or warns:
        print(f"模型契约校验：{len(warns)} 警告")
    return 2 if warns else 0


if __name__ == "__main__":
    sys.exit(main())
