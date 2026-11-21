# -*- coding: utf-8 -*-
"""核验台账哈希链测试（INFORMATION-VERIFICATION-SPEC v1.0 第三节）。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from verification_ledger import (  # noqa: E402
    GENESIS_HASH,
    append,
    backfill_from_registries,
    compute_hash,
    iter_events,
    last_event,
    verify,
)


class TestHashChain(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "ledger.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_ledger_is_ok(self):
        ok, problems, stats = verify(self.path)
        self.assertTrue(ok)
        self.assertEqual(problems, [])
        self.assertEqual(stats["records"], 0)

    def test_append_and_verify(self):
        append("source_verified", {"business_line": "content/a/b", "source_id": "S-1"},
               actor="test", ledger_path=self.path)
        append("source_reviewed", {"business_line": "content/a/b", "source_id": "S-2"},
               actor="test", ledger_path=self.path)
        ok, problems, stats = verify(self.path)
        self.assertTrue(ok, problems)
        self.assertEqual(stats["records"], 2)
        evs = iter_events(self.path)
        self.assertEqual([e["seq"] for e in evs], [1, 2])
        self.assertEqual(evs[0]["prev_hash"], GENESIS_HASH)
        self.assertEqual(evs[1]["prev_hash"], evs[0]["hash"])

    def test_hash_is_deterministic(self):
        payload = {"b": 2, "a": 1}
        self.assertEqual(compute_hash(GENESIS_HASH, payload),
                         compute_hash(GENESIS_HASH, payload))

    def test_tamper_detected(self):
        append("source_verified", {"business_line": "content/a/b", "source_id": "S-1"},
               ledger_path=self.path)
        lines = self.path.read_text(encoding="utf-8").splitlines()
        rec = json.loads(lines[0])
        rec["payload"]["source_id"] = "S-999"
        lines[0] = json.dumps(rec, ensure_ascii=False, sort_keys=True)
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        ok, problems, _ = verify(self.path)
        self.assertFalse(ok)
        self.assertTrue(any("hash" in p for p in problems))

    def test_broken_link_detected(self):
        append("source_verified", {"business_line": "content/a/b", "source_id": "S-1"},
               ledger_path=self.path)
        append("source_reviewed", {"business_line": "content/a/b", "source_id": "S-2"},
               ledger_path=self.path)
        lines = self.path.read_text(encoding="utf-8").splitlines()
        rec = json.loads(lines[1])
        rec["prev_hash"] = "f" * 64
        lines[1] = json.dumps(rec, ensure_ascii=False, sort_keys=True)
        self.path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        ok, problems, _ = verify(self.path)
        self.assertFalse(ok)
        self.assertTrue(any("prev_hash" in p for p in problems))

    def test_unknown_event_rejected(self):
        with self.assertRaises(ValueError):
            append("nope", {}, ledger_path=self.path)

    def test_last_event(self):
        self.assertIsNone(last_event(self.path))
        append("source_verified", {"source_id": "S-1"}, ledger_path=self.path)
        self.assertEqual(last_event(self.path)["seq"], 1)

    def test_backfill_idempotent(self):
        # 空台账回填一次；非空台账再次回填应跳过（幂等，不重复追加）
        n1 = backfill_from_registries(ledger_path=self.path)
        n2 = backfill_from_registries(ledger_path=self.path)
        self.assertEqual(n2, 0)
        self.assertEqual(len(iter_events(self.path)), n1)
        self.assertTrue(verify(self.path)[0])


if __name__ == "__main__":
    unittest.main()
