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


def test_mobile_rouge_block_rule_does_not_target_inline_code():
    """``display: block`` on ``.highlighter-rouge`` must not apply to ``code`` in headings."""
    block = _mobile_paper_body_block()
    idx = block.index("Rouge block wrapper only")
    snippet = block[idx : idx + 320]
    assert ".paper-body div.highlighter-rouge" in snippet
    assert "display: block" in snippet
    assert ".paper-body .highlighter-rouge {" not in block


def _mobile_paper_body_block() -> str:
    text = STYLE.read_text(encoding="utf-8")
    marker = ".paper-body .table-wrapper"
    table_idx = text.find(marker, text.find("@media (max-width: 1200px)"))
    assert table_idx != -1
    start = text.rfind("@media (max-width: 1200px)", 0, table_idx)
    assert start != -1
    return text[start:]
