# -*- coding: utf-8 -*-
"""目标对齐 P0 增量测试（IGI 度量 / 滚动 gate-period / 语义门禁 / 词库漂移）。

锁定：
- `gate_period.resolve` 的滚动基线语义（auto = 当前自然月 + 1；显式周期原样；非法回落）；
- `info_gap_metrics.compute` 产出 IGI-01..08 且合成口径自洽；
- `info_density_check` ID-04 只对**结论性**推断/假设判定（提示块与 CSS 注释不误报）；
- `decision_hub_check` 剥离注释后判定（CSS 注释里的「决策卡」不再蒙混过关）；
- `vocab_drift_check` 三类检查可检出（区块不成对 / 空词库 / 规范形未命中）。
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "engine" / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # dataclass 类型解析需要模块已注册
    spec.loader.exec_module(mod)
    return mod


gate_period = _load("gate_period", "engine/tools/gate_period.py")
info_gap = _load("info_gap_metrics", "engine/tools/info_gap_metrics.py")
info_density = _load("info_density_check", "engine/tools/info_density_check.py")
decision_hub = _load("decision_hub_check", "engine/tools/decision_hub_check.py")
vocab_drift = _load("vocab_drift_check", "engine/tools/vocab_drift_check.py")
build_hub = _load("build_hub", "engine/tools/build_hub.py")
monitoring_render = _load("monitoring_render", "engine/tools/monitoring_render_check.py")
consistency = _load("consistency_check", "engine/tools/consistency_check.py")
naming = _load("naming_check", "engine/tools/naming_check.py")
prompt_consistency = _load("prompt_consistency", "engine/tools/prompt_consistency_check.py")


class TestGatePeriod(unittest.TestCase):
    def test_auto_is_next_month(self):
        self.assertEqual(gate_period.resolve("auto", today=date(2026, 11, 18)), "2026-12")
        self.assertEqual(gate_period.resolve("auto", today=date(2026, 12, 31)), "2027-01")

    def test_explicit_period_passthrough(self):
        for p in ("2026-12", "2026-Q3", "2026", "2026-11-13"):
            self.assertEqual(gate_period.resolve(p, today=date(2026, 11, 18)), p)

    def test_invalid_falls_back_to_rolling(self):
        """非法周期不得让门禁静默失效——回落滚动基线。"""
        self.assertEqual(gate_period.resolve("not-a-period", today=date(2026, 11, 18)), "2026-12")

    def test_none_is_auto(self):
        self.assertEqual(gate_period.resolve(None, today=date(2026, 11, 18)), "2026-12")


class TestInfoGapMetrics(unittest.TestCase):
    def test_compute_returns_eight_metrics(self):
        rep = info_gap.compute(today=date(2026, 11, 18))
        vals = rep["values"]
        for i in range(1, 9):
            self.assertIn(f"IGI-0{i}", vals)
            self.assertGreaterEqual(vals[f"IGI-0{i}"], 0.0)
            self.assertLessEqual(vals[f"IGI-0{i}"], 1.0)

    def test_synthetic_index_is_weighted_gap(self):
        rep = info_gap.compute(today=date(2026, 11, 18))
        vals = rep["values"]
        gap = sum(info_gap.WEIGHTS[m] * (1 - vals[m]) for m in info_gap.WEIGHTS)
        self.assertAlmostEqual(vals["IGI-08"], round(1 - gap, 4), places=4)

    def test_theme_coverage_reflects_actual_state(self):
        """实测口径：P1-9 四主题接入就绪化后，六主题均有业务线 → 6/6。"""
        v, detail = info_gap.igi_01_theme_coverage()
        self.assertEqual(v, round(6 / 6, 4))
        self.assertEqual(
            set(detail["covered"]),
            {"economy", "tech", "education", "international", "political", "society"},
        )


class TestInfoDensitySemantics(unittest.TestCase):
    _BASE = ('<h2 class="sec" id="s1">一、决策摘要</h2>{body}'
             '<h2 class="sec" id="s2">二、证据</h2>')

    def test_summary_inference_is_flagged(self):
        body = '<ol><li>判断 X。<span class="lvl lvl-inferred">推断</span> '
        body += '<span class="fact-ref">[FC-IND-001]</span></li></ol>'
        findings = dict(info_density.check_text(self._BASE.format(body=body)))
        self.assertIn("ID-04", findings)

    def test_note_block_and_lamp_are_not_flagged(self):
        """口径提示块与信号灯复用 lvl 类不算摘要越级（防误报）。"""
        body = ('<div class="note">当前信号灯为<span class="lvl lvl-assumption">预校准（ex-ante）</span>。</div>'
                '<ol><li>K13 <span class="lvl lvl-assumption">灰灯</span>。</li></ol>')
        findings = dict(info_density.check_text(self._BASE.format(body=body)))
        self.assertNotIn("ID-04", findings)

    def test_css_comment_does_not_trigger(self):
        """CSS 注释里的「决策卡」等字样不得参与判定。"""
        html = '<style>.lvl-inferred{color:red}/* 决策卡 */</style>' + self._BASE.format(body="<p>x</p>")
        findings = dict(info_density.check_text(html))
        self.assertNotIn("ID-04", findings)

    def test_summary_length_uses_or_not_and(self):
        body = "<p>" + "字" * 950 + "</p>"
        findings = dict(info_density.check_text(self._BASE.format(body=body)))
        self.assertIn("ID-02", findings)


class TestDecisionHubSemantics(unittest.TestCase):
    def test_css_comment_decision_card_does_not_pass(self):
        """trends 周报式陷阱：决策卡只写在 CSS 注释里 → 不得误判为通过。"""
        html = "<style>/* 决策卡 */</style><h2 class=\"sec\">一、本周要点</h2><p>正文</p>"
        findings = decision_hub.check_text(html, "economy/trends")
        # 剥离注释后「决策卡」不再存在 → DC-01 根本不应被触发
        self.assertEqual(findings, [])

    def test_per_card_field_check(self):
        good = ('<div class="decision-card"><div class="dc-grid">'
                '<div><span class="k">结论：</span>A</div>'
                '<div><span class="k">证据强度：</span>强</div>'
                '<div><span class="k">反向证据：</span>B</div></div></div>')
        bad = ('<div class="decision-card"><div class="dc-grid">'
               '<div><span class="k">结论：</span>A</div></div></div>')
        html_good = ('<h3>决策卡</h3>' + good + '<h3>决策卡</h3>' + bad)
        findings = dict(decision_hub.check_text(html_good, ""))
        self.assertIn("DC-01", findings)
        self.assertTrue(any("第 2 张决策卡" in m for m in findings.values()))


class TestHubBasePeriod(unittest.TestCase):
    """P0-5：hub 不得标注实际不存在的环比基期（算术虚构）。"""

    def _topic(self, reports):
        return build_hub.Topic(rel="content/x", region="", name="X", type_id="",
                               type_name="", reports=reports)

    def test_no_previous_period_is_not_a_base(self):
        t = self._topic([build_hub.ReportEntry("monthly", "2026-11", "p", "t")])
        self.assertFalse(build_hub.has_previous_period(
            t, build_hub.ReportEntry("monthly", "2026-11", "p", "t")))

    def test_same_cycle_previous_period_counts(self):
        t = self._topic([build_hub.ReportEntry("monthly", "2026-10", "p", "t"),
                         build_hub.ReportEntry("monthly", "2026-11", "p", "t")])
        self.assertTrue(build_hub.has_previous_period(
            t, build_hub.ReportEntry("monthly", "2026-11", "p", "t")))

    def test_other_cycle_does_not_count(self):
        """上一期必须同周期：2026-Q3 报告不能充当 2026-11 月报的环比基期。"""
        t = self._topic([build_hub.ReportEntry("quarterly", "2026-Q3", "p", "t")])
        self.assertFalse(build_hub.has_previous_period(
            t, build_hub.ReportEntry("monthly", "2026-11", "p", "t")))


class TestHubCardDistinguishability(unittest.TestCase):
    """P1-15：同周期并列的多份报告，仅凭卡片即可区分（标题 / 类型 / 地区）。"""

    def _topic(self):
        return build_hub.Topic(
            rel="content/tech/x/dubai", region="迪拜（阿联酋）", name="X",
            type_id="industry-research", type_name="行业深度研究型")

    def _group(self):
        return build_hub.CycleGroup(cycle="monthly", latest="2026-11",
                                    current=True)

    def test_card_carries_type_and_region(self):
        html = build_hub._render_card(
            self._group(),
            build_hub.ReportEntry("monthly", "2026-11", "p.html", "读数"),
            self._topic(), reader=False)
        self.assertIn("tag-type", html)
        self.assertIn("行业深度研究型", html)
        self.assertIn('data-region="迪拜（阿联酋）"', html)
        self.assertIn('data-type="industry-research"', html)

    def test_missing_title_falls_back_to_type_and_period(self):
        """标题缺失不再退化为纯期间（否则同期间卡片彼此不可区分）。"""
        html = build_hub._render_card(
            self._group(),
            build_hub.ReportEntry("monthly", "2026-11", "p.html", ""),
            self._topic(), reader=False)
        self.assertIn("行业研究 · 2026-11", html)

    def test_existing_title_is_preserved(self):
        html = build_hub._render_card(
            self._group(),
            build_hub.ReportEntry("monthly", "2026-11", "p.html", "阿联酋网安市场读数"),
            self._topic(), reader=False)
        self.assertIn("阿联酋网安市场读数", html)
        self.assertNotIn("行业研究 · 2026-11", html)

    def test_generated_hub_has_one_type_tag_per_card(self):
        text = (build_hub.ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(text.count('class="rcard"'), text.count('class="tag tag-type"'))


class TestTechDataLayerThin(unittest.TestCase):
    """P1-14：两条 tech 业务线数据层补薄——台账 + 量化数据 + 官方来源快照落 raw。"""

    LINES = {
        "content/tech/competitive-intelligence/dubai": {
            "processed": "data/processed/tech/competitive-intelligence/dubai",
            "registry": "ai_cyber_competition_registry.md",
            "quant": ["quant_model_layer_share.csv",
                      "quant_enterprise_ai_deploy_spend.csv"],
            "raw": "data/raw/tech/competitive-intelligence/dubai",
        },
        "content/tech/industry-research/dubai": {
            "processed": "data/processed/tech/industry-research/dubai",
            "registry": "ai_cybersecurity_indicator_registry.md",
            "quant": ["quant_ai_cyber_market_size.csv"],
            "raw": "data/raw/tech/industry-research/dubai",
        },
    }

    def _pdir(self, line):
        return ROOT / self.LINES[line]["processed"]

    def test_registry_declares_sources_and_raw_pointer(self):
        for line in self.LINES:
            text = (self._pdir(line) / self.LINES[line]["registry"]).read_text(encoding="utf-8")
            self.assertIn("| # |", text)
            self.assertIn("source_registry.json", text)
            self.assertIn("official_snapshot_manifest.json", text)

    def test_quant_csvs_are_rectangular(self):
        for line, spec in self.LINES.items():
            for name in spec["quant"]:
                with (self._pdir(line) / name).open(encoding="utf-8") as fh:
                    rows = list(csv.reader(fh))
                self.assertGreater(len(rows), 1, name)
                width = len(rows[0])
                for r in rows:
                    self.assertEqual(len(r), width, f"{name}: 列数不一致")

    def test_quant_source_ids_are_registered(self):
        for line, spec in self.LINES.items():
            reg = json.loads(
                (self._pdir(line) / "source_registry.json").read_text(encoding="utf-8"))
            known = {s["source_id"] for s in reg["sources"]}
            for name in spec["quant"]:
                text = (self._pdir(line) / name).read_text(encoding="utf-8")
                for sid in set(re.findall(r"\bS-\d{3}\b", text)):
                    self.assertIn(sid, known, f"{name}: {sid} 未登记")

    def test_raw_manifest_matches_tier1_sources(self):
        for line, spec in self.LINES.items():
            raw = ROOT / spec["raw"]
            man = json.loads(
                (raw / "official_snapshot_manifest.json").read_text(encoding="utf-8"))
            reg = json.loads(
                (self._pdir(line) / "source_registry.json").read_text(encoding="utf-8"))
            tier1 = {s["source_id"] for s in reg["sources"] if s["tier"] == 1}
            self.assertEqual({e["source_id"] for e in man["sources"]}, tier1)
            snaps = [e["snapshot"] for e in man["sources"] if e["snapshot"]]
            self.assertTrue(snaps, f"{line}: 无官方快照")
            for fname in snaps:
                body = (raw / fname).read_text(encoding="utf-8")
                self.assertIn("已核验摘录", body, fname)
            self.assertEqual(man["counts"]["snapshot"], len(snaps))
            self.assertEqual(man["counts"]["tier1_total"], len(man["sources"]))


class TestDeadCodeCleanup(unittest.TestCase):
    """P2-1 / C-15：规范外目录已撤销；存档与生成器按依据保留；文档漂移已修正。"""

    def test_followup_dir_removed_and_archived(self):
        self.assertFalse((ROOT / "content/economy/trends/followup").exists())
        self.assertTrue(
            (ROOT / "content/economy/trends/sources/archives"
             / "2026-11-13_followup-execution.md").is_file())

    def test_legacy_sources_kept(self):
        """存档目录有文档依据，不得当作规范外结构删除。"""
        self.assertTrue((ROOT / "content/tech/weekly-roundup/sources/legacy").is_dir())

    def test_registry_generator_kept(self):
        """v1 是 tracked xlsx 的生产者（v2 以其输出为输入），删除破坏可重放性。"""
        self.assertTrue(
            (ROOT / "content/economy/dubai/apartment/script/build_registry_v1.py").is_file())

    def test_docs_no_longer_claim_reports_legacy_exists(self):
        claims = {
            "content/tech/weekly-roundup/README.md":
                "历史报告与 md 源稿存于 `reports/legacy/`",
            "content/tech/weekly-roundup/operations-guide.md":
                "| 历史报告迁移 | `reports/legacy/{ai-security,ai-agent}/` |",
            "data/processed/tech/weekly-roundup/ai_trend_ledger.md":
                "历史版本见 `reports/legacy/{ai-security,ai-agent}/`",
        }
        for rel, stale in claims.items():
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn(stale, text, rel)
            self.assertIn("sources/legacy", text, rel)


class TestVocabDrift(unittest.TestCase):
    def test_pair_issue_detects_mismatch(self):
        """合成用例：BEGIN/END 数量不等必须可检出；当前仓库处于成对状态。"""
        self.assertIsNotNone(vocab_drift.pair_issue("<!-- VOCAB-SYNC:BEGIN topic=x -->"))
        self.assertIsNone(vocab_drift.pair_issue(
            "<!-- VOCAB-SYNC:BEGIN topic=x -->a<!-- VOCAB-SYNC:END -->"))
        self.assertEqual([r for r, _ in vocab_drift.check_sync_blocks()], [])

    def test_empty_theme_detected(self):
        """合成用例：空词库主题必须可检出 VD-02；当前仓库六主题均非空。"""
        import tempfile
        from pathlib import Path as P
        with tempfile.TemporaryDirectory() as d:
            (P(d) / "empty").mkdir()
            (P(d) / "empty" / "terms.md").write_text("", encoding="utf-8")
            orig_dir, orig_layout = vocab_drift.TERMS_DIR, vocab_drift.load_layout
            vocab_drift.TERMS_DIR = P(d)
            vocab_drift.load_layout = lambda: type("L", (), {"themes": {"empty": ("空主题", ())}})()
            try:
                findings = dict(vocab_drift.check_theme_terms())
            finally:
                vocab_drift.TERMS_DIR, vocab_drift.load_layout = orig_dir, orig_layout
            self.assertIn("VD-02", findings)

    def test_canonical_form_drift_detected(self):
        """P1-11 补录后仓库 VD-03 清零；检测逻辑用合成用例验证仍可检出。"""
        self.assertEqual([r for r, _ in vocab_drift.check_canonical_forms()], [])
        import tempfile
        from pathlib import Path as P
        with tempfile.TemporaryDirectory() as d:
            td = P(d) / "economy"
            td.mkdir()
            (td / "prompt-x.md").write_text(
                "术语一致：使用词库规范形（如「贷款市场报价利率」）。", encoding="utf-8")
            orig_dir, orig_load, orig_root = (vocab_drift.PROMPTS_DIR, vocab_drift.load_terms,
                                              vocab_drift.ROOT)
            vocab_drift.PROMPTS_DIR = P(d)
            vocab_drift.ROOT = P(d)
            vocab_drift.load_terms = lambda theme: (["消费者价格指数"], 1)
            try:
                rules = [r for r, _ in vocab_drift.check_canonical_forms()]
            finally:
                (vocab_drift.PROMPTS_DIR, vocab_drift.load_terms,
                 vocab_drift.ROOT) = orig_dir, orig_load, orig_root
            self.assertIn("VD-03", rules)

    def test_load_terms_counts_rows(self):
        forms, n = vocab_drift.load_terms("economy")
        self.assertGreater(n, 0)
        self.assertGreaterEqual(len(forms), n)


class TestMonitoringRender(unittest.TestCase):
    """批次 A：监测渲染规范机械项（MON-01..05）可检出，且不误报合规写法。"""

    def _check(self, html: str):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.html"
            p.write_text(html, encoding="utf-8")
            return monitoring_render.check_report(p)

    def test_compliant_report_is_clean(self):
        html = ('<div class="chart-box"><h3>图 1 · 序列（单位：%；来源：X）</h3>'
                '<div class="chart-eh" id="c1"></div>'
                '<div class="chart-note">口径并列，不可相减。来源：X。</div></div>'
                '<table class="fixed"><tr><th style="width:50%">A</th>'
                '<th style="width:50%">B</th></tr></table>')
        errs, warns = self._check(html)
        self.assertEqual(errs, [])
        self.assertEqual(warns, [])

    def test_mon01_missing_note(self):
        html = '<div class="chart-box"><div class="chart-eh" id="c1"></div></div>'
        _e, warns = self._check(html)
        self.assertTrue(any("MON-01" in w for w in warns))

    def test_mon02_caliber_without_warning(self):
        html = ('<div class="chart-box"><h3>图 1 · 多口径（%；来源：X）</h3>'
                '<div class="chart-eh" id="c1"></div>'
                '<div class="chart-note">口径并列，图示仅为对照。</div></div>')
        _e, warns = self._check(html)
        self.assertTrue(any("MON-02" in w for w in warns))

    def test_mon03_narrow_column(self):
        html = ('<table class="fixed"><tr>' + ''.join(
            f'<th style="width:1%">列{i}</th>' for i in range(7)) + '</tr></table>')
        _e, warns = self._check(html)
        self.assertTrue(any("MON-03" in w for w in warns))

    def test_mon04_missing_noopener(self):
        html = '<a href="https://example.com/x">x</a>'
        _e, warns = self._check(html)
        self.assertTrue(any("MON-04" in w for w in warns))

    def test_mon04_self_link_exempt(self):
        html = ('<a href="https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/x">x</a>')
        _e, warns = self._check(html)
        self.assertFalse(any("MON-04" in w for w in warns))

    def test_mon05_native_title(self):
        html = '<a href="https://example.com/x" title="https://example.com/x">x</a>'
        _e, warns = self._check(html)
        self.assertTrue(any("MON-05" in w for w in warns))


class TestConsistency(unittest.TestCase):
    """批次 A：看板-台账一致（LC）与版本治理（VG）。"""

    def test_ledger_rows_parse(self):
        text = ("## 一、数据看板追踪表\n\n"
                "| 板块 | 指标 | 上期值 | 本期值 | 来源 |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| 宏观 | 美国 CPI | +0.6% | +0.4% | BLS |\n")
        rows = consistency.parse_ledger_rows(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(consistency.metric_name(rows[0]), "美国 CPI")

    def test_vg01_missing_reading_time(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "2026-11_monthly.html"
            p.write_text("<html><body>无时点</body></html>", encoding="utf-8")
            warns = consistency.check_version(p, p.read_text(encoding="utf-8"))
        self.assertTrue(any("VG-01" in w for w in warns))

    def test_vg02_semver_requires_fixed_list(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "2026-11_monthly.html"
            p.write_text("读数时点 2026-11-13 ｜ 报告版本 v2.0", encoding="utf-8")
            warns = consistency.check_version(p, p.read_text(encoding="utf-8"))
        self.assertTrue(any("VG-02" in w for w in warns))

    def test_vg02_reading_time_identifier_not_semver(self):
        """vYYYY.MM.DD 为读数时点标识，不得被当作语义版本升级。"""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "2026-11_monthly.html"
            p.write_text("读数时点 2026-11-13 ｜ 报告版本 v2026.11.13", encoding="utf-8")
            warns = consistency.check_version(p, p.read_text(encoding="utf-8"))
        self.assertFalse(any("VG-02" in w for w in warns))

    def test_repo_is_consistent(self):
        """现行仓库：台账结构 / 指标名 / 读数时点均无告警。"""
        from _common import iter_business_dirs, iter_business_reports
        warns = []
        for b in iter_business_dirs():
            cfg = b.path / "prompts" / "business-config.md"
            text = cfg.read_text(encoding="utf-8") if cfg.exists() else ""
            warns += consistency.check_ledger(b, text)
            for r in iter_business_reports(b):
                warns += consistency.check_version(ROOT / r.rel,
                                                   (ROOT / r.rel).read_text(encoding="utf-8"))
        self.assertEqual(warns, [])


class TestNaming(unittest.TestCase):
    """批次 A：命名规范全量扫描（NC-01..02）。"""

    def test_repo_is_clean(self):
        self.assertEqual(naming.check_dirs() + naming.check_files(), [])

    def test_file_rule_detects_violations(self):
        self.assertIsNotNone(naming._check_file("engine/tools/BadName.py", "BadName.py"))
        self.assertIsNotNone(naming._check_file("engine/docs/Bad Name.md", "Bad Name.md"))
        self.assertIsNotNone(naming._check_file("content/x/reports/foo.html", "foo.html"))
        self.assertIsNone(naming._check_file("engine/tools/validate_layout.py", "validate_layout.py"))
        self.assertIsNone(naming._check_file("engine/docs/page-build-spec.md", "page-build-spec.md"))
        self.assertIsNone(naming._check_file("content/x/reports/2026-11_monthly.html", "2026-11_monthly.html"))


class TestPromptConsistency(unittest.TestCase):
    """批次 C（P1-10）：类型注册表一致 / business-config 去复述 / 周期模板齐备。"""

    def test_repo_is_consistent(self):
        self.assertEqual(
            prompt_consistency.pc01_registry()
            + prompt_consistency.pc02_restatement()
            + prompt_consistency.pc03_prompt_files(), [])

    def test_pc01_detects_unregistered(self):
        """合成用例：登记缺失 / 未登记双向可检出。"""
        import tempfile
        from pathlib import Path as P
        with tempfile.TemporaryDirectory() as d:
            reg = P(d) / "template-registry.md"
            reg.write_text("## 二、已注册类型清单\n"
                           "| foo-type | x | y | z | content/a；content/b |\n", encoding="utf-8")
            orig = prompt_consistency.REGISTRY
            prompt_consistency.REGISTRY = reg
            try:
                warns = prompt_consistency.pc01_registry()
            finally:
                prompt_consistency.REGISTRY = orig
            self.assertTrue(any("不存在" in w for w in warns))
            self.assertTrue(any("未登记" in w for w in warns))


if __name__ == "__main__":
    unittest.main()
