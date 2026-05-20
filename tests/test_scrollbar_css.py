"""Scrollbar track must stay transparent (no default white gutter)."""

from pathlib import Path

STYLE = Path(__file__).resolve().parents[1] / "assets" / "css" / "style.css"


def test_global_scrollbar_track_is_transparent():
    text = STYLE.read_text(encoding="utf-8")
    assert "scrollbar-color: var(--border) transparent" in text
    assert "::-webkit-scrollbar-track" in text
    track_block = text[text.index("::-webkit-scrollbar-track") :]
    track_block = track_block[: track_block.index("}", track_block.index("{"))]
    assert "background: transparent" in track_block
    assert "#fff" not in track_block
    assert "#ffffff" not in track_block.lower()


def test_toc_scrollbar_does_not_set_white_track():
    text = STYLE.read_text(encoding="utf-8")
    idx = text.index(".toc-sidebar::-webkit-scrollbar-thumb")
    end = text.index("/* Sidebar Toggle", idx)
    block = text[idx:end]
    assert "scrollbar-track" not in block or "transparent" in block
    assert "background:" not in block or "var(--border)" in block
    assert "#fff" not in block
    assert "#ffffff" not in block.lower()
