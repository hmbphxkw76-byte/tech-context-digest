"""engine/tools 单元测试（CI: ci.yml / scheduled-maintenance 的 unittest 步骤）。

覆盖纯函数：报告名解析、周期解析与任务推导、期望输出名、
归档保留策略、lint 检查、活跃度天数计算、目录结构布局解析。
运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import _common  # noqa: E402
from archive_reports import KEEP, archive_cycle_dir, rotate_audit_docs, select_archives, select_audit_docs  # noqa: E402
from automation_status import days_since_latest  # noqa: E402
from build_hub import (  # noqa: E402
    ReportEntry,
    Topic,
    _render_cycle_group,
    build_outputs,
    collect_topics,
    displayed_report_count,
    global_base_period,
    group_topic_reports,
    normalize_for_check,
)
from compliance_check import check_report, cycle_rule, detect_type, load_rules  # noqa: E402
from lint_reports import lint_html  # noqa: E402
from restyle_reports import normalize_tables  # noqa: E402
from update_planner import build_tasks, default_period  # noqa: E402


class TestDetectReport(unittest.TestCase):
    def test_monthly(self):
        self.assertEqual(_common.detect_report("2026-11_monthly.html"), ("monthly", "2026-11", "html"))

    def test_quarterly(self):
        self.assertEqual(_common.detect_report("2026-Q3_quarterly.html"), ("quarterly", "2026-Q3", "html"))

    def test_annual(self):
        self.assertEqual(_common.detect_report("2026_annual.html"), ("annual", "2026", "html"))

    def test_baseline(self):
        self.assertEqual(
            _common.detect_report("2026-11_baseline_report.html"), ("baseline", "2026-11", "html")
        )
        self.assertEqual(_common.detect_report("2026-11_baseline.html"), ("baseline", "2026-11", "html"))

    def test_md_variant(self):
        self.assertEqual(_common.detect_report("2026-11_monthly.md"), ("monthly", "2026-11", "md"))

    def test_weekly(self):
        # 周报：period 为数据截止日（ISO 日期），与月 / 季 / 年日历周期不同
        self.assertEqual(_common.detect_report("2026-11-13_weekly.html"), ("weekly", "2026-11-13", "html"))
        self.assertEqual(_common.detect_report("2026-02-28_weekly.md"), ("weekly", "2026-02-28", "md"))
        self.assertIsNone(_common.detect_report("2026-13-01_weekly.html"))  # 非法月份
        self.assertIsNone(_common.detect_report("2026-11-13_weekly.txt"))  # 非法扩展名

    def test_non_report(self):
        self.assertIsNone(_common.detect_report("dubai_apartment_indicator_registry_2026-11.xlsx"))
        self.assertIsNone(_common.detect_report("2026-13_monthly.html"))  # 非法月份
        self.assertIsNone(_common.detect_report("random.html"))


class TestParsePeriod(unittest.TestCase):
    def test_month(self):
        self.assertEqual(_common.parse_period("2026-11"), ("month", 2026, 11))

    def test_quarter(self):
        self.assertEqual(_common.parse_period("2026-Q3"), ("quarter", 2026, 3))

    def test_year(self):
        self.assertEqual(_common.parse_period("2026"), ("year", 2026, None))

    def test_invalid(self):
        for bad in ("2026-13", "2026-Q5", "26-Q1", "abc", "2026-1"):
            with self.assertRaises(ValueError):
                _common.parse_period(bad)


class TestTasksForPeriod(unittest.TestCase):
    def test_plain_month(self):
        self.assertEqual(_common.tasks_for_period("month", 2026, 11), [("monthly", 2026, 11)])

    def test_quarter_start_month(self):
        self.assertEqual(
            _common.tasks_for_period("month", 2026, 1),
            [("monthly", 2026, 1), ("quarterly", 2026, 1), ("annual", 2025, None)],
        )

    def test_quarter_period(self):
        self.assertEqual(_common.tasks_for_period("quarter", 2026, 4), [("quarterly", 2026, 4)])

    def test_year_period(self):
        self.assertEqual(_common.tasks_for_period("year", 2026, None), [("annual", 2026, None)])


class TestExpectedOutput(unittest.TestCase):
    def test_names(self):
        self.assertEqual(_common.expected_output("monthly", 2026, 11), "2026-11_monthly.html")
        self.assertEqual(_common.expected_output("quarterly", 2026, 1), "2026-Q1_quarterly.html")
        self.assertEqual(_common.expected_output("annual", 2026, None), "2026_annual.html")
        self.assertEqual(
            _common.expected_output("baseline", 2026, 11), "2026-11_baseline_report.html"
        )


class TestDefaultPeriod(unittest.TestCase):
    def test_plain_month(self):
        self.assertEqual(default_period(datetime(2026, 11, 13, tzinfo=timezone.utc)), "2026-11")

    def test_quarter_start_month(self):
        self.assertEqual(default_period(datetime(2026, 1, 1, tzinfo=timezone.utc)), "2026-Q1")
        self.assertEqual(default_period(datetime(2026, 10, 31, tzinfo=timezone.utc)), "2026-Q4")


class TestBuildTasks(unittest.TestCase):
    def test_status_done_when_output_exists(self):
        # content/economy/dubai/apartment 已有 2026-11_monthly.html（真实仓库状态）
        tasks = build_tasks("2026-11", _common.iter_business_dirs())
        self.assertTrue(tasks, "至少应识别出一条业务线")
        by_out = {t["output"]: t for t in tasks}
        t = by_out["content/economy/dubai/apartment/reports/2026-11_monthly.html"]
        self.assertEqual(t["status"], "done")
        self.assertEqual(t["cycle"], "monthly")
        self.assertTrue(t["prompt"].endswith("prompt-monthly-monitor.md"))

    def test_pending_when_output_missing(self):
        tasks = build_tasks("2026-12", _common.iter_business_dirs())
        by_out = {t["output"]: t for t in tasks}
        self.assertEqual(by_out["content/economy/dubai/apartment/reports/2026-12_monthly.html"]["status"], "pending")

    def test_conditional_cycle_not_scheduled(self):
        # security 月度为核验型轻运行（提示词含 report-output: none），不派月度任务
        tasks = build_tasks("2026-11", _common.iter_business_dirs())
        outs = {t["output"] for t in tasks}
        self.assertNotIn("content/tech/security/dubai/reports/2026-11_monthly.html", outs)
        # 其季度任务仍应正常派发
        q = build_tasks("2026-Q4", _common.iter_business_dirs())
        self.assertTrue(any(t["project"] == "content/tech/security/dubai" for t in q))

    def test_no_task_before_baseline(self):
        # competitive-intelligence 基线 2026-12，不应派 2026-11 月度任务
        tasks = build_tasks("2026-11", _common.iter_business_dirs())
        self.assertFalse(any(t["project"] == "content/tech/competitive-intelligence/dubai" for t in tasks))
        # 其 2026-12 月度任务应派发
        dec = build_tasks("2026-12", _common.iter_business_dirs())
        self.assertTrue(any(t["project"] == "content/tech/competitive-intelligence/dubai" for t in dec))


class TestPromptFileCandidates(unittest.TestCase):
    def test_annual_alias(self):
        c = _common.prompt_file_candidates("annual")
        self.assertEqual(c[0], "prompt-annual-review.md")
        self.assertIn("prompt-annual-refresh.md", c)

    def test_baseline_year_month_parse(self):
        biz = {b.rel: b for b in _common.iter_business_dirs()}
        self.assertEqual(_common.baseline_year_month(biz["content/economy/dubai/apartment"]), (2026, 11))


class TestPromptProducesReport(unittest.TestCase):
    def test_none_marker(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prompt-monthly-monitor.md"
            p.write_text("<!-- report-output: none -->\n", encoding="utf-8")
            self.assertFalse(_common.prompt_produces_report(p))

    def test_default_true(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "prompt-monthly-monitor.md"
            p.write_text("# 月度提示词\n无标记\n", encoding="utf-8")
            self.assertTrue(_common.prompt_produces_report(p))

    def test_missing_file_true(self):
        self.assertTrue(_common.prompt_produces_report(Path("/nonexistent/x.md")))


class TestSelectArchives(unittest.TestCase):
    def _paths(self, names):
        return [Path(n) for n in names]

    def test_keep_newest(self):
        items = [
            ("monthly", f"2026-{m:02d}", p)
            for m, p in enumerate(self._paths([f"2026-{m:02d}_monthly.html" for m in range(1, 13)]), start=1)
        ]
        to_archive = select_archives(items, {"monthly": 12})
        self.assertEqual(to_archive, [], "恰好 12 期时不应归档")

    def test_archive_oldest(self):
        names = [f"2025-{m:02d}_monthly.html" for m in range(1, 13)] + ["2026-01_monthly.html"]
        items = [
            ("monthly", n.split("_")[0], p)
            for n, p in zip(names, self._paths(names))
        ]
        to_archive = select_archives(items, {"monthly": 12})
        # 13 期保留最新 12 期，归档最早 1 期（排序为 period 降序）
        self.assertEqual([p.name for p in to_archive], ["2025-01_monthly.html"])


class TestArchiveCycleDir(unittest.TestCase):
    def test_sources_archive_oldest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "sources"
            root.mkdir()
            # 19 期月报源稿：默认保留 18 期（与展示窗口同源），归档最早 1 期
            names = [f"2024-{m:02d}_monthly.md" for m in range(1, 13)] + \
                    [f"2025-{m:02d}_monthly.md" for m in range(1, 8)]
            for n in names:
                (root / n).write_text("# x\n", encoding="utf-8")
            moved = archive_cycle_dir(root, "content/demo/sources")
            self.assertEqual(moved, 1)
            self.assertFalse((root / "2024-01_monthly.md").exists())
            self.assertTrue((root / "archives" / "2024-01_monthly.md").exists())

    def test_legacy_dir_not_archived(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "sources"
            legacy = root / "legacy" / "ai-security"
            legacy.mkdir(parents=True)
            f = legacy / "2026-11-14_weekly.md"
            f.write_text("# x\n", encoding="utf-8")
            moved = archive_cycle_dir(root, "content/demo/sources")
            self.assertEqual(moved, 0)
            self.assertTrue(f.exists())


class TestAuditDocRotation(unittest.TestCase):
    """审计文档轮转（Phase 3.2）：根只保留最近 12 个月，无日期账本型不轮转。"""

    def _mk(self, tmp, names):
        for n in names:
            (Path(tmp) / n).write_text("# x\n", encoding="utf-8")

    def test_select_old_and_keep_recent(self):
        with tempfile.TemporaryDirectory() as d:
            self._mk(d, ["a-2025-01-01.md", "b-2026-11-17.md", "coverage-matrix.md"])
            out = select_audit_docs(Path(d), keep_months=12, today=date(2026, 11, 17))
            self.assertEqual([p.name for p in out], ["a-2025-01-01.md"])

    def test_boundary_is_archived(self):
        with tempfile.TemporaryDirectory() as d:
            self._mk(d, ["c-2025-11-17.md"])
            out = select_audit_docs(Path(d), keep_months=12, today=date(2026, 11, 17))
            self.assertEqual([p.name for p in out], ["c-2025-11-17.md"])

    def test_rotate_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            self._mk(d, ["old-2024-05-05.md", "new-2026-11-17.md"])
            rc = rotate_audit_docs(Path(d), keep_months=12, today=date(2026, 11, 17))
            self.assertEqual(rc, 0)
            self.assertFalse((Path(d) / "old-2024-05-05.md").exists())
            self.assertTrue((Path(d) / "archives" / "old-2024-05-05.md").exists())
            rc2 = rotate_audit_docs(Path(d), keep_months=12, today=date(2026, 11, 17))
            self.assertEqual(rc2, 0)


class TestLintHtml(unittest.TestCase):
    def test_clean_report(self):
        text = (
            "<html><body>"
            '<nav class="report-nav" aria-label="报告导航"></nav>'
            "<table class=\"fixed\"><thead><tr>"
            '<th style="width:20%">A</th><th style="width:20%">B</th><th style="width:20%">C</th>'
            '<th style="width:20%">D</th><th style="width:20%">E</th>'
            "</tr></thead><tbody><tr><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr></tbody></table>"
            "</body></html>"
        )
        errors = [i for i in lint_html(text) if i[0] == "E"]
        self.assertEqual(errors, [])

    def test_duplicate_tbody_close(self):
        text = (
            "<table><thead><tr><th>A</th></tr></thead>"
            "<tbody><tr><td>1</td></tr></tbody></tbody></table>"
            "<p>正文。</p>"
        )
        issues = lint_html(text)
        self.assertTrue(any(i[0] == "E" and "</tbody>" in i[1] for i in issues))

    def test_malformed_th(self):
        text = '<table><thead><tr><th scope="col"ead>A</th></tr></thead></table><p>正文。</p>'
        issues = lint_html(text)
        self.assertTrue(any("畸形" in i[1] for i in issues))

    def test_wide_table_missing_width(self):
        ths = "".join(f"<th>列{i}</th>" for i in range(8))
        text = (
            f"<table><thead><tr>{ths}</tr></thead><tbody><tr><td>1</td></tr></tbody></table>"
            "<p>正文。</p>"
        )
        issues = lint_html(text)
        self.assertTrue(any(i[0] == "W" and "未声明百分比列宽" in i[1] for i in issues))

    def test_fixed_class_merged(self):
        """合并类名（如 class="rl-table fixed"）应识别为已声明 fixed。"""
        ths = "".join(f'<th style="width:{100 // 8}%">列{i}</th>' for i in range(8))
        text = (
            f'<table class="rl-table fixed"><thead><tr>{ths}</tr></thead>'
            "<tbody><tr><td>1</td></tr></tbody></table>"
        )
        issues = lint_html(text)
        self.assertFalse(any("缺少 class" in i[1] for i in issues))


class TestNormalizeTables(unittest.TestCase):
    """表格规范化（restyle_reports.normalize_tables）用例。"""

    def test_adds_fixed_and_content_width(self):
        text = (
            "<table><thead><tr><th>编号</th><th>监测对象</th></tr></thead>"
            "<tbody><tr><td>1</td><td>2</td></tr></tbody></table>"
        )
        out = normalize_tables(text)
        self.assertIn('class="fixed"', out)
        widths = [int(x) for x in re.findall(r"width:(\d+)px", out)]
        self.assertEqual(len(widths), 2)
        self.assertGreaterEqual(widths[0], 48)   # 编号
        self.assertGreaterEqual(widths[1], 74)   # 监测对象

    def test_merges_existing_class(self):
        text = '<table class="rl-table"><thead><tr><th>编号</th></tr></thead></table>'
        out = normalize_tables(text)
        self.assertIn('class="rl-table fixed"', out)

    def test_keeps_wider_original_px(self):
        text = '<table class="fixed"><thead><tr><th style="width:200px">编号</th></tr></thead></table>'
        self.assertIn('width:200px', normalize_tables(text))

    def test_body_untouched(self):
        text = (
            "<table><thead><tr><th>编号</th></tr></thead>"
            "<tbody><tr><td>VALUE</td></tr></tbody></table>"
        )
        out = normalize_tables(text)
        self.assertIn('VALUE', out)
        self.assertIn('编号', out)


class TestComplianceCheck(unittest.TestCase):
    """报告模板合规校验（compliance_check.py）纯函数用例。"""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules()
        cls.common = cls.rules["common"]
        cls.monthly_rule, _ = cycle_rule(cls.rules, "market-monitoring", "monthly")
        cls.baseline_rule, _ = cycle_rule(cls.rules, "market-monitoring", "baseline")

    @staticmethod
    def _html(sections=8, nav=True, ids=True, title="测试报告",
              extra_anchor=None, extra_id=None):
        parts = [f"<html><head><title>{title}</title></head><body>"]
        if nav:
            anchors = "".join(
                f'<a href="#s{i}">节{i}</a>' for i in range(1, sections + (1 if extra_anchor else 0))
            )
            parts.append(f'<nav class="report-nav" aria-label="报告导航">{anchors}</nav>')
        if extra_id:
            parts.append(f'<div id="{extra_id}"></div>')
        for i in range(1, sections + 1):
            id_attr = f' id="s{i}"' if ids else ""
            parts.append(f'<h2 class="sec"{id_attr}>节{i}</h2><p>正文</p>')
        if extra_anchor:
            parts.append('<a href="#missing-anchor">断链</a>')
        parts.append("</body></html>")
        return "".join(parts)

    def test_detect_type_from_config(self):
        text = "继承声明：周期提示词 = [类型模板](../../../../engine/templates/employment-research/) × 本文件"
        self.assertEqual(detect_type(text), "employment-research")

    def test_detect_type_none(self):
        self.assertIsNone(detect_type("没有模板引用的配置"))

    def test_cycle_rule_inherits_baseline(self):
        rule, inherited = cycle_rule(self.rules, "competitive-intelligence", "quarterly")
        self.assertTrue(inherited)
        self.assertEqual(rule["sections"], self.rules["types"]["competitive-intelligence"]["cycles"]["baseline"]["sections"])

    def test_business_override_takes_precedence(self):
        rule, inherited = cycle_rule(self.rules, "trend-weekly", "weekly", "content/tech/weekly-roundup")
        self.assertFalse(inherited)
        self.assertEqual(rule["sections"], 10)
        # 未指定业务线时回落类型规则（8 节）
        rule2, _ = cycle_rule(self.rules, "trend-weekly", "weekly")
        self.assertEqual(rule2["sections"], 8)

    def test_clean_cycle_report_passes(self):
        self.assertEqual(check_report(self._html(), self.monthly_rule, self.common), [])

    def test_missing_section_is_error(self):
        issues = check_report(self._html(sections=7), self.monthly_rule, self.common)
        self.assertTrue(any(i[0] == "E" and "结构不完整" in i[1] for i in issues))

    def test_extra_section_is_warning(self):
        issues = check_report(self._html(sections=10), self.monthly_rule, self.common)
        self.assertTrue(any(i[0] == "W" and "超出模板骨架" in i[1] for i in issues))
        self.assertFalse(any(i[0] == "E" for i in issues))

    def test_non_sequential_ids_is_error(self):
        issues = check_report(self._html(ids=False), self.monthly_rule, self.common)
        # 无 id 时不做编号检查（基线形态），此处应无编号错误
        self.assertFalse(any("编号不连续" in i[1] for i in issues))
        html = self._html().replace('id="s3"', 'id="sX"')
        issues = check_report(html, self.monthly_rule, self.common)
        self.assertTrue(any(i[0] == "E" and "编号不连续" in i[1] for i in issues))

    def test_missing_nav_cycle_is_error(self):
        issues = check_report(self._html(nav=False), self.monthly_rule, self.common)
        self.assertTrue(any(i[0] == "E" and "顶部导航" in i[1] for i in issues))

    def test_missing_nav_baseline_is_warning(self):
        issues = check_report(self._html(nav=False), self.baseline_rule, self.common)
        self.assertTrue(any(i[0] == "W" and "缺少简化锚点导航" in i[1] for i in issues))

    def test_missing_title_is_error(self):
        issues = check_report(self._html(title=""), self.monthly_rule, self.common)
        self.assertTrue(any(i[0] == "E" and "title" in i[1] for i in issues))

    def test_broken_anchor_is_error(self):
        issues = check_report(self._html(extra_anchor=True), self.monthly_rule, self.common)
        self.assertTrue(any(i[0] == "E" and "断头锚点" in i[1] for i in issues))

    def test_in_page_anchor_with_extra_id_resolves(self):
        html = self._html(extra_anchor=True, extra_id="missing-anchor")
        self.assertEqual(check_report(html, self.monthly_rule, self.common), [])


class TestBuildHubCheck(unittest.TestCase):
    """汇总页 --check 归一化比对（build_hub.py）用例。"""

    def test_normalize_strips_timestamp(self):
        a = '<p class="muted">最近生成：2026-11-13 01:00 UTC</p>\n<h2>x</h2>'
        b = '<p class="muted">最近生成：2026-11-13 09:30 UTC</p>\n<h2>x</h2>'
        self.assertEqual(normalize_for_check(a), normalize_for_check(b))

    def test_normalize_keeps_other_diffs(self):
        a = '<p class="muted">最近生成：2026-11-13 01:00 UTC</p>\n<h2>x</h2>'
        b = '<p class="muted">最近生成：2026-11-13 01:00 UTC</p>\n<h2>y</h2>'
        self.assertNotEqual(normalize_for_check(a), normalize_for_check(b))

    def test_normalize_noop_without_timestamp(self):
        text = "<html><body><h1>报告</h1></body></html>"
        self.assertEqual(normalize_for_check(text), text)

    def test_committed_index_matches_regen_ignoring_timestamp(self):
        # 真实仓库状态回归：已提交 index.html 与重算内容仅时间戳不同时应判为最新
        committed = (_common.ROOT / "index.html").read_text(encoding="utf-8", errors="replace")
        self.assertEqual(
            normalize_for_check(committed),
            normalize_for_check(build_outputs()["index.html"]),
            "报告清单未变时，已提交 index.html 归一化后应与重算内容一致",
        )

    def test_committed_reader_matches_regen(self):
        committed = (_common.ROOT / "reader.html").read_text(encoding="utf-8", errors="replace")
        self.assertEqual(
            committed,
            build_outputs()["reader.html"],
            "已提交 reader.html 应与重算内容一致",
        )

    def test_reader_reuses_hub_design_system(self):
        reader = build_outputs()["reader.html"]
        # 共用同一套 canonical 设计令牌
        self.assertIn("--navy:#16324f", reader)
        self.assertIn("--font-sans:\"Microsoft YaHei\"", reader)
        # 复用主页公共组件类名
        for cls in ("filterbar", "chip", "rcard", "footer", "totop"):
            self.assertIn(cls, reader)
        # 响应式断点与主页一致
        self.assertIn("@media (max-width:960px)", reader)
        self.assertIn("@media (max-width:560px)", reader)
        # 阅读器专属结构
        self.assertIn('class="reader-head"', reader)
        self.assertIn('class="sidebar"', reader)
        self.assertIn('id="frame"', reader)

    def test_reader_lists_all_reports(self):
        reader = build_outputs()["reader.html"]
        n_reports = displayed_report_count(collect_topics())
        self.assertEqual(reader.count('href="?report='), n_reports)
        self.assertIn('id="empty"', reader)

    def test_hub_shows_base_and_cycle_grouping(self):
        hub = build_outputs()["index.html"]
        self.assertIn("cycle-head", hub)
        # 基期展示口径：仓库内最新月报；「本期更新 · 环比基期」仅在存在上一期报告时标注
        self.assertIn("最新月报 2026-11", hub)
        self.assertNotIn("环比基期 2026-10", hub)
        self.assertIn("该周期首期报告，无环比基期", hub)

    def test_hub_tokens_match_canonical(self):
        from report_style import CANONICAL_CSS
        hub = build_outputs()["index.html"]
        m = re.search(r":root\{(.*?)\}", hub, re.DOTALL)
        self.assertTrue(m, "hub 应含 :root 令牌块")
        hub_tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+)", m.group(1)))
        shared = [
            "--navy", "--navy2", "--blue", "--bg", "--card", "--ink",
            "--ink2", "--ink3", "--line", "--red", "--green", "--amber",
            "--gray", "--font-sans", "--radius", "--radius-sm", "--shadow",
        ]
        for key in shared:
            if key in hub_tokens:
                self.assertIn(
                    f"{key}:{hub_tokens[key].strip()}",
                    CANONICAL_CSS,
                    f"hub 令牌 {key} 应与 canonical 同值",
                )


class TestReportCycleWindows(unittest.TestCase):
    """报告周期窗口与环比高亮（REPORT-CYCLE-WINDOWS-SPEC v1.0）。"""

    @staticmethod
    def _r(cycle, period):
        return ReportEntry(cycle=cycle, period=period,
                           path=f"demo/{period}_{cycle}.html", title=period)

    @classmethod
    def _topic(cls, reports):
        return Topic(rel="demo/line", region="demo", name="demo",
                     type_id="market-monitoring", type_name="市场指标监测型",
                     reports=list(reports))

    @staticmethod
    def _group(reports, cycle):
        return {g.cycle: g for g in group_topic_reports(reports)}[cycle]

    def test_period_months_and_prev(self):
        self.assertEqual(_common.period_months("2026-11"), 2026 * 12 + 10)
        self.assertEqual(_common.period_months("2026-Q3"), 2026 * 12 + 6)
        self.assertEqual(_common.period_months("2026"), 2026 * 12)
        self.assertEqual(_common.prev_period("2026-11"), "2026-10")
        self.assertEqual(_common.prev_period("2026-01"), "2025-12")
        self.assertEqual(_common.prev_period("2026-Q1"), "2025-Q4")
        self.assertEqual(_common.prev_period("2026"), "2025")

    def test_monthly_window_18_and_direct_6(self):
        reports = [self._r("monthly", f"2025-{m:02d}") for m in range(1, 13)] + \
                  [self._r("monthly", f"2026-{m:02d}") for m in range(1, 8)]
        g = self._group(self._topic(reports), "monthly")
        self.assertEqual(g.latest, "2026-07")
        # 直接展示最近 6 期：2026-02..2026-07
        self.assertEqual([r.period for r in g.direct],
                         [f"2026-{m:02d}" for m in range(7, 1, -1)])
        # 更多：窗口内更早的 12 期（2025-02..2026-01）；2025-01 超出 18 个月窗口
        self.assertEqual(len(g.more), 12)
        self.assertEqual(g.more[0].period, "2026-01")
        self.assertEqual(g.more[-1].period, "2025-02")
        self.assertTrue(g.current)

    def test_monthly_beyond_retention_hidden(self):
        reports = [self._r("monthly", "2024-01"), self._r("monthly", "2026-07")]
        g = self._group(self._topic(reports), "monthly")
        self.assertEqual([r.period for r in g.direct], ["2026-07"])
        self.assertEqual(g.more, [])

    def test_quarterly_window_24_months(self):
        reports = [self._r("quarterly", "2024-Q3"), self._r("quarterly", "2024-Q4")] + \
                  [self._r("quarterly", f"2025-Q{q}") for q in range(1, 5)] + \
                  [self._r("quarterly", f"2026-Q{q}") for q in range(1, 4)]
        g = self._group(self._topic(reports), "quarterly")
        self.assertEqual(g.latest, "2026-Q3")
        self.assertEqual(len(g.direct), 8)  # 近 24 个月 = 8 期
        self.assertEqual(g.direct[-1].period, "2024-Q4")
        self.assertEqual(g.more, [])

    def test_annual_max_5(self):
        reports = [self._r("annual", str(y)) for y in range(2018, 2027)]
        g = self._group(self._topic(reports), "annual")
        self.assertEqual([r.period for r in g.direct],
                         ["2026", "2025", "2024", "2023", "2022"])
        self.assertEqual(g.more, [])

    def test_weekly_and_baseline_not_highlighted(self):
        reports = [self._r("weekly", "2026-11-13"), self._r("baseline", "2026-11")]
        groups = {g.cycle: g for g in group_topic_reports(self._topic(reports))}
        self.assertFalse(groups["weekly"].current)
        self.assertFalse(groups["baseline"].current)
        self.assertEqual(groups["weekly"].direct[0].period, "2026-11-13")
        self.assertEqual(groups["baseline"].direct[0].period, "2026-11")

    def test_displayed_and_base(self):
        topic = self._topic([self._r("monthly", "2026-11"),
                             self._r("weekly", "2026-11-13")])
        self.assertEqual(displayed_report_count([topic]), 2)
        self.assertEqual(global_base_period([topic]), "2026-11")

    def test_more_details_rendered_for_monthly(self):
        reports = [self._r("monthly", f"2026-{m:02d}") for m in range(1, 8)]
        topic = self._topic(reports)
        g = self._group(topic, "monthly")
        html = "".join(_render_cycle_group(g, topic, reader=False))
        self.assertIn("<details class=\"more\">", html)
        self.assertIn("更多 1 份", html)

    def test_archive_keep_aligned_with_windows(self):
        self.assertEqual(KEEP["monthly"], _common.CYCLE_WINDOWS["monthly"]["retention"])
        self.assertEqual(KEEP["quarterly"], _common.CYCLE_WINDOWS["quarterly"]["retention"] // 3)
        self.assertEqual(KEEP["annual"], _common.CYCLE_WINDOWS["annual"]["retention"] // 12)


class TestCanonicalReportStyle(unittest.TestCase):
    """canonical 报告样式：全部报告与 hub 共用同一设计系统。"""

    def setUp(self):
        from report_style import CANONICAL_CSS
        self.css = CANONICAL_CSS

    def test_all_reports_use_canonical_tokens(self):
        for t in collect_topics():
            for r in t.reports:
                text = (_common.ROOT / r.path).read_text(encoding="utf-8", errors="replace")
                self.assertIn("--navy:#16324f", text, f"{r.path} 应使用 canonical 主色")
                self.assertIn(
                    '--font-sans:"Microsoft YaHei"', text,
                    f"{r.path} 应使用 canonical 字体",
                )

    def test_all_reports_have_canonical_header_and_nav(self):
        for t in collect_topics():
            for r in t.reports:
                text = (_common.ROOT / r.path).read_text(encoding="utf-8", errors="replace")
                self.assertTrue(
                    'class="report-head"' in text or 'class="hero"' in text,
                    f"{r.path} 应含 canonical 页头",
                )
                self.assertIn('class="report-nav"', text, f"{r.path} 应含 canonical 导航")
                self.assertIn('class="wrap"', text, f"{r.path} 应含 canonical 容器")

    def test_md2html_output_uses_canonical(self):
        from md2html import convert
        md = _common.ROOT / "content/tech/security/dubai/sources/2026-11_baseline_report.md"
        html = convert(md)
        self.assertIn("--navy:#16324f", html)
        self.assertIn('<header class="report-head">', html)
        self.assertIn('class="report-nav"', html)
        self.assertIn('class="sec"', html)


class TestPageBuildCheck(unittest.TestCase):
    """PAGE-BUILD-SPEC 门禁校验器。"""

    BASE_REPORT = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>t</title><style>
:root{--navy:#16324f;--navy2:#2f5597}
.skip-link{position:absolute}
a:focus-visible{outline:1px}
@media (prefers-reduced-motion:reduce){}
@media print{}
</style></head><body>
<header class="report-head"><div class="wrap"><h1>t</h1></div></header>
<nav class="report-nav"><div class="wrap"><div class="nav-tabs"><a href="#s1">a</a></div></div></nav>
<main class="wrap"><h2 class="sec" id="s1">a</h2>
<table><thead><tr><th>a</th></tr></thead><tbody><tr><td>b</td></tr></tbody></table>
</main></body></html>"""

    def setUp(self):
        from page_build_check import check_page, collect_pages

        self.check_page = check_page
        self.collect_pages = collect_pages
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _write(self, name: str, text: str) -> Path:
        p = self.tmp / name
        p.write_text(text, encoding="utf-8")
        return p

    def test_all_repo_pages_pass(self):
        pages = self.collect_pages()
        self.assertGreaterEqual(len(pages), 10, "应扫描到 hub + 报告页")
        for kind, p in pages:
            errs, _warns = self.check_page(kind, p)
            self.assertEqual(errs, [], f"{p} 不应有 [E]：{errs}")

    def test_hub_pages_have_skip_link_and_print(self):
        for name in ("index.html", "reader.html"):
            text = (_common.ROOT / name).read_text(encoding="utf-8")
            self.assertIn("skip-link", text)
            self.assertIn("@media print", text)

    def test_drift_color_is_error(self):
        p = self._write("r.html", self.BASE_REPORT.replace("#16324f", "#1f3d63", 1))
        errs, _ = self.check_page("report", p)
        self.assertTrue(any("P03" in e for e in errs), errs)

    def test_missing_canonical_navy_is_error(self):
        p = self._write("r.html", self.BASE_REPORT.replace("--navy:#16324f", "--navy:#123456"))
        errs, _ = self.check_page("report", p)
        self.assertTrue(any("P02" in e for e in errs), errs)

    def test_report_skeleton_missing_nav(self):
        p = self._write("r.html", self.BASE_REPORT.replace('class="report-nav"', 'class="x"'))
        errs, _ = self.check_page("report", p)
        self.assertTrue(any("P09" in e for e in errs), errs)

    def test_h2_without_sec_is_error(self):
        p = self._write("r.html", self.BASE_REPORT.replace('<h2 class="sec"', "<h2"))
        errs, _ = self.check_page("report", p)
        self.assertTrue(any("P10" in e for e in errs), errs)

    def test_echarts_container_must_be_chart_eh(self):
        text = self.BASE_REPORT.replace(
            "<main", '<script src="https://cdn.jsdelivr.net/npm/echarts@5"></script><main', 1
        ).replace("<table>", '<div class="chart"></div><table>')
        p = self._write("r.html", text)
        errs, _ = self.check_page("report", p)
        self.assertTrue(any("P11" in e for e in errs), errs)

    def test_valid_report_has_no_errors(self):
        p = self._write("r.html", self.BASE_REPORT)
        errs, _warns = self.check_page("report", p)
        self.assertEqual(errs, [], errs)


