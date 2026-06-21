"""Sync ``progress.json`` from on-disk paper notes.

Walks ``papers/`` and updates ``progress.json`` with each note's current
status (``done``/``pending``) plus folder/filename metadata. Stub detection is
delegated to :mod:`_common` so it stays consistent with ``prepare_pages.py``.
"""

import json
import os
import re
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
PAPERS_JSON_FILE = os.path.join(BASE_DIR, "_data", "papers.json")

# Modules 04–14 must stay aligned with upstream YanjieZe/awesome-humanoid-robot-learning.
_CONSTRAINED_MODULE_RE = re.compile(r"papers[/\\](0[4-9]|1[0-4])_")


def _load_upstream_allowlist() -> set[str]:
    """Return the set of arXiv IDs allowed for modules 04–14 per _data/papers.json."""
    try:
        with open(PAPERS_JSON_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return set()

    # papers.json is a flat dict keyed by module folder name (e.g. "09_State_Estimation")
    allowed: set[str] = set()
    for folder_name, module in data.items():
        if not _CONSTRAINED_MODULE_RE.match(f"papers/{folder_name}"):
            continue
        if not isinstance(module, dict):
            continue
        for paper in module.get("papers", []):
            arxiv_id = paper.get("arxiv", "").strip()
            if arxiv_id:
                allowed.add(arxiv_id)
    return allowed


def sync():
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        progress = json.load(f)

    papers_in_json = progress["papers"]
    folder_map = {p["folder"]: i for i, p in enumerate(papers_in_json) if "folder" in p}
    title_map = {p["title"]: i for i, p in enumerate(papers_in_json)}

    upstream_allowlist = _load_upstream_allowlist()

    for md_path in iter_paper_md_files(PAPERS_DIR):
        with open(md_path, encoding="utf-8") as f:
            content = f.read()

        front = parse_frontmatter(content)
        title = front.get("title", "")
        category = front.get("category", "")
        arxiv_id = front.get("arxiv", "").strip()

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
            # Warn when a new notebook for a constrained module is not in the upstream allowlist.
            if _CONSTRAINED_MODULE_RE.search(rel_folder):
                if not arxiv_id or arxiv_id not in upstream_allowlist:
                    print(
                        f"[WARN] 新发现的笔记不在上游白名单中，已跳过自动加入 progress.json：\n"
                        f"       标题: {title!r}\n"
                        f"       路径: {rel_folder}/{note_file}\n"
                        f"       arXiv: {arxiv_id or '(未填写)'}\n"
                        f"       请确认该论文已收录于上游 YanjieZe/awesome-humanoid-robot-learning，"
                        f"并在 _data/papers.json 中添加条目后再重新运行。"
                    )
                    continue

            new_entry = {
                "title": title,
                "folder": rel_folder,
                "note_file": note_file,
                "status": status,
                "arxiv": arxiv_id,
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
