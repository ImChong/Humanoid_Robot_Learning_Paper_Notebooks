import os
import sys

# Add the project root to sys.path to import from scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.prepare_pages import normalize_name  # noqa: E402


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
