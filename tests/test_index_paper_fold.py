"""Homepage paper-list fold: exempt categories and CSS hooks."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STYLE = ROOT / "assets" / "css" / "style.css"


def test_index_declares_fold_exempt_categories():
    text = INDEX.read_text(encoding="utf-8")
    assert "01_Foundational_RL" in text
    assert "02_Motion_Retargeting" in text
    assert "03_High_Impact_Selection" in text
    assert "fold_limit = 10" in text
    assert "paper-list-item-folded" in text
    assert "paper-list-toggle-btn" in text


def test_index_fold_search_expansion_hook():
    text = INDEX.read_text(encoding="utf-8")
    assert "search-expanded" in text
    assert "has-paper-fold" in text


def test_style_hides_folded_items_when_collapsed():
    css = STYLE.read_text(encoding="utf-8")
    assert ".paper-list.is-folded:not(.search-expanded) .paper-list-item-folded" in css
    assert ".paper-list-toggle-btn" in css
