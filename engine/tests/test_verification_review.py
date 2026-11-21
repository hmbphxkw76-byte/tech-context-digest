# -*- coding: utf-8 -*-
"""来源定期复核测试（INFORMATION-VERIFICATION-SPEC v1.0 第四节）。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from verification_review import (  # noqa: E402
    DUE_SOON_RATIO,
    RECHECK_DAYS,
    emit,
    period_end,
    review,
)


def _reg(sources):
    return {"schema_version": "1.1", "sources": sources}


class TestPeriodEnd(unittest.TestCase):
    def test_month_end(self):
        self.assertEqual(period_end("2026-11"), dt.date(2026, 11, 30))
        self.assertEqual(period_end("2026-02"), dt.date(2026, 2, 28))

    def test_quarter_end(self):
        self.assertEqual(period_end("2026-Q3"), dt.date(2026, 9, 30))


class TestReview(unittest.TestCase):
    def test_overdue(self):
        as_of = dt.date(2026, 11, 30)
        regs = [("content/a/b", _reg([
            {"source_id": "S-1", "tier": 1, "updated": "2020-01-01"},
        ]))]
        rep = review("2026-11", as_of=as_of, registries=regs)
        self.assertEqual(rep["counts"]["overdue"], 1)
        self.assertEqual(rep["items"][0]["state"], "overdue")

    def test_due_soon(self):
        as_of = dt.date(2026, 11, 30)
        # tier 1 周期 180 天；基准日 = as_of - 150 天（> 80% 且 <= 100%）
        base = (as_of - dt.timedelta(days=150)).isoformat()
        regs = [("content/a/b", _reg([{"source_id": "S-1", "tier": 1, "updated": base}]))]
        rep = review("2026-11", as_of=as_of, registries=regs)
        self.assertEqual(rep["counts"]["due_soon"], 1)

    def test_ok_and_unknown(self):
        as_of = dt.date(2026, 11, 30)
        regs = [("content/a/b", _reg([
            {"source_id": "S-1", "tier": 1, "updated": as_of.isoformat()},
            {"source_id": "S-2", "tier": 2},
        ]))]
        rep = review("2026-11", as_of=as_of, registries=regs)
        self.assertEqual(rep["counts"]["ok"], 1)
        self.assertEqual(rep["counts"]["unknown"], 1)

    def test_snapshot_date_preferred(self):
        as_of = dt.date(2026, 11, 30)
        regs = [("content/a/b", _reg([
            {"source_id": "S-1", "tier": 1, "updated": "2026-11-01",
             "evidence": {"snapshot_date": "2020-01-01"}},
        ]))]
        rep = review("2026-11", as_of=as_of, registries=regs)
        self.assertEqual(rep["items"][0]["base_date"], "2020-01-01")
        self.assertEqual(rep["items"][0]["state"], "overdue")

    def test_deterministic(self):
        regs = [("content/a/b", _reg([{"source_id": "S-1", "tier": 1, "updated": "2024-01-01"}]))]
        a = review("2026-11", registries=regs)
        b = review("2026-11", registries=regs)
        self.assertEqual(a, b)

    def test_emit_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "pending.json"
            rep = review("2026-11", registries=[])
            emit(rep, p)
            self.assertEqual(json.loads(p.read_text(encoding="utf-8"))["as_of"],
                             rep["as_of"])

    def test_policy_constants(self):
        self.assertEqual(RECHECK_DAYS, {1: 180, 2: 120, 3: 90, 4: 60})
        self.assertEqual(DUE_SOON_RATIO, 0.8)


if __name__ == "__main__":
    unittest.main()
