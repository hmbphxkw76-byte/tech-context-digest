"""N1 · 宏观周期时钟（实施方案第一节 N1，P0）。

把「增长—通胀—政策—流动性」四维读数合成为周期阶段判定：
    复苏 / 过热 / 滞胀 / 衰退 / 过渡带（过热→滞胀）

规则（显式、可复现，无时间戳、无随机）：
- 增长 ↑ 且 通胀 ↑ 且 政策或流动性收紧 → 过渡带（过热→滞胀）
- 增长 ↑ 且 通胀 ↑ 且 政策/流动性不紧           → 过热
- 增长 ↓ 且 通胀 ↑                              → 滞胀
- 增长 ↑ 且 通胀 ≤ 0                            → 复苏
- 增长 ↓ 且 通胀 ≤ 0                            → 衰退
- 增长或通胀方向缺失/中性                        → 过渡带（数据不足）

输入：归一化记录列表（CSV：indicator,date,value），指标 ID 见 DIMENSIONS。
输出：PhaseResult(phase, confidence, evidence)，可 JSON 序列化。

用法：
    python engine/tools/cycle_clock.py --input <csv> [--json]
    python engine/tools/cycle_clock.py --snapshot data/processed/economy/dubai/apartment/quant_macro_snapshot.csv
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import mean, read_csv_records, to_float  # noqa: E402

# 维度 → 指标 ID 列表（值均为「同比 %」或点位，口径见数据文件注释）
DIMENSIONS = {
    "growth": ("GDP_YOY", "PMI", "INDUSTRIAL_YOY"),
    "inflation": ("CPI_YOY", "CORE_CPI_YOY", "PPI_YOY"),
    "policy": ("POLICY_RATE", "FISCAL_DEFICIT_GDP", "CREDIT_GROWTH"),
    "liquidity": ("M2_GROWTH", "EIBOR_3M", "TERM_SPREAD_10Y_3M"),
}

# 指标方向语义：positive 表示「读数上升」对应该维度的「紧/热」方向
# threshold: (中性下界, 中性上界)；超出上界记 +1，低于下界记 -1
_NEUTRAL = {
    "GDP_YOY": (2.0, 6.0),
    "PMI": (50.0, 55.0),
    "INDUSTRIAL_YOY": (1.0, 8.0),
    "CPI_YOY": (1.0, 2.5),
    "CORE_CPI_YOY": (1.0, 2.5),
    "PPI_YOY": (-1.0, 4.0),
    "POLICY_RATE": (-1.0, 1.0),      # 变动值（pp），非点位
    "FISCAL_DEFICIT_GDP": (-1.0, 2.0),
    "CREDIT_GROWTH": (3.0, 12.0),
    "M2_GROWTH": (4.0, 12.0),
    "EIBOR_3M": (-1.0, 1.0),         # 变动值（pp），非点位
    "TERM_SPREAD_10Y_3M": (-1.0, 1.5),
}


@dataclass
class PhaseResult:
    phase: str
    confidence: float
    evidence: dict = field(default_factory=dict)
    scores: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def _latest_series(records: list[dict], indicator: str) -> list[tuple[date, float]]:
    """取某指标按日期升序的 (date, value) 序列。"""
    out = []
    for r in records:
        if str(r.get("indicator", "")).strip() != indicator:
            continue
        d = str(r.get("date", "")).strip()
        try:
            y, m, dd = (int(x) for x in d.split("-"))
            dt = date(y, m, dd)
        except (ValueError, TypeError):
            continue
        out.append((dt, to_float(r.get("value"))))
    out.sort()
    return out


def _direction(indicator: str, series: list[tuple[date, float]]) -> int:
    """单指标方向打分：+1 偏热/紧，-1 偏冷/松，0 中性/数据不足。"""
    if not series:
        return 0
    latest = series[-1][1]
    prev = series[-4][1] if len(series) >= 4 else (series[0][1] if len(series) > 1 else latest)
    lo, hi = _NEUTRAL.get(indicator, (-1.0, 1.0))
    rising = latest > prev
    falling = latest < prev
    if latest > hi:
        return 1
    if latest < lo:
        return -1
    # 中性区间：用趋势方向
    if rising:
        return 1
    if falling:
        return -1
    return 0


def classify(records: list[dict]) -> PhaseResult:
    """周期阶段判定（纯函数）。"""
    evidence: dict = {}
    dim_score: dict = {}
    dims_with_data = 0
    for dim, ids in DIMENSIONS.items():
        votes = []
        ev = {}
        for ind in ids:
            series = _latest_series(records, ind)
            d = _direction(ind, series)
            if series:
                votes.append(d)
                ev[ind] = {"latest": series[-1][1], "date": series[-1][0].isoformat(),
                           "score": d, "n": len(series)}
        if votes:
            dims_with_data += 1
            dim_score[dim] = 1 if mean(votes) > 0.1 else (-1 if mean(votes) < -0.1 else 0)
        else:
            dim_score[dim] = 0
        evidence[dim] = ev

    g = dim_score.get("growth", 0)
    i = dim_score.get("inflation", 0)
    p = dim_score.get("policy", 0)
    l = dim_score.get("liquidity", 0)

    if g == 0 or i == 0:
        phase = "过渡带"
    elif g > 0 and i > 0:
        phase = "过渡带" if (p > 0 or l > 0) else "过热"
    elif g < 0 and i > 0:
        phase = "滞胀"
    elif g > 0 and i <= 0:
        phase = "复苏"
    else:  # g < 0 and i <= 0
        phase = "衰退"

    confidence = round(dims_with_data / len(DIMENSIONS), 3)
    return PhaseResult(phase=phase, confidence=confidence, evidence=evidence, scores=dim_score)


def classify_snapshot(path: Path) -> PhaseResult:
    """从 CSV 文件读取记录并判定。"""
    return classify(read_csv_records(path))


def main() -> int:
    ap = argparse.ArgumentParser(description="宏观周期时钟（N1）")
    ap.add_argument("--input", "--snapshot", dest="input", help="归一化宏观读数 CSV")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
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
    result = classify_snapshot(p)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"周期阶段：{result.phase}（置信度 {result.confidence:.0%}）")
        for dim, sc in result.scores.items():
            print(f"  {dim}: {sc:+d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
