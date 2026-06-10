#!/usr/bin/env python3
"""Fill missing ``发布时间`` rows in paper notes from arXiv and existing metadata."""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import BASE_DIR, iter_paper_md_files  # noqa: E402
from prepare_pages import (  # noqa: E402
    _BASIC_INFO_SECTION_RE,
    _EMPTY_TABLE_ROW_RE,
    _LABEL_STARS_RE,
    _NEXT_H2_RE,
    _PUBLISH_DATE_LABEL_RE,
    _extract_basic_info_section,
    extract_arxiv,
    extract_published_date,
)

_ARXIV_MENTION_RE = re.compile(r"arXiv|arxiv", re.IGNORECASE)
_VENUE_IN_DATE_RE = re.compile(
    r"SIGGRAPH|ICCV|ICLR|RSS|CoRL|IROS|CVPR|NeurIPS|HRI|ICRA|Science Robotics|ACM TOG|GitHub",
    re.IGNORECASE,
)
_CHINESE_DATE_RE = re.compile(r"[年月日]")

_ARXIV_API = "http://export.arxiv.org/api/query"
_ARXIV_NS = {"a": "http://www.w3.org/2005/Atom"}
_CONFERENCE_LABEL_RE = re.compile(r"会议|venue|conference", re.IGNORECASE)
_TIME_LABEL_RE = re.compile(r"^时间$")
_CODE_LABEL_RE = re.compile(
    r"(?:代码|源码|GitHub|官方代码|算法代码|实现说明|配套文档|官方代码)",
    re.IGNORECASE,
)
_ANCHOR_LABEL_RE = re.compile(
    r"(?:机构|作者|会议|期刊|荣誉|硬件|机器人|训练规模|数据|DOI|项目页|项目主页)",
    re.IGNORECASE,
)


def _table_label(line: str) -> str | None:
    line = line.strip()
    if not line.startswith("|") or _EMPTY_TABLE_ROW_RE.match(line):
        return None
    cols = [c.strip() for c in line.split("|")]
    cols = [c for c in cols if c]
    if len(cols) < 2:
        return None
    return _LABEL_STARS_RE.sub("", cols[0]).strip()


def _table_value(line: str) -> str | None:
    line = line.strip()
    if not line.startswith("|") or _EMPTY_TABLE_ROW_RE.match(line):
        return None
    cols = [c.strip() for c in line.split("|")]
    cols = [c for c in cols if c]
    if len(cols) < 2:
        return None
    return cols[-1] if len(cols) == 2 else " | ".join(cols[1:])


def _extract_conference(section: str) -> str | None:
    for line in section.splitlines():
        label = _table_label(line)
        if label and _CONFERENCE_LABEL_RE.search(label):
            value = _table_value(line)
            if value:
                return value.strip()
    return None


def _extract_time_row(section: str) -> str | None:
    for line in section.splitlines():
        label = _table_label(line)
        if label and _TIME_LABEL_RE.match(label):
            value = _table_value(line)
            if value:
                return re.sub(r"\s+", " ", value).strip()
    return None


def ensure_arxiv_tag(date: str) -> str:
    """Append ``(arXiv)`` / ``（arXiv）`` when the date has no arXiv marker or venue label."""
    date = date.strip()
    if not date or _ARXIV_MENTION_RE.search(date) or _VENUE_IN_DATE_RE.search(date):
        return date
    suffix = "（arXiv）" if _CHINESE_DATE_RE.search(date) else " (arXiv)"
    return f"{date}{suffix}"


def _format_publish_date(arxiv_date: str | None, conference: str | None) -> str | None:
    if arxiv_date and conference:
        return f"{arxiv_date} (arXiv), {conference}"
    if arxiv_date:
        return ensure_arxiv_tag(arxiv_date)
    if conference:
        return conference
    return None


def _fetch_arxiv_dates(arxiv_ids: list[str]) -> dict[str, str]:
    results: dict[str, str] = {}
    chunk_size = 40
    for start in range(0, len(arxiv_ids), chunk_size):
        chunk = arxiv_ids[start : start + chunk_size]
        query = ",".join(chunk)
        url = f"{_ARXIV_API}?id_list={query}&max_results={len(chunk)}"
        req = urllib.request.Request(url, headers={"User-Agent": "HumanoidPaperNotes/1.0"})
        for attempt in range(4):
            try:
                payload = urllib.request.urlopen(req, timeout=60).read()
                break
            except urllib.error.URLError:
                if attempt == 3:
                    raise
                time.sleep(2**attempt)
        root = ET.fromstring(payload)
        for entry in root.findall("a:entry", namespaces=_ARXIV_NS):
            entry_id = entry.find("a:id", namespaces=_ARXIV_NS)
            published = entry.find("a:published", namespaces=_ARXIV_NS)
            if entry_id is None or published is None:
                continue
            arxiv_id = entry_id.text.rsplit("/abs/", 1)[-1]
            base_id = re.sub(r"v\d+$", "", arxiv_id)
            results[base_id] = published.text[:10]
        time.sleep(3)
    return results


