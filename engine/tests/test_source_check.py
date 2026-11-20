# -*- coding: utf-8 -*-
"""来源登记前置校验（source_check.py / T1）单元测试。"""
from __future__ import annotations

import importlib.util
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "engine" / "tools" / "source_check.py"

spec = importlib.util.spec_from_file_location("source_check", TOOL)
source_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source_check)


def _reg(*sources):
    return {"schema_version": "1.0", "sources": list(sources)}


class TestNormalizeUrl(unittest.TestCase):
    def test_trailing_slash_and_case(self):
        self.assertEqual(source_check.normalize_url("HTTPS://IMF.org/a/"),
                         "https://imf.org/a")

    def test_fragment_removed(self):
        self.assertEqual(source_check.normalize_url("https://imf.org/a#x"),
                         "https://imf.org/a")

    def test_path_case_is_preserved(self):
        """path 区分大小写：整串小写会把可访问链接误判为死链（P1-7 续）。"""
        self.assertEqual(
            source_check.normalize_url("https://www.163.com/dy/article/LBEFH3E00556ENJI.html"),
            "https://www.163.com/dy/article/LBEFH3E00556ENJI.html")


class TestProbeUrlSet(unittest.TestCase):
    """R6 探测集：自引用（本仓库链接）不是外部来源，不得参与可达性探测。"""

    def test_self_reference_excluded(self):
        text = ('<p><a href="https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/x.html">x</a>'
                ' <a href="https://imf.org/a">IMF</a></p>')
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        urls = source_check.probe_url_set(text, reg)
        self.assertIn("https://imf.org/a", urls)
        self.assertFalse(any("tech-context-digest" in u for u in urls))


