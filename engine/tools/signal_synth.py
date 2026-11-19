"""N2 · 信号合成器（实施方案第一节 N2，P0）。

把 K01–K15 重组为领先 / 同步 / 滞后三层，输出「周期阶段 + 信号一致性」双维度，
替代单一红绿灯。与 cycle_clock 阶段交叉校验，冲突即告警。

层权重：领先 0.50 / 同步 0.35 / 滞后 0.15（和为 1）。
层内权重：一等 0.5 / 二等 0.3 / 三等 0.2（归一化）。

状态严重度：绿 0 / 黄 1 / 预警红 2 / 硬红·方向 3 / 硬红·完全 4；灰 = 数据缺口（不计权）。

用法：
    python engine/tools/signal_synth.py --input <k-status.csv> [--phase 过渡带] [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import read_csv_records  # noqa: E402

LAYER_WEIGHT = {"领先": 0.50, "同步": 0.35, "滞后": 0.15}
TIER_WEIGHT = {"一等": 0.5, "二等": 0.3, "三等": 0.2}
SEVERITY = {"绿": 0, "黄": 1, "预警红": 2, "硬红·方向": 3, "硬红·完全": 4, "灰": None}

# K 编号 → (层, 等级)
K_META = {
    "K01": ("领先", "一等"),   # 3M EIBOR
    "K02": ("领先", "一等"),   # Fed 票型 / 点阵图
    "K03": ("领先", "二等"),   # 许可建筑面积同比
    "K04": ("同步", "一等"),   # 交付兑现率
    "K05": ("领先", "三等"),   # 新推盘量同比
    "K06": ("领先", "一等"),   # 降租续约占比
    "K07": ("同步", "二等"),   # 公寓中位价同比
    "K08": ("同步", "一等"),   # 成交量同比
    "K09": ("同步", "三等"),   # 现房成交金额占比
    "K10": ("滞后", "二等"),   # 登记口径毛收益率
    "K11": ("领先", "二等"),   # FDI 流入同比
    "K12": ("领先", "二等"),   # 人口 / 家庭增速
    "K13": ("领先", "三等"),   # 就业 / 失业
    "K14": ("同步", "三等"),   # 酒店入住率 / 游客
    "K15": ("滞后", "二等"),   # 官方 GDP/CPI 分歧
}


@dataclass
class SynthResult:
    phase: str | None
    layer_counts: dict = field(default_factory=dict)
    layer_scores: dict = field(default_factory=dict)
    overall_score: float = 0.0
    consistency: str = "未知"
    alerts: list = field(default_factory=list)
    phase_conflict: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


def _norm_layer_weights(layer: str, ids: list[str]) -> dict:
    raw = {k: TIER_WEIGHT[K_META[k][1]] for k in ids if k in K_META}
    total = sum(raw.values())
    return {k: v / total for k, v in raw.items()} if total else {}


def synthesize(statuses: dict, phase: str | None = None) -> SynthResult:
    """合成信号（纯函数）。statuses: {K 编号: 状态字符串}。"""
    layer_counts: dict = {layer: {} for layer in LAYER_WEIGHT}
    layer_scores = {}
    alerts = []

    for layer in LAYER_WEIGHT:
        ids = [k for k in K_META if K_META[k][0] == layer]
        counts = {"绿": 0, "黄": 0, "预警红": 0, "硬红·方向": 0, "硬红·完全": 0, "灰": 0, "未报": 0}
        num = den = 0.0
        w = _norm_layer_weights(layer, ids)
        for k in ids:
            st = statuses.get(k, "未报")
            if st not in counts:
                st = "未报"
            counts[st] += 1
            sev = SEVERITY.get(st)
            if sev is not None:
                num += w.get(k, 0.0) * sev
                den += w.get(k, 0.0)
        layer_counts[layer] = counts
        layer_scores[layer] = round(num / den, 3) if den else None
        if counts["未报"]:
            alerts.append(f"{layer}层有 {counts['未报']} 项未报数（K 系状态缺失）")

    lead = layer_scores.get("领先")
    coin = layer_scores.get("同步")
    if lead is not None and coin is not None:
        if (lead >= 2) == (coin >= 2):
            consistency = "高"
        elif abs(lead - coin) >= 1.5:
            consistency = "低"
            alerts.append(f"领先层（{lead}）与同步层（{coin}）方向冲突")
        else:
            consistency = "中"
    else:
        consistency = "未知"

    overall = sum(LAYER_WEIGHT[k] * (layer_scores[k] or 0.0) for k in LAYER_WEIGHT)

    phase_conflict = False
    if phase:
        hot = lead is not None and lead >= 2
        if phase in ("复苏",) and hot:
            phase_conflict = True
            alerts.append(f"信号偏热（领先层 {lead}）与阶段「{phase}」不一致")
        if phase in ("衰退", "滞胀") and lead is not None and lead < 1:
            phase_conflict = True
            alerts.append(f"信号不弱（领先层 {lead}）与阶段「{phase}」不一致")

    return SynthResult(
        phase=phase,
        layer_counts=layer_counts,
        layer_scores=layer_scores,
        overall_score=round(overall, 3),
        consistency=consistency,
        alerts=alerts,
        phase_conflict=phase_conflict,
    )


def synthesize_from_csv(path: Path, phase: str | None = None) -> SynthResult:
    statuses = {}
    for r in read_csv_records(path):
        kid = str(r.get("k_id", "")).strip()
        st = str(r.get("status", "")).strip()
        if kid:
            statuses[kid] = st
    return synthesize(statuses, phase)


def main() -> int:
    ap = argparse.ArgumentParser(description="信号合成器（N2）")
    ap.add_argument("--input", help="K 状态 CSV（列：k_id,status）")
    ap.add_argument("--phase", help="周期阶段（来自 cycle_clock，用于交叉校验）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not args.input:
        print("[ERROR] 需要 --input <csv>")
        return 1
    p = Path(args.input)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / args.input
    if not p.exists():
        print(f"[ERROR] 输入不存在: {p}")
        return 1
    result = synthesize_from_csv(p, args.phase)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"合成结果：overall={result.overall_score} 一致性={result.consistency} "
              f"阶段冲突={result.phase_conflict}")
        for layer, sc in result.layer_scores.items():
            print(f"  {layer}: score={sc} counts={result.layer_counts[layer]}")
        for a in result.alerts:
            print(f"  [ALERT] {a}")
    return 1 if result.phase_conflict else 0


if __name__ == "__main__":
    sys.exit(main())
