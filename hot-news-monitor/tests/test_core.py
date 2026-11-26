"""聚合与模型单元测试。"""
from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.aggregate import (  # noqa: E402
    background_note,
    build_events,
    build_metrics,
    classify,
    cluster,
    compute_heat,
    jaccard,
    tokenize,
)
from app.models import HeatPoint, HotEvent, NewsItem  # noqa: E402


def _item(iid: str, title: str, source: str, tier: str = "media_t1",
          age_h: float = 1.0, url: str = "") -> NewsItem:
    ts = (datetime.now(timezone.utc) - timedelta(hours=age_h)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return NewsItem(id=iid, title=title, url=url or f"https://example.org/{iid}",
                    source_id=source, source_name=f"Source {source}", tier=tier, published_at=ts)


class TestClassify(unittest.TestCase):
    def test_keyword_mapping(self):
        self.assertEqual(classify("Federal Reserve holds interest rates steady"), "金融")
        self.assertEqual(classify("OPEC+ weighs output increase as oil prices steady"), "能源")
        self.assertEqual(classify("Something completely unrelated zzz"), "国际要闻")

    def test_tokenize_stopwords(self):
        toks = tokenize("The President and the Parliament")
        self.assertIn("president", toks)
        self.assertNotIn("the", toks)

    def test_jaccard(self):
        self.assertAlmostEqual(jaccard({"a", "b"}, {"b", "c"}), 1 / 3)


class TestCluster(unittest.TestCase):
    def test_same_event_merged(self):
        items = [
            _item("1", "Strait of Hormuz shipping reroutes after security warnings", "s1"),
            _item("2", "Strait of Hormuz ships reroute amid war-risk insurance surge", "s2"),
        ]
        groups = cluster(items)
        self.assertEqual(len(groups), 1)
        self.assertEqual(len(groups[0]), 2)

    def test_different_events_split(self):
        items = [
            _item("1", "Federal Reserve holds interest rates steady", "s1"),
            _item("2", "Climate summit negotiators clash over emission targets", "s2"),
        ]
        self.assertEqual(len(cluster(items)), 2)


class TestHeatAndEvents(unittest.TestCase):
    WEIGHTS = {"official": 3.0, "rating": 3.0, "media_t1": 2.5, "media": 2.0}

    def test_heat_decay_and_cap(self):
        now = datetime.now(timezone.utc)
        fresh = [_item(f"f{i}", f"Crisis talk {i} continues", "s", "media_t1", age_h=0.1) for i in range(3)]
        old = [_item(f"o{i}", f"Crisis talk {i} continues", "s", "media_t1", age_h=200) for i in range(3)]
        h_fresh = compute_heat(fresh, self.WEIGHTS, now)
        h_old = compute_heat(old, self.WEIGHTS, now)
        self.assertGreater(h_fresh, h_old)
        self.assertLessEqual(compute_heat(fresh * 20, self.WEIGHTS, now), 100.0)

    def test_build_events_levels_and_series(self):
        now = datetime.now(timezone.utc)
        items = [
            _item("a", "Fed signals rate path shift", "nyt", "media_t1", 0.2),
            _item("b", "Fed rate path shift rattles markets", "wapo", "media_t1", 1.0),
            _item("c", "Fed shift on rates draws reactions", "pbs", "media", 2.0),
            _item("d", "Totally different space launch story", "bbc", "media_t1", 0.5),
        ]
        prev = [HotEvent(id="c", title="Fed signals rate path shift", tag="金融", heat=40,
                         level=2, first_seen="", last_seen="", source_ids=["pbs"],
                         items=[items[2]], heat_series=[HeatPoint(ts="2026-11-26T00:00:00Z", value=40)])]
        events = build_events(items, prev, self.WEIGHTS, threshold=50, now=now, interval_seconds=300)
        self.assertGreaterEqual(len(events), 2)
        fed = [e for e in events if e.id == "c"]  # 事件 id 取簇内最早报道 c
        self.assertTrue(fed)
        self.assertGreaterEqual(fed[0].level, 1)  # 三源交叉，超过阈值
        self.assertEqual(fed[0].tag, "金融")
        self.assertGreater(len(fed[0].heat_series), 1)
        m = build_metrics(events, len(items))
        self.assertEqual(m["total_events"], len(events))

    def test_background_note(self):
        ev = HotEvent(id="x", title="t", tag="政治", heat=10, level=2, first_seen="", last_seen="",
                      source_ids=["a", "b"], items=[_item("1", "x y z", "a"), _item("2", "x y", "b")])
        note = background_note(ev)
        self.assertIn("2 家独立信源", note)
        self.assertIn("不足三家", note)


if __name__ == "__main__":
    unittest.main()
