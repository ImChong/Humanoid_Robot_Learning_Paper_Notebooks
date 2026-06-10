"""Tests for the pure helpers in ``scripts.prepare_pages``."""

from scripts import prepare_pages
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


def test_parse_high_impact_h_order_reads_h_rows(tmp_path, monkeypatch):
    """``Hn`` first-column rows map titles and arXiv IDs to integer order."""
    progress = tmp_path / "PROGRESS.md"
    progress.write_text(
        "| # | 论文 | 来源 |\n"
        "|---|------|------|\n"
        "| H1 | [Short Paper Name](https://arxiv.org/abs/1111.11111) | x |\n"
        "| H2 | [Other](https://arxiv.org/abs/2222.22222v2) | y |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(prepare_pages, "PROGRESS_PATH", str(progress))
    by_name, by_arxiv = prepare_pages.parse_high_impact_h_order()
    assert by_arxiv["1111.11111"] == 1
    assert by_arxiv["2222.22222"] == 2
    assert by_name[normalize_name("Short Paper Name")] == 1


def test_match_high_impact_h_order_prefers_arxiv():
    """When title text drifts from PROGRESS, arXiv still pins the H index."""
    by_name = {normalize_name("Progress Title Only"): 5}
    by_arxiv = {"3333.33333": 7}
    got = prepare_pages.match_high_impact_h_order(
        "Different Title on Disk",
        "Some_Dir",
        "3333.33333",
        by_name,
        by_arxiv,
    )
    assert got == 7


def test_sort_papers_by_arxiv_newest_first():
    papers = [
        {"title": "old", "arxiv": "2001.00001", "_order": 1},
        {"title": "new", "arxiv": "2501.00001", "_order": 2},
    ]
    prepare_pages.sort_papers_by_arxiv(papers, newest_first=True)
    assert [p["title"] for p in papers] == ["new", "old"]


def test_sort_papers_by_arxiv_oldest_first():
    papers = [
        {"title": "new", "arxiv": "2501.00001", "_order": 2},
        {"title": "old", "arxiv": "2001.00001", "_order": 1},
    ]
    prepare_pages.sort_papers_by_arxiv(papers, newest_first=False)
    assert [p["title"] for p in papers] == ["old", "new"]


def test_category_sort_policy_constants():
    """Only foundational RL keeps PROGRESS order; motion retargeting & high impact are oldest-first."""
    assert prepare_pages.CATEGORIES_PROGRESS_ORDER == frozenset({"01_Foundational_RL"})
    assert prepare_pages.CATEGORIES_ARXIV_OLDEST_FIRST == frozenset({
        "02_Motion_Retargeting",
        "03_High_Impact_Selection",
    })
