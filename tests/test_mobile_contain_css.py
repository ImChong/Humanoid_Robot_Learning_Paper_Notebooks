"""Regression: mobile ``contain: strict`` on tables/code must not collapse height."""

from pathlib import Path

STYLE = Path(__file__).resolve().parents[1] / "assets" / "css" / "style.css"


def _mobile_paper_body_block() -> str:
    text = STYLE.read_text(encoding="utf-8")
    marker = ".paper-body .table-wrapper"
    table_idx = text.find(marker)
    assert table_idx != -1, "table-wrapper mobile rules missing"
    start = text.rfind("@media (max-width: 1200px)", 0, table_idx)
    assert start != -1, "mobile paper-body block missing"
    return text[start:]


def _assert_uses_inline_size_only(snippet: str) -> None:
    """Property lines only — ignore comments that mention ``strict``."""
    for line in snippet.splitlines():
        stripped = line.strip()
        if stripped.startswith("/*") or stripped.startswith("*"):
            continue
        assert "contain: strict" not in stripped


def test_mobile_table_wrapper_not_contain_strict():
    block = _mobile_paper_body_block()
    idx = block.index(".paper-body .table-wrapper")
    _assert_uses_inline_size_only(block[idx : idx + 200])


def test_mobile_code_block_not_contain_strict():
    block = _mobile_paper_body_block()
    idx = block.index(".paper-body .code-block")
    _assert_uses_inline_size_only(block[idx : idx + 320])


def test_mobile_code_wraps_not_per_line_scroll():
    """Mobile code blocks must wrap (no horizontal scroll). The earlier per-row
    ``overflow-x: auto`` on ``.code-cell`` caused finger-tracked iOS overlay
    scrollbars; switching the block to wrap keeps content on screen instead."""
    block = _mobile_paper_body_block()
    snippet = block[block.index(".paper-body .code-block") :]
    snippet = snippet[: snippet.index(".paper-body .table-wrapper")]
    # Block itself does not scroll horizontally on mobile.
    assert "overflow-x: hidden" in snippet
    assert "overflow-x: auto" not in snippet
    # Cell wraps with pre-wrap + overflow-wrap so long lines fold to the next line.
    assert "white-space: pre-wrap" in snippet
    assert "overflow-wrap: anywhere" in snippet


def test_mobile_inline_code_does_not_shatter_identifiers():
    """Inline code inside paragraphs/lists must not inherit the parent's
    ``word-break: break-word`` (which splits ``foo_bar_baz.py`` between
    arbitrary underscores). Override to ``word-break: normal`` + ``overflow-wrap:
    anywhere`` so breaks only happen at <wbr> hints and as a last-resort
    overflow fallback."""
    block = _mobile_paper_body_block()
    # Pull the inline-code rule block (".paper-body p code, ..., .paper-body dd code { ... }").
    idx = block.index(".paper-body p code")
    end = block.index("}", idx)
    snippet = block[idx:end]
    assert "word-break: normal" in snippet
    assert "overflow-wrap: anywhere" in snippet
