# -*- coding: utf-8 -*-
"""指标实测覆盖测试（METRIC-COVERAGE v1.0，批次 B）。

锁定：
- `metric_coverage.measure()` 覆盖字典全部 38 项，且 TOOL 指标全部为 measured / probe；
- 覆盖率报告把未接线项显式列为 gap（不静默跳过）；
- `metric_registry audit --coverage` 输出覆盖与缺口；
- 2026-11-19 二次校准口径：R-03 排除来源/链接段落、L-03 仅统计指标编号
  相邻阈值、A-03 真值核对只出候选差异不计分（见 tech-debt-ledger §十三）。
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mc = _load("metric_coverage", "engine/tools/metric_coverage.py")


class TestCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.meas = mc.measure()
        cls.rep = mc.coverage_report(cls.meas)

    def test_all_dictionary_metrics_present(self):
        dictionary = json.loads((TOOLS / "metrics-dictionary.json").read_text(encoding="utf-8"))
        ids = {m["metric_id"] for m in dictionary["metrics"]}
        self.assertEqual(set(self.meas), ids)

    def test_tool_metrics_are_measured_or_probe(self):
        dictionary = json.loads((TOOLS / "metrics-dictionary.json").read_text(encoding="utf-8"))
        tool_ids = {m["metric_id"] for m in dictionary["metrics"]
                    if m["detected_by"] == "TOOL"}
        bad = {mid for mid in tool_ids if self.meas[mid]["status"] not in ("measured", "probe")}
        self.assertEqual(bad, set(), f"TOOL 指标未接线：{bad}")

    def test_igi_values_match_info_gap(self):
        ig = _load("info_gap_metrics", "engine/tools/info_gap_metrics.py")
        vals = ig.compute()["values"]
        for mid, v in vals.items():
            self.assertAlmostEqual(self.meas[mid]["value"], v, places=4)

    def test_gaps_are_explicit(self):
        self.assertNotIn("A-05", self.rep["gaps"])  # 已接线（读定期落盘记录）
        self.assertTrue(all(self.meas[mid]["status"] in ("fallback", "probe")
                            for mid in self.rep["gaps"]))

    def test_a05_is_measured(self):
        if not mc.LINK_PROBE_PATH.exists():
            self.skipTest("link-probe.json 未落盘（scheduled-maintenance 尚未运行）")
        rec = self.meas["A-05"]
        self.assertEqual(rec["status"], "measured")
        probe = json.loads(mc.LINK_PROBE_PATH.read_text(encoding="utf-8"))
        self.assertAlmostEqual(
            rec["value"], round(probe["ok"] / (probe["ok"] + probe["dead"]), 4),
            places=4)

    def test_llm_metrics_are_not_faked(self):
        dictionary = json.loads((TOOLS / "metrics-dictionary.json").read_text(encoding="utf-8"))
        llm_ids = {m["metric_id"] for m in dictionary["metrics"] if m["detected_by"] == "LLM"}
        for mid in llm_ids:
            self.assertEqual(self.meas[mid]["status"], "llm")
            self.assertIsNone(self.meas[mid]["value"])

    def test_audit_coverage_cli(self):
        r = subprocess.run([sys.executable, "engine/tools/metric_registry.py",
                            "audit", "--coverage"], cwd=ROOT, capture_output=True, text=True)
        self.assertIn("[coverage]", r.stdout)
        # A-05 接线后无 fallback / probe 缺口；仅当存在缺口时才输出 [gap]
        self.assertEqual("[gap]" in r.stdout, bool(self.rep["gaps"]))


class TestA05LinkReachability(unittest.TestCase):
    """A-05 链接可达率接线：复用 link-probe.json，缺失 / 不可判显式 probe。"""

    def _write(self, tmp, content):
        p = Path(tmp) / "probe.json"
        p.write_text(content, encoding="utf-8")
        return p

    def test_reads_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, json.dumps({"probed": 275, "dead": 4,
                                              "unreachable": 90, "ok": 181}))
            value, detail = mc.a05_link_reachability(p)
            # 口径：ok / (ok + dead)，unreachable 不计入分母
            self.assertAlmostEqual(value, round(181 / 185, 4), places=4)
            self.assertIn("181/185", detail)

    def test_missing_record_is_probe(self):
        value, detail = mc.a05_link_reachability(Path("/nonexistent/link-probe.json"))
        self.assertIsNone(value)
        self.assertIn("缺失", detail)

    def test_zero_denominator_is_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, json.dumps({"probed": 0, "dead": 0,
                                              "unreachable": 0, "ok": 0}))
            value, _ = mc.a05_link_reachability(p)
            self.assertIsNone(value)

    def test_malformed_record_is_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, "not-json")
            value, _ = mc.a05_link_reachability(p)
            self.assertIsNone(value)

    def test_inconsistent_record_is_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, json.dumps({"probed": 10, "ok": 11}))
            value, _ = mc.a05_link_reachability(p)
            self.assertIsNone(value)


class TestA03NumericConsistency(unittest.TestCase):
    """A-03 数值一致率（相邻显式数值对代理，2026-11-19 校准）。"""

    def test_consistent_pairs(self):
        value, _ = mc.a03_numeric_consistency(
            {"a.html": "<p>P01 1,817 AED/sqft；另一处 P01 1,817</p>"})
        self.assertAlmostEqual(value, 1.0, places=4)

    def test_conflict_counts(self):
        value, detail = mc.a03_numeric_consistency(
            {"a.html": "<p>P01 1,817；P01 1,659</p>"})
        self.assertLess(value, 1.0)
        self.assertIn("冲突 1/1", detail)

    def test_false_positive_classes_excluded(self):
        # 区间上界 / 发布日 / 枚举 / 公司名 / 「编号 + 3M」不得被当作数值对
        text = "P01–P14 价格区间；P02 2026-10-12 发布；K02、K04、K06；G42 集团；K01 3M EIBOR"
        self.assertEqual(mc._VALUE_PAIR_RE.findall(text), [])

    def test_report_value_pair_extracted(self):
        text = "M02 4.394390% 定盘；P03 1,659 AED/sqft"
        pairs = {m.group(1): m.group(2) for m in mc._VALUE_PAIR_RE.finditer(text)}
        self.assertEqual(pairs.get("M02"), "4.394390")
        self.assertEqual(pairs.get("P03"), "1,659")


class TestI04FactCard(unittest.TestCase):
    """I-04 事实卡片引用率：分母 = 有卡片库业务线（字典口径对齐）。"""

    def test_shared_tokens_include_apartment(self):
        tokens = mc._shared_fact_tokens()
        self.assertIn("apartment", tokens)
        self.assertIn("security", tokens)

    def test_in_shared_by_path_segment(self):
        self.assertTrue(mc._in_shared_fact("content/economy/dubai/apartment", {"apartment"}))
        self.assertFalse(mc._in_shared_fact("content/other/topic", {"apartment"}))

    def test_denominator_excludes_non_shared(self):
        reports = {
            "content/economy/dubai/apartment/reports/a.html": "<p>[FC-APT-001]</p>",
            "content/other/topic/reports/b.html": "<p>无指针</p>",
        }
        value, detail = mc.i04_fact_card(reports)
        self.assertAlmostEqual(value, 1.0, places=4)
        self.assertIn("1/1", detail)

    def test_missing_ref_in_shared_is_counted(self):
        reports = {"content/economy/dubai/apartment/reports/a.html": "<p>无指针</p>"}
        value, detail = mc.i04_fact_card(reports)
        self.assertAlmostEqual(value, 0.0, places=4)
        self.assertIn("0/1", detail)


class TestR03DuplicateRate(unittest.TestCase):
    """R-03 跨主题重复率口径（2026-11-19 校准）：排除来源/链接段落。"""

    LINE_A = "content/tech/weekly-roundup"
    LINE_B = "content/economy/trends"

    def test_source_link_paragraph_excluded(self):
        body = "<p>来源：Gulf News https://www.gulfnews.com/dubai</p>"
        reports = {
            f"{self.LINE_A}/reports/a.html": body,
            f"{self.LINE_B}/reports/b.html": body,
        }
        value, detail = mc.r03_duplicate_rate(reports)
        self.assertEqual(value, 0.0)
        self.assertIn("重复 0/0", detail)

    def test_analytical_duplicate_counted(self):
        shared = "迪拜公寓市场在 2026 年延续供需两旺格局，价格与成交量同步上行。"
        only_a = "科技板块的竞争情报需要以季度频率更新，保持与行业节奏一致。"
        only_b = "经济趋势段落聚焦宏观指标，与科技板块的分析框架相互独立。"
        reports = {
            f"{self.LINE_A}/reports/a.html": f"<p>{shared}</p><p>{only_a}</p>",
            f"{self.LINE_B}/reports/b.html": f"<p>{shared}</p><p>{only_b}</p>",
        }
        value, detail = mc.r03_duplicate_rate(reports)
        # 共享段落被两条业务线各计一次重复：2 / 4
        self.assertAlmostEqual(value, 0.5, places=4)
        self.assertIn("重复 2/4", detail)

    def test_same_line_duplicate_not_cross_counted(self):
        para = "同一业务线内部的重复表述不计入跨主题重复率的分母与分子。"
        reports = {f"{self.LINE_A}/reports/a.html": f"<p>{para}</p><p>{para}</p>"}
        value, detail = mc.r03_duplicate_rate(reports)
        self.assertEqual(value, 0.0)
        self.assertIn("重复 0/1", detail)


class TestL03ThresholdConsistency(unittest.TestCase):
    """L-03 阈值一致率口径（2026-11-19 校准）：仅统计指标编号相邻阈值。"""

    def _scoped(self):
        """选一个 business-config 含阈值表达式且有报告的业务线，返回 (line, rel, tokens)。"""
        for b in mc.iter_business_dirs():
            cfg = b.path / "prompts" / "business-config.md"
            if not cfg.exists():
                continue
            toks = mc._thresh_tokens(mc._plain(mc._clean(
                cfg.read_text(encoding="utf-8", errors="replace"))))
            if not toks:
                continue
            reps = [r for r in mc.iter_reports() if r.business_line == b.rel]
            if reps:
                return b.rel, reps[0].rel, toks
        self.fail("无带阈值表达式且有报告的业务线")

    def test_id_adjacent_threshold_included(self):
        _, rel, toks = self._scoped()
        tok = sorted(toks)[0]
        value, detail = mc.l03_threshold_consistency({rel: f"<p>R06 {tok}</p>"})
        self.assertAlmostEqual(value, 1.0, places=4)
        self.assertIn("1/1", detail)

    def test_id_adjacent_threshold_miss(self):
        _, rel, toks = self._scoped()
        self.assertNotIn("≥9.99%", toks)
        value, detail = mc.l03_threshold_consistency({rel: "<p>R06 ≥9.99%</p>"})
        self.assertAlmostEqual(value, 0.0, places=4)
        self.assertIn("0/1", detail)

    def test_general_threshold_excluded_zero_denominator(self):
        _, rel, _ = self._scoped()
        value, detail = mc.l03_threshold_consistency({rel: "<p>本节共 ≥1 项指标</p>"})
        self.assertIsNone(value)
        self.assertIn("分母 0", detail)

    def test_mixed_denominator_excludes_general(self):
        _, rel, toks = self._scoped()
        tok = sorted(toks)[0]
        self.assertNotIn("≥9.99%", toks)
        filler = "本段为口径说明文字，用于拉开与指标编号的距离。" * 4
        reports = {rel: f"<p>R06 {tok}；R07 ≥9.99%。{filler}共 ≥1 项</p>"}
        value, detail = mc.l03_threshold_consistency(reports)
        self.assertAlmostEqual(value, 0.5, places=4)
        self.assertIn("1/2", detail)


class TestA03TruthCandidates(unittest.TestCase):
    """A-03 真值核对辅助函数（2026-11-19）：只出候选差异，不计分。"""

    REG = {"R06": ("21.4", "2026Q3"), "P01": ("1817", "2026-10")}

    def _patched(self):
        return mock.patch.object(mc, "_apartment_registry",
                                 return_value=(Path("fake.xlsx"), dict(self.REG)))

    def test_result_structure(self):
        with self._patched():
            res = mc.a03_truth_candidates({})
        self.assertEqual(set(res), {"registry", "compared", "same", "diff",
                                    "uncomparable", "diffs"})
        self.assertEqual(res["registry"], "fake.xlsx")
        self.assertEqual(res["compared"], res["same"] + res["diff"])
        self.assertEqual(res["diffs"], [])

    def test_same_diff_uncomparable_and_scope(self):
        reports = {
            "content/economy/dubai/apartment/reports/a.html": "<p>R06 21.4；P01 1,817</p>",
            "content/economy/dubai/apartment/reports/b.html": "<p>R06 20</p>",
            "content/economy/dubai/apartment/reports/c.html": "<p>Z99 5</p>",
            "content/tech/weekly-roundup/reports/d.html": "<p>R06 999</p>",
        }
        with self._patched():
            res = mc.a03_truth_candidates(reports)
        self.assertEqual(res["same"], 2)
        self.assertEqual(res["diff"], 1)
        self.assertEqual(res["uncomparable"], 1)
        self.assertEqual(res["compared"], 3)
        self.assertEqual(len(res["diffs"]), 1)
        d = res["diffs"][0]
        self.assertEqual(d["indicator"], "R06")
        self.assertEqual(d["report_value"], "20")
        self.assertEqual(d["registry_value"], "21.4")
        self.assertEqual(d["registry_period"], "2026Q3")
        self.assertIn("人工", d["note"])

    def test_truth_diff_does_not_change_a03_value(self):
        reports = {"content/economy/dubai/apartment/reports/a.html": "<p>R06 20%</p>"}
        with self._patched():
            res = mc.a03_truth_candidates(reports)
        self.assertEqual(res["diff"], 1)
        value, detail = mc.a03_numeric_consistency(reports)
        self.assertAlmostEqual(value, 1.0, places=4)
        self.assertIn("冲突 0/1", detail)

    def test_unreadable_registry(self):
        with mock.patch.object(mc, "_apartment_registry", return_value=(None, {})):
            res = mc.a03_truth_candidates({})
        self.assertEqual(res["error"], "登记册不可读")
        self.assertIsNone(res["registry"])
        self.assertEqual(res["compared"], 0)
        self.assertEqual(res["diffs"], [])

    def test_real_metric_value_stays_one(self):
        # 实测口径：真值候选存在差异时，A-03 代理值仍为 1.0（真值核对不计分）。
        value, detail = mc.a03_numeric_consistency(mc._reports_text())
        self.assertAlmostEqual(value, 1.0, places=4)
        self.assertIn("冲突 0/", detail)


if __name__ == "__main__":
    unittest.main()
