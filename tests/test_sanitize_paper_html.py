"""Tests for scripts/sanitize_paper_html.py."""

from pathlib import Path

import pytest

from scripts.sanitize_paper_html import main, sanitize_paper_body_fragment


def test_sanitize_paper_body_fragment_strips_script() -> None:
    dirty = "<p>ok</p><script>alert(1)</script>"
    clean = sanitize_paper_body_fragment(dirty)
    assert "script" not in clean.lower()
    assert "ok" in clean
    assert "<p>" in clean


def test_sanitize_paper_body_fragment_strips_onerror() -> None:
    dirty = '<p>x</p><img src=x onerror="alert(1)">'
    clean = sanitize_paper_body_fragment(dirty)
    assert "onerror" not in clean.lower()


def test_sanitize_paper_body_fragment_keeps_safe_markup() -> None:
    dirty = (
        '<div class="highlighter-rouge"><pre class="highlight"><code>'
        '<span class="n">print</span>(1)\n</code></pre></div>'
    )
    clean = sanitize_paper_body_fragment(dirty)
    assert "highlighter-rouge" in clean
    assert "print" in clean


@pytest.mark.parametrize(
    ("snippet", "forbidden"),
    [
        ('<a href="javascript:alert(1)">x</a>', "javascript:"),
        ('<iframe src="https://evil"></iframe>', "iframe"),
    ],
)
def test_sanitize_paper_body_fragment_blocks_vectors(snippet: str, forbidden: str) -> None:
    clean = sanitize_paper_body_fragment(snippet)
    assert forbidden.lower() not in clean.lower()


def test_main_rewrites_built_paper_file(tmp_path: Path) -> None:
    site_root = tmp_path / "_site"
    paper = site_root / "papers" / "01_Cat" / "Note" / "Note.html"
    paper.parent.mkdir(parents=True)
    paper.write_text(
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head>"
        '<body><div id="paper-body"><p>hi</p><script>evil()</script></div></body></html>',
        encoding="utf-8",
    )
    assert main([str(site_root)]) == 0
    out = paper.read_text(encoding="utf-8")
    assert "evil()" not in out
    assert "hi" in out
