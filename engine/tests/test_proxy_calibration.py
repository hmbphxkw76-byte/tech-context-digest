# -*- coding: utf-8 -*-
"""代理指标抽样校准测试（PROXY-CALIBRATION v1.0，方案 T-02）。

锁定：
- `metrics-dictionary.json` 中代理指标均带 `calibration` 备注（只加备注，不改阈值）；
- IGI-05 / A-01 的 unit 抽取与 `info_gap_metrics` 实测**同口径**（数量与正例一致）；
- 分层抽样（主题 / 业务线 / 断言类型）确定性可重放，且比例分配 + 薄层覆盖；
- 混淆矩阵 TP/FP/FN/TN 与 precision / recall / F1 计算正确，分母 0 不静默给 0；
- truth 未填齐时不产出 precision / recall（不编造校准数值）；
- 记录含口径版本 + 样本数 + 日期，同 (metric, n, seed, date) 字节可重放。
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
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))

_spec = importlib.util.spec_from_file_location("proxy_calibration", TOOLS / "proxy_calibration.py")
pc = importlib.util.module_from_spec(_spec)
sys.modules["proxy_calibration"] = pc
_spec.loader.exec_module(pc)

DICT_PATH = TOOLS / "metrics-dictionary.json"


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _unit(uid: str, theme: str = "tech", bl: str = "content/tech/x",
          bt: str = "li", verdict: bool = True, truth: bool | None = None) -> dict:
    return {"uid": uid, "report": f"{bl}/reports/r.html", "theme": theme,
            "business_line": bl, "block_type": bt, "proxy_verdict": verdict,
            "detail": "d", "truth": truth}


def _dictionary() -> dict:
    return json.loads(DICT_PATH.read_text(encoding="utf-8"))


class TestProxyRegistry(unittest.TestCase):
    """代理指标清单与字典备注（验收：字典中代理指标均带 calibration 备注）。"""

    def test_every_listed_proxy_has_calibration_note(self):
        ids = {m["metric_id"]: m for m in _dictionary()["metrics"]}
        for mid in pc.PROXY_METRICS:
            self.assertIn(mid, ids, f"代理清单 {mid} 不在字典")
            self.assertTrue(str(ids[mid].get("calibration", "")).strip(),
                            f"{mid} 缺 calibration 备注")

    def test_every_dict_proxy_note_is_listed(self):
        # 反向：字典 note 含「代理」的指标必须登记进 PROXY_METRICS（避免漏标）
        noted = {m["metric_id"] for m in _dictionary()["metrics"]
                 if "代理" in str(m.get("note", "")) or "代理" in str(m.get("formula", ""))}
        self.assertEqual(noted - set(pc.PROXY_METRICS), set(),
                         f"字典标代理但未登记校准清单：{sorted(noted - set(pc.PROXY_METRICS))}")

    def test_wired_targets_are_proxy(self):
        self.assertTrue(set(pc.WIRED_TARGETS) <= set(pc.PROXY_METRICS))
        self.assertIn("IGI-05", pc.WIRED_TARGETS)

    def test_proxy_metrics_follow_dictionary_order(self):
        order = [m["metric_id"] for m in _dictionary()["metrics"]]
        self.assertEqual(pc.proxy_metrics(_dictionary()),
                         [m for m in order if m in set(pc.PROXY_METRICS)])

    def test_list_cli(self):
        r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py", "--list"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("IGI-05", r.stdout)
        self.assertIn("已接线", r.stdout)
        self.assertIn("待接线", r.stdout)

    def test_unknown_metric_rejected(self):
        r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                            "--metric", "NOPE-99"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("不伪造", r.stderr)

    def test_unwired_target_reports_not_wired(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                                "--metric", "L-03", "--n", "5",
                                "--records-dir", str(Path(tmp))],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("待接线", r.stderr)


class TestAssertionUnits(unittest.TestCase):
    """IGI-05 / A-01 unit 抽取与 info_gap_metrics 同口径（不得另写一套口径）。"""

    def test_matches_info_gap_stats_on_real_reports(self):
        ig = _load("info_gap_metrics", "engine/tools/info_gap_metrics.py")
        from _common import iter_reports
        n_num = n_src = 0
        checked = 0
        for ref in iter_reports():
            if ref.category != "report":
                continue
            text = (ROOT / ref.rel).read_text(encoding="utf-8", errors="replace")
            a, b = ig._assertion_stats(text)
            units = pc.iter_assertion_units(text, ref.rel)
            self.assertEqual(len(units), a, f"{ref.rel} 断言块数不一致")
            self.assertEqual(sum(1 for u in units if u["proxy_verdict"]), b,
                             f"{ref.rel} 带指针断言数不一致")
            n_num += a
            n_src += b
            checked += 1
        self.assertGreater(checked, 0, "无正式报告可校验")
        self.assertGreater(n_num, 0)
        self.assertEqual(pc._ratio(n_src, n_num), round(n_src / n_num, 4))

    def test_meta_and_nondigit_excluded(self):
        html = ("<p>2026 年报告版本说明</p>"                 # 非断言块（版本）
                "<p>本节无数字</p>"                          # 无数字
                "<li>2026 年 1,817 AED/sqft 来源：Savills</li>")
        units = pc.iter_assertion_units(html, "content/tech/x/reports/a.html")
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0]["block_type"], "li")
        self.assertTrue(units[0]["proxy_verdict"])

    def test_block_type_classification(self):
        html = ('<li>1</li><p>2</p><div class="kpi">3</div>'
                '<div class="stat-strip">4</div>')
        self.assertEqual([u["block_type"] for u in pc.iter_assertion_units(html, "r.html")],
                         ["li", "p", "kpi", "stat-strip"])

    def test_value_pair_units(self):
        text = "<p>P01 1,817；P01 1,659；P02 3.5；G42 集团</p>"
        units = pc.iter_value_pair_units(text, "r.html")
        self.assertEqual(len(units), 2)          # G42 不构成数值对
        self.assertFalse(next(u for u in units if "P01" in u["detail"])["proxy_verdict"])
        self.assertTrue(next(u for u in units if "P02" in u["detail"])["proxy_verdict"])

    def test_uid_stable(self):
        self.assertEqual(pc._uid("a", "b"), pc._uid("a", "b"))
        self.assertNotEqual(pc._uid("a", "b"), pc._uid("a", "c"))


class TestStratifiedSample(unittest.TestCase):
    """分层抽样：确定性 + 比例分配 + 薄层覆盖。"""

    @staticmethod
    def _corpus(sizes: dict[tuple[str, str, str], int]) -> list[dict]:
        out = []
        for (theme, bl, bt), n in sizes.items():
            for i in range(n):
                out.append(_unit(pc._uid(theme, bl, bt, str(i)), theme, bl, bt))
        return out

    def test_deterministic_replay(self):
        units = self._corpus({("tech", "content/tech/a", "li"): 40,
                              ("economy", "content/economy/b", "p"): 20})
        a, sa = pc.stratified_sample(units, 12, seed=7, metric_id="IGI-05")
        b, sb = pc.stratified_sample(units, 12, seed=7, metric_id="IGI-05")
        self.assertEqual([u["uid"] for u in a], [u["uid"] for u in b])
        self.assertEqual(sa, sb)
        # 不同种子 → 不同抽样（概率极高，断言至少一条不同）
        c, _ = pc.stratified_sample(units, 12, seed=8, metric_id="IGI-05")
        self.assertNotEqual([u["uid"] for u in a], [u["uid"] for u in c])

    def test_proportional_allocation(self):
        units = self._corpus({("tech", "content/tech/a", "li"): 30,
                              ("economy", "content/economy/b", "p"): 10})
        sample, sampling = pc.stratified_sample(units, 8)
        self.assertEqual(len(sample), 8)
        self.assertEqual(sampling["allocated"],
                         {"economy|content/economy/b|p": 2, "tech|content/tech/a|li": 6})

    def test_thin_stratum_coverage(self):
        units = self._corpus({("a", "content/a", "li"): 100,
                              ("b", "content/b", "li"): 1,
                              ("c", "content/c", "li"): 1,
                              ("d", "content/d", "li"): 1,
                              ("e", "content/e", "li"): 1})
        sample, _ = pc.stratified_sample(units, 5)
        themes = {u["theme"] for u in sample}
        self.assertEqual(themes, {"a", "b", "c", "d", "e"})

    def test_n_ge_total_returns_all_truncated(self):
        units = self._corpus({("tech", "content/tech/a", "li"): 3})
        sample, sampling = pc.stratified_sample(units, 10)
        self.assertEqual(len(sample), 3)
        self.assertTrue(sampling["truncated"])

    def test_invalid_n(self):
        with self.assertRaises(ValueError):
            pc.stratified_sample([], 0)


class TestConfusion(unittest.TestCase):
    """混淆矩阵与派生指标。"""

    def test_hand_computed(self):
        units = [
            _unit("1", verdict=True, truth=True),    # TP
            _unit("2", verdict=True, truth=True),    # TP
            _unit("3", verdict=True, truth=False),   # FP
            _unit("4", verdict=False, truth=True),   # FN
            _unit("5", verdict=False, truth=False),  # TN
            _unit("6", verdict=False, truth=False),  # TN
            _unit("7", verdict=True, truth=None),    # pending
        ]
        res = pc.confusion(units)
        self.assertEqual((res["tp"], res["fp"], res["fn"], res["tn"]), (2, 1, 1, 2))
        self.assertEqual(res["n"], 6)
        self.assertEqual(res["pending"], 1)
        self.assertAlmostEqual(res["precision"], 0.6667, places=4)
        self.assertAlmostEqual(res["recall"], 0.6667, places=4)
        self.assertAlmostEqual(res["f1"], 0.6667, places=4)
        self.assertAlmostEqual(res["agreement"], 0.6667, places=4)

    def test_zero_denominators_are_none(self):
        res = pc.confusion([_unit("1", verdict=False, truth=True),
                            _unit("2", verdict=False, truth=True)])
        self.assertIsNone(res["precision"])     # TP+FP = 0
        self.assertAlmostEqual(res["recall"], 0.0, places=4)
        self.assertIsNone(res["f1"])

    def test_zero_precision_and_recall_gives_zero_f1(self):
        res = pc.confusion([_unit("1", verdict=True, truth=False),
                            _unit("2", verdict=False, truth=True)])
        self.assertAlmostEqual(res["precision"], 0.0, places=4)
        self.assertAlmostEqual(res["recall"], 0.0, places=4)
        self.assertAlmostEqual(res["f1"], 0.0, places=4)

    def test_perfect(self):
        res = pc.confusion([_unit("1", verdict=True, truth=True),
                            _unit("2", verdict=False, truth=False)])
        self.assertEqual((res["precision"], res["recall"], res["f1"]), (1.0, 1.0, 1.0))


class TestRecordAndWorkflow(unittest.TestCase):
    """记录 schema、可重放与「无人工核验不产出指标」。"""

    def test_record_fields(self):
        units = [_unit("1"), _unit("2")]
        sample = {"requested_n": 2, "total": 2, "truncated": True, "allocated": {},
                  "seed": pc.DEFAULT_SEED}
        rec = pc.build_record("IGI-05", units, sample, "2026-11-19")
        self.assertEqual(rec["caliber_version"], pc.CALIBER_VERSION)
        self.assertEqual(rec["sample_size"], 2)
        self.assertEqual(rec["date"], "2026-11-19")
        self.assertEqual(rec["pending_truth"], 2)
        self.assertIsNone(rec["result"])

    def test_emit_replay_byte_identical(self):
        units = [_unit(pc._uid("tech", "content/tech/a", "li", str(i))) for i in range(10)]
        sample = {"requested_n": 10, "total": 10, "truncated": True, "allocated": {},
                  "seed": pc.DEFAULT_SEED}
        rec = pc.build_record("IGI-05", units, sample, "2026-11-19")
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            p1 = pc.write_record(rec, Path(t1))
            p2 = pc.write_record(rec, Path(t2))
            self.assertEqual(p1.read_bytes(), p2.read_bytes())
            self.assertEqual(p1.read_text(encoding="utf-8"), pc.render_record(rec))

    def test_score_without_truth_yields_no_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                                "--metric", "IGI-05", "--n", "5", "--date", "2026-11-19",
                                "--records-dir", str(Path(tmp)), "--emit"],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            sheet = json.loads((Path(tmp) / "IGI-05.json").read_text(encoding="utf-8"))
            self.assertEqual(sheet["pending_truth"], 5)
            self.assertIsNone(sheet["result"])
            # 未填 truth 直接 score：仍不产出 precision / recall
            r2 = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                                 "--metric", "IGI-05", "--score",
                                 "--records-dir", str(Path(tmp))],
                                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertIn("待人工核验", r2.stdout)
            self.assertNotIn("precision=", r2.stdout)

    def test_score_with_truth_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                                "--metric", "IGI-05", "--n", "6", "--date", "2026-11-19",
                                "--records-dir", str(Path(tmp)), "--emit"],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            sheet = json.loads((Path(tmp) / "IGI-05.json").read_text(encoding="utf-8"))
            truth = {u["uid"]: (i % 2 == 0) for i, u in enumerate(sheet["units"])}
            tpath = Path(tmp) / "truth.json"
            tpath.write_text(json.dumps(truth), encoding="utf-8")
            r2 = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                                 "--metric", "IGI-05", "--score",
                                 "--records-dir", str(Path(tmp)),
                                 "--truth", str(tpath), "--emit"],
                                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertIn("precision=", r2.stdout)
            scored = json.loads((Path(tmp) / "IGI-05.json").read_text(encoding="utf-8"))
            self.assertEqual(scored["pending_truth"], 0)
            res = scored["result"]
            self.assertEqual(res["n"], 6)
            self.assertEqual(res["tp"] + res["fp"] + res["fn"] + res["tn"], 6)
            # 与纯函数重算一致
            self.assertEqual(res, pc.confusion(scored["units"]))

    def test_score_all_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            units = [_unit("1"), _unit("2", verdict=False)]
            sample = {"requested_n": 2, "total": 2, "truncated": True, "allocated": {},
                      "seed": pc.DEFAULT_SEED}
            rec = pc.build_record("IGI-05", units, sample, "2026-11-19")
            pc.write_record(rec, Path(tmp))
            tpath = Path(tmp) / "truth.json"
            tpath.write_text(json.dumps({"all": True}), encoding="utf-8")
            r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py",
                                "--metric", "IGI-05", "--score",
                                "--records-dir", str(Path(tmp)), "--truth", str(tpath)],
                               cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            # u1 代理 True / 真值 True → TP；u2 代理 False / 真值 True → FN
            self.assertIn("TP=1 FP=0 FN=1 TN=0", r.stdout)
            self.assertIn("precision=1.0", r.stdout)
            self.assertIn("recall=0.5", r.stdout)

    def test_load_truth_forms(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "t.json"
            p.write_text(json.dumps({"a": True, "b": False}), encoding="utf-8")
            self.assertEqual(pc.load_truth(p), {"a": True, "b": False})
            p.write_text(json.dumps({"all": True}), encoding="utf-8")
            self.assertEqual(pc.load_truth(p), {"__all__": True})
            p.write_text(json.dumps({"units": [{"uid": "a", "truth": True},
                                                {"uid": "b", "truth": None}]}),
                         encoding="utf-8")
            self.assertEqual(pc.load_truth(p), {"a": True})

    def test_export_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = pc.export_csv([_unit("u1", verdict=True, truth=None)], Path(tmp) / "s.csv")
            text = p.read_text(encoding="utf-8")
            self.assertIn("proxy_verdict", text)
            self.assertIn("u1", text)

    def test_cli_help(self):
        r = subprocess.run([sys.executable, "engine/tools/proxy_calibration.py", "--help"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("--emit", r.stdout)
        self.assertIn("--score", r.stdout)


if __name__ == "__main__":
    unittest.main()
