"""Sync ``progress.json`` from on-disk paper notes.

Walks ``papers/`` and updates ``progress.json`` with each note's current
status (``done``/``pending``) plus folder/filename metadata. Stub detection is
delegated to :mod:`_common` so it stays consistent with ``prepare_pages.py``.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    BASE_DIR,
    PAPERS_DIR,
    is_stub,
    iter_paper_md_files,
    parse_frontmatter,
)

PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")


def sync():
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        progress = json.load(f)

    papers_in_json = progress["papers"]
    folder_map = {p["folder"]: i for i, p in enumerate(papers_in_json) if "folder" in p}
    title_map = {p["title"]: i for i, p in enumerate(papers_in_json)}

    for md_path in iter_paper_md_files(PAPERS_DIR):
        with open(md_path, encoding="utf-8") as f:
            content = f.read()

        front = parse_frontmatter(content)
        title = front.get("title", "")
        category = front.get("category", "")

        rel_folder = os.path.relpath(os.path.dirname(md_path), BASE_DIR)
        note_file = os.path.basename(md_path)

        idx = folder_map.get(rel_folder)
        if idx is None:
            # ⚡ Bolt Optimization: O(1) exact title lookup before O(N) fuzzy matching
            idx = title_map.get(title)
            if idx is None:
                for t in title_map:
                    if title and (t in title or title in t):
                        idx = title_map[t]
                        break

        status = "done" if not is_stub(content) else "pending"

        if idx is not None:
            papers_in_json[idx]["status"] = status
            papers_in_json[idx]["folder"] = rel_folder
            papers_in_json[idx]["note_file"] = note_file
        else:
            new_entry = {
                "title": title,
                "folder": rel_folder,
                "note_file": note_file,
                "status": status,
                "arxiv": "",
                "pdf_file": "",
                "route": category,
                "title_cn": "",
            }
            papers_in_json.append(new_entry)
            print(f"Added new entry to progress.json: {title}")

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sync()