class TestDaysSinceLatest(unittest.TestCase):
    def test_none_when_empty(self):
        now = datetime(2026, 11, 13, tzinfo=timezone.utc)
        self.assertIsNone(days_since_latest(now, []))

    def test_days(self):
        now = datetime(2026, 11, 13, tzinfo=timezone.utc)
        records = [{"timestamp": "2026-11-10T00:00:00+00:00"}]
        self.assertEqual(days_since_latest(now, records), 3)

    def test_ignores_bad_timestamp(self):
        now = datetime(2026, 11, 13, tzinfo=timezone.utc)
        records = [{"timestamp": "not-a-date"}]
        self.assertIsNone(days_since_latest(now, records))

    def test_naive_treated_as_utc(self):
        now = datetime(2026, 11, 13, tzinfo=timezone.utc)
        records = [{"timestamp": "2026-11-12T00:00:00"}]
        self.assertEqual(days_since_latest(now, records), 1)


if __name__ == "__main__":
    unittest.main()


class TestLayout(unittest.TestCase):
    """目录结构单一事实源（layout.json）与业务线发现。"""

    @classmethod
    def setUpClass(cls):
        cls.layout = _common.load_layout()

    def test_six_themes_registered(self):
        self.assertEqual(
            set(self.layout.themes),
            {"economy", "tech", "education", "international", "political", "society"},
        )

    def test_root_reserved_contains_engine(self):
        self.assertIn("engine", self.layout.root_reserved)
        self.assertIn("content", self.layout.root_reserved)
        self.assertIn(".github", self.layout.root_reserved)

    def test_regions_whitelist(self):
        self.assertEqual(set(self.layout.regions), {"dubai"})

    def test_business_depth(self):
        for theme in ("economy", "tech", "education", "international", "political", "society"):
            self.assertEqual(_common.business_depth(theme), 3)

    def test_discovers_eleven_business_lines(self):
        rels = {b.rel for b in _common.iter_business_dirs()}
        self.assertEqual(
            rels,
            {
                "content/economy/dubai/apartment",
                "content/economy/trends",
                "content/economy/insight",
                "content/tech/security/dubai",
                "content/tech/weekly-roundup",
                "content/tech/industry-research/dubai",
                "content/tech/competitive-intelligence/dubai",
                "content/education/education-system",
                "content/international/international-relations",
                "content/political/political-system",
                "content/society/social-structure",
            },
        )

    def test_four_new_themes_ready(self):
        """P1-9 四主题接入就绪化：region 可选，业务线以 category 段落位且可被发现。"""
        by_rel = {b.rel: b for b in _common.iter_business_dirs()}
        for rel, category in (
            ("content/education/education-system", "education-system"),
            ("content/international/international-relations", "international-relations"),
            ("content/political/political-system", "political-system"),
            ("content/society/social-structure", "social-structure"),
        ):
            self.assertIn(rel, by_rel)
            self.assertEqual(by_rel[rel].category, category, rel)
            self.assertEqual(by_rel[rel].region, "", rel)
            self.assertIn("region", self.layout.optional_dims(by_rel[rel].theme), rel)

    def test_region_and_property_type(self):
        by_rel = {b.rel: b for b in _common.iter_business_dirs()}
        self.assertEqual(by_rel["content/economy/dubai/apartment"].region, "dubai")
        self.assertEqual(by_rel["content/economy/dubai/apartment"].property_type, "apartment")
        self.assertEqual(by_rel["content/economy/trends"].region, "")
        self.assertEqual(by_rel["content/economy/trends"].property_type, "trends")
        self.assertEqual(by_rel["content/economy/insight"].region, "")
        self.assertEqual(by_rel["content/economy/insight"].property_type, "insight")
        self.assertEqual(by_rel["content/tech/security/dubai"].region, "dubai")
        self.assertEqual(by_rel["content/tech/security/dubai"].property_type, "security")
        self.assertEqual(by_rel["content/tech/weekly-roundup"].region, "")
        self.assertEqual(by_rel["content/tech/weekly-roundup"].property_type, "weekly-roundup")

    def test_optional_region_resolution(self):
        """region 为可选维度：缺省时 category 直接落位，存在时按声明顺序映射。"""
        by_rel = {b.rel: b for b in _common.iter_business_dirs()}
        self.assertEqual(by_rel["content/economy/trends"].category, "trends")
        self.assertEqual(by_rel["content/tech/weekly-roundup"].category, "weekly-roundup")
        self.assertEqual(by_rel["content/tech/security/dubai"].category, "security")
        self.assertEqual(by_rel["content/tech/security/dubai"].region, "dubai")

    def test_business_path_exists(self):
        for b in _common.iter_business_dirs():
            self.assertTrue((b.path / "prompts" / "business-config.md").exists(), b.rel)

    def test_iter_theme_dirs_only_existing(self):
        names = {p.name for p in _common.iter_theme_dirs()}
        self.assertIn("economy", names)
        self.assertIn("tech", names)
        self.assertIn("education", names)


