#!/usr/bin/env python3
"""Adapt paper mermaid blocks for KaTeX math + source snapshot compatibility."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PAPERS_DIR = Path(__file__).resolve().parents[1] / "papers"

MERMAID_FENCE_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
MERMAID_DIV_RE = re.compile(
    r'(<div class="mermaid"[^>]*>\s*)(.*?)(\s*</(?:motion\.)?div>)',
    re.DOTALL,
)


def escape_pipes_in_node_labels(text: str) -> str:
    """Escape | inside node labels; leave edge labels (-->|...|) untouched."""

    def fix_label_content(content: str) -> str:
        # Concatenation / stacking: keep readable without mermaid pipe syntax issues.
        content = re.sub(r"\|\|", " ## ", content)
        # Conditional bar: space-pipe-space or tight a|s style in policy notation.
        content = re.sub(r"\s\|\s", " #124; ", content)
        content = re.sub(
            r"([)\]}a-zA-Z0-9_·πφθλΣμσ])(\|)([({a-zA-Z0-9_·πφθλΣμσ])",
            r"\1#124;\3",
            content,
        )
        return content

    def repl_node(match: re.Match[str]) -> str:
        return match.group(1) + fix_label_content(match.group(2)) + match.group(3)

    # ["..."], ("..."), {"..."}, subgraph titles ["..."]
    for opener, closer in (("[", "]"), ("(", ")"), ("{", "}")):
        pattern = re.compile(
            re.escape(opener) + r'"([^"]*)"' + re.escape(closer)
        )
        text = pattern.sub(
            lambda m, o=opener, c=closer: o + '"' + fix_label_content(m.group(1)) + '"' + c,
            text,
        )
    return text


def adapt_mermaid_source(source: str) -> str:
    source = source.replace("</motion.div>", "</div>")
    source = source.replace("\\n", "<br/>")
    source = escape_pipes_in_node_labels(source)
    return source


def adapt_block(source: str) -> tuple[str, bool]:
    adapted = adapt_mermaid_source(source)
    return adapted, adapted != source


def fence_to_div(source: str) -> str:
    body = source.strip("\n")
    return f'<div class="mermaid">\n{body}\n</div>'


def process_markdown(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def fence_repl(match: re.Match[str]) -> str:
        nonlocal changed
        body = match.group(1)
        new_body, block_changed = adapt_block(body)
        if block_changed:
            changed = True
        return fence_to_div(new_body)

    new_text = MERMAID_FENCE_RE.sub(fence_repl, text)
    if new_text != text:
        changed = True
        text = new_text

    def div_repl(match: re.Match[str]) -> str:
        nonlocal changed
        open_tag, body, _close_tag = match.group(1), match.group(2), match.group(3)
        new_body, block_changed = adapt_block(body)
        if block_changed:
            changed = True
        return open_tag + new_body + "\n</div>"

    new_text = MERMAID_DIV_RE.sub(div_repl, text)
    if new_text != text:
        changed = True
        text = new_text

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    changed_files: list[str] = []
    for path in sorted(PAPERS_DIR.rglob("*.md")):
        if process_markdown(path):
            changed_files.append(str(path.relative_to(PAPERS_DIR.parent)))
    print(f"Updated {len(changed_files)} files")
    for name in changed_files:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
