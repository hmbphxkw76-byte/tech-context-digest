"""专题数据、报告渲染与轮换机制单元测试。"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import brief as brief_mod  # noqa: E402
from app.verify_brief import check_links, check_structure, verify_brief  # noqa: E402

BRIEF_DIR = Path(__file__).resolve().parents[1] / "config" / "briefs"


class TestBriefData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads((BRIEF_DIR / "nvidia-2026-11-26.json").read_text(encoding="utf-8"))
        cls.manifest = json.loads((BRIEF_DIR / "index.json").read_text(encoding="utf-8"))

    def test_structure_ok(self):
        self.assertEqual(check_structure(self.data), [])

    def test_links_ok(self):
        rows = check_links(self.data)
        self.assertFalse(any(r["problems"] for r in rows))

    def test_verify_no_probe(self):
        rep = verify_brief(self.data, do_probe=False)
        self.assertTrue(rep["ok"])

    def test_render_sections(self):
        html = brief_mod.render(self.data, data_file_label="nvidia-2026-11-26.json")
        for marker in ("决策摘要", "决策卡", "多信源交叉验证", "事件发展时间线", "来源清单", "覆盖缺口",
                       "已核验", "部分核验", "待核实", 'id="src-S1"', "data-tier=", "#tierFilter"):
            self.assertIn(marker, html)
        self.assertIn('lang="zh-CN"', html)

    def test_summary_refs_exist(self):
        refs = {s.get("ref") for s in self.data["sources"]}
        for line in self.data["summary_zh"]:
            for token in [t for t in line.split("[") if t.endswith("]")]:
                self.assertIn(token[:-1], refs)

    def test_manifest_shape(self):
        briefs = self.manifest["briefs"]
        self.assertTrue(briefs)
        for b in briefs:
            self.assertTrue((BRIEF_DIR / b["data_file"]).is_file())
            self.assertIn(b["status"], ("active", "hidden"))
            self.assertTrue(b["out_name"].startswith("brief-"))

    def test_heat_tier_mapping(self):
        self.assertEqual(brief_mod.heat_tier(50, 50)[0], "热")
        self.assertEqual(brief_mod.heat_tier(25, 50)[0], "高")
        self.assertEqual(brief_mod.heat_tier(24.9, 50)[0], "中")

    def test_render_current_rotates_and_matches(self):
        state = {
            "generated_at": "2026-11-26T00:00:00Z",
            "mode": "live",
            "threshold": 50,
            "events": [{
                "id": "abc123", "title": "NVIDIA CEO reinstated amid chip export debate",
                "tag": "科技", "heat": 61.5, "level": 1,
                "source_ids": ["s1", "s2"],
                "items": [
                    {"published_at": "2026-11-23T00:00:00Z", "tier": "official", "source_name": "NVIDIA",
                     "title": "Board reinstates Jensen Huang", "url": "https://example.org/a"},
                    {"published_at": "2026-11-22T00:00:00Z", "tier": "media_t1", "source_name": "CNBC",
                     "title": "Huang returns as CEO", "url": "https://example.org/b"},
                ],
                "heat_series": [{"ts": "2026-11-26T00:00:00Z", "value": 61.5}],
            }],
        }
        html = brief_mod.render_current(state, self.manifest)
        self.assertIn("NVIDIA CEO reinstated", html)           # 标题随事件滚动
        self.assertIn("编译层", html)                          # 命中 Nvidia 关键词
        self.assertIn("#event/abc123", html)
        # 未命中场景（事件标题与关联报道均不含已登记关键词）
        other = json.loads(json.dumps(state))
        other["events"][0]["title"] = "Some unrelated shipping story"
        for it in other["events"][0]["items"]:
            it["title"] = "Local port authority announces new schedule"
            it["source_name"] = "Port Gazette"
        html2 = brief_mod.render_current(other, self.manifest)
        self.assertNotIn("编译层", html2)
        self.assertIn("机械聚合视图", html2)

    def test_rebuild_all_writes_pages(self):
        with tempfile.TemporaryDirectory() as td:
            written = brief_mod.rebuild_all(Path(td))
            names = sorted(p.name for p in written)
            self.assertIn("brief-nvidia-2026-11-26.html", names)
            self.assertIn("brief-current.html", names)  # 无快照时为占位页
            cur = (Path(td) / "brief-current.html").read_text(encoding="utf-8")
            self.assertTrue(("当前热点" in cur) or ("热点事件专题" in cur))  # 有快照=事件标题；无快照=占位


if __name__ == "__main__":
    unittest.main()