class TestDimensionOrder(unittest.TestCase):
    """维度顺序：由 layout.json 各主题声明（economy 地区优先，其余细分优先）。

    专项校验：声明自洽（无重复 / 无未登记维度名），且实例路径段序与声明一致。
    """

    @classmethod
    def setUpClass(cls):
        cls.layout = _common.load_layout()

    def test_dimension_decl_self_consistent(self):
        import validate_layout

        validate_layout.ERRORS.clear()
        try:
            validate_layout.check_dimension_priority(self.layout)
            self.assertEqual(validate_layout.ERRORS, [], validate_layout.ERRORS)
        finally:
            validate_layout.ERRORS.clear()

    def test_validator_rejects_duplicate_dimension(self):
        import validate_layout

        bad = _common.Layout(
            root_reserved=frozenset({"content"}),
            themes={"x": ("X", ("region", "region"))},
            regions=frozenset({"dubai"}),
            naming_pattern=r"^[a-z0-9]+$",
            max_depth=4,
        )
        validate_layout.ERRORS.clear()
        try:
            validate_layout.check_dimension_priority(bad)
            self.assertTrue(
                any("重复" in e for e in validate_layout.ERRORS), validate_layout.ERRORS
            )
        finally:
            validate_layout.ERRORS.clear()

    def test_validator_rejects_unknown_dimension(self):
        import validate_layout

        bad = _common.Layout(
            root_reserved=frozenset({"content"}),
            themes={"x": ("X", ("region", "sector_x"))},
            regions=frozenset({"dubai"}),
            naming_pattern=r"^[a-z0-9]+$",
            max_depth=4,
        )
        validate_layout.ERRORS.clear()
        try:
            validate_layout.check_dimension_priority(bad)
            self.assertTrue(
                any("未登记维度名" in e for e in validate_layout.ERRORS), validate_layout.ERRORS
            )
        finally:
            validate_layout.ERRORS.clear()

    def test_every_business_segments_follow_declared_order(self):
        for b in _common.iter_business_dirs():
            dims = self.layout.dimensions(b.theme)
            optional = self.layout.optional_dims(b.theme)
            segs = list(b.segments)
            allowed = {len(dims)}
            if "region" in dims and "region" in optional:
                allowed.add(len(dims) - 1)
            self.assertIn(len(segs), allowed, f"{b.rel}: 段数与维度数不符")
            mapping = _common.resolve_segments(self.layout, b.theme, tuple(segs))
            region = mapping.get("region")
            if region is not None:
                self.assertIn(region, self.layout.regions, f"{b.rel}: region 段 {region} 不在白名单")

    def test_property_type_is_not_region(self):
        for b in _common.iter_business_dirs():
            self.assertNotEqual(b.property_type, b.region, b.rel)


