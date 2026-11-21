#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""来源定期复核与到期告警（INFORMATION-VERIFICATION-SPEC v1.0 第 4 节）。

本仓库此前只有「登记时核验」，没有「来源级重核周期」：一条来源一旦登记为
verified，就永久沿用，无法发现「官方页面已更新 / 门户数据已改版 / 快照已过期」。
本模块按机构 tier 设定重核周期，扫描全部 ``source_registry.json``，输出
到期 / 临期清单，供定期维护告警与人工复核。

重核周期（按机构 tier，天数；tier 越低越权威，重核越宽）：
    tier 1 官方一手 180 天；tier 2 行业机构 120 天；
    tier 3 挂牌门户 90 天；tier 4 媒体转述 60 天。
基准日：``evidence.snapshot_date`` 优先，其次 ``updated``；两者都缺记 ``unknown``。
临期阈值：达到周期 80% 即 ``due_soon``。

输出：``engine/audit/records/pending_verification.json``（确定性排序、无墙钟时间戳，
周期由 ``--period`` 锚定，同周期重跑为覆盖）。

退出码：0 无到期 / 临期；2 存在到期或临期（告警，不阻断提交）。
"""
from __future__ import annotations

import argparse
import calendar
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402
from gate_period import AUTO  # noqa: E402
from gate_period import resolve as resolve_period
from source_normalize import normalize_date  # noqa: E402
from verification_ledger import collect_registries  # noqa: E402

PENDING_PATH = ROOT / "engine" / "audit" / "records" / "pending_verification.json"
PENDING_SCHEMA = "1.0"

# 重核周期（天）：key = 机构 tier
RECHECK_DAYS = {1: 180, 2: 120, 3: 90, 4: 60}
DEFAULT_TIER_DAYS = 60          # tier 缺失 / 非法时按最严口径
DUE_SOON_RATIO = 0.8            # 达到周期 80% 视为临期

STATE_OK = "ok"
STATE_DUE_SOON = "due_soon"
STATE_OVERDUE = "overdue"
STATE_UNKNOWN = "unknown"


def period_end(period: str) -> _dt.date:
    """周期标识 -> 该周期最后一日（``auto`` 解析为当前自然月）。"""
    p = resolve_period(period)  # YYYY-MM / YYYY-Qn / YYYY
    if "Q" in p:
        y, q = int(p[:4]), int(p.split("Q")[1])
        m = q * 3
    elif len(p) >= 7 and p[4] == "-":
        y, m = int(p[:4]), int(p[5:7])
    else:
        y, m = int(p[:4]), 12
    last = calendar.monthrange(y, m)[1]
    return _dt.date(y, m, last)


def _base_date(source: dict) -> str | None:
    ev = source.get("evidence")
    if isinstance(ev, dict):
        d = normalize_date(ev.get("snapshot_date"))
        if d:
            return d
    return normalize_date(source.get("updated"))


def _tier_days(tier) -> int:
    try:
        t = int(tier)
    except (TypeError, ValueError):
        return DEFAULT_TIER_DAYS
    return RECHECK_DAYS.get(t, DEFAULT_TIER_DAYS)


def review(period: str = AUTO, as_of: _dt.date | None = None,
           registries: list[tuple[str, dict]] | None = None) -> dict:
    """扫描登记 -> 复核报告（确定性）。

    as_of 缺省取 period 的最后一日（周期锚定，不取墙钟，保证可重放）。
    """
    as_of = as_of or period_end(period)
    regs = registries if registries is not None else collect_registries()
    items: list[dict] = []
    counts = {STATE_OK: 0, STATE_DUE_SOON: 0, STATE_OVERDUE: 0, STATE_UNKNOWN: 0}
    for business_line, reg in regs:
        sources = reg.get("sources", []) if isinstance(reg, dict) else []
        for s in sources:
            sid = str(s.get("source_id", "")).strip() or "<无 source_id>"
            base = _base_date(s)
            tier = s.get("tier")
            days_limit = _tier_days(tier)
            if base is None:
                state = STATE_UNKNOWN
                days = None
            else:
                bd = _dt.date.fromisoformat(base)
                days = (as_of - bd).days
                if days > days_limit:
                    state = STATE_OVERDUE
                elif days > int(days_limit * DUE_SOON_RATIO):
                    state = STATE_DUE_SOON
                else:
                    state = STATE_OK
            counts[state] += 1
            items.append({
                "business_line": business_line,
                "source_id": sid,
                "publisher": str(s.get("publisher", "")).strip(),
                "tier": tier,
                "verify_status": str(s.get("verify_status", "")).strip(),
                "base_date": base,
                "days": days,
                "limit_days": days_limit,
                "state": state,
            })
    items.sort(key=lambda x: (x["business_line"], x["source_id"]))
    return {
        "schema_version": PENDING_SCHEMA,
        "period": resolve_period(period),
        "as_of": as_of.isoformat(),
        "policy": {"recheck_days": dict(sorted(RECHECK_DAYS.items())),
                   "due_soon_ratio": DUE_SOON_RATIO,
                   "default_tier_days": DEFAULT_TIER_DAYS},
        "counts": counts,
        "items": items,
    }


def emit(report: dict, path: str | Path | None = None) -> Path:
    p = Path(path) if path else PENDING_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description="来源定期复核与到期告警")
    ap.add_argument("--period", default=AUTO,
                    help="复核周期锚（默认 auto = 当前自然月；可显式 YYYY-MM / YYYY-Qn / YYYY）")
    ap.add_argument("--as-of", default=None, help="复核基准日 YYYY-MM-DD（缺省取 period 末日）")
    ap.add_argument("--emit", default=None, help="输出 JSON 路径（缺省 engine/audit/records/pending_verification.json）")
    ap.add_argument("--json", action="store_true", help="向 stdout 打印报告 JSON")
    args = ap.parse_args()

    as_of = _dt.date.fromisoformat(args.as_of) if args.as_of else None
    rep = review(args.period, as_of=as_of)
    if args.emit:
        emit(rep, args.emit)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        c = rep["counts"]
        print(f"来源定期复核（{as_of or rep['as_of']}）："
              f"到期 {c[STATE_OVERDUE]}，临期 {c[STATE_DUE_SOON]}，"
              f"正常 {c[STATE_OK]}，缺基准日 {c[STATE_UNKNOWN]}")
        for it in rep["items"]:
            if it["state"] in (STATE_OVERDUE, STATE_DUE_SOON):
                print(f"[{it['state']}] {it['business_line']} {it['source_id']} "
                      f"（{it['publisher']}，tier={it['tier']}，基准 {it['base_date']}，"
                      f"{it['days']} 天 / 周期 {it['limit_days']} 天）")
    if rep["counts"][STATE_OVERDUE] or rep["counts"][STATE_DUE_SOON]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
