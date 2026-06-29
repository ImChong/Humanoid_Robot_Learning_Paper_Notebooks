"""Regression: mobile main column and header must not exceed viewport width."""

from pathlib import Path

STYLE = Path(__file__).resolve().parents[1] / "assets" / "css" / "style.css"


def _block(start_marker: str, end_marker: str | None = None) -> str:
    text = STYLE.read_text(encoding="utf-8")
    start = text.find(start_marker)
    assert start != -1, f"missing marker: {start_marker!r}"
    if end_marker is None:
        return text[start:]
    end = text.find(end_marker, start)
    assert end != -1, f"missing end marker: {end_marker!r}"
    return text[start:end]


def test_mobile_header_inner_constrained_to_viewport():
    block = _block("@media (max-width: 1200px) {\n  .header-inner {")
    assert "width: 100%" in block
    assert "max-width: 100%" in block
    assert "min-width: 0" in block


def test_mobile_site_title_uses_flex_shrink_not_fixed_calc_width():
    """``calc(100% - 220px)`` sized the title against an already-over-wide
    header and let ``white-space: nowrap`` expand the page past the viewport."""
    text = STYLE.read_text(encoding="utf-8")
    assert "calc(100% - 220px)" not in text


def test_paper_layout_max_width_none_is_desktop_only():
    text = STYLE.read_text(encoding="utf-8")
    assert ".paper-content .paper-layout {\n    max-width: none;\n  }" in text
    desktop_idx = text.index("@media (min-width: 1201px)")
    assert text.index(".paper-content .paper-layout", desktop_idx) > desktop_idx


def test_mobile_code_block_grid_allows_internal_scroll():
    block = _block(".paper-body .code-block {", ".paper-body .table-wrapper")
    assert "grid-template-columns: 3rem minmax(0, auto)" in block
    assert "min-width: 0" in block


def test_mobile_container_chain_has_full_width():
    block = _block("@media (max-width: 1200px) {\n  html,")
    snippet = block[: block.index("/* Wider container")]
    for selector in (".container", ".paper-content", ".paper-layout", ".paper-body"):
        assert selector in snippet
    assert snippet.count("width: 100%") >= 4
