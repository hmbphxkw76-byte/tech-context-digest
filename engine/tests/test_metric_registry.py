# -*- coding: utf-8 -*-
"""指标单一事实源（metric_registry / T3）单元测试。"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

spec = importlib.util.spec_from_file_location("metric_registry", ROOT / "engine" / "tools" / "metric_registry.py")
mr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mr)


class TestDictionary(unittest.TestCase):
    def test_has_30_metrics(self):
        d = mr.load_dictionary()
        self.assertEqual(len(mr.metric_ids(d)), 30)

    def test_get_and_alias(self):
        d = mr.load_dictionary()
        self.assertEqual(mr.get_metric(d, "A-01")["name"], "来源可追溯率")
        self.assertIsNotNone(mr.by_alias(d, "L3-4.2"))

    def test_threshold_parsing(self):
        self.assertEqual(mr.parse_threshold(">=0.95"), (">=", 0.95))
        self.assertEqual(mr.parse_threshold("100%"), ("=", 1.0))
        self.assertEqual(mr.parse_threshold("<=5%"), ("<=", 0.05))

    def test_evaluate(self):
        ok, _ = mr.evaluate(">=0.95", 0.97)
        self.assertTrue(ok)
        ok2, _ = mr.evaluate(">=0.95", 0.90)
        self.assertFalse(ok2)
        ok3, _ = mr.evaluate("=1.0", "100%")
        self.assertTrue(ok3)


class TestNormalizeRows(unittest.TestCase):
    def test_valid(self):
        rows = [{"date": "2026-11-15", "indicator_id": "K01", "value": "4.5",
                 "unit": "%", "caliber": "3M", "source_id": "S1", "status": "已核验"}]
        ok, errs = mr.normalize_rows(rows)
        self.assertEqual(len(ok), 1)
        self.assertEqual(errs, [])

    def test_missing_field(self):
        ok, errs = mr.normalize_rows([{"indicator_id": "K01"}])
        self.assertEqual(ok, [])
        self.assertTrue(errs)

    def test_bad_status(self):
        rows = [{"date": "2026-11-15", "indicator_id": "K01", "value": "1", "unit": "%",
                 "caliber": "x", "source_id": "S1", "status": "随便"}]
        ok, errs = mr.normalize_rows(rows)
        self.assertEqual(ok, [])
        self.assertTrue(errs)


class TestAliasUniqueness(unittest.TestCase):
    def test_metric_ids_unique(self):
        d = mr.load_dictionary()
        ids = mr.metric_ids(d)
        self.assertEqual(len(ids), len(set(ids)))

    def test_alias_unique_no_l3_43_conflict(self):
        """L3-4.3 冲突已去重：L3-4.3 唯一归属 L-01；L-03 使用独立别名。"""
        d = mr.load_dictionary()
        self.assertEqual(mr.dictionary_conflicts(d), [])
        self.assertEqual(mr.resolve_alias(d, "L3-4.3")[0]["metric_id"], "L-01")
        self.assertEqual(mr.resolve_alias(d, "L3-4.3")[1], [])
        self.assertEqual(mr.resolve_alias(d, "L3-4.3-阈值")[0]["metric_id"], "L-03")

    def test_dedupe_aliases_keeps_first(self):
        d = {"metrics": [
            {"metric_id": "X-01", "aliases": ["dup"]},
            {"metric_id": "X-02", "aliases": ["dup"]},
        ]}
        self.assertTrue(mr.dictionary_conflicts(d))
        clean, removed = mr.dedupe_aliases(d)
        self.assertEqual(clean["metrics"][0]["aliases"], ["dup"])
        self.assertEqual(clean["metrics"][1]["aliases"], [])
        self.assertTrue(removed)
        self.assertEqual(mr.dictionary_conflicts(clean), [])

    def test_check_dictionary_ok(self):
        self.assertEqual(mr.check_dictionary(mr.load_dictionary()), [])


class TestDedupeRows(unittest.TestCase):
    def _row(self, date, iid, cal, value, unit="%", src="S1"):
        return {"date": date, "indicator_id": iid, "value": value, "unit": unit,
                "caliber": cal, "source_id": src, "status": "已核验"}

    def test_case_sensitive_dedupe(self):
        rows = [self._row("2026-11-15", "K01", "3M", "4.5"),
                self._row("2026-11-15", "k01", "3M", "4.5")]
        kept, _lineage, _conflicts = mr.dedupe_rows(rows, case_sensitive=True)
        self.assertEqual(len(kept), 2)  # 大小写敏感：K01 != k01

    def test_case_insensitive_dedupe(self):
        rows = [self._row("2026-11-15", "K01", "3M", "4.5"),
                self._row("2026-11-15", "k01", "3M", "4.5")]
        kept, lineage, conflicts = mr.dedupe_rows(rows, case_sensitive=False)
        self.assertEqual(len(kept), 1)
        self.assertEqual(lineage[0]["dropped_rows"], [2])
        self.assertEqual(conflicts, [])

    def test_conflict_detail(self):
        rows = [self._row("2026-11-15", "K01", "3M", "4.5"),
                self._row("2026-11-15", "K01", "3M", "4.6")]
        kept, lineage, conflicts = mr.dedupe_rows(rows)
        self.assertEqual(len(kept), 1)
        self.assertEqual(conflicts[0]["fields"], ["value"])
        self.assertEqual(conflicts[0]["kept"], {"value": "4.5"})
        self.assertEqual(conflicts[0]["incoming"], {"value": "4.6"})
        self.assertEqual(lineage[0]["conflicts"], conflicts)


class TestCheckAllMetrics(unittest.TestCase):
    def test_fallback_covers_all(self):
        d = mr.load_dictionary()
        rep = mr.check_all_metrics(d)
        self.assertEqual(len(rep["metrics"]), len(d["metrics"]))
        self.assertEqual(rep["fallback_count"], len(d["metrics"]))
        self.assertEqual(rep["issues"], [])

    def test_measured_value_evaluated(self):
        d = mr.load_dictionary()
        rep = mr.check_all_metrics(d, measured={"A-01": 0.97})
        rec = next(r for r in rep["metrics"] if r["metric_id"] == "A-01")
        self.assertFalse(rec["fallback"])
        self.assertEqual(rec["status"], "ok")
        rep2 = mr.check_all_metrics(d, measured={"A-01": 0.5})
        rec2 = next(r for r in rep2["metrics"] if r["metric_id"] == "A-01")
        self.assertEqual(rec2["status"], "fail")
        self.assertIn("A-01", rep2["failures"])


class TestAdapters(unittest.TestCase):
    def test_md_table(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.md"
            p.write_text("| 指标 | 值 | 来源 |\n|---|---|---|\n| K01 | 4.5 | S1 |\n", encoding="utf-8")
            rows = mr.read_md_table(p)
            self.assertEqual(rows[0]["指标"], "K01")

    def test_xlsx(self):
        openpyxl = __import__("openpyxl")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.xlsx"
            wb = openpyxl.Workbook(); ws = wb.active
            ws.append(["指标", "值"]); ws.append(["K01", 4.5])
            wb.save(p)
            rows = mr.read_xlsx(p)
            self.assertEqual(rows[0]["指标"], "K01")

    def test_store_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "metrics.csv"
            rows = [{"date": "2026-11-15", "indicator_id": "K01", "value": "4.5", "unit": "%",
                     "caliber": "3M", "source_id": "S1", "status": "已核验"}]
            mr.write_store(rows, p)
            self.assertEqual(mr.read_store(p), rows)


if __name__ == "__main__":
    unittest.main()
