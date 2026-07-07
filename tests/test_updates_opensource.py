"""Update log timeline: open-source star on notes with code links."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATES = ROOT / "updates.html"
STYLE = ROOT / "assets" / "css" / "style.css"


def test_updates_item_renders_open_source_star():
    text = UPDATES.read_text(encoding="utf-8")
    assert "updates-item-opensource" in text
    assert "note && note.o" in text
    assert "笔记含开源源码链接" in text


def test_updates_open_source_star_css():
    css = STYLE.read_text(encoding="utf-8")
    assert ".updates-item-opensource" in css
