"""Update log heatmap: fixed 53-week sliding window."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPDATES = ROOT / "updates.html"
STYLE = ROOT / "assets" / "css" / "style.css"


def test_updates_heatmap_fixed_week_window():
    text = UPDATES.read_text(encoding="utf-8")
    assert "var WEEKS = 53" in text
    assert "for (var week = 0; week < WEEKS; week++)" in text
    assert "heatmapStartMs = heatmapLastWeekStartMs - (WEEKS - 1) * 7 * DAY_MS" in text
    assert 'data-weeks="' in text
    assert "sliding window" in text
    assert "weekMs <= endWeekStartMs" not in text


def test_updates_heatmap_css_locked_columns():
    css = STYLE.read_text(encoding="utf-8")
    assert "grid-template-columns: repeat(53, minmax(var(--hm-cell-min), 1fr))" in css
    assert "grid-auto-flow: column" in css
    assert ".updates-heatmap-grid" in css
    assert ".updates-heatmap-months" in css
