"""Tests for recommended-learning-roadmap note quality gates."""

from scripts.check_roadmap_quality import check_roadmap


def test_roadmap_papers_have_deep_technical_details():
    """Every paper in _data/roadmap_order.yml must pass quality checks."""
    failures = check_roadmap()
    assert failures == [], "Roadmap quality failures:\n" + "\n".join(failures)
