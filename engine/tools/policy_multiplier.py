"""N3 · 政策乘数表（实施方案第一节 N3，P0）。

维护 G01–G05 的「工具 → 中间目标 → 最终目标 → 时滞 → 乘数」链条。
数据源：data/processed/economy/dubai/apartment/quant_policy_multipliers.csv（可执行、可更新）。

硬规则：
- 状态非「已核验」的政策，`multiplier` 必须为空（不得给数值），只能给 `reference_range`；
- reference_range 为「文献/经验参考，未经本地回测」，仅供压力测试情景参用，须显式标注。

用法：
    python engine/tools/policy_multiplier.py --list
    python engine/tools/policy_multiplier.py --coverage
    python engine/tools/policy_multiplier.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _quant import read_csv_records, to_float  # noqa: E402

DEFAULT_CSV = "data/processed/economy/dubai/apartment/quant_policy_multipliers.csv"
VERIFIED = "已核验"


@dataclass
class Policy:
    id: str
    name: str
    tool: str
    chain: str
    lag_quarters: str
    status: str
    source_url: str = ""
    effective_date: str = ""
    review_date: str = ""
    multiplier_low: float | None = None
    multiplier_high: float | None = None
    multiplier_unit: str = ""
    multiplier_note: str = ""
    reference_low: float | None = None
    reference_high: float | None = None
    reference_basis: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def load(path: str | Path | None = None) -> list[Policy]:
    """读取政策乘数表并执行硬规则校验。"""
    p = Path(path) if path else Path(__file__).resolve().parents[2] / DEFAULT_CSV
    if not p.exists():
        raise FileNotFoundError(f"政策乘数表不存在: {p}")
    out = []
    for r in read_csv_records(p):
        pid = str(r.get("id", "")).strip()
        if not pid:
            continue
        lo = to_float(r.get("multiplier_low"), float("nan"))
        hi = to_float(r.get("multiplier_high"), float("nan"))
        rlo = to_float(r.get("reference_low"), float("nan"))
        rhi = to_float(r.get("reference_high"), float("nan"))
        pol = Policy(
            id=pid,
            name=str(r.get("name", "")).strip(),
            tool=str(r.get("tool", "")).strip(),
            chain=str(r.get("chain", "")).strip(),
            lag_quarters=str(r.get("lag_quarters", "")).strip(),
            status=str(r.get("status", "")).strip(),
            source_url=str(r.get("source_url", "")).strip(),
            effective_date=str(r.get("effective_date", "")).strip(),
            review_date=str(r.get("review_date", "")).strip(),
            multiplier_low=None if lo != lo else lo,
            multiplier_high=None if hi != hi else hi,
            multiplier_unit=str(r.get("multiplier_unit", "")).strip(),
            multiplier_note=str(r.get("multiplier_note", "")).strip(),
            reference_low=None if rlo != rlo else rlo,
            reference_high=None if rhi != rhi else rhi,
            reference_basis=str(r.get("reference_basis", "")).strip(),
        )
        validate_policy(pol)
        out.append(pol)
    return out


def validate_policy(pol: Policy) -> None:
    """硬规则：未核验不得给乘数；乘数区间必须 low<=high。"""
    has_mult = pol.multiplier_low is not None or pol.multiplier_high is not None
    if pol.status != VERIFIED and has_mult:
        raise ValueError(f"{pol.id}: 状态非「{VERIFIED}」不得给出乘数数值")
    if has_mult and pol.multiplier_low is not None and pol.multiplier_high is not None:
        if pol.multiplier_low > pol.multiplier_high:
            raise ValueError(f"{pol.id}: 乘数区间 low>high")


def coverage(policies: list[Policy]) -> tuple[int, int, float]:
    """-> (已核验数, 总数, 覆盖率)。"""
    total = len(policies)
    verified = sum(1 for p in policies if p.status == VERIFIED)
    return verified, total, (verified / total if total else 0.0)


def main() -> int:
    ap = argparse.ArgumentParser(description="政策乘数表（N3）")
    ap.add_argument("--input", help="政策乘数表 CSV（缺省用业务线默认路径）")
    ap.add_argument("--list", action="store_true", help="列表输出")
    ap.add_argument("--coverage", action="store_true", help="只输出核验覆盖率")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        policies = load(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"[ERROR] {e}")
        return 1
    verified, total, rate = coverage(policies)
    if args.coverage:
        print(f"政策核验覆盖率：{verified}/{total}（{rate:.0%}）")
        return 0
    if args.json:
        print(json.dumps([p.to_dict() for p in policies], ensure_ascii=False, indent=2))
        return 0
    print(f"政策乘数表（{verified}/{total} 已核验，覆盖率 {rate:.0%}）\n")
    for p in policies:
        mult = (f"{p.multiplier_low}~{p.multiplier_high}{p.multiplier_unit}"
                if p.multiplier_low is not None else "不可估（未核验/数据不足）")
        ref = (f"；参考区间 {p.reference_low}~{p.reference_high}（未校准）"
               if p.reference_low is not None else "")
        print(f"{p.id} {p.name}｜状态={p.status}｜链条={p.chain}｜时滞={p.lag_quarters}")
        print(f"    乘数={mult}{ref}")
        if p.multiplier_note:
            print(f"    说明={p.multiplier_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