def _find_basic_info_bounds(content: str) -> tuple[int, int] | None:
    if "基本信息" not in content:
        return None
    match = _BASIC_INFO_SECTION_RE.search(content)
    if not match:
        return None
    start = match.end()
    next_heading = _NEXT_H2_RE.search(content, start)
    end = next_heading.start() if next_heading else len(content)
    return start, end


def _find_insert_offset(section_lines: list[str]) -> int:
    insert_at = len(section_lines)
    last_anchor = 0
    for idx, line in enumerate(section_lines):
        label = _table_label(line)
        if not label:
            continue
        if _CODE_LABEL_RE.search(label):
            return idx
        if _ANCHOR_LABEL_RE.search(label):
            last_anchor = idx + 1
    return insert_at if last_anchor == 0 else last_anchor


def replace_published_date_value(content: str, new_value: str) -> tuple[str, bool]:
    bounds = _find_basic_info_bounds(content)
    if bounds is None:
        return content, False

    start, end = bounds
    section_lines = content[start:end].splitlines(keepends=True)
    changed = False
    for idx, line in enumerate(section_lines):
        label = _table_label(line)
        if not label or not _PUBLISH_DATE_LABEL_RE.search(label):
            continue
        cols = [c.strip() for c in line.strip().split("|")]
        cols = [c for c in cols if c]
        if len(cols) < 2:
            continue
        label_cell = cols[0]
        section_lines[idx] = f"| {label_cell} | {new_value} |\n"
        changed = True
        break

    if not changed:
        return content, False

    new_section = "".join(section_lines)
    return content[:start] + new_section + content[end:], True


def normalize_arxiv_tags_in_note(path: str, dry_run: bool) -> bool:
    content = open(path, encoding="utf-8").read()
    if not extract_arxiv(content):
        return False
    current = extract_published_date(content)
    if not current:
        return False
    new_date = ensure_arxiv_tag(current)
    if new_date == current:
        return False
    new_content, changed = replace_published_date_value(content, new_date)
    if not changed:
        return False
    rel = os.path.relpath(path, BASE_DIR)
    print(f"{'[dry-run] ' if dry_run else ''}normalize {rel}: {current} -> {new_date}")
    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return True


def insert_published_date_row(content: str, date_value: str) -> tuple[str, bool]:
    if extract_published_date(content):
        return content, False

    bounds = _find_basic_info_bounds(content)
    if bounds is None:
        return content, False

    start, end = bounds
    section = content[start:end]
    section_lines = section.splitlines(keepends=True)
    insert_offset = _find_insert_offset(section_lines)
    row = f"| **发布时间** | {date_value} |\n"
    section_lines.insert(insert_offset, row)
    new_section = "".join(section_lines)
    return content[:start] + new_section + content[end:], True


def collect_targets() -> list[dict]:
    targets = []
    for path in iter_paper_md_files():
        content = open(path, encoding="utf-8").read()
        if extract_published_date(content):
            continue
        section = _extract_basic_info_section(content)
        if not section:
            continue
        arxiv = extract_arxiv(content)
        conference = _extract_conference(section)
        time_row = _extract_time_row(section)
        targets.append(
            {
                "path": path,
                "arxiv": arxiv,
                "conference": conference,
                "time_row": time_row,
            }
        )
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print planned updates only")
    parser.add_argument(
        "--skip-normalize",
        action="store_true",
        help="Do not add missing (arXiv) markers to existing publish dates",
    )
    args = parser.parse_args()

    if not args.skip_normalize:
        normalized = sum(
            normalize_arxiv_tags_in_note(path, args.dry_run) for path in iter_paper_md_files()
        )
        print(f"\nNormalized arXiv tags: {normalized}")

    targets = collect_targets()
    arxiv_ids = sorted({t["arxiv"] for t in targets if t["arxiv"]})
    arxiv_dates = _fetch_arxiv_dates(arxiv_ids) if arxiv_ids else {}

    updated = 0
    skipped = []
    for target in targets:
        arxiv_date = arxiv_dates.get(target["arxiv"]) if target["arxiv"] else None
        date_value = target["time_row"] or _format_publish_date(arxiv_date, target["conference"])
        if not date_value:
            skipped.append(target["path"])
            continue

        content = open(target["path"], encoding="utf-8").read()
        new_content, changed = insert_published_date_row(content, date_value)
        if not changed:
            skipped.append(target["path"])
            continue

        rel = os.path.relpath(target["path"], BASE_DIR)
        print(f"{'[dry-run] ' if args.dry_run else ''}update {rel}: {date_value}")
        if not args.dry_run:
            with open(target["path"], "w", encoding="utf-8") as f:
                f.write(new_content)
        updated += 1

    print(f"\nInserted missing publish dates: {updated}")
    if skipped:
        print(f"Skipped (no date source): {len(skipped)}")
        for path in skipped:
            print("  -", os.path.relpath(path, BASE_DIR))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
