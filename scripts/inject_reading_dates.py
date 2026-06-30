#!/usr/bin/env python3
"""Inject each note's git last-commit date into its ``阅读日期`` header field.

Build-time helper: rewrites the ``> 📅 阅读日期: …`` blockquote line in every
paper note so the rendered detail page shows the markdown file's last
modification date (its most recent git commit date) instead of a hand-written
reading date.

This is meant to run on the ephemeral CI checkout *after* ``prepare_pages.py``
and *before* the Jekyll build (see ``.github/workflows/deploy.yml``). It
mutates files in place, but those changes are never committed, so the source
markdown keeps its original reading dates — only the built site shows the
last-modified date.

Requires full git history (``fetch-depth: 0``); on a shallow clone every file
resolves to the same single fetched commit.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import BASE_DIR, iter_paper_md_files  # noqa: E402

# Matches the header reading-date blockquote line, capturing the
# ``> 📅 阅读日期: `` prefix (group 1) so only the value is replaced. Notes carry
# exactly one such line; prose mentions never start with ``>``.
_READING_DATE_LINE_RE = re.compile(
    r"^(>\s*📅\s*阅读日期\s*[:：]\s*).*$",
    re.MULTILINE,
)


def git_last_modified_date(path: str) -> str | None:
    """Return the ISO date (``YYYY-MM-DD``) of the last commit touching *path*.

    Returns ``None`` when git is unavailable, *path* is untracked, or the
    repository has no history for it (e.g. unit-test fixtures running outside a
    git work tree).
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path],
            cwd=os.path.dirname(path) or ".",
            capture_output=True,
            text=True,
            check=False,
        )
    except (OSError, ValueError):
        return None
    if result.returncode != 0:
        return None
    date = result.stdout.strip()
    return date or None


def replace_reading_date(content: str, new_date: str) -> tuple[str, bool]:
    """Replace the value of the ``阅读日期`` header line with *new_date*.

    Returns ``(content, changed)``. Only the first matching line is rewritten;
    the prefix (``> 📅 阅读日期: ``) is preserved and any existing value —
    including placeholders like ``-`` or trailing annotations — is dropped in
    favour of the single ISO date.
    """
    new_content, count = _READING_DATE_LINE_RE.subn(
        lambda m: m.group(1) + new_date, content, count=1
    )
    return new_content, count > 0 and new_content != content


def inject(path: str, *, dry_run: bool) -> bool:
    """Rewrite *path*'s reading date to its git last-commit date.

    Returns ``True`` when the file content changed (or would change under
    ``dry_run``).
    """
    date = git_last_modified_date(path)
    if not date:
        return False
    with open(path, encoding="utf-8") as f:
        content = f.read()
    new_content, changed = replace_reading_date(content, date)
    if not changed:
        return False
    rel = os.path.relpath(path, BASE_DIR)
    print(f"{'[dry-run] ' if dry_run else ''}{rel}: 阅读日期 -> {date}")
    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print planned updates only")
    args = parser.parse_args()

    updated = sum(inject(path, dry_run=args.dry_run) for path in iter_paper_md_files())
    print(f"\nInjected git last-modified reading dates: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
