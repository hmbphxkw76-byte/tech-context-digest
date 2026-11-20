# -*- coding: utf-8 -*-
"""指标实测覆盖测试（METRIC-COVERAGE v1.0，批次 B）。

锁定：
- `metric_coverage.measure()` 覆盖字典全部 41 项，且 TOOL 指标全部为 measured / probe；
- 覆盖率报告把未接线项显式列为 gap（不静默跳过）；
- `metric_registry audit --coverage` 输出覆盖与缺口；
- 2026-11-19 口径：R-03 排除来源/链接段落；L-03 升级为报告 ↔ business-config ↔
  登记册三处一致（排除有意泛化）；A-03 计分改为真值核对一致率与代理一致率组合；
  A-02 / A-04 / L-01 / L-02 / L-04 / L-05 / R-05 由 LLM 兜底转为机械代理（均为代理
  口径，不得当作语义达标）。
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
isc = _load("indicator_sidecar", "engine/tools/indicator_sidecar.py")


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


class TestIndicatorSidecar(unittest.TestCase):
    """indicator_latest.json sidecar：确定性可重放、字段固定、主表优先。"""

    def test_build_deterministic_and_byte_replay(self):
        self.assertEqual(isc.build(), isc.build())
        with tempfile.TemporaryDirectory() as tmp:
            p1 = Path(tmp) / "a.json"
            p2 = Path(tmp) / "b.json"
            isc.write(isc.build(), p1)
            isc.write(isc.build(), p2)
            self.assertEqual(p1.read_bytes(), p2.read_bytes())

    def test_fields_and_order(self):
        sidecar = isc.build()
        ids = [r["indicator_id"] for r in sidecar["indicators"]]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(sidecar["count"], len(ids))
        for r in sidecar["indicators"]:
            self.assertEqual(set(r), set(isc.FIELDS))

    def test_primary_sheet_precedence(self):
        # 年度基线2027 为主表：P05 取「168.1 / 218.6」；首期基线值仅补缺（S13）
        reg = {r["indicator_id"]: r for r in isc.build()["indicators"]}
        self.assertEqual(reg["P05"]["value"], "168.1 / 218.6")
        self.assertIn("S13", reg)
        self.assertEqual(reg["P05"]["updated"], "2027-01")

    def test_on_disk_matches_build(self):
        if not isc.SIDECAR_PATH.exists():
            self.skipTest("sidecar 未落盘")
        self.assertEqual(isc.load(isc.SIDECAR_PATH), isc.build())


class TestA03TruthCheck(unittest.TestCase):
    """A-03 真值核对（sidecar 版）：一致 / 差异 / 不可比。"""

    ROWS = [
        {"indicator_id": "P01", "value": "1,817", "unit": "AED/sqft",
         "period": "2026Q3", "source": "Savills", "updated": "2027-01"},
        {"indicator_id": "P05", "value": "168.1 / 218.6", "unit": "点",
         "period": "2026Q3", "source": "ValuStrat", "updated": "2027-01"},
        {"indicator_id": "M05", "value": "3.75–4.00", "unit": "%",
         "period": "2026-10-28", "source": "Federal Reserve", "updated": "2027-01"},
        {"indicator_id": "S05", "value": ">525,000", "unit": "套",
         "period": "2027–2030", "source": "Savills", "updated": "2027-01"},
    ]

    def _sidecar(self, tmp, rows):
        p = Path(tmp) / "sidecar.json"
        p.write_text(json.dumps({"indicators": rows}, ensure_ascii=False), encoding="utf-8")
        return p

    def test_verdicts(self):
        reports = {"content/economy/dubai/apartment/reports/a.html":
                   "<p>P01 1,817；P01 1,659；P05 218.6；M05 3.9；S05 600,000；Z99 5</p>"}
        with tempfile.TemporaryDirectory() as tmp:
            res = mc.a03_truth_check(reports, self._sidecar(tmp, self.ROWS))
        self.assertEqual(res["same"], 3)            # P01 / P05 / M05
        self.assertEqual(res["diff"], 1)            # P01 1,659
        self.assertEqual(res["uncomparable"], 2)    # S05 不等式 / Z99 未登记
        self.assertEqual(res["compared"], 4)
        by = {(r["indicator"], r["report_value"]): r["verdict"] for r in res["records"]}
        self.assertEqual(by[("P01", "1,817")], "一致")
        self.assertEqual(by[("P01", "1,659")], "差异")
        self.assertEqual(by[("P05", "218.6")], "一致")
        self.assertEqual(by[("M05", "3.9")], "一致")
        self.assertEqual(by[("S05", "600,000")], "不可比")
        self.assertEqual(by[("Z99", "5")], "不可比")

    def test_range_outside_is_diff(self):
        rows = [{"indicator_id": "M05", "value": "3.75–4.00", "unit": "%",
                 "period": "2026-10-28", "source": "Federal Reserve", "updated": "2027-01"}]
        reports = {"content/economy/dubai/apartment/reports/a.html": "<p>M05 4.5</p>"}
        with tempfile.TemporaryDirectory() as tmp:
            res = mc.a03_truth_check(reports, self._sidecar(tmp, rows))
        self.assertEqual(res["diff"], 1)
        self.assertEqual(res["records"][0]["verdict"], "差异")

    def test_missing_sidecar(self):
        res = mc.a03_truth_check({}, Path("/nonexistent/sidecar.json"))
        self.assertIn("缺失", res["error"])
        self.assertEqual(res["compared"], 0)

    def test_value_kind_parser(self):
        self.assertEqual(mc._sidecar_value_kind("1,817")[0], "single")
        self.assertEqual(mc._sidecar_value_kind("−1.7")[0], "single")
        self.assertEqual(mc._sidecar_value_kind("168.1 / 218.6")[0], "multi")
        self.assertEqual(mc._sidecar_value_kind("3.75–4.00")[0], "range")
        self.assertEqual(mc._sidecar_value_kind("60,000–162,500")[0], "range")
        self.assertEqual(mc._sidecar_value_kind(">525,000")[0], "qualified")
        self.assertEqual(mc._sidecar_value_kind("≈3.9")[0], "qualified")
        self.assertEqual(mc._sidecar_value_kind("现行")[0], "nonnumeric")
        self.assertEqual(mc._sidecar_value_kind("")[0], "empty")

    def test_report_number_parser(self):
        self.assertEqual(mc._report_number("1,817"), 1817.0)
        self.assertEqual(mc._report_number("−1.7"), -1.7)
        self.assertIsNone(mc._report_number("abc"))

    def test_real_registry_loads(self):
        if not mc.TRUTH_REGISTRY_PATH.exists():
            self.skipTest("结构化登记册未落盘")
        res = mc.a03_truth_check(mc._reports_text())
        self.assertGreater(res["compared"], 0)
        self.assertTrue(all(r["verdict"] in ("一致", "差异", "不可比")
                            for r in res["records"]))
        # 辅助不计分：A-03 代理值不受真值核对影响
        value, _ = mc.a03_numeric_consistency(mc._reports_text())
        self.assertAlmostEqual(value, 1.0, places=4)


class TestN6MechanicalProxies(unittest.TestCase):
    """N-6：七项 LLM 兜底接线为机械代理（2026-11-19），均为代理口径。"""

    def test_a02_entry_grading(self):
        text = '<a href="https://news.example/x">n</a> 需核实原文'
        self.assertTrue(mc._a02_entry_compliant(
            text, {"url": "https://news.example/x", "tier": 4}))
        self.assertFalse(mc._a02_entry_compliant(
            '<a href="https://news.example/x">n</a>',
            {"url": "https://news.example/x", "tier": 4}))
        self.assertTrue(mc._a02_entry_compliant(
            "anything", {"url": "https://x.example/a", "tier": 1}))

    def test_a04_entry_window(self):
        # 月度容差 1：同期 / 上月合规，前两月不合规；无周期不可判
        self.assertTrue(mc._a04_entry_fresh("2026-12", "monthly", "2026-12-01"))
        self.assertTrue(mc._a04_entry_fresh("2026-12", "monthly", "2026-11-01"))
        self.assertFalse(mc._a04_entry_fresh("2026-12", "monthly", "2026-10-01"))
        self.assertIsNone(mc._a04_entry_fresh("", "monthly", "2026-12-01"))

    def test_l01_cross_section_conflict(self):
        reports = {"a.html": ('<h2 class="sec">一</h2><p> P01 1,817</p>'
                              '<h2 class="sec">二</h2><p> P01 1,659</p>')}
        value, detail = mc.l01_cross_section(reports)
        self.assertLess(value, 1.0)
        self.assertIn("冲突 1/1", detail)

    def test_l02_conflation_detected(self):
        self.assertTrue(mc._has_caliber_conflation("均价 = 中位价", ["均价", "中位价"]))
        self.assertTrue(mc._has_caliber_conflation("均价折算为中位价", ["均价", "中位价"]))
        self.assertFalse(mc._has_caliber_conflation("均价与中位价分列", ["均价", "中位价"]))

    def test_l04_conclusion_evidence(self):
        card_ok = ('<div class="decision-card"><div class="dc-grid">'
                   '<div><span class="k">结论：</span>x</div>'
                   '<div><span class="k">证据强度：</span>强（官方）</div></div></div>')
        card_bad = ('<div class="decision-card"><div class="dc-grid">'
                    '<div><span class="k">结论：</span>x</div>'
                    '<div><span class="k">证据强度：</span></div></div></div>')
        value, detail = mc.l04_conclusion_evidence({"a.html": card_ok + card_bad})
        self.assertAlmostEqual(value, 0.5, places=4)
        self.assertIn("1/2", detail)

    def test_l05_year_wrap_and_order(self):
        items = ["11-18", "12-30", "2027-01"]
        dates = mc._parse_timeline_dates(items, "2027-01")
        self.assertEqual(dates, [(2026, 11, 18), (2026, 12, 30), (2027, 1, 0)])
        html = "".join(f'<div class="tl-item"><div class="tl-date">{d}</div></div>'
                       for d in items)
        value, _ = mc.l05_timeline_consistency({"2027-01_monthly.html": html})
        self.assertAlmostEqual(value, 1.0, places=4)

    def test_r05_topic_tokens(self):
        self.assertEqual(mc._topic_tokens("{{TOPIC}} = 公寓住宅市场"), ["公寓住宅市场"])
        self.assertEqual(mc._topic_tokens("{{TOPIC}} = AI 网安竞争格局"),
                         ["AI", "网安竞争格局"])

    def test_l03_generalized_excluded_and_real_value(self):
        value, detail = mc.l03_threshold_consistency(mc._reports_text())
        self.assertAlmostEqual(value, 1.0, places=4)
        self.assertIn("有意泛化", detail)

    def test_a03_combined_uses_truth(self):
        value, detail = mc.a03_combined(mc._reports_text())
        self.assertIn("真值核对", detail)
        self.assertGreater(value, 0.0)
        # 阈值语境排除后，可比项真值一致 → 组合值应达阈值（≥0.99）。
        self.assertGreaterEqual(value, 0.99)

    def test_a03_fallback_when_no_comparable(self):
        # 无 apartment 报告 → 真值可比 0，回退代理并显式标注
        value, detail = mc.a03_combined({"x.html": "<p>P01 1</p>"})
        self.assertIn("回退代理", detail)
        self.assertAlmostEqual(value, 1.0, places=4)


class TestConsumerMetricsCoverage(unittest.TestCase):
    """CF-01…CF-03 消费侧接线（2026-11-20）。"""

    def test_cf01_counts_registry_card_references(self):
        value, detail = mc.cf01_card_references(mc._reports_text())
        self.assertIsNotNone(value)
        self.assertGreater(value, 0.0)
        self.assertIn("登记册决策卡", detail)

    def test_cf01_probe_without_registry(self):
        with mock.patch.object(mc, "_decision_card_ids", return_value=set()):
            value, detail = mc.cf01_card_references({})
        self.assertIsNone(value)
        self.assertIn("probe", detail)

    def test_cf02_honest_zero(self):
        value, detail = mc.cf02_corrections()
        self.assertEqual(value, 0.0)
        self.assertIn("如实呈现", detail)

    def test_cf03_zero_when_no_revisit(self):
        reports = mc._reports_text()
        value, detail = mc.cf03_revisit_rate(reports)
        self.assertEqual(value, 0.0)
        self.assertIn(f"0/{len(reports)}", detail)

    def test_cf03_probe_without_reports(self):
        value, detail = mc.cf03_revisit_rate({})
        self.assertIsNone(value)
        self.assertIn("probe", detail)

    def test_cf_metrics_in_measure(self):
        meas = mc.measure()
        for mid in ("CF-01", "CF-02", "CF-03"):
            self.assertEqual(meas[mid]["status"], "measured")


if __name__ == "__main__":
    unittest.main()
