# -*- coding: utf-8 -*-
"""finding→规则回写台账测试（finding_rule）。

锁定：
- schema 字段完整、14 项历史 finding 映射率 100%、无时间戳、可重放；
- register 幂等且确定性（重登字节一致、同 id 覆盖更新）；
- match 对测试 finding 至少命中 1 条规则，无关文本不命中；
- stats 计数与映射率正确。

运行：python -m unittest discover -s engine/tests -p "test_finding_rule.py"
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "tools" / "finding_rule.py"
LEDGER = ROOT / "engine" / "audit" / "records" / "finding-rules.json"

HISTORICAL_IDS = ["F1-1", "F1-2", "F1-3", "F1-4",
                  "F2-1", "F2-2", "F2-3",
                  "F3-1", "F3-2", "F3-3",
                  "F4-1", "F4-2", "F4-3", "F4-4"]


def _load():
    spec = importlib.util.spec_from_file_location("finding_rule", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def test_ledger_exists_and_has_14_historical_findings(self):
        self.assertTrue(LEDGER.exists(), f"缺台账：{LEDGER}")
        data = self.mod.load(LEDGER)
        ids = [r["finding_id"] for r in data["records"]]
        for fid in HISTORICAL_IDS:
            self.assertIn(fid, ids, f"历史 finding {fid} 未回填")
        self.assertEqual(len(ids), 14)

    def test_required_fields_complete(self):
        data = self.mod.load(LEDGER)
        for r in data["records"]:
            for f in ("finding_id", "source", "root_cause", "prevention_rule",
                      "rule_type", "rule_location", "hit_count", "status"):
                self.assertIn(f, r, f"{r.get('finding_id')} 缺字段 {f}")
                self.assertTrue(str(r[f]).strip() or isinstance(r[f], int),
                                f"{r.get('finding_id')} 字段 {f} 为空")

    def test_enum_and_mapping_rate(self):
        s = self.mod.stats(LEDGER)
        self.assertEqual(s["total"], 14)
        self.assertEqual(s["pending"], 0)
        self.assertEqual(s["mapping_rate"], 1.0)
        self.assertEqual(s["by_status"]["已映射"] + s["by_status"]["新建"], 14)

    def test_no_timestamp_fields(self):
        blob = LEDGER.read_text(encoding="utf-8")
        for k in ("timestamp", "generated_at", "updated_at", "created_at"):
            self.assertNotIn(f'"{k}"', blob)

    def test_check_passes(self):
        self.assertEqual(self.mod.check(LEDGER), [])


class TestRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def _rec(self, fid="F9-1"):
        return self.mod.build_record(
            finding_id=fid, source="engine/report-audits/test.md#f9",
            root_cause="测试根因：正文期次与台账期次错配",
            prevention_rule="测试规则：期次须一致",
            rule_type="校验项", rule_location="engine/tools/test_check.py#r1",
            keywords=["期次", "台账", "错配"], status="新建")

    def test_register_and_reload(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "finding-rules.json"
            self.mod.register(self._rec(), p)
            data = self.mod.load(p)
            self.assertEqual(len(data["records"]), 1)
            self.assertEqual(data["records"][0]["finding_id"], "F9-1")
            self.assertEqual(self.mod.check(p), [])

    def test_register_deterministic_and_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "finding-rules.json"
            self.mod.register(self._rec(), p)
            first = p.read_text(encoding="utf-8")
            self.mod.register(self._rec(), p)
            second = p.read_text(encoding="utf-8")
            self.assertEqual(first, second)
            self.assertEqual(len(self.mod.load(p)["records"]), 1)

    def test_register_updates_same_id_without_duplicating(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "finding-rules.json"
            self.mod.register(self._rec(), p)
            updated = self._rec()
            updated["status"] = "已映射"
            updated["hit_count"] = 3
            self.mod.register(updated, p)
            data = self.mod.load(p)
            self.assertEqual(len(data["records"]), 1)
            self.assertEqual(data["records"][0]["status"], "已映射")
            self.assertEqual(data["records"][0]["hit_count"], 3)

    def test_register_rejects_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "finding-rules.json"
            bad = self._rec()
            bad["rule_type"] = "未知类型"
            with self.assertRaises(ValueError):
                self.mod.register(bad, p)


class TestMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def test_match_hits_at_least_one_rule(self):
        hits = self.mod.match("正文期次与台账期次错配，租金口径不一致", LEDGER)
        self.assertGreaterEqual(len(hits), 1)
        self.assertIn("F1-1", [h["finding_id"] for h in hits])

    def test_match_sorted_by_score_desc(self):
        hits = self.mod.match("期次 台账 口径 租金 错配", LEDGER)
        scores = [h["score"] for h in hits]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_match_unrelated_text_no_hit(self):
        hits = self.mod.match("今天天气晴朗，适合出门散步", LEDGER, threshold=1)
        self.assertEqual(hits, [])

    def test_match_threshold_filters(self):
        text = "期次 台账 口径 租金 错配"
        low = self.mod.match(text, LEDGER, threshold=1)
        high = self.mod.match(text, LEDGER, threshold=999)
        self.assertGreaterEqual(len(low), 1)
        self.assertEqual(high, [])


class TestStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def test_stats_counts(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "finding-rules.json"
            self.mod.register(self.mod.build_record(
                finding_id="F9-1", source="s", root_cause="r",
                prevention_rule="p", rule_type="校验项",
                rule_location="loc", status="已映射", hit_count=2), p)
            self.mod.register(self.mod.build_record(
                finding_id="F9-2", source="s", root_cause="r",
                prevention_rule="p", rule_type="规范条款",
                rule_location="loc", status="新建", hit_count=1), p)
            s = self.mod.stats(p)
            self.assertEqual(s["total"], 2)
            self.assertEqual(s["mapped"], 2)
            self.assertEqual(s["mapping_rate"], 1.0)
            self.assertEqual(s["total_hits"], 3)
            self.assertEqual(s["by_status"]["已映射"], 1)
            self.assertEqual(s["by_status"]["新建"], 1)


class TestCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load()

    def test_cli_stats(self):
        r = subprocess.run([sys.executable, str(TOOL), "stats"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("记录 14 条", r.stdout)

    def test_cli_check(self):
        r = subprocess.run([sys.executable, str(TOOL), "check"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[OK]", r.stdout)

    def test_cli_match_exit_codes(self):
        hit = subprocess.run([sys.executable, str(TOOL), "match",
                              "--text", "期次 台账 口径 租金 错配"],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(hit.returncode, 0, hit.stdout + hit.stderr)
        miss = subprocess.run([sys.executable, str(TOOL), "match",
                               "--text", "今天天气晴朗，适合出门散步"],
                              cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(miss.returncode, 2, miss.stdout + miss.stderr)

    def test_cli_match_json(self):
        r = subprocess.run([sys.executable, str(TOOL), "match",
                            "--text", "期次 台账 口径 租金 错配", "--json"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        self.assertGreaterEqual(len(data), 1)


if __name__ == "__main__":
    unittest.main()
