"""Tests for publish-date helpers in ``prepare_pages``."""

from scripts.prepare_pages import (
    extract_published_date,
    to_published_date_en,
    to_published_date_zh,
)

_BASIC_INFO = """# Sample

## 📋 基本信息

| 项目 | 链接 |
|------|------|
{rows}

---

## 🔧 方法详解

Body.
"""


def _note(*rows):
    body = "\n".join(f"| {label} | {value} |" for label, value in rows)
    return _BASIC_INFO.format(rows=body)


def test_extracts_publish_date_row():
    content = _note(
        ("**arXiv**", "[1707.06347](https://arxiv.org/abs/1707.06347)"),
        ("**发布时间**", "2017年7月20日"),
    )
    assert extract_published_date(content) == "2017年7月20日"


def test_extracts_publish_date_without_bold_label():
    content = _note(("发布时间", "2026-03-09"))
    assert extract_published_date(content) == "2026-03-09"


def test_strips_markdown_links_and_html_breaks():
    content = _note(
        (
            "**发布时间**",
            "2023-03 (arXiv), 2024-05 (ICLR)",
        ),
    )
    assert extract_published_date(content) == "2023-03 (arXiv), 2024-05 (ICLR)"


def test_returns_none_without_basic_info_section():
    assert extract_published_date("# Title only\n\nNo table here.\n") is None


def test_returns_none_when_publish_date_missing():
    content = _note(("**arXiv**", "[1234.56789](https://arxiv.org/abs/1234.56789)"))
    assert extract_published_date(content) is None


def test_to_published_date_en_full_chinese_date():
    assert to_published_date_en("2017年7月20日") == "Jul 20, 2017"


def test_to_published_date_en_always_uses_short_months():
    assert to_published_date_en("2026年2月25日（arXiv）") == "Feb 25, 2026 (arXiv)"
    assert to_published_date_en("2026-02-25 (arXiv)") == "Feb 25, 2026 (arXiv)"


def test_to_published_date_en_year_with_venue():
    assert to_published_date_en("2018年（SIGGRAPH 2018）") == "2018 (SIGGRAPH 2018)"


def test_to_published_date_en_year_month_with_suffix():
    assert to_published_date_en("2025 年 9 月（arXiv）") == "Sep 2025 (arXiv)"


def test_to_published_date_en_iso_and_mixed_phrases():
    assert to_published_date_en("2023-03 (arXiv), 2024-05 (ICLR)") == (
        "Mar 2023 (arXiv), May 2024 (ICLR)"
    )
    assert to_published_date_en("2025-10-15 初版；2026-01-18 v4") == (
        "Oct 15, 2025 initial release; v4 Jan 18, 2026"
    )


def test_to_published_date_en_leaves_plain_year_unchanged():
    assert to_published_date_en("2025") == "2025"


def test_extracts_time_row_as_publish_date():
    content = _note(("时间", "2025 年 12 月（SIGGRAPH Asia 2025）"))
    assert extract_published_date(content) == "2025 年 12 月（SIGGRAPH Asia 2025）"


def test_to_published_date_zh_converts_iso_dates():
    assert to_published_date_zh("2017-12-15 (arXiv)") == "2017年12月15日（arXiv）"
    assert to_published_date_zh("2023-08") == "2023年8月"
    assert to_published_date_zh("2021-09 (arXiv)") == "2021年9月（arXiv）"


def test_to_published_date_zh_compacts_spaced_chinese_dates():
    assert to_published_date_zh("2025 年 10 月（arXiv）") == "2025年10月（arXiv）"
    assert to_published_date_zh("2017年7月20日（arXiv）") == "2017年7月20日（arXiv）"


def test_to_published_date_zh_marks_bare_year_before_venue():
    assert to_published_date_zh("2025 (arXiv)") == "2025年（arXiv）"
    assert to_published_date_zh("2018 (RSS), 2019 (arXiv)") == "2018年（RSS），2019年（arXiv）"
    # Venue-year tails must stay untouched.
    assert to_published_date_zh("2023-03 (arXiv), RSS 2023") == "2023年3月（arXiv），RSS 2023"


def test_to_published_date_zh_keeps_separators_inside_parentheses():
    assert to_published_date_zh(
        "2022-09-29 (arXiv), ACM SIGGRAPH 2020（ACM TOG, Vol. 39, No. 4, Article 53）"
    ) == "2022年9月29日（arXiv），ACM SIGGRAPH 2020（ACM TOG, Vol. 39, No. 4, Article 53）"


def test_to_published_date_zh_wraps_bare_arxiv_tag():
    assert to_published_date_zh("2024-06-13 arXiv；CoRL 2024") == "2024年6月13日（arXiv）；CoRL 2024"


def test_to_published_date_zh_is_idempotent():
    samples = (
        "2017-12-15 (arXiv)",
        "2025 年 12 月（v1）· 2026 年 3 月（v2 修订）（arXiv）",
        "2025-10-15 初版；2026-01-18 v4 (arXiv)",
        "2018 (RSS), 2019 (arXiv)",
    )
    for raw in samples:
        once = to_published_date_zh(raw)
        assert to_published_date_zh(once) == once


def test_to_published_date_en_accepts_normalized_zh():
    assert to_published_date_en(to_published_date_zh("2025-10-15 初版；2026-01-18 v4 (arXiv)")) == (
        "Oct 15, 2025 initial release; v4 Jan 18, 2026 (arXiv)"
    )
    assert to_published_date_en(to_published_date_zh("2026-02-26 (arXiv), CVPR 2026（仓库 README 标识）")) == (
        "Feb 26, 2026 (arXiv), CVPR 2026 (per repository README)"
    )
