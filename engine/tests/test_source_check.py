# -*- coding: utf-8 -*-
"""来源登记前置校验（source_check.py / T1）单元测试。"""
from __future__ import annotations

import importlib.util
import unittest
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
    def test_number_without_source_is_error(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report("规模 1,000 亿", reg)
        self.assertTrue(any(lvl == "E" and "R4" in msg for lvl, msg in issues))

    def test_number_with_source_marker_passes(self):
        reg = _reg({"source_id": "S1", "tier": 1, "url": "https://imf.org/a"})
        issues = source_check.check_report("规模 1,000 亿（来源：IMF）", reg)
        self.assertFalse(any(lvl == "E" and "R4" in msg for lvl, msg in issues))


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
                    "updated": "2026-11-18"})
        self.assertEqual(source_check.check_registry_fields(reg), [])

    def test_unverifiable_is_allowed(self):
        reg = _reg({"source_id": "S1", "tier": 2, "verify_status": "unverifiable",
                    "updated": "2026-11-18"})
        self.assertEqual(source_check.check_registry_fields(reg), [])

    def test_illegal_status_and_missing_updated_warn(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "待核实"})
        issues = source_check.check_registry_fields(reg)
        self.assertTrue(all(lvl == "W" for lvl, _ in issues))
        self.assertEqual(len(issues), 2)
        self.assertTrue(any("verify_status" in msg for _, msg in issues))
        self.assertTrue(any("updated" in msg for _, msg in issues))

    def test_malformed_updated_warns(self):
        reg = _reg({"source_id": "S1", "tier": 1, "verify_status": "verified",
                    "updated": "2026/11/18"})
        issues = source_check.check_registry_fields(reg)
        self.assertEqual(len(issues), 1)
        self.assertIn("updated", issues[0][1])

    def test_repo_registries_are_clean(self):
        """全仓来源登记条目字段完备（P1-6 存量补字段后应零告警）。"""
        import glob
        import json
        found = False
        for f in glob.glob(str(ROOT / "data" / "processed" / "**" / "source_registry.json"),
                           recursive=True):
            found = True
            reg = json.loads(Path(f).read_text(encoding="utf-8"))
            self.assertEqual(source_check.check_registry_fields(reg), [], f)
        self.assertTrue(found, "未找到任何 source_registry.json")


if __name__ == "__main__":
    unittest.main()
