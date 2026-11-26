"""抓取解析 / 存储 / 流水线 / API / 抽样核验 单元测试。"""
from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.fetch import parse_feed, probe  # noqa: E402
from app.models import HotEvent, NewsItem, Snapshot  # noqa: E402
from app.pipeline import refresh  # noqa: E402
from app.server import make_server  # noqa: E402
from app.store import Store  # noqa: E402
from app.verify import verify_items  # noqa: E402

RSS_XML = b"""<?xml version="1.0"?><rss version="2.0"><channel>
<item><title>Fed holds rates</title><link>https://src.example/a</link>
<pubDate>Tue, 25 Nov 2026 10:00:00 GMT</pubDate><description>Rate decision</description></item>
<item><title>Climate talks</title><link>https://src.example/b</link>
<pubDate>2026-11-25T09:00:00Z</pubDate><description>Summit</description></item>
</channel></rss>"""

ATOM_XML = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>Energy market update</title><link href="https://src.example/c"/>
<updated>2026-11-25T08:00:00Z</updated><summary>Oil steady</summary></entry>
</feed>"""


class TestFetchParse(unittest.TestCase):
    SRC = {"id": "s", "name": "S", "tier": "media"}

    def test_rss_parse(self):
        items = parse_feed(RSS_XML, self.SRC)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].published_at, "2026-11-25T10:00:00Z")
        self.assertTrue(items[0].url.startswith("https://"))

    def test_atom_parse(self):
        items = parse_feed(ATOM_XML, self.SRC)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "Energy market update")

    def test_probe_bad_url(self):
        st = probe("http://127.0.0.1:1/none", timeout=2)
        self.assertFalse(st["ok"])


class TestStore(unittest.TestCase):
    def test_roundtrip_and_prev_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            store = Store(Path(td))
            snap = Snapshot(generated_at="2026-11-26T00:00:00Z", interval_seconds=300,
                            mode="seed", threshold=50, events=[], source_status=[], metrics={})
            store.save_state(snap)
            loaded = store.load_state()
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.interval_seconds, 300)
            store.state_path.write_text("{ broken", encoding="utf-8")
            fallback = store.load_state()
            self.assertIsNotNone(fallback)  # 回退 state.prev.json
            self.assertEqual(fallback.mode, "seed")

    def test_append_items_dedupe(self):
        with tempfile.TemporaryDirectory() as td:
            store = Store(Path(td))
            it = NewsItem(id="i1", title="t", url="u", source_id="s", source_name="n",
                          tier="media", published_at="2026-11-26T00:00:00Z")
            self.assertEqual(store.append_items([it]), 1)
            self.assertEqual(store.append_items([it]), 0)


class TestPipelineSeed(unittest.TestCase):
    def test_seed_mode_when_no_sources(self):
        with tempfile.TemporaryDirectory() as td:
            store = Store(Path(td))
            snap = refresh(store, config={"sources": [], "heat_weights": {
                "official": 3.0, "rating": 3.0, "media_t1": 2.5, "media": 2.0}},
                threshold=50, interval_seconds=300)
            self.assertEqual(snap.mode, "seed")
            self.assertGreater(len(snap.events), 5)
            self.assertTrue(all(e.level in (1, 2, 3) for e in snap.events))


class TestApi(unittest.TestCase):
    def test_endpoints(self):
        with tempfile.TemporaryDirectory() as td:
            store = Store(Path(td))
            srv = make_server("127.0.0.1", 0, store, threshold=50, interval=300,
                              config={"sources": [], "heat_weights": {
                                  "official": 3.0, "rating": 3.0, "media_t1": 2.5, "media": 2.0}})
            port = srv.server_address[1]
            th = threading.Thread(target=srv.serve_forever, daemon=True)
            th.start()
            try:
                base = f"http://127.0.0.1:{port}"
                state = json.loads(urllib.request.urlopen(base + "/api/state", timeout=10).read())
                self.assertEqual(state["mode"], "seed")
                eid = state["events"][0]["id"]
                detail = json.loads(urllib.request.urlopen(base + f"/api/events/{eid}", timeout=10).read())
                self.assertIn("timeline", detail)
                health = json.loads(urllib.request.urlopen(base + "/api/health", timeout=10).read())
                self.assertTrue(health["ok"])
            finally:
                srv.shutdown()
                srv.server_close()


class TestVerify(unittest.TestCase):
    def _snap_with(self, item: NewsItem) -> Snapshot:
        ev = HotEvent(id=item.id, title=item.title, tag="国际要闻", heat=10, level=2,
                      first_seen=item.published_at, last_seen=item.published_at,
                      source_ids=[item.source_id], items=[item])
        return Snapshot(generated_at="2026-11-26T00:00:00Z", interval_seconds=300,
                        mode="live", threshold=50, events=[ev], source_status=[], metrics={})

    def test_demo_not_counted(self):
        demo = NewsItem(id="d1", title="demo", url="", source_id="bbc-world", source_name="BBC",
                        tier="media_t1", published_at="2026-11-26T00:00:00Z", is_demo=True)
        rep = verify_items(self._snap_with(demo), n=100)
        self.assertEqual(rep["real_items"], 0)
        self.assertEqual(rep["failed"], [])

    def test_forbidden_host_flagged(self):
        bad = NewsItem(id="x1", title="bad item here", url="https://www.globaltimes.cn/x",
                       source_id="unknown-src", source_name="X", tier="media",
                       published_at="2026-11-26T00:00:00Z")
        rep = verify_items(self._snap_with(bad), n=100)
        problems = ",".join(f["problems"] for f in rep["failed"])
        self.assertIn("forbidden_chinese_media_host", problems)
        self.assertIn("source_not_whitelisted", problems)


if __name__ == "__main__":
    unittest.main()
