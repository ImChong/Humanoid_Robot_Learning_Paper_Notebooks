"""Regression: mobile ``contain: strict`` on tables/code must not collapse height."""

from pathlib import Path

STYLE = Path(__file__).resolve().parents[1] / "assets" / "css" / "style.css"


def _mobile_paper_body_block() -> str:
    text = STYLE.read_text(encoding="utf-8")
    marker = ".paper-body .table-wrapper"
    table_idx = text.find(marker)
    assert table_idx != -1, "table-wrapper mobile rules missing"
    start = text.rfind("@media (max-width: 1200px)", 0, table_idx)
    assert start != -1, "mobile paper-body block missing"
    return text[start:]


def _assert_uses_inline_size_only(snippet: str) -> None:
    """Property lines only — ignore comments that mention ``strict``."""
    for line in snippet.splitlines():
        stripped = line.strip()
        if stripped.startswith("/*") or stripped.startswith("*"):
            continue
        assert "contain: strict" not in stripped


def test_mobile_table_wrapper_not_contain_strict():
    block = _mobile_paper_body_block()
    idx = block.index(".paper-body .table-wrapper")
    _assert_uses_inline_size_only(block[idx : idx + 200])


def test_mobile_code_block_not_contain_strict():
    block = _mobile_paper_body_block()
    idx = block.index(".paper-body .code-block")
    _assert_uses_inline_size_only(block[idx : idx + 320])
