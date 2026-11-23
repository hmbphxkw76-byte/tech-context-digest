"""生成物重生成比对自检（REGEN-DRIFT-CHECK v1.0）。"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import regen_drift_check as rdc  # noqa: E402


class TestNormalize(unittest.TestCase):
    def test_strips_timestamp_value(self) -> None:
        a = "> 最近生成：2026-11-23 11:03 UTC（由 engine/tools/build_index.py 自动维护）"
        b = "> 最近生成：2026-12-01 08:00 UTC（由 engine/tools/build_index.py 自动维护）"
        self.assertEqual(rdc._normalize(a, "最近生成"), rdc._normalize(b, "最近生成"))

    def test_strips_iso_timestamp_embedded_in_line(self) -> None:
        a = "> 由 `script/vocab_tool.py index` 自动生成。生成时间：2026-11-24T06:24:14"
        b = "> 由 `script/vocab_tool.py index` 自动生成。生成时间：2027-01-01T00:00:00"
        self.assertEqual(rdc._normalize(a, "生成时间"), rdc._normalize(b, "生成时间"))

    def test_keeps_real_content_difference(self) -> None:
        self.assertNotEqual(rdc._normalize("| tech | 273 |", "生成时间"),
                            rdc._normalize("| tech | 282 |", "生成时间"))

    def test_none_and_no_marker(self) -> None:
        self.assertEqual(rdc._normalize(None, "生成时间"), "")
        self.assertEqual(rdc._normalize("abc", ""), "abc")


class TestCheck(unittest.TestCase):
    """对当前工作树重放生成器：应无漂移，且不得改动任何文件。"""

    def test_no_drift_and_non_destructive(self) -> None:
        targets = [rdc.ROOT / o for g in rdc._GROUPS for o in g.outputs]
        before = {p: p.read_bytes() for p in targets}
        try:
            drift = rdc.check()
        finally:
            after = {p: p.read_bytes() for p in targets}
        self.assertEqual(after, before, "检查必须是只读的（字节级还原）")
        if drift:  # 工作树未提交时不强制；仅在干净树上断言
            import subprocess
            dirty = subprocess.run(["git", "status", "--porcelain"], cwd=rdc.ROOT,
                                   capture_output=True, text=True).stdout.strip()
            if not dirty:
                self.fail(f"已提交树仍有漂移：{drift}")


if __name__ == "__main__":
    unittest.main()
