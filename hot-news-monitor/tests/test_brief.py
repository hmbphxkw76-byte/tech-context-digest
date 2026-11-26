"""专题数据与报告渲染单元测试。"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import brief as brief_mod  # noqa: E402
from app.verify_brief import check_links, check_structure, verify_brief  # noqa: E402

BRIEF_PATH = Path(__file__).resolve().parents[1] / "config" / "nvidia-brief-2026-11-26.json"


class TestBriefData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(BRIEF_PATH.read_text(encoding="utf-8"))

    def test_structure_ok(self):
        self.assertEqual(check_structure(self.data), [])

    def test_links_ok(self):
        rows = check_links(self.data)
        self.assertFalse(any(r["problems"] for r in rows))

    def test_verify_no_probe(self):
        rep = verify_brief(self.data, do_probe=False)
        self.assertTrue(rep["ok"])
        self.assertEqual(rep["reachable"], {})

    def test_render_sections(self):
        html = brief_mod.render(self.data)
        for marker in ("决策摘要", "决策卡", "多信源交叉验证", "事件发展时间线", "来源清单", "覆盖缺口",
                       "已核验", "部分核验", "待核实", 'id="src-S1"', "data-tier=", "#tierFilter"):
            self.assertIn(marker, html)
        self.assertIn('lang="zh-CN"', html)

    def test_summary_refs_exist(self):
        refs = {s.get("ref") for s in self.data["sources"]}
        for line in self.data["summary_zh"]:
            for token in [t for t in line.split("[") if t.endswith("]")]:
                ref = token[:-1]
                self.assertIn(ref, refs, f"摘要引用 {ref} 不存在于来源")


if __name__ == "__main__":
    unittest.main()
