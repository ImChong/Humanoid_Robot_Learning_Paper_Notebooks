"""Back-to-top FAB must mirror the sidebar toggle across the page's centre axis."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "assets" / "css" / "style.css"
LAYOUT = ROOT / "_layouts" / "default.html"


def _rule(selector: str) -> str:
    text = STYLE.read_text(encoding="utf-8")
    match = re.search(
        r"(?m)^\s*" + re.escape(selector) + r"\s*\{(.*?)^\}",
        text,
        re.DOTALL,
    )
    assert match, f"rule {selector} not found"
    return match.group(1)


def _decl(block: str, prop: str) -> str:
    match = re.search(r"(?m)^\s*" + re.escape(prop) + r"\s*:\s*([^;]+);", block)
    assert match, f"{prop} not declared"
    return match.group(1).strip()


def test_back_to_top_mirrors_sidebar_toggle():
    fab = _rule(".back-to-top")
    toggle = _rule(".sidebar-toggle")

    # Mirror symmetry: same distance from the bottom and the near horizontal
    # edge, same size — only the anchored side flips (left <-> right).
    assert _decl(fab, "right") == _decl(toggle, "left")
    assert _decl(fab, "bottom") == _decl(toggle, "bottom")
    assert _decl(fab, "width") == _decl(toggle, "width")
    assert _decl(fab, "height") == _decl(toggle, "height")
    assert "left:" not in fab
    assert "right:" not in toggle


def test_back_to_top_has_no_breakpoint_offset_override():
    """A media-query override of the geometry would break the mirror."""
    text = STYLE.read_text(encoding="utf-8")
    blocks = re.findall(r"(?m)^\s*\.back-to-top\s*\{(.*?)^\s*\}", text, re.DOTALL)
    assert len(blocks) >= 1
    for prop in ("bottom", "right", "left", "width", "height"):
        declared = sum(
            1 for block in blocks if re.search(r"(?m)^\s*" + prop + r"\s*:", block)
        )
        assert declared <= 1, f"{prop} declared {declared} times on .back-to-top"


def test_back_to_top_button_is_injected_on_every_page():
    layout = LAYOUT.read_text(encoding="utf-8")
    assert 'class="back-to-top" id="back-to-top"' in layout
    assert 'data-zh-aria-label="回到顶部"' in layout
    assert "window.scrollTo({ top: 0" in layout
