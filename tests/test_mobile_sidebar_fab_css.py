"""Mobile TOC drawer must end above the floating sidebar toggle."""

from pathlib import Path

STYLE = Path(__file__).resolve().parents[1] / "assets" / "css" / "style.css"


def _mobile_toc_block() -> str:
    text = STYLE.read_text(encoding="utf-8")
    marker = "/* Show TOC only on wide screens */"
    start = text.index(marker)
    end = text.index("/* Wider container for paper pages", start)
    return text[start:end]


def test_mobile_toc_sidebar_clears_floating_toggle():
    block = _mobile_toc_block()
    assert "bottom: calc(24px + 48px + 28px + env(safe-area-inset-bottom, 0px))" in block
    assert "height: auto" in block
    assert "max-height: none" in block
    assert "overflow-y: auto" in block


def test_index_mobile_toc_sidebar_matches_subpage_drawer():
    text = STYLE.read_text(encoding="utf-8")
    start = text.index("@media (max-width: 1200px) {\n  .index-layout .toc-sidebar")
    end = text.index("/* ===== Search Box ===== */", start)
    block = text[start:end]
    assert "float: none" in block
    assert "bottom: calc(24px + 48px + 28px + env(safe-area-inset-bottom, 0px))" in block
    assert "height: auto" in block
    assert "overflow-y: auto" in block
    assert "background: var(--bg)" in block
