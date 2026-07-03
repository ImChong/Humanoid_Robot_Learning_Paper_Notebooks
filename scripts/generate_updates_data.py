#!/usr/bin/env python3
"""Generate ``_data/updates.json`` — data behind the site's update-log page.

Walks the repository's git history for paper note markdown files and records,
for every calendar day, which notes were added (their first commit) and which
were maintained (any later commit). ``updates.html`` renders this as a
GitHub-style activity heatmap plus a day-by-day timeline.

Like ``inject_reading_dates.py`` this needs the full git history
(``fetch-depth: 0`` in the deploy workflow); on a shallow clone every note
collapses onto the single fetched commit. A committed snapshot of
``_data/updates.json`` keeps local ``jekyll serve`` previews working — CI
regenerates the file on every deploy, after ``prepare_pages.py`` has refreshed
``_data/papers.json`` (the source of note titles/URLs).

Output schema (keys kept short — the JSON is embedded into the page)::

    {
      "generated": "2026-07-03",          # build date (UTC)
      "notes": [                           # one entry per current note
        {"t": "Title", "z": "中文标题", "u": "/papers/...html",
         "c": "Locomotion", "cz": "行走运动"},
        ...
      ],
      "days": [                            # newest first; indices into notes
        {"d": "2026-07-03", "a": [12], "m": [3, 45]},
        ...
      ]
    }
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import BASE_DIR, iter_paper_md_files  # noqa: E402

PAPERS_JSON_PATH = os.path.join(BASE_DIR, "_data", "papers.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "_data", "updates.json")

# Commit boundary marker in ``git log`` output; never appears in file paths.
_BOUNDARY = "\x01"


def run_git_log(base_dir: str = BASE_DIR) -> str:
    """Return ``git log`` name-status output for the papers tree.

    ``--topo-order`` guarantees children are listed before parents so rename
    chains can be followed while scanning newest → oldest. ``%cs`` matches the
    committer date used by ``inject_reading_dates.py``.
    """
    result = subprocess.run(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "log",
            "--topo-order",
            "--no-merges",
            f"--format={_BOUNDARY}%cs",
            "--name-status",
            "--",
            "papers",
        ],
        cwd=base_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def collect_note_events(
    log_text: str, current_paths: list[str]
) -> tuple[dict[str, set[str]], dict[str, str]]:
    """Parse ``git log --name-status`` output into per-day note activity.

    Scans newest → oldest, following renames so that history recorded under a
    note's previous path still counts toward the current file. Returns
    ``(touched_by_date, added_date)`` where ``touched_by_date`` maps an ISO
    date to the set of current note paths committed that day, and
    ``added_date`` maps each note to the date of its oldest add.
    """
    # Historical path (at the point the scan has reached) -> current path.
    alias = {p: p for p in current_paths}
    touched_by_date: dict[str, set[str]] = defaultdict(set)
    added_date: dict[str, str] = {}
    date = None

    for line in log_text.splitlines():
        if line.startswith(_BOUNDARY):
            date = line[1:].strip() or None
            continue
        if not date or "\t" not in line:
            continue
        parts = line.split("\t")
        status = parts[0]
        if not status:
            continue
        kind = status[0]

        if kind in ("R", "C") and len(parts) >= 3:
            old, new = parts[1], parts[2]
            cur = alias.get(new)
            if cur is None:
                continue
            touched_by_date[date].add(cur)
            if kind == "R":
                # Older than this commit, the note lived at *old*.
                if new != old:
                    del alias[new]
                alias[old] = cur
            else:
                # A copy creates the file here; the source path belongs to a
                # different note, and anything older under *new* is a dead
                # namesake.
                added_date[cur] = date
                del alias[new]
        elif len(parts) >= 2:
            path = parts[1]
            cur = alias.get(path)
            if cur is None:
                continue
            if kind == "D":
                # The note was re-created after this deletion; older history
                # under the same path belongs to a different, dead file.
                del alias[path]
                continue
            touched_by_date[date].add(cur)
            if kind == "A":
                added_date[cur] = date

    return dict(touched_by_date), added_date


def load_note_meta(papers_json_path: str = PAPERS_JSON_PATH) -> dict[str, dict]:
    """Map note markdown path -> display metadata from ``_data/papers.json``."""
    try:
        with open(papers_json_path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}

    meta: dict[str, dict] = {}
    for cat in data.values():
        cat_en = cat.get("display_name")
        cat_zh = cat.get("zhname")
        papers = list(cat.get("papers", []))
        for subcat in cat.get("subcategories", []):
            papers.extend(subcat.get("papers", []))
        for paper in papers:
            path = paper.get("path")
            if not path:
                continue
            entry = {"t": paper.get("title") or "", "u": paper.get("url") or ""}
            zh = paper.get("zh_title") or paper.get("zhname")
            if zh and zh != entry["t"]:
                entry["z"] = zh
            if cat_en:
                entry["c"] = cat_en
            if cat_zh:
                entry["cz"] = cat_zh
            meta[path] = entry
    return meta


def _fallback_meta(path: str) -> dict:
    """Minimal display metadata for notes missing from ``papers.json``."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return {
        "t": stem.replace("__", ": ").replace("_", " "),
        "u": "/" + os.path.splitext(path)[0].replace(os.sep, "/") + ".html",
    }


def build_updates_payload(
    touched_by_date: dict[str, set[str]],
    added_date: dict[str, str],
    meta_by_path: dict[str, dict],
) -> dict:
    """Assemble the JSON payload from per-day activity and note metadata."""
    all_paths = sorted({p for paths in touched_by_date.values() for p in paths})
    note_index = {path: i for i, path in enumerate(all_paths)}
    notes = [meta_by_path.get(path) or _fallback_meta(path) for path in all_paths]

    # A note with no recorded ``A`` (history quirk) counts as added on its
    # oldest touch instead.
    effective_added = dict(added_date)
    for date in sorted(touched_by_date, reverse=True):
        for path in touched_by_date[date]:
            if path not in added_date:
                effective_added[path] = date

    days = []
    for date in sorted(touched_by_date, reverse=True):
        added = []
        maintained = []
        for path in touched_by_date[date]:
            if effective_added.get(path) == date:
                added.append(note_index[path])
            else:
                maintained.append(note_index[path])
        day: dict = {"d": date}
        if added:
            day["a"] = sorted(added)
        if maintained:
            day["m"] = sorted(maintained)
        days.append(day)

    return {
        "generated": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d"),
        "notes": notes,
        "days": days,
    }


def main() -> int:
    current_paths = [os.path.relpath(p, BASE_DIR) for p in iter_paper_md_files()]
    if not current_paths:
        print("No paper notes found; skipping updates.json generation.")
        return 0

    log_text = run_git_log()
    touched_by_date, added_date = collect_note_events(log_text, current_paths)
    if not touched_by_date:
        print("No git history found for paper notes; skipping updates.json generation.")
        return 0

    payload = build_updates_payload(touched_by_date, added_date, load_note_meta())

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")

    total_events = sum(len(d.get("a", [])) + len(d.get("m", [])) for d in payload["days"])
    print(
        f"Generated _data/updates.json: {len(payload['notes'])} notes, "
        f"{len(payload['days'])} active days, {total_events} note-day events"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
