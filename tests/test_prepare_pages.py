"""Tests for the pure helpers in ``scripts.prepare_pages``."""

from scripts.prepare_pages import extract_arxiv, normalize_name


def test_normalize_name_basic():
    """Test basic lowercase conversion."""
    assert normalize_name("Hello World") == "hello world"


def test_normalize_name_lowercase():
    """Test that all characters are lowercased."""
    assert normalize_name("PYTHON") == "python"


def test_normalize_name_special_chars():
    """Test removal of special characters."""
    assert normalize_name("Paper Title: Subtitle!") == "paper title subtitle"


def test_normalize_name_extra_spaces():
    """Test collapsing multiple spaces and stripping."""
    assert normalize_name("  extra   spaces  ") == "extra spaces"


def test_normalize_name_alphanumeric():
    """Test that alphanumeric characters are preserved and others removed."""
    assert normalize_name("Agent-007") == "agent007"


def test_normalize_name_empty_after_cleaning():
    """Test strings that become empty after cleaning."""
    assert normalize_name("!!!") == ""


def test_normalize_name_numbers():
    """Test strings with numbers."""
    assert normalize_name("123 test 456") == "123 test 456"


def test_normalize_name_mixed():
    """Test complex mixed input."""
    assert normalize_name(" [2024] Paper_Name (ArXiv) ") == "2024 papername arxiv"


def test_extract_arxiv_table_all_caps_header():
    """Table rows may spell ARXIV in all caps; extraction must not short-circuit."""
    body = "| ARXIV | 1234.5678 |\n"
    assert extract_arxiv(body) == "1234.5678"


def test_extract_arxiv_abs_url_all_caps_host():
    """Abs links may use an all-caps host; the pre-check must not skip them."""
    body = "Paper: https://ARXIV.ORG/abs/9876.54321\n"
    assert extract_arxiv(body) == "9876.54321"


def test_extract_arxiv_no_mention_returns_none():
    """No arxiv token anywhere → no ID (cheap path)."""
    assert extract_arxiv("Only doi:10.1000/182 and no preprint link.") is None
