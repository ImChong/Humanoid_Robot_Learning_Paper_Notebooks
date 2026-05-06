"""Shared helpers for repository maintenance scripts.

Centralises logic that previously diverged between ``prepare_pages.py`` and
``sync_progress.py``:

* ``BASE_DIR`` / ``PAPERS_DIR`` / ``SKIP_DIRS`` constants
* :func:`is_stub` — single source of truth for "is this note a skeleton?"
* :func:`normalize_name` — fuzzy-match key for paper titles
* :func:`parse_frontmatter` — minimal YAML front matter parser (no external deps)
* :func:`iter_paper_md_files` — iterate paper notes while skipping todos/PROGRESS
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS_DIR = os.path.join(BASE_DIR, 'papers')
SKIP_DIRS = {'todos'}

# A note is considered a stub when EITHER:
#   1. it is short AND has no recognisable "方法" (method) section heading, OR
#   2. it has many 🚧 placeholder markers.
# Both ``prepare_pages.check_stub`` (warning) and ``sync_progress.is_stub``
# (status gate) historically used different thresholds; this constant is the
# single source of truth.
STUB_MIN_LINES = 150
STUB_CONSTRUCTION_THRESHOLD = 5
_METHOD_HEADING_RE = re.compile(r'^##\s*(?:🔧|🛠️)?\s*.*方法', re.MULTILINE)


def is_stub(content: str) -> bool:
    """Return True if ``content`` looks like an unfilled note skeleton.

    See module docstring for the rule. The function intentionally accepts the
    full file body (including any front matter) — line counting includes the
    front matter, which is acceptable since real notes are far longer than the
    threshold either way.
    """
    line_count = content.count('\n') + 1
    has_method = bool(_METHOD_HEADING_RE.search(content))
    construction_count = content.count('🚧')
    if line_count < STUB_MIN_LINES and not has_method:
        return True
    if construction_count >= STUB_CONSTRUCTION_THRESHOLD:
        return True
    return False


def stub_reason(content: str) -> str | None:
    """Human-readable reason this note is a stub, or None if it is not."""
    line_count = content.count('\n') + 1
    has_method = bool(_METHOD_HEADING_RE.search(content))
    construction_count = content.count('🚧')
    if line_count < STUB_MIN_LINES and not has_method:
        return f"{line_count} lines, missing 方法详解"
    if construction_count >= STUB_CONSTRUCTION_THRESHOLD:
        return f"{construction_count} 🚧 markers, skeleton"
    return None


def normalize_name(name: str) -> str:
    """Lowercase, strip non-alphanumeric chars, collapse spaces.

    Used as a fuzzy-match key for paper titles between PROGRESS.md table rows
    and on-disk note directories.
    """
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def has_frontmatter(content: str) -> bool:
    """Check if ``content`` already starts with a Jekyll front matter block."""
    return content.startswith('---\n') or content.startswith('---\r\n')


def parse_frontmatter(content: str) -> dict:
    """Parse the YAML front matter at the start of ``content``.

    Only the simple ``key: value`` lines are recognised; values surrounded by
    matching quotes are unquoted. Returns ``{}`` if no front matter is present
    or it cannot be parsed.
    """
    if not has_frontmatter(content):
        return {}
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    body = parts[1]
    result: dict[str, str] = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' not in line:
            continue
        key, _, value = line.partition(':')
        key = key.strip()
        value = value.strip()
        # Unquote symmetric quote characters
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        if key:
            result[key] = value
    return result


def iter_paper_md_files(papers_dir: str = PAPERS_DIR) -> Iterator[str]:
    """Yield absolute paths of paper note markdown files.

    Skips: ``SKIP_DIRS`` (e.g. ``papers/todos/``), top-level ``PROGRESS.md`` and
    ``DAILY_SUMMARY_LOG.md``, and any non-``.md`` file. Order is sorted by
    category then paper directory for stable output.
    """
    if not os.path.isdir(papers_dir):
        return
    for category in sorted(os.listdir(papers_dir)):
        if category in SKIP_DIRS:
            continue
        cat_path = os.path.join(papers_dir, category)
        if not os.path.isdir(cat_path):
            continue
        for paper_dir in sorted(os.listdir(cat_path)):
            paper_path = os.path.join(cat_path, paper_dir)
            if not os.path.isdir(paper_path):
                continue
            for fname in sorted(os.listdir(paper_path)):
                if fname.endswith('.md'):
                    yield os.path.join(paper_path, fname)
