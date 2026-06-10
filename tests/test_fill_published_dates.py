"""Tests for ``fill_published_dates`` helpers."""

from scripts.fill_published_dates import _format_publish_date, ensure_arxiv_tag


def test_format_publish_date_arxiv_only_includes_tag():
    assert _format_publish_date("2025-11-11", None) == "2025-11-11 (arXiv)"


def test_format_publish_date_with_conference_keeps_arxiv_tag():
    assert _format_publish_date("2025-02-03", "RSS 2025") == "2025-02-03 (arXiv), RSS 2025"


def test_ensure_arxiv_tag_skips_when_already_present():
    assert ensure_arxiv_tag("2023-03 (arXiv), RSS 2023") == "2023-03 (arXiv), RSS 2023"


def test_ensure_arxiv_tag_skips_venue_primary_dates():
    assert ensure_arxiv_tag("2018年（SIGGRAPH 2018）") == "2018年（SIGGRAPH 2018）"


def test_ensure_arxiv_tag_uses_chinese_parens_for_chinese_dates():
    assert ensure_arxiv_tag("2017年7月20日") == "2017年7月20日（arXiv）"


def test_ensure_arxiv_tag_uses_ascii_parens_for_iso_dates():
    assert ensure_arxiv_tag("2024-12-18") == "2024-12-18 (arXiv)"
