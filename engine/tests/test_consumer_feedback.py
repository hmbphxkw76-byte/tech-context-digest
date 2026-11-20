# -*- coding: utf-8 -*-
"""消费端反馈台账测试（CONSUMER-FEEDBACK-LEDGER v1.0，2026-11-20）。

锁定：
- schema / 字段校验（entry_id、kind、status、report、source）；
- 写盘确定性（同输入重放字节一致，`check` 可重放）；
- `stats()` 口径与 CF-02 / CF-03 一致（纠错条目数、有回访记录的报告数）。
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load():
    spec = importlib.util.spec_from_file_location("consumer_feedback",
                                                  TOOLS / "consumer_feedback.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["consumer_feedback"] = mod
    spec.loader.exec_module(mod)
    return mod


cf = _load()


class TestSchema(unittest.TestCase):
    def test_new_ledger_fields(self):
        d = cf.new_ledger()
        self.assertEqual(d["spec"], "CONSUMER-FEEDBACK-LEDGER v1.0")
        self.assertEqual(d["kinds"], ["纠错", "回访"])
        self.assertEqual(d["records"], [])

    def test_register_ok(self):
        d, errs = cf.register(cf.new_ledger(), "CFB-001",
                              "content/economy/trends/reports/2026-11-20_weekly.html",
                              "纠错", "open", "github-issue #1", "数值有误", "2026-11")
        self.assertEqual(errs, [])
        self.assertEqual(len(d["records"]), 1)

    def test_register_rejects_bad_values(self):
        base = ("CFB-001", "content/x/reports/a.html")
        cases = [
            ("CFB-001", "纠错", "bogus", "github-issue #1"),      # status 非法
            ("CFB-001", "其他", "open", "github-issue #1"),       # kind 非法
            ("CFB-001", "纠错", "open", ""),                      # source 为空
            ("CFB-001", "纠错", "open", "github-issue #1"),       # 合法（对照）
        ]
        for eid, kind, status, source in cases:
            _, errs = cf.register(cf.new_ledger(), eid, base[1], kind, status, source)
            if source and kind == "纠错" and status == "open":
                self.assertEqual(errs, [])
            else:
                self.assertTrue(errs)

    def test_register_rejects_bad_id_and_period(self):
        _, errs = cf.register(cf.new_ledger(), "CFB-1", "content/x/reports/a.html",
                              "纠错", "open", "github-issue #1")
        self.assertTrue(any("entry_id" in e for e in errs))
        _, errs = cf.register(cf.new_ledger(), "CFB-002", "content/x/reports/a.html",
                              "纠错", "open", "github-issue #1", period="2026/11")
        self.assertTrue(any("period" in e for e in errs))

    def test_register_rejects_duplicate(self):
        d, _ = cf.register(cf.new_ledger(), "CFB-001", "content/x/reports/a.html",
                           "纠错", "open", "github-issue #1")
        _, errs = cf.register(d, "CFB-001", "content/x/reports/b.html",
                              "回访", "open", "github-issue #2")
        self.assertTrue(any("重复" in e for e in errs))


class TestDeterminism(unittest.TestCase):
    def _filled(self):
        d = cf.new_ledger()
        for i, (kind, status) in enumerate((("纠错", "open"), ("回访", "resolved"),
                                            ("纠错", "wontfix")), start=1):
            d, _ = cf.register(d, f"CFB-{i:03d}", f"content/x/reports/r{i}.html",
                               kind, status, f"github-issue #{i}")
        return d

    def test_render_sorted_and_replayable(self):
        d = self._filled()
        self.assertEqual(cf.render(d), cf.render(self._filled()))
        self.assertEqual([r["entry_id"] for r in d["records"]],
                         ["CFB-001", "CFB-002", "CFB-003"])

    def test_save_then_check_ok(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "consumer-feedback.json"
            cf.save(self._filled(), p)
            self.assertEqual(cf.check(cf.load(p), p), [])

    def test_check_detects_hand_edit(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "consumer-feedback.json"
            cf.save(self._filled(), p)
            text = p.read_text(encoding="utf-8").replace('"records"', '"records_x"')
            p.write_text(text, encoding="utf-8")
            self.assertTrue(cf.check(cf.load(p), p))


class TestStats(unittest.TestCase):
    def test_stats_counts(self):
        d = cf.new_ledger()
        d, _ = cf.register(d, "CFB-001", "content/x/reports/a.html", "纠错", "open", "i#1")
        d, _ = cf.register(d, "CFB-002", "content/x/reports/a.html", "纠错", "resolved", "i#2")
        d, _ = cf.register(d, "CFB-003", "content/x/reports/b.html", "回访", "open", "i#3")
        s = cf.stats(d)
        self.assertEqual(s["total"], 3)
        self.assertEqual(s["correction_count"], 2)
        self.assertEqual(s["revisit_count"], 1)
        self.assertEqual(s["feedback_report_count"], 2)
        self.assertEqual(s["revisit_report_count"], 1)

    def test_stats_empty(self):
        s = cf.stats(cf.new_ledger())
        self.assertEqual(s["correction_count"], 0)
        self.assertEqual(s["revisit_report_count"], 0)


if __name__ == "__main__":
    unittest.main()
