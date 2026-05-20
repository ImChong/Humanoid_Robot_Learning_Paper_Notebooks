"""Regression: headings with parenthetical inline code must not break across lines."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "assets" / "css" / "style.css"
PAPER_JS = ROOT / "assets" / "js" / "paper.js"


def test_heading_code_phrase_css():
    text = STYLE.read_text(encoding="utf-8")
    assert ".paper-body .heading-code-phrase" in text
    idx = text.index(".paper-body .heading-code-phrase")
    block = text[idx : idx + 120]
    assert "white-space: nowrap" in block


def test_wrap_heading_inline_code_phrases_in_paper_js():
    text = PAPER_JS.read_text(encoding="utf-8")
    assert "function wrapHeadingInlineCodePhrases()" in text
    assert "heading-code-phrase" in text
    assert "wrapHeadingInlineCodePhrases();" in text
