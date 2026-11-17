# -*- coding: utf-8 -*-
"""盲区台账门禁（DECISION-DELIVERY-SPEC v1.0 第六节）单元测试。

覆盖 blind_spot_check：字段 / 状态 / 责任周期 / P0 四类。
运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import blind_spot_check as m  # noqa: E402

HEADER = "| ID | 项目 | 优先级 | 影响 | 发现日期 | 责任周期 | 消号条件 | 状态 | 关联 KPI |\n|---|---|---|---|---|---|---|---|---|\n"


class TestBlindSpot(unittest.TestCase):
    def test_actual_ledger_passes(self):
        text = m.LEDGER.read_text(encoding="utf-8")
        self.assertEqual(m.check_text(text), [])

    def test_missing_p0_flagged(self):
        text = HEADER + "| B99 | 其他 | P1 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("BS-04", rules)

    def test_invalid_status_flagged(self):
        text = HEADER + ("| B01 | 空置 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | done | KPI |\n"
                         "| B02 | 就业 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B03 | 竣工 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B15 | 收入 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n")
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("BS-02", rules)

    def test_missing_priority_flagged(self):
        text = HEADER + ("| B01 | 空置 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B02 | 就业 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B03 | 竣工 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B15 | 收入 | — | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n")
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("BS-01", rules)

    def test_bad_cycle_flagged(self):
        text = HEADER + ("| B01 | 空置 | P0 | 影响 | 2026-11-14 | 近期 | 条件 | open | KPI |\n"
                         "| B02 | 就业 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B03 | 竣工 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n"
                         "| B15 | 收入 | P0 | 影响 | 2026-11-14 | 2026-12 | 条件 | open | KPI |\n")
        rules = {r for r, _ in m.check_text(text)}
        self.assertIn("BS-01", rules)


if __name__ == "__main__":
    unittest.main()
