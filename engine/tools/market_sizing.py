"""N6 · 规模测算模块（实施方案第一节 N6，P1）。

TAM / SAM / SOM 双口径（自上而下 + 自下而上），含敏感性与一致性校验。
硬规则：SOM ≤ SAM ≤ TAM；双口径差异 >30% 必须给出解释（由调用方在 note 说明）。

用法：
    python engine/tools/market_sizing.py --demo
    python engine/tools/market_sizing.py --tam 58.3e9 --sam-penetration 0.45 --som-penetration 0.20
    python engine/tools/market_sizing.py --bottom-up --units 858000 --arpu 68000
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import mean  # noqa: E402


@dataclass
class SizingResult:
    tam: float
    sam: float
    som: float
    method: str
    assumptions: dict
    consistency: str

    def to_dict(self) -> dict:
        return asdict(self)


def top_down(tam: float, sam_penetration: float, som_penetration: float,
             assumptions: dict | None = None) -> SizingResult:
    if not (0 < sam_penetration <= 1 and 0 < som_penetration <= 1):
        raise ValueError("渗透率须在 (0,1]")
    sam = tam * sam_penetration
    som = sam * som_penetration
    _check(sam, som, tam)
    return SizingResult(round(tam, 2), round(sam, 2), round(som, 2), "自上而下",
                        assumptions or {}, "OK")


def bottom_up(units: float, arpu: float, sam_share: float = 1.0, som_share: float = 1.0,
              assumptions: dict | None = None) -> SizingResult:
    """自下而上：units × ARPU = TAM；SAM/SOM 按份额折算。"""
    if units <= 0 or arpu <= 0:
        raise ValueError("units/arpu 必须为正")
    tam = units * arpu
    sam = tam * sam_share
    som = sam * som_share
    _check(sam, som, tam)
    return SizingResult(round(tam, 2), round(sam, 2), round(som, 2), "自下而上",
                        assumptions or {}, "OK")


def compare(top: SizingResult, bottom: SizingResult) -> dict:
    """双口径对照：差异率 = |TAM_td - TAM_bu| / mean。"""
    denom = mean([top.tam, bottom.tam])
    gap = abs(top.tam - bottom.tam) / denom if denom else 0.0
    return {
        "top_down_tam": top.tam,
        "bottom_up_tam": bottom.tam,
        "gap_pct": round(gap * 100, 1),
        "within_30pct": gap <= 0.30,
        "note": "" if gap <= 0.30 else "双口径差异 >30%，须补充解释",
    }


def sensitivity(tam: float, sam_p: float, som_p: float,
                sam_range=(-0.1, 0.0, 0.1), som_range=(-0.05, 0.0, 0.05)) -> list:
    """渗透率敏感性网格（SOM 输出）。"""
    out = []
    for ds in sam_range:
        for dso in som_range:
            sam = tam * min(max(sam_p + ds, 0.01), 1.0)
            som = sam * min(max(som_p + dso, 0.01), 1.0)
            out.append({"sam_penetration": round(sam_p + ds, 3),
                        "som_penetration": round(som_p + dso, 3),
                        "som": round(som, 2)})
    return out


def _check(sam: float, som: float, tam: float) -> None:
    if not (som <= sam <= tam):
        raise ValueError(f"规模约束违背：SOM={som} SAM={sam} TAM={tam}")


def demo() -> dict:
    """迪拜公寓租赁市场算例（假设已标注，数值取自 apartment 年度已核验口径）。"""
    assumptions = {
        "家庭户数": "858,000（2025，DDSE，未核验，仅英文媒体转述）",
        "户均年租金": "68,000 AED（2026-10 新签中位，Peak Trust/DXBinteract）",
        "公寓租赁渗透率": "0.45（假设，待核验）",
        "可服务份额": "0.20（假设，待核验）",
    }
    top = top_down(858000 * 68000, 0.45, 0.20, assumptions)
    bottom = bottom_up(858000, 68000, 1.0, 1.0, assumptions)
    return {"top_down": top.to_dict(), "bottom_up": bottom.to_dict(),
            "compare": compare(top, bottom),
            "sensitivity": sensitivity(858000 * 68000, 0.45, 0.20)}


def main() -> int:
    ap = argparse.ArgumentParser(description="规模测算（N6）")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--tam", type=float)
    ap.add_argument("--sam-penetration", type=float)
    ap.add_argument("--som-penetration", type=float)
    ap.add_argument("--bottom-up", action="store_true")
    ap.add_argument("--units", type=float)
    ap.add_argument("--arpu", type=float)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        if args.demo:
            out = demo()
        elif args.bottom_up:
            if args.units is None or args.arpu is None:
                print("[ERROR] --bottom-up 需要 --units 与 --arpu")
                return 1
            out = bottom_up(args.units, args.arpu).to_dict()
        elif args.tam is not None and args.sam_penetration and args.som_penetration:
            out = top_down(args.tam, args.sam_penetration, args.som_penetration).to_dict()
        else:
            print("[ERROR] 需要 --demo / --bottom-up / --tam+渗透率")
            return 1
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
