"""md2html 外链 noopener 后处理（MON-04 的生成器侧修复）。

md 源里的行内 HTML 由 markdown 包原样透传，不会自动带 target/rel；
缺失会触发 MON-04，且 html-sync 重生成时会回退对产物的手工修补。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from md2html import _fix_links, _preserve_audit_mark  # noqa: E402


class TestFixLinks(unittest.TestCase):
    def test_adds_target_and_noopener(self) -> None:
        out = _fix_links('<a href="https://example.org/x">来源</a>')
        self.assertIn('target="_blank"', out)
        self.assertIn('rel="noopener"', out)

    def test_idempotent(self) -> None:
        once = _fix_links('<a href="https://example.org/x">来源</a>')
        self.assertEqual(_fix_links(once), once)

    def test_keeps_existing_target_and_rel(self) -> None:
        html = '<a href="https://example.org/x" target="_blank" rel="noopener">来源</a>'
        self.assertEqual(_fix_links(html), html)

    def test_adds_rel_when_only_target_present(self) -> None:
        out = _fix_links('<a href="https://example.org/x" target="_blank">来源</a>')
        self.assertIn("rel=", out)
        self.assertIn('target="_blank"', out)

    def test_ignores_internal_anchor(self) -> None:
        html = '<a href="#s1">章节</a>'
        self.assertEqual(_fix_links(html), html)

    def test_supports_single_quoted_href(self) -> None:
        out = _fix_links("<a href='https://example.org/x'>来源</a>")
        self.assertIn('target="_blank"', out)
        self.assertIn('rel="noopener"', out)

    def test_preserves_other_attributes(self) -> None:
        out = _fix_links('<a class="src" href="https://example.org/x">来源</a>')
        self.assertIn('class="src"', out)
        self.assertIn('target="_blank"', out)


class TestPreserveAuditMark(unittest.TestCase):
    MARK = '<div class="audit-mark" data-audit-id="a1">已审计</div>'

    def test_preserves_existing_mark(self) -> None:
        old = "<html><body>\n" + self.MARK + "\n</body></html>"
        new = "<html><body>\n<p>x</p>\n</body></html>"
        self.assertIn(self.MARK, _preserve_audit_mark(old, new))

    def test_no_mark_in_old(self) -> None:
        new = "<html><body></body></html>"
        self.assertEqual(_preserve_audit_mark("<html><body></body></html>", new), new)

    def test_no_old_html(self) -> None:
        new = "<html><body></body></html>"
        self.assertEqual(_preserve_audit_mark(None, new), new)

    def test_idempotent_when_already_present(self) -> None:
        old = "<html><body>\n" + self.MARK + "\n</body></html>"
        new = "<html><body>\n" + self.MARK + "\n</body></html>"
        self.assertEqual(_preserve_audit_mark(old, new), new)


if __name__ == "__main__":
    unittest.main()
