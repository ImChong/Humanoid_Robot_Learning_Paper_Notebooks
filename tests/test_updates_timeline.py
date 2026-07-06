"""Update log timeline: expand/collapse/back-to-top controls."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATES = ROOT / "updates.html"
STYLE = ROOT / "assets" / "css" / "style.css"


def test_updates_timeline_expand_and_collapse_controls():
    text = UPDATES.read_text(encoding="utf-8")
    assert "TIMELINE_WINDOW_DAYS = 30" in text
    assert "updates-timeline-more-days" in text
    assert "updates-timeline-show-all" in text
    assert "updates-timeline-collapse" in text
    assert "updates-timeline-back-to-top" in text
    assert "collapseTo30Days" in text
    assert "backToTop" in text
    assert "isTimelineExpanded" in text
    assert "收起至 30 天" in text
    assert "回到顶部" in text


def test_updates_timeline_collapse_resets_window():
    text = UPDATES.read_text(encoding="utf-8")
    assert "currentWindowDays = TIMELINE_WINDOW_DAYS" in text
    assert "timelineShowAll = false" in text
    assert "window.scrollTo({ top: 0, behavior: 'smooth' })" in text


def test_updates_timeline_back_to_top_always_rendered():
    text = UPDATES.read_text(encoding="utf-8")
    assert "updates-timeline-actions-left" in text
    assert "updates-timeline-back-to-top" in text
    assert "activeDate ? '' : timelineActionsHtml" not in text


def test_style_back_to_top_right_aligned():
    css = STYLE.read_text(encoding="utf-8")
    assert ".updates-timeline-back-to-top" in css
    assert "margin-left: auto" in css
