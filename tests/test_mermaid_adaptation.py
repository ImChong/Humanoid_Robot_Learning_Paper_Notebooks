"""Guards for paper mermaid blocks after KaTeX / snapshot adaptation."""

from __future__ import annotations

import re
from pathlib import Path

PAPERS_DIR = Path(__file__).resolve().parents[1] / "papers"

MERMAID_DIV_RE = re.compile(
    r'<div class="mermaid"[^>]*>(.*?)</div>',
    re.DOTALL,
)
NODE_LABEL_RE = re.compile(r'\["([^"]*)"\]')


def _iter_mermaid_blocks(md: str) -> list[str]:
    return MERMAID_DIV_RE.findall(md)


def test_no_motion_div_closers():
    for path in PAPERS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "</motion.div>" not in text, path


def test_no_mermaid_fences():
    for path in PAPERS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "```mermaid" not in text, path


def test_mermaid_node_labels_escape_pipes():
    for path in PAPERS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for block in _iter_mermaid_blocks(text):
            assert "\\n" not in block, path
            for match in NODE_LABEL_RE.finditer(block):
                label = match.group(1)
                stripped = label.replace("#124;", "")
                assert "|" not in stripped, (path, label)
