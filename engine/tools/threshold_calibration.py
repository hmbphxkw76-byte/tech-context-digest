"""阈值滚动校准模块（实施方案第四节 4.3）。

- calibrate：滚动窗口分位数阈值（缺省 36 个月；样本不足用全样本并标注）。
- state_count：状态计数（首次进入 + 持续时长），替代触发计数。
- backtest：阈值命中率 / MAPE。

用法：
    python engine/tools/threshold_calibration.py --input <csv> --column value --window 36
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import mean, percentile, read_csv_records, to_float  # noqa: E402


@dataclass
class Calibration:
    low: float
    high: float
    median: float
    n: int
    window: int
    lower_q: float
    upper_q: float
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def calibrate(series: list[float], window: int = 36, lower_q: float = 10,
              upper_q: float = 90) -> Calibration:
    vals = [float(v) for v in series if v is not None]
    if not vals:
        raise ValueError("空序列")
    used = vals[-window:] if window > 0 else vals
    s = sorted(used)
    note = "" if len(used) >= window else f"样本不足 {window}，用全样本 {len(used)}"
    return Calibration(
        low=round(percentile(s, lower_q), 4),
        high=round(percentile(s, upper_q), 4),
        median=round(percentile(s, 50), 4),
        n=len(used), window=window, lower_q=lower_q, upper_q=upper_q, note=note,
    )


def state_count(series: list[float], threshold: float, direction: str = "above",
                min_duration: int = 1) -> list[dict]:
    """状态计数：返回连续区间 [{start, end, duration}]（索引从 0 起）。"""
    episodes = []
    start = None
    for i, v in enumerate(series):
        hit = (v >= threshold) if direction == "above" else (v <= threshold)
        if hit and start is None:
            start = i
        elif not hit and start is not None:
            if i - start >= min_duration:
                episodes.append({"start": start, "end": i - 1, "duration": i - start})
            start = None
    if start is not None and len(series) - start >= min_duration:
        episodes.append({"start": start, "end": len(series) - 1, "duration": len(series) - start})
    return episodes


def trigger_count(series: list[float], threshold: float, direction: str = "above") -> int:
    """触发计数（对照用，不用于阈值校准）。"""
    return sum(1 for v in series
               if ((v >= threshold) if direction == "above" else (v <= threshold)))


def backtest(predicted: list[float], actual: list[float]) -> dict:
    """命中率（方向一致）与 MAPE。"""
    if len(predicted) != len(actual) or not predicted:
        raise ValueError("长度不一致或为空")
    n = len(actual)
    hit = sum(1 for p, a in zip(predicted, actual) if (p >= 0) == (a >= 0))
    mape = mean([abs((a - p) / a) for p, a in zip(predicted, actual) if a != 0])
    return {"n": n, "hit_rate": round(hit / n, 4), "mape": round(mape, 4)}


def main() -> int:
    ap = argparse.ArgumentParser(description="阈值滚动校准（4.3）")
    ap.add_argument("--input", required=True)
    ap.add_argument("--column", default="value")
    ap.add_argument("--window", type=int, default=36)
    ap.add_argument("--lower-q", type=float, default=10)
    ap.add_argument("--upper-q", type=float, default=90)
    ap.add_argument("--threshold", type=float, help="给定阈值时输出状态计数")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    p = Path(args.input)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / args.input
    if not p.exists():
        print(f"[ERROR] 输入不存在: {p}")
        return 1
    series = [to_float(r.get(args.column)) for r in read_csv_records(p)]
    try:
        cal = calibrate(series, args.window, args.lower_q, args.upper_q)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return 1
    out: dict = {"calibration": cal.to_dict()}
    if args.threshold is not None:
        out["state_count"] = state_count(series, args.threshold)
        out["trigger_count"] = trigger_count(series, args.threshold)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
