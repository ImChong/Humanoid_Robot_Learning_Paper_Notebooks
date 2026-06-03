#!/usr/bin/env python3
"""Post-process Jekyll ``_site`` output: sanitize ``#paper-body`` inner HTML.

Paper notes are rendered with Liquid ``{{ content }}`` (see ``_layouts/paper.html``),
so raw HTML or ``<script>`` from merged markdown becomes live markup. GitHub Pages
builds use ``jekyll-build-pages``, which does not run custom Jekyll plugins; this
script runs after the static build and rewrites only the paper body fragment with
`nh3 <https://github.com/messense/nh3>`_ so obvious stored XSS payloads are
stripped before publish.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nh3
from bs4 import BeautifulSoup, SoupStrainer

_ALLOWED_TAGS = frozenset(
    {
        "a",
        "abbr",
        "b",
        "blockquote",
        "br",
        "caption",
        "cite",
        "code",
        "col",
        "colgroup",
        "dd",
        "del",
        "details",
        "div",
        "dl",
        "dt",
        "em",
        "figcaption",
        "figure",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "i",
        "img",
        "ins",
        "kbd",
        "li",
        "mark",
        "ol",
        "p",
        "pre",
        "q",
        "rp",
        "rt",
        "ruby",
        "s",
        "samp",
        "section",
        "small",
        "span",
        "strong",
        "sub",
        "summary",
        "sup",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "time",
        "tr",
        "u",
        "ul",
        "var",
        "wbr",
    }
)

# nh3 uses ``"*"`` for attributes allowed on any tag (see nh3 docs).
_ALLOWED_ATTRIBUTES: dict[str, frozenset[str]] = {
    "*": frozenset({"class", "id", "title", "lang", "dir", "role"}),
    "a": frozenset({"href", "name", "target", "download"}),
    "blockquote": frozenset({"cite"}),
    "col": frozenset({"span"}),
    "colgroup": frozenset({"span"}),
    "img": frozenset({"src", "alt", "width", "height", "loading", "decoding", "srcset", "sizes"}),
    "ol": frozenset({"start", "type", "reversed"}),
    "q": frozenset({"cite"}),
    "td": frozenset({"colspan", "rowspan", "headers", "align"}),
    "th": frozenset({"colspan", "rowspan", "headers", "scope", "abbr", "align"}),
    "time": frozenset({"datetime"}),
}

_URL_SCHEMES = frozenset({"http", "https", "mailto"})

# Strip tag *and* subtree for hosts that historically carried executable payloads.
_CLEAN_CONTENT_TAGS = frozenset({"script", "iframe", "object", "embed", "noscript"})


def sanitize_paper_body_fragment(html_fragment: str) -> str:
    """Return an nh3-sanitized HTML fragment suitable for ``#paper-body``."""
    return nh3.clean(
        html_fragment,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        url_schemes=_URL_SCHEMES,
        clean_content_tags=_CLEAN_CONTENT_TAGS,
        strip_comments=True,
        generic_attribute_prefixes=frozenset({"aria-", "data-"}),
        link_rel="noopener noreferrer",
    )


def _replace_paper_body(site_root: Path, path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")

    # ⚡ Bolt Optimization: Use SoupStrainer to parse only the #paper-body element
    # for the initial sanitization check, avoiding the massive O(N) overhead of
    # parsing the entire DOM (sidebar, header, footer) for files that are already clean.
    strainer = SoupStrainer(id="paper-body")
    fast_soup = BeautifulSoup(raw, "html.parser", parse_only=strainer)
    paper_body_fast = fast_soup.find(id="paper-body")

    if paper_body_fast is None:
        return False

    inner = paper_body_fast.decode_contents()
    cleaned = sanitize_paper_body_fragment(inner)

    if inner == cleaned:
        return False

    # Slow path: if we actually need to rewrite the file, parse the full DOM
    soup = BeautifulSoup(raw, "html.parser")
    paper_body = soup.find(id="paper-body")

    if paper_body is None:
        return False

    for child in list(paper_body.contents):
        child.extract()

    wrapper = BeautifulSoup(cleaned, "html.parser")
    container = wrapper.body if wrapper.body is not None else wrapper
    for node in list(container.contents):
        paper_body.append(node)

    path.write_text(str(soup), encoding="utf-8")
    rel = path.relative_to(site_root)
    print(f"  sanitized: {rel}")
    return True


def iter_paper_html_files(site_root: Path) -> list[Path]:
    papers = site_root / "papers"
    if not papers.is_dir():
        return []
    return sorted(papers.rglob("*.html"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sanitize #paper-body in built paper HTML under _site.")
    parser.add_argument(
        "site_dir",
        type=Path,
        help="Jekyll output directory (usually _site)",
    )
    args = parser.parse_args(argv)

    site_root = args.site_dir.resolve()
    if not site_root.is_dir():
        print(f"error: not a directory: {site_root}", file=sys.stderr)
        return 1

    paths = iter_paper_html_files(site_root)
    if not paths:
        print(f"warning: no HTML under {site_root / 'papers'}", file=sys.stderr)
        return 0

    count = 0
    for path in paths:
        if _replace_paper_body(site_root, path):
            count += 1
    print(f"Sanitized paper-body in {count} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
