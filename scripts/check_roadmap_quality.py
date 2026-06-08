#!/usr/bin/env python3
"""Verify recommended-learning-roadmap papers meet note-quality gates.

Reads ``_data/roadmap_order.yml`` and checks each linked ``papers/**/*.md`` note
for skeleton markers, missing method sections, and the legacy
``深度技术细节待细化`` banner.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import _METHOD_HEADING_RE, BASE_DIR, PAPERS_DIR, is_stub, stub_reason  # noqa: E402

_H2_METHOD_RE = re.compile(
    r"^##\s+(?:🔧|🛠️)?\s*.*(?:方法|是怎么做的|Method)",
    re.MULTILINE,
)
_H2_FORMULA_RE = re.compile(r"^##\s+.*关键公式", re.MULTILINE)

ROADMAP_PATH = os.path.join(BASE_DIR, "_data", "roadmap_order.yml")
PENDING_BANNER = "深度技术细节待细化"
FILLED_MARKER = "深度技术细节已填充"
MIN_LINES = 200
MIN_METHOD_SECTION_CHARS = 300


def _md_path_from_html(site_path: str) -> str:
    rel = site_path.removeprefix("/papers/")
    return os.path.join(PAPERS_DIR, rel.replace(".html", ".md"))


def load_roadmap_entries(path: str = ROADMAP_PATH) -> list[dict[str, str]]:
    """Parse ``_data/roadmap_order.yml`` without a PyYAML dependency."""
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("- short:"):
                if current is not None:
                    entries.append(current)
                current = {"short": line.split(":", 1)[1].strip()}
                continue
            if current is None:
                continue
            if line.startswith("  path:"):
                current["path"] = line.split(":", 1)[1].strip()
    if current is not None:
        entries.append(current)
    return entries


def _section_chars(content: str, heading_re: re.Pattern[str]) -> int:
    capturing = False
    buf: list[str] = []
    for line in content.splitlines():
        if heading_re.match(line):
            capturing = True
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            buf.append(line)
    return len("".join(buf))


def _has_method_section(content: str) -> bool:
    if not _H2_METHOD_RE.search(content) and not _METHOD_HEADING_RE.search(content):
        return False

    technical_chars = _section_chars(content, _H2_METHOD_RE)
    technical_chars += _section_chars(content, _H2_FORMULA_RE)
    return technical_chars >= MIN_METHOD_SECTION_CHARS


def check_roadmap() -> list[str]:
    """Return human-readable failure messages (empty list = all pass)."""
    entries = load_roadmap_entries()

    failures: list[str] = []
    for entry in entries:
        short = entry.get("short", "?")
        md_path = _md_path_from_html(entry["path"])
        if not os.path.isfile(md_path):
            failures.append(f"{short}: missing note file {md_path}")
            continue

        with open(md_path, encoding="utf-8") as f:
            content = f.read()

        line_count = content.count("\n") + 1
        if PENDING_BANNER in content:
            failures.append(f"{short}: still has pending banner ({PENDING_BANNER})")
        if is_stub(content):
            failures.append(f"{short}: classified as stub ({stub_reason(content)})")
        if line_count < MIN_LINES:
            failures.append(f"{short}: only {line_count} lines (min {MIN_LINES})")
        if not _has_method_section(content):
            failures.append(
                f"{short}: method section too short or missing "
                f"(min {MIN_METHOD_SECTION_CHARS} chars)"
            )
        if FILLED_MARKER not in content and PENDING_BANNER not in content:
            # Legacy complete notes (PPO, etc.) predate the filled marker — allow if not stub.
            if is_stub(content) or line_count < MIN_LINES:
                failures.append(f"{short}: missing filled-status marker and below quality bar")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    failures = check_roadmap()
    if failures:
        print("Roadmap quality check FAILED:", file=sys.stderr)
        for msg in failures:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    count = len(load_roadmap_entries())
    print(f"Roadmap quality check OK ({count} papers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
