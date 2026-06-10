"""Tests for ``extract_published_date`` in ``prepare_pages``."""

from scripts.prepare_pages import extract_published_date

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
