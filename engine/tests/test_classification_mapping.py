# -*- coding: utf-8 -*-
"""分类口径映射校验（P0-5）：十二类 ↔ 注册类型 ↔ 规则文件 ↔ 业务配置。"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine" / "tools"))

from _common import TEMPLATE_TYPE_DIRS, business_report_type, iter_business_dirs  # noqa: E402

RULES = ROOT / "engine" / "templates" / "compliance-rules.json"
REGISTRY_MD = ROOT / "engine" / "templates" / "template-registry.md"
DOC_MD = ROOT / "engine" / "docs" / "report-classification.md"

# 六族十二类（领域口径）→ 注册类型 ID
TAXONOMY_12 = {
    "A1 市场指标监测型": "market-monitoring",
    "A2 竞争情报监测型": "competitive-intelligence",
    "A3 舆情传播监测型": "sentiment-monitoring",
    "B1 职业就业调研型": "employment-research",
    "B2 消费者·用户调研型": "consumer-research",
    "C1 行业深度研究型": "industry-research",
    "C2 市场规模测算与预测型": "market-sizing",
    "D1 投资分析与尽调型": "investment-research",
    "D2 政策法规解读型": "policy-analysis",
    "D3 可行性与市场进入型": "feasibility-study",
    "E1 快评·事件点评型": "flash-commentary",
    "F1 白皮书·专题深度型": "whitepaper",
}


def _registry_type_ids() -> set[str]:
    """解析 template-registry.md 第二节类型清单表。"""
    text = REGISTRY_MD.read_text(encoding="utf-8")
    sec = text.split("## 二、已注册类型清单", 1)[1].split("## 三、", 1)[0]
    return set(re.findall(r"^\| ([a-z0-9-]+) \|", sec, re.M))


class TestMappingConsistency(unittest.TestCase):
    def test_rules_template_common_equal(self):
        rules = json.loads(RULES.read_text(encoding="utf-8"))
        self.assertEqual(set(rules["types"]), set(TEMPLATE_TYPE_DIRS))
        self.assertEqual(set(rules["types"]), _registry_type_ids())

    def test_twelve_categories_all_registered(self):
        rules = json.loads(RULES.read_text(encoding="utf-8"))
        for cat, tid in TAXONOMY_12.items():
            self.assertIn(tid, rules["types"], cat)

    def test_extension_types_documented(self):
        """A4 行业趋势周报型为十二类之外的注册扩展类型。"""
        self.assertIn("trend-weekly", TEMPLATE_TYPE_DIRS)
        self.assertNotIn("A4", TAXONOMY_12)

    def test_docs_have_mapping_and_no_stale_text(self):
        doc = DOC_MD.read_text(encoding="utf-8")
        self.assertIn("十二类 ↔ 注册类型映射", doc)
        self.assertNotIn("已有两类接入", doc)


class TestStructuredTypeDeclaration(unittest.TestCase):
    def test_all_business_configs_structured(self):
        for b in iter_business_dirs():
            tid, structured, note = business_report_type(b)
            self.assertTrue(tid, b.rel)
            self.assertTrue(structured, f"{b.rel}: 缺 {{{{REPORT_TYPE}}}} 结构化声明")

    def test_declaration_matches_template_ref(self):
        for b in iter_business_dirs():
            cfg = b.path / "prompts" / "business-config.md"
            text = cfg.read_text(encoding="utf-8")
            var = re.search(r"\{\{REPORT_TYPE\}\}\s*=\s*([a-z0-9-]+)", text)
            ref = re.search(r"engine/templates/([a-z0-9-]+)/", text)
            self.assertIsNotNone(var, b.rel)
            if ref:
                self.assertEqual(var.group(1), ref.group(1), b.rel)


if __name__ == "__main__":
    unittest.main()