class TestR1RegistryCoverage(unittest.TestCase):
    def test_unmatched_url_is_error(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report('<a href="https://unknown.example/x">x</a>', reg)
        self.assertTrue(any(lvl == "E" and "R1" in msg for lvl, msg in issues))

    def test_matched_url_passes(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report('<a href="https://imf.org/a">IMF</a>', reg)
        self.assertFalse(any(lvl == "E" and "R1" in msg for lvl, msg in issues))

    def test_empty_registry_with_url_is_error(self):
        issues = source_check.check_report('<a href="https://imf.org/a">x</a>', _reg())
        self.assertTrue(any(lvl == "E" and "R1" in msg for lvl, msg in issues))

    def test_empty_registry_without_url_warns(self):
        issues = source_check.check_report("纯文本无链接", _reg())
        self.assertTrue(any(lvl == "W" and "R1" in msg for lvl, msg in issues))

    def test_synthesis_only_layer_exempt_from_empty_registry(self):
        """无外部来源的综合层：空登记 + 无外部 URL 属预期，不告警。"""
        issues = source_check.check_report("纯文本无链接", _reg(),
                                           {"source_strategy": "synthesis_only"})
        self.assertFalse(any("R1" in msg for _, msg in issues))

    def test_synthesis_only_layer_still_requires_registration_for_urls(self):
        """综合层一旦引入外部 URL，仍须登记（豁免仅限空登记 + 无 URL）。"""
        issues = source_check.check_report('<a href="https://imf.org/a">x</a>', _reg(),
                                           {"source_strategy": "synthesis_only"})
        self.assertTrue(any(lvl == "E" and "R1" in msg for lvl, msg in issues))

    def test_unknown_strategy_does_not_exempt(self):
        issues = source_check.check_report("纯文本无链接", _reg(),
                                           {"source_strategy": ""})
        self.assertTrue(any(lvl == "W" and "R1" in msg for lvl, msg in issues))


class TestSourceStrategyParsing(unittest.TestCase):
    def test_tokens(self):
        self.assertEqual(source_check.parse_source_strategy("synthesis_only"), "synthesis_only")
        self.assertEqual(source_check.parse_source_strategy("no_external"), "synthesis_only")
        self.assertEqual(source_check.parse_source_strategy("无外部来源"), "synthesis_only")
        self.assertEqual(source_check.parse_source_strategy("综合层"), "synthesis_only")

    def test_natural_language(self):
        self.assertEqual(
            source_check.parse_source_strategy("synthesis_only（无外部来源的综合层；引用走事实卡片）"),
            "synthesis_only")
        self.assertEqual(source_check.parse_source_strategy("无外部来源，只收敛仓库内事实"),
                         "synthesis_only")

    def test_unknown_and_empty(self):
        self.assertEqual(source_check.parse_source_strategy(""), "")
        self.assertEqual(source_check.parse_source_strategy("official_en"), "")

    def test_decision_hub_config_declares_synthesis_only(self):
        ctx = source_check._ctx_for("content/economy/insight")
        self.assertEqual(ctx.get("source_strategy"), "synthesis_only")


class TestR2TierCompliance(unittest.TestCase):
    def test_media_without_marker_is_error(self):
        reg = _reg({"source_id": "M1", "tier": 4, "url": "https://news.example/c"})
        issues = source_check.check_report('<a href="https://news.example/c">media</a>', reg)
        self.assertTrue(any(lvl == "E" and "R2" in msg for lvl, msg in issues))

    def test_media_with_marker_passes(self):
        reg = _reg({"source_id": "M1", "tier": 4, "url": "https://news.example/c"})
        issues = source_check.check_report(
            '<a href="https://news.example/c">media</a> 需核实原文', reg)
        self.assertFalse(any(lvl == "E" and "R2" in msg for lvl, msg in issues))

    def test_portal_without_marker_warns(self):
        reg = _reg({"source_id": "P1", "tier": 3, "url": "https://portal.example/d"})
        issues = source_check.check_report('<a href="https://portal.example/d">p</a>', reg)
        self.assertTrue(any(lvl == "W" and "R2" in msg for lvl, msg in issues))


class TestR3DualSource(unittest.TestCase):
    def test_two_synthesis_sources_pass(self):
        reg = _reg(
            {"source_id": "S1", "tier": 1, "url": "https://imf.org/a", "in_synthesis": True},
            {"source_id": "S2", "tier": 2, "url": "https://oecd.org/b", "in_synthesis": True},
        )
        text = '<a href="https://imf.org/a">a</a> <a href="https://oecd.org/b">b</a>'
        issues = source_check.check_report(text, reg)
        self.assertFalse(any("R3" in msg for _, msg in issues))

    def test_single_synthesis_source_is_error(self):
        reg = _reg(
            {"source_id": "S1", "tier": 1, "url": "https://imf.org/a", "in_synthesis": True},
            {"source_id": "S2", "tier": 2, "url": "https://oecd.org/b", "in_synthesis": True},
        )
        issues = source_check.check_report('<a href="https://imf.org/a">a</a>', reg)
        self.assertTrue(any(lvl == "E" and "R3" in msg for lvl, msg in issues))


class TestR4KeyNumber(unittest.TestCase):
    """P1-7：R4 块级逐点指针——含单位/量级数字的正文断言块附近窗口内须有来源标记。"""

    def test_bare_number_block_without_source_is_error(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            "<p>阿联酋网安市场规模 8.2 亿美元，CAGR 10.66%。</p>", reg)
        self.assertTrue(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_number_with_source_marker_passes(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            "<p>阿联酋网安市场规模 8.2 亿美元（来源：IMF，2026）。</p>", reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_marker_in_proximity_window_passes(self):
        """来源标记不在块内、但在 ±PROXIMITY_WINDOW 窗口内，视为已标。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            "<p>规模 1,000 亿。</p><p>数据来源：IMF（2026）</p>", reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_table_cells_are_out_of_scope(self):
        """表格数值不逐单元格判定（来源多写在表注 / 报告来源清单，逐格判定误报不可控）。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        row = ('<table><tr><th>指标</th><th>读数</th></tr>'
               '<tr><td>MENA 支出</td><td>33 亿美元</td></tr>'
               '<tr><td>GCC 增速</td><td>14% YoY</td></tr></table>')
        issues = source_check.check_report(row, reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_plain_year_is_not_a_key_number(self):
        """年份 / 版本号不算关键数字，不得误报。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            "<p>ISR v3.1 于 2026-09 发布，含 13 个控制域。</p>", reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_declared_derived_value_is_exempt(self):
        """自算 / 推断 / 假设 / 待核属已声明信息，不计。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        for word in ("自算", "推断", "假设性测算", "待核"):
            issues = source_check.check_report(
                f"<p>情景测算规模 52.5 亿（{word}）。</p>", reg)
            self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues), word)

    def test_advisory_container_is_exempt(self):
        """场景切片 / 行动卡内的阈值与建议不是事实断言。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            '<div class="slice"><p>目标基本月薪 ≥30,000 AED 以锁定黄金签证。</p></div>', reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_advisory_heading_section_is_exempt(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            "<h3>分背景切入路径（建议 / 推断）</h3>"
            "<ol><li>在职提升：目标基本月薪 ≥30,000 AED。</li></ol>", reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_verified_badge_counts_as_marker(self):
        """核验等级标本明该断言已经核验，视为有来源标注。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report(
            '<p>规模 1,000 亿。<span class="lvl lvl-verified">已核验</span></p>', reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_corpus_has_no_r4_gaps(self):
        """现有正式报告在 P1-7 口径下无命中（回归锚）。"""
        from _common import iter_reports
        hits = {}
        for ref in iter_reports():
            if ref.category != "report":
                continue
            p = source_check.ROOT / ref.rel
            if not p.exists():
                continue
            gaps = source_check.r4_assertion_gaps(
                p.read_text(encoding="utf-8", errors="replace"))
            if gaps:
                hits[ref.rel] = gaps
        self.assertEqual(hits, {})

    def _compliant_blocks(self):
        """覆盖全部合法来源标记形态 + 各类豁免情形（每条都是一个合规块）。"""
        return [
            '<p>规模 8.2 亿美元（来源：Gartner，2025）。</p>',
            '<p>规模 8.2 亿美元 [FC-IND-006]。</p>',
            '<p>规模 8.2 亿美元（Gartner, 2025）。</p>',
            '<p>规模 8.2 亿美元。<span class="lvl lvl-verified">已核验</span></p>',
            '<p>规模 8.2 亿美元（部分核验）。</p>',
            '<p>规模 8.2 亿美元（<a href="https://gartner.com/x">Gartner</a>）。</p>',
            '<p>规模 8.2 亿美元（数值指针 K07）。</p>',
            '<p>规模 8.2 亿美元 [S-005]。</p>',
            '<p>规模 8.2 亿美元（自算，34,500 × 72.2%）。</p>',
            '<p>规模 8.2 亿美元（推断，机制分析）。</p>',
            '<p>规模 8.2 亿美元（假设性测算，区间 8–9 亿）。</p>',
            '<div class="slice"><p>目标月薪 ≥30,000 AED 以锁定黄金签证。</p></div>',
            '<h3>场景切片 · 就业决策</h3><p>目标月薪 ≥30,000 AED。</p>',
            '<p>方法：偏离度 =（实际 ÷ 对照）− 1，|偏离| &gt; 30% 须重设。</p>',
            '<header><p>数据截止 2026-11，汇率 1 USD = 3.6725 AED。</p></header>',
            '<p>规模 8.2 亿美元（数据来源见 <a href="https://x.example/a">来源清单</a>）。</p>',
            '<p class="note">来源与时点：本期读数时点 2026-11-13；已修正事实 10 条。</p>',
            '<h3>未核验项</h3><ul><li>Stargate UAE 首批 200MW 是否已运营（待官方确认）。</li></ul>',
            '<h3>监测竞品清单与入选标准</h3><p>入选标准：共 11 项分层条目（直接 6 / 间接 3 / 潜在 2）。</p>',
        ]

    def test_false_positive_rate_under_5pct(self):
        """合规块误报率 < 5%（P1-7 验收口径）。"""
        blocks = self._compliant_blocks()
        fp = sum(1 for h in blocks if source_check.r4_assertion_gaps(h))
        self.assertLess(fp / len(blocks), 0.05, f"误报 {fp}/{len(blocks)}")

    def test_bare_number_blocks_are_recalled(self):
        """无标记的裸数字块必须被召回（防止规则过窄而失效）。"""
        for html in ('<p>规模 8.2 亿美元。</p>',
                     '<p>成交量 34,500 笔 / AED 70.8 亿。</p>',
                     '<ul><li>Q3 住宅成交 ≈34,500 笔。</li></ul>',
                     '<ul><li>建筑许可 +54%（份）/ 48%（面积）YoY。</li></ul>'):
            self.assertTrue(source_check.r4_assertion_gaps(html), html)


class TestR5Language(unittest.TestCase):
    def test_language_mismatch_official_en_is_error(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a", "lang": "zh"})
        issues = source_check.check_report('<a href="https://imf.org/a">a</a>', reg,
                                           {"language_rule": "official_en"})
        self.assertTrue(any(lvl == "E" and "R5" in msg for lvl, msg in issues))

    def test_language_rule_tokenized(self):
        """token 化分级：official_en=E；en_or_zh 对集外语言=W；自然语言『仅英文』=E。"""
        self.assertEqual(source_check.parse_language_rule("official_en")["severity"], "E")
        self.assertEqual(source_check.parse_language_rule("en_or_zh")["severity"], "W")
        self.assertEqual(source_check.parse_language_rule("仅英文（全部取自英文网站，严禁中文来源）")["severity"], "E")
        self.assertIsNone(source_check.parse_language_rule("随便什么"))

    def test_lang_normalization(self):
        self.assertEqual(source_check.normalize_lang("en/US"), "en")
        self.assertEqual(source_check.normalize_lang("zh-CN"), "zh")


class TestProximity(unittest.TestCase):
    def test_marker_far_from_link_is_not_nearby(self):
        reg = _reg({"source_id": "M1", "tier": 4, "url": "https://news.example/c"})
        text = '<a href="https://news.example/c">media</a>' + "填充" * 200 + "需核实原文"
        issues = source_check.check_report(text, reg)
        self.assertTrue(any(lvl == "E" and "R2" in msg for lvl, msg in issues))

    def test_marker_within_window_passes(self):
        reg = _reg({"source_id": "M1", "tier": 4, "url": "https://news.example/c"})
        issues = source_check.check_report('<a href="https://news.example/c">m</a> 需核实原文', reg)
        self.assertFalse(any(lvl == "E" and "R2" in msg for lvl, msg in issues))


class TestInstitutionMaster(unittest.TestCase):
    def test_load_default_master(self):
        master = source_check.load_institution_master()
        self.assertTrue(master.get("institutions"))

    def test_tier_mismatch_graded(self):
        master = {"institutions": [{"name": "IMF", "tier": 1, "aliases": ["International Monetary Fund"]}]}
        reg = _reg({"source_id": "S1", "tier": 2, "publisher": "IMF", "url": "https://imf.org/a"})
        new_issues = source_check.check_institution_consistency(reg, master)
        self.assertTrue(any(lvl == "E" and "R7" in msg for lvl, msg in new_issues))
        hist = source_check.check_institution_consistency(reg, master, ctx={"historical": True})
        self.assertTrue(any(lvl == "W" and "R7" in msg for lvl, msg in hist))
        self.assertFalse(any(lvl == "E" for lvl, _ in hist))

    def test_duplicate_source_id_is_structural_error(self):
        master = {"institutions": [{"name": "IMF", "tier": 1}]}
        reg = _reg(
            {"source_id": "S1", "tier": 1, "publisher": "IMF", "url": "https://imf.org/a"},
            {"source_id": "S1", "tier": 1, "publisher": "IMF", "url": "https://imf.org/b"},
        )
        issues = source_check.check_institution_consistency(reg, master)
        self.assertTrue(any(lvl == "E" and "重复" in msg for lvl, msg in issues))

    def test_unknown_publisher_warns(self):
        master = {"institutions": []}
        reg = _reg({"source_id": "S1", "tier": 1, "publisher": "Unknown Org", "url": "https://x"})
        issues = source_check.check_institution_consistency(reg, master)
        self.assertTrue(any(lvl == "W" and "未录入" in msg for lvl, msg in issues))


class TestGatePeriodPreCheck(unittest.TestCase):
    def test_historical_downgrades_r1_and_r6(self):
        # 历史报告不追溯阻断：R1 / R6 均降级为 W（P0-5 口径）
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        text = '<a href="https://unknown.example/x">x</a> <a href="https://imf.org/a">a</a>'
        issues = source_check.check_report(text, reg, {"historical": True,
                                                 "dead_urls": {"https://imf.org/a"}})
        self.assertTrue(any(lvl == "W" and "R1" in msg for lvl, msg in issues))
        self.assertFalse(any(lvl == "E" and "R1" in msg for lvl, msg in issues))
        self.assertTrue(any(lvl == "W" and "R6" in msg for lvl, msg in issues))
        self.assertFalse(any(lvl == "E" and "R6" in msg for lvl, msg in issues))

    def test_r6_strict_period_gates_dead_link_blocking(self):
        """R6 死链阻断自 R6_STRICT_PERIOD 起；此前仅告警（P1-8 集中清理期）。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        strict = source_check.check_report('<a href="https://imf.org/a">a</a>', reg,
                                           {"dead_urls": {"https://imf.org/a"}, "r6_strict": True})
        self.assertTrue(any(lvl == "E" and "R6" in msg for lvl, msg in strict))
        pre = source_check.check_report('<a href="https://imf.org/a">a</a>', reg,
                                        {"dead_urls": {"https://imf.org/a"}})
        self.assertTrue(any(lvl == "W" and "R6" in msg for lvl, msg in pre))
        self.assertFalse(any(lvl == "E" and "R6" in msg for lvl, msg in pre))

    def test_is_historical(self):
        self.assertTrue(source_check._is_historical("economy/x/reports/2026-11_monthly.html", "2027-01"))
        self.assertFalse(source_check._is_historical("economy/x/reports/2027-01_monthly.html", "2027-01"))
        self.assertFalse(source_check._is_historical("economy/x/reports/2026-11_monthly.html", None))

    def test_valid_period(self):
        self.assertTrue(source_check.valid_period("2026-12"))
        self.assertTrue(source_check.valid_period("2026-Q4"))
        self.assertFalse(source_check.valid_period("2026/12"))


class TestCoverageAndProbe(unittest.TestCase):
    def test_coverage_report(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        cov = source_check.coverage_report(reg, '<a href="https://imf.org/a">a</a>'
                                            '<a href="https://x.example/b">b</a>')
        self.assertEqual(cov["cited"], 2)
        self.assertEqual(cov["matched"], 1)
        self.assertAlmostEqual(cov["coverage"], 0.5)

    def test_probe_urls_with_stub_opener(self):
        class Resp:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *a): return False
        class Opener:
            def __init__(self): self.calls = []
            def urlopen(self, req, timeout=None):
                self.calls.append(req.full_url)
                if "dead" in req.full_url:
                    raise OSError("boom")
                return Resp()
        op = Opener()
        dead = source_check.probe_urls(["https://ok.example/a", "https://dead.example/b"], opener=op)
        self.assertEqual(dead, {source_check.normalize_url("https://dead.example/b")})



class TestR6DeadLink(unittest.TestCase):
    def test_dead_url_is_error_in_strict_period(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report('<a href="https://imf.org/a">a</a>', reg,
                                           {"dead_urls": {"https://imf.org/a"}, "r6_strict": True})
        self.assertTrue(any(lvl == "E" and "R6" in msg for lvl, msg in issues))

    def test_self_reference_link_is_exempt(self):
        """指向本仓库自身的 GitHub 链接是内部指针，不计入 R1 / R6。"""
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        url = "https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/x"
        self.assertTrue(source_check.is_self_reference(url))
        issues = source_check.check_report(f'<a href="{url}">x</a>', reg,
                                           {"dead_urls": {url}, "r6_strict": True})
        self.assertFalse(any("R1" in msg or "R6" in msg for _lvl, msg in issues))


class TestBusinessRelFor(unittest.TestCase):
    def test_derives_business_line_from_report_path(self):
        self.assertEqual(
            source_check._business_rel_for("content/economy/dubai/apartment/reports/2026-11_monthly.html"),
            "content/economy/dubai/apartment")

    def test_non_report_path_is_empty(self):
        self.assertEqual(source_check._business_rel_for("README.md"), "")


class TestSingleFileUsesBusinessRegistry(unittest.TestCase):
    def test_monthly_report_passes_with_line_registry(self):
        reg_path = ROOT / "content/economy/dubai/apartment/data/source_registry.json"
        if not reg_path.exists():
            self.skipTest("业务线来源登记尚未建立")
        rel = "content/economy/dubai/apartment/reports/2026-11_monthly.html"
        errors, _warnings, lines = source_check.run(rel, gate_period="2026-11")
        self.assertEqual(errors, 0, lines)


class TestLoadRegistry(unittest.TestCase):
    def test_missing_file_returns_empty(self):
        reg = source_check.load_registry(ROOT / "no" / "such" / "file.json")
        self.assertEqual(reg["sources"], [])


class TestPeriodKey(unittest.TestCase):
    def test_ordering(self):
        self.assertLess(source_check._period_key("2026-11"),
                        source_check._period_key("2026-Q4"))
        self.assertLess(source_check._period_key("2026-Q4"),
                        source_check._period_key("2027"))


class TestSelfTest(unittest.TestCase):
    def test_self_test_passes(self):
        self.assertEqual(source_check._self_test(), 0)


class TestR8RegistryFields(unittest.TestCase):
    """R8 登记字段：verify_status 取值合法 + updated 为 YYYY-MM-DD（仅 [W]）。"""

    def test_valid_entry_has_no_findings(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026-11-18",
                    "evidence": {"method": "manual", "snapshot_date": "2026-11-18"},
                    "document_tier": "official_release", "statement_type": "fact"})
        self.assertEqual(source_check.check_registry_fields(reg), [])

    def test_unverifiable_is_allowed(self):
        reg = _reg({"source_id": "S1", "tier": 2, "verify_status": "unverifiable",
                    "updated": "2026-11-18",
                    "evidence": {"method": "web_fetch", "snapshot_date": "2026-11-18"},
                    "document_tier": "industry_report", "statement_type": "restatement"})
        self.assertEqual(source_check.check_registry_fields(reg), [])

    def test_illegal_status_and_missing_updated_warn(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "待核实"})
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        # verify_status 非法 + updated 缺失 + evidence 覆盖汇总 + document_tier 覆盖汇总（缺失不阻断）
        self.assertEqual(len(issues), 4)
        self.assertTrue(any("verify_status" in msg for _, msg in issues))
        self.assertTrue(any("updated" in msg for _, msg in issues))
        self.assertTrue(any("evidence 覆盖" in msg for _, msg in issues))
        self.assertTrue(any("document_tier 覆盖" in msg for _, msg in issues))

    def test_malformed_updated_warns(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026/11/18"})
        issues = source_check.check_registry_fields(reg)
        # updated 非法 + evidence 覆盖汇总 + document_tier 覆盖汇总
        self.assertEqual(len(issues), 3)
        self.assertTrue(any("updated" in msg for _, msg in issues))

    def test_repo_registries_are_clean(self):
        """全仓来源登记条目字段完备（P1-6 存量补字段后应零告警）。

        T-01 起 evidence 为可选数据卫生项：缺失仅汇总 [W]，不计入「字段完备」断言。
        """
        import glob
        import json
        found = False
        for f in glob.glob(str(ROOT / "data" / "processed" / "**" / "source_registry.json"),
                           recursive=True):
            found = True
            reg = json.loads(Path(f).read_text(encoding="utf-8"))
            issues = [msg for _, msg in source_check.check_registry_fields(reg)
                       if "evidence 覆盖" not in msg and "document_tier 覆盖" not in msg]
            self.assertEqual(issues, [], f)
        self.assertTrue(found, "未找到任何 source_registry.json")


class TestEvidenceField(unittest.TestCase):
    """T-01：evidence 可选字段——合法取值 / 非法告警 / 覆盖率统计（缺失不阻断）。"""

    def test_valid_evidence_has_no_finding(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026-11-18",
                    "evidence": {"method": "web_fetch", "snapshot_date": "2026-11-18",
                                "archive_hash": "a" * 64, "note": "已抓取正文"},
                    "document_tier": "primary_data", "statement_type": "fact"})
        issues = source_check.check_registry_fields(reg)
        self.assertEqual(issues, [])

    def test_illegal_method_warns_only(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026-11-18",
                    "evidence": {"method": "口头", "snapshot_date": "2026-11-18"}})
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        self.assertTrue(any("evidence.method" in msg for _, msg in issues))

    def test_illegal_snapshot_date_warns(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026-11-18",
                    "evidence": {"method": "pdf", "snapshot_date": "2026/11/18"}})
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(any("snapshot_date" in msg for _, msg in issues))

    def test_illegal_archive_hash_warns(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026-11-18",
                    "evidence": {"method": "manual", "archive_hash": "zz"}})
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(any("archive_hash" in msg for _, msg in issues))

    def test_non_dict_evidence_warns(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026-11-18", "evidence": "manual"})
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(any("evidence 须为对象" in msg for _, msg in issues))

    def test_missing_evidence_is_aggregate_warning_not_blocking(self):
        reg = _reg(
            {"source_id": "S1", "tier": 1, "verify_status": "verified",
             "updated": "2026-11-18"},
            {"source_id": "S2", "tier": 2, "verify_status": "verified",
             "updated": "2026-11-18",
             "evidence": {"method": "manual", "snapshot_date": "2026-11-18"}},
        )
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        # evidence 覆盖汇总 + document_tier 覆盖汇总（均缺失不阻断）
        self.assertEqual(len(issues), 2)
        ev_msgs = [msg for _, msg in issues if "evidence 覆盖" in msg]
        self.assertEqual(len(ev_msgs), 1)
        self.assertIn("1/2", ev_msgs[0])
        self.assertIn("不阻断", ev_msgs[0])
        self.assertTrue(any("document_tier 覆盖" in msg for _, msg in issues))

    def test_coverage_stats(self):
        reg = _reg(
            {"source_id": "S1", "tier": 1, "verify_status": "verified",
             "updated": "2026-11-18"},
            {"source_id": "S2", "tier": 2, "verify_status": "verified",
             "updated": "2026-11-18", "evidence": {"note": "仅备注"}},
        )
        cov = source_check.evidence_coverage(reg)
        self.assertEqual(cov, {"total": 2, "with_evidence": 1, "missing": 1, "ratio": 0.5})
        self.assertEqual(source_check.evidence_coverage(_reg())["ratio"], 1.0)

    def test_sample_registry_has_three_evidence_entries(self):
        """T-01 验收：抽样登记至少 3 条含 evidence（示例补登记）。"""
        import json
        reg = json.loads((ROOT / "data" / "processed" / "tech" / "security" / "dubai"
                          / "source_registry.json").read_text(encoding="utf-8"))
        cov = source_check.evidence_coverage(reg)
        self.assertGreaterEqual(cov["with_evidence"], 3)


class TestContentFingerprint(unittest.TestCase):
    """T-01：tier∈{1,2} 且 in_synthesis=true 的来源正文指纹与变更检测。"""

    def _reg(self):
        return _reg(
            {"source_id": "S1", "tier": 1, "in_synthesis": True,
             "verify_status": "verified", "updated": "2026-11-18"},
            {"source_id": "S2", "tier": 2, "in_synthesis": True,
             "verify_status": "verified", "updated": "2026-11-18"},
            {"source_id": "S3", "tier": 3, "in_synthesis": True,
             "verify_status": "verified", "updated": "2026-11-18"},
            {"source_id": "S4", "tier": 1, "in_synthesis": False,
             "verify_status": "verified", "updated": "2026-11-18"},
        )

    def test_fingerprint_is_sha256_and_crlf_stable(self):
        import hashlib
        nl = chr(10)
        crlf = chr(13) + nl
        self.assertEqual(source_check.content_fingerprint("正文" + nl),
                         hashlib.sha256(("正文" + nl).encode("utf-8")).hexdigest())
        self.assertEqual(source_check.content_fingerprint("正文" + crlf),
                         source_check.content_fingerprint("正文" + nl))

    def test_eligible_is_tier12_and_in_synthesis(self):
        ids = {s["source_id"] for s in source_check.fingerprint_eligible(self._reg())}
        self.assertEqual(ids, {"S1", "S2"})

    def test_collect_only_eligible_with_snapshot(self):
        fps = source_check.collect_fingerprints(
            self._reg(), {"S1": "甲", "S2": "乙", "S3": "丙", "S4": "丁"})
        self.assertEqual(set(fps), {"S1", "S2"})
        self.assertEqual(fps["S1"], source_check.content_fingerprint("甲"))

    def test_change_detection(self):
        reg = self._reg()
        prev = source_check.collect_fingerprints(reg, {"S1": "甲", "S2": "乙"})
        cur = source_check.collect_fingerprints(reg, {"S1": "甲改", "S2": "乙"})
        d = source_check.compare_fingerprints(prev, cur)
        self.assertEqual(d["changed"], ["S1"])
        self.assertEqual(d["new"], [])
        self.assertEqual(d["removed"], [])

    def test_new_and_removed_detection(self):
        reg = self._reg()
        prev = source_check.collect_fingerprints(reg, {"S1": "甲"})
        cur = source_check.collect_fingerprints(reg, {"S2": "乙"})
        d = source_check.compare_fingerprints(prev, cur)
        self.assertEqual(d["new"], ["S2"])
        self.assertEqual(d["removed"], ["S1"])

    def test_store_roundtrip_and_deterministic(self):
        import json
        import tempfile
        reg = self._reg()
        fps = source_check.collect_fingerprints(reg, {"S1": "甲", "S2": "乙"})
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "fp.json"
            source_check.emit_fingerprint_store(p, fps)
            source_check.emit_fingerprint_store(p, fps)
            self.assertEqual(p.read_text(encoding="utf-8"),
                             p.read_text(encoding="utf-8"))
            self.assertEqual(source_check.load_fingerprint_store(p), fps)
            doc = json.loads(p.read_text(encoding="utf-8"))
            self.assertEqual(doc["schema_version"], source_check.FINGERPRINT_STORE_SCHEMA)

    def test_load_snapshots_reads_txt_and_md(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "S1.txt").write_text("甲", encoding="utf-8")
            (Path(tmp) / "S2.md").write_text("乙", encoding="utf-8")
            (Path(tmp) / "ignore.json").write_text("{}", encoding="utf-8")
            self.assertEqual(source_check.load_snapshots(Path(tmp)), {"S1": "甲", "S2": "乙"})

    def test_fingerprint_mode_requires_args(self):
        code, lines = source_check.fingerprint_mode(None, "x")
        self.assertEqual(code, 1)
        code, lines = source_check.fingerprint_mode("x", None)
        self.assertEqual(code, 1)

    def test_fingerprint_mode_emits_and_detects_change(self):
        import json
        import tempfile
        reg_rel = "data/processed/economy/dubai/apartment/source_registry.json"
        with tempfile.TemporaryDirectory() as tmp:
            snap = Path(tmp) / "snap"
            snap.mkdir()
            store = Path(tmp) / "fp.json"
            # 选两条合格来源：从登记中取 tier1/2 且 in_synthesis 的 source_id
            reg = json.loads((ROOT / reg_rel).read_text(encoding="utf-8"))
            eligible = source_check.fingerprint_eligible(reg)
            self.assertGreaterEqual(len(eligible), 2)
            for s in eligible[:2]:
                (snap / f"{s['source_id']}.txt").write_text(
                    f"正文 {s['source_id']}", encoding="utf-8")
            code, lines = source_check.fingerprint_mode(reg_rel, str(snap))
            self.assertEqual(code, 0, lines)
            code, lines = source_check.fingerprint_mode(reg_rel, str(snap),
                                                        store_path=str(store), emit=True)
            self.assertEqual(code, 0, lines)
            # 变更一条正文 -> 漂移
            first = eligible[0]["source_id"]
            (snap / f"{first}.txt").write_text("正文 已改", encoding="utf-8")
            code, lines = source_check.fingerprint_mode(reg_rel, str(snap), store_path=str(store))
            self.assertEqual(code, 2)
            self.assertTrue(any("CHANGED" in ln and first in ln for ln in lines), lines)


class TestProbeExemptions(unittest.TestCase):
    """探测豁免：登记豁免的官方 URL 单次 404 归环境性不可达，不判死链。"""

    def test_load_active_exemptions(self):
        ex = source_check.load_probe_exemptions()
        self.assertIn(source_check.normalize_url("https://gisec.ae"), ex)

    def test_is_probe_exempt_normalized(self):
        self.assertTrue(source_check.is_probe_exempt("https://gisec.ae/"))
        self.assertFalse(source_check.is_probe_exempt("https://example.com"))

    def test_missing_file_is_empty(self):
        self.assertEqual(
            source_check.load_probe_exemptions(Path("/nonexistent/x.json")), {})

    def test_dead_exempt_reclassified_unreachable(self):
        class Resp:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *a): return False

        class Opener:
            def urlopen(self, req, timeout=None):
                if "gisec" in req.full_url:
                    raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {}, None)
                return Resp()

        ex = {source_check.normalize_url("https://gisec.ae"): {"url": "https://gisec.ae"}}
        dead, unreachable = source_check.probe_urls_detail(
            ["https://gisec.ae", "https://ok.example/a"], opener=Opener(), exemptions=ex)
        self.assertEqual(dead, set())
        self.assertEqual(unreachable, {source_check.normalize_url("https://gisec.ae")})

    def test_dead_non_exempt_stays_dead(self):
        class Opener:
            def urlopen(self, req, timeout=None):
                raise urllib.error.HTTPError(req.full_url, 404, "Not Found", {}, None)

        dead, _unreachable = source_check.probe_urls_detail(
            ["https://dead.example/a"], opener=Opener(),
            exemptions={source_check.normalize_url("https://gisec.ae"): {}})
        self.assertEqual(dead, {source_check.normalize_url("https://dead.example/a")})


class TestDocumentTier(unittest.TestCase):
    """T-08：document_tier / statement_type 可选字段——取值合法性 / 机构上限一致性 / 覆盖率。"""

    MASTER = {"institutions": [
        {"name": "IMF", "tier": 1, "aliases": []},
        {"name": "Gartner", "tier": 2, "aliases": []},
        {"name": "Portal", "tier": 3, "aliases": []},
        {"name": "News", "tier": 4, "aliases": []},
    ]}

    def _entry(self, **kw):
        base = {"source_id": "S1", "tier": 1, "verify_status": "verified",
                "updated": "2026-11-18",
                "evidence": {"method": "manual", "snapshot_date": "2026-11-18"}}
        base.update(kw)
        return base

    def test_valid_fields_have_no_finding(self):
        reg = _reg(self._entry(publisher="Gartner", document_tier="industry_report",
                               statement_type="restatement"))
        self.assertEqual(source_check.check_registry_fields(reg, {"master": self.MASTER}), [])

    def test_illegal_document_tier_warns_only(self):
        reg = _reg(self._entry(document_tier="一手数据"))
        issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        self.assertTrue(any("document_tier" in msg and "非法" in msg for _, msg in issues))

    def test_illegal_statement_type_warns_only(self):
        reg = _reg(self._entry(statement_type="事实"))
        issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        self.assertTrue(any("statement_type" in msg and "非法" in msg for _, msg in issues))

    def test_document_tier_above_tier4_ceiling_warns(self):
        """tier 4 媒体转述机构上限 media：不得标 primary_data / official_release / industry_report。"""
        for dt in ("primary_data", "official_release", "industry_report", "opinion"):
            reg = _reg(self._entry(publisher="News", tier=4, document_tier=dt))
            issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
            self.assertTrue(any("高于机构 tier=4" in msg for _, msg in issues), dt)

    def test_document_tier_at_tier4_ceiling_passes(self):
        reg = _reg(self._entry(publisher="News", tier=4, document_tier="media"))
        issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
        self.assertFalse(any("高于机构 tier" in msg for _, msg in issues))

    def test_document_tier_above_tier3_ceiling_warns(self):
        """tier 3 挂牌门户上限 media/opinion。"""
        for dt in ("primary_data", "official_release", "industry_report"):
            reg = _reg(self._entry(publisher="Portal", tier=3, document_tier=dt))
            issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
            self.assertTrue(any("高于机构 tier=3" in msg for _, msg in issues), dt)

    def test_tier3_ceiling_media_and_opinion_pass(self):
        for dt in ("media", "opinion"):
            reg = _reg(self._entry(publisher="Portal", tier=3, document_tier=dt))
            issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
            self.assertFalse(any("高于机构 tier" in msg for _, msg in issues), dt)

    def test_tier1_tier2_have_no_ceiling(self):
        for pub, tier in (("IMF", 1), ("Gartner", 2)):
            for dt in source_check.DOCUMENT_TIER_VALUES:
                reg = _reg(self._entry(publisher=pub, tier=tier, document_tier=dt))
                issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
                self.assertFalse(any("高于机构 tier" in msg for _, msg in issues), (pub, dt))

    def test_no_master_skips_consistency(self):
        """未传 master 时跳过一致性校验（无先验可比，不误报）。"""
        reg = _reg(self._entry(publisher="News", tier=4, document_tier="primary_data"))
        issues = source_check.check_registry_fields(reg)
        self.assertFalse(any("高于机构 tier" in msg for _, msg in issues))

    def test_unknown_publisher_skips_consistency(self):
        reg = _reg(self._entry(publisher="未录入机构", tier=4, document_tier="primary_data"))
        issues = source_check.check_registry_fields(reg, {"master": self.MASTER})
        self.assertFalse(any("高于机构 tier" in msg for _, msg in issues))

    def test_coverage_stats(self):
        reg = _reg(self._entry(document_tier="media"), self._entry(source_id="S2"))
        cov = source_check.document_tier_coverage(reg)
        self.assertEqual(cov, {"total": 2, "with_document_tier": 1,
                               "missing": 1, "ratio": 0.5})
        self.assertEqual(source_check.document_tier_coverage(_reg())["ratio"], 1.0)

    def test_missing_document_tier_is_aggregate_warning(self):
        reg = _reg(self._entry(), self._entry(source_id="S2"))
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        dt_msgs = [msg for _, msg in issues if "document_tier 覆盖" in msg]
        self.assertEqual(len(dt_msgs), 1)
        self.assertIn("0/2", dt_msgs[0])
        self.assertIn("不阻断", dt_msgs[0])

    def test_sample_registry_has_three_document_tier_entries(self):
        """T-08 验收：抽样登记至少 3 条含 document_tier（示例补登记）。"""
        import json
        reg = json.loads((ROOT / "data" / "processed" / "tech" / "security" / "dubai"
                          / "source_registry.json").read_text(encoding="utf-8"))
        cov = source_check.document_tier_coverage(reg)
        self.assertGreaterEqual(cov["with_document_tier"], 3)


if __name__ == "__main__":
    unittest.main()
