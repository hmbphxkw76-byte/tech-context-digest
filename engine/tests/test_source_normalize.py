# -*- coding: utf-8 -*-
"""来源归一化测试（INFORMATION-VERIFICATION-SPEC v1.0 第五节）。

运行：python -m unittest discover -s engine/tests -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from source_normalize import (  # noqa: E402
    host_key,
    normalize_date,
    normalize_publisher,
    normalize_url,
)


class TestUrl(unittest.TestCase):
    def test_lowercase_scheme_host_keep_path(self):
        self.assertEqual(normalize_url("HTTPS://WWW.Example.COM/Path/To"),
                         "https://www.example.com/Path/To")

    def test_strip_fragment(self):
        self.assertEqual(normalize_url("https://x.com/a#frag"), "https://x.com/a")

    def test_strip_tracking_params(self):
        self.assertEqual(normalize_url("https://x.com/a?utm_source=y&b=2&gclid=z"),
                         "https://x.com/a?b=2")

    def test_empty_and_non_string(self):
        self.assertEqual(normalize_url(""), "")
        self.assertEqual(normalize_url(None), "")


class TestPublisher(unittest.TestCase):
    def test_whitespace_and_fullwidth(self):
        self.assertEqual(normalize_publisher("  Central  Bank  of  X "),
                         "Central Bank of X")

    def test_edge_punct(self):
        self.assertEqual(normalize_publisher("...Bank of X."), "Bank of X")


class TestHostKey(unittest.TestCase):
    def test_register_domain(self):
        self.assertEqual(host_key("https://www.example.com/a"), "example.com")
        self.assertEqual(host_key("https://sub.example.co.uk/x"), "sub.example.co.uk")
        self.assertEqual(host_key(""), "")


class TestDate(unittest.TestCase):
    def test_iso_variants(self):
        self.assertEqual(normalize_date("2026-11-18"), "2026-11-18")
        self.assertEqual(normalize_date("2026/11/18"), "2026-11-18")
        self.assertEqual(normalize_date("2026.11.18"), "2026-11-18")

    def test_chinese(self):
        self.assertEqual(normalize_date("2026年11月18日"), "2026-11-18")

    def test_english(self):
        self.assertEqual(normalize_date("18 March 2026"), "2026-03-18")
        self.assertEqual(normalize_date("March 18, 2026"), "2026-03-18")

    def test_invalid(self):
        for bad in ("", None, "not-a-date", "2026-13-01"):
            self.assertIsNone(normalize_date(bad), bad)


if __name__ == "__main__":
    unittest.main()
