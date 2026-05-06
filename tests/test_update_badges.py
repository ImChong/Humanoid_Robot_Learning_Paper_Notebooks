"""Tests for ``scripts.update_badges`` —  badge regex replacement is the most
fragile part and easy to break with copy-paste edits to the README."""

from scripts.update_badges import update_badge


def test_update_badge_replaces_papers_count():
    text = "[![Papers](https://img.shields.io/badge/Papers-468-orange.svg)](papers/)"
    out = update_badge(text, "Papers", 531)
    assert "Papers-531-orange.svg" in out
    assert "Papers-468-orange" not in out


def test_update_badge_replaces_notes_count():
    text = "[![Notes](https://img.shields.io/badge/Notes-12-green.svg)](papers/)"
    out = update_badge(text, "Notes", 57)
    assert "Notes-57-green.svg" in out


def test_update_badge_no_match_returns_original():
    text = "no badge here"
    assert update_badge(text, "Papers", 100) == text


def test_update_badge_handles_label_with_special_chars():
    text = "Papers-100-orange.svg"
    out = update_badge(text, "Papers", 200)
    assert out == "Papers-200-orange.svg"


def test_update_badge_only_touches_named_label():
    text = (
        "[![Papers](https://img.shields.io/badge/Papers-1-orange.svg)]\n"
        "[![Notes](https://img.shields.io/badge/Notes-9-green.svg)]"
    )
    out = update_badge(text, "Papers", 999)
    assert "Papers-999-orange.svg" in out
    assert "Notes-9-green.svg" in out, "Other badges must remain untouched"
