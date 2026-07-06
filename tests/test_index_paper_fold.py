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
    assert "fold_limit = 5" in text
    assert "paper-list-item-folded" in text
    assert "paper-list-more-btn" in text
    assert "paper-list-all-btn" in text
    assert "paper-list-collapse-btn" in text
    assert "paper-list-toggle-group" in text


def test_index_search_unfolds_folded_lists():
    text = INDEX.read_text(encoding="utf-8")
    assert "setSearchFoldMode" in text
    assert "index-search-active" in text
    assert "foldStateBeforeSearch" in text
    assert "resetAllItemDisplays" in text
    assert "compositionend" in text
    assert "search-expanded" not in text
    assert "applyVisibleCount" in text


def test_index_fold_toggle_follows_paper_list():
    text = INDEX.read_text(encoding="utf-8")
    assert "</ul>\n      {% if should_fold %}\n      <div class=\"paper-list-toggle-group\"" in text
    assert "paper-list-toggle-item" not in text


def test_style_hides_folded_items_when_collapsed():
    css = STYLE.read_text(encoding="utf-8")
    assert ".paper-list.is-folded .paper-list-item-folded" in css
    assert "body.index-search-active .paper-list-toggle-group" in css
    assert ".paper-list-toggle-group" in css
    assert ".paper-list-toggle-btn" in css
    assert "min-height: 44px" in css
    assert "body:has(.index-layout) .site-footer" in css
    assert "body:has(.index-layout)" in css
    assert "padding-bottom: calc(24px + 48px" not in css