class TestCheckLinks(unittest.TestCase):
    """路径引用可达性校验（check_links.py）。"""

    @classmethod
    def setUpClass(cls):
        import check_links

        cls.cl = check_links

    def test_case_ok_matches_disk(self):
        good = self.cl.ROOT / "content/economy/dubai/apartment/reports/2026-Q3_quarterly.html"
        self.assertTrue(good.exists())
        self.assertTrue(self.cl._case_ok(good))

    def test_case_ok_rejects_wrong_case(self):
        # Windows 大小写不敏感会 exists() 为真，但 Linux（CI）会为断链
        bad = self.cl.ROOT / "content/economy/dubai/apartment/reports/2026-q3_quarterly.html"
        self.assertFalse(self.cl._case_ok(bad))

    def test_data_search_lowercase_index_ignored(self):
        # build_hub 生成的 data-search 是小写化搜索索引，非真实引用
        p = self.cl.ROOT / "index.html"
        rel = "index.html"
        roots = self.cl.known_roots()
        broken = self.cl.check_file(p, rel, roots)
        self.assertEqual([b for b in broken if "data-search" in b[1]], [])
        # 全文件扫描应无断链
        self.assertEqual(broken, [])

    def test_check_links_passes_repo(self):
        import io
        import sys as _sys
        from contextlib import redirect_stdout

        buf = io.StringIO()
        argv = _sys.argv
        _sys.argv = ["check_links.py"]
        try:
            with redirect_stdout(buf):
                code = self.cl.main()
        finally:
            _sys.argv = argv
        self.assertEqual(code, 0, buf.getvalue())
