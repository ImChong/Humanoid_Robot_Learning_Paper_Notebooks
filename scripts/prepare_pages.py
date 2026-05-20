#!/usr/bin/env python3
"""
Prepare paper markdown files for Jekyll:
1. Add minimal front matter if not present (Jekyll requires it to process files)
2. Generate index data (category -> papers mapping) ordered by README appearance
"""

import json
import os
import re
import sys

# Allow running both as a script (``python scripts/prepare_pages.py``) and as a
# module (``from scripts.prepare_pages import normalize_name`` in tests).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    BASE_DIR,
    PAPERS_DIR,
    SKIP_DIRS,
    has_frontmatter,
    is_stub,
    normalize_name,
    normalize_paper_meta_blockquotes,
    parse_frontmatter,
    stub_reason,
)

PROGRESS_PATH = os.path.join(PAPERS_DIR, 'PROGRESS.md')


_TITLE_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)

def extract_title(content):
    """Extract title from first H1 heading."""
    start_idx = 0
    # ⚡ Bolt Optimization: Use `find` to skip frontmatter without string copies,
    # and use `find('#')` as a fast pre-check before running the regex.
    if has_frontmatter(content):
        end_idx = content.find('---', 3)
        if end_idx != -1:
            start_idx = end_idx + 3

    if content.find('#', start_idx) != -1:
        match = _TITLE_RE.search(content, start_idx)
        if match:
            return match.group(1).strip()
    return None


# ``is_stub`` and ``normalize_name`` are now provided by ``_common``; we keep
# this module-level binding so ``from scripts.prepare_pages import normalize_name``
# (used by tests) still works.
_ = (is_stub, normalize_name)  # re-exported for backwards compatibility


def extract_arxiv(content):
    """Extract arXiv ID from common note metadata table formats."""
    # ⚡ Bolt Optimization: Avoid re.search and string lowercasing copies by
    # checking for the most common casing variants with the fast `in` operator.
    # Case-insensitive pre-check: the patterns below use IGNORECASE, so the
    # guard must not require the exact substrings ``arxiv`` / ``arXiv`` (e.g.
    # ``| ARXIV |`` or ``Arxiv:`` would otherwise be skipped and drop metadata).
    if ('arxiv' not in content and 'arXiv' not in content and
        'Arxiv' not in content and 'ARXIV' not in content and
        'ArXiv' not in content):
        # Fallback to a case-insensitive regex check for unusual casings
        # to guarantee 100% correctness without regressions.
        if re.search(r'arxiv', content, re.IGNORECASE) is None:
            return None

    patterns = [
        r'\|\s*(?:\*\*)?arXiv(?:\*\*)?\s*\|\s*\[?(\d{4}\.\d{4,5}(?:v\d+)?)',
        r'(?:arXiv:|arxiv\.org/(?:abs|html|pdf)/)(\d{4}\.\d{4,5}(?:v\d+)?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def get_category_name(category_dir):
    """Clean category directory name for display."""
    name = re.sub(r'^\d+_', '', category_dir)
    name = name.replace('_', ' ')
    return name


def parse_progress_order():
    """
    Parse PROGRESS.md to extract paper ordering within each section.
    Returns a dict: { normalized_paper_name: order_index }
    We use the paper title/name from the PROGRESS.md table rows.
    """
    if not os.path.exists(PROGRESS_PATH):
        return {}

    with open(PROGRESS_PATH, encoding='utf-8') as f:
        content = f.read()

    # Extract all paper names mentioned in table rows (| # | paper_name | ... |)
    # This captures the order they appear in README
    order = {}
    idx = 0

    for line in content.split('\n'):
        line = line.strip()
        if not line.startswith('|'):
            continue
        # Skip header/separator rows
        cols = [c.strip() for c in line.split('|')]
        cols = [c for c in cols if c]  # remove empty
        if len(cols) < 2:
            continue
        if cols[0] in ('#', '---', '----', '-----') or re.match(r'^-+$', cols[0]):
            continue
        # First col is usually the number, second is paper name/title
        paper_col = cols[1] if len(cols) > 1 else cols[0]

        # Extract the key text (remove markdown links, bold, etc.)
        paper_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', paper_col)
        paper_text = re.sub(r'[*_`\[\]]', '', paper_text)
        paper_text = paper_text.strip()

        if not paper_text or paper_text in ('论文', '---', '笔记', '状态', '日期', '路线'):
            continue

        # Normalize for matching: lowercase, remove special chars
        normalized = normalize_name(paper_text)
        if normalized and len(normalized) > 3:
            order[normalized] = idx
            idx += 1

    return order


_H_INDEX_RE = re.compile(r'^H(\d+)$', re.IGNORECASE)
_ARXIV_IN_MARKDOWN_CELL_RE = re.compile(
    r'(?:arxiv\.org/(?:abs|html|pdf)/|arxiv:)(\d{4}\.\d{4,5}(?:v\d+)?)',
    re.IGNORECASE,
)


def parse_high_impact_h_order():
    """Parse PROGRESS.md rows whose first column is ``H1``…``H23``.

    Returns two dicts used only for ``03_High_Impact_Selection``:

    * ``by_name``: :func:`normalize_name` of the linked title → H index (int)
    * ``by_arxiv``: arXiv id without version suffix → H index (int)

    ArXiv keys are normalized to lowercase and stripped of a trailing ``vN``.
    """
    if not os.path.exists(PROGRESS_PATH):
        return {}, {}

    with open(PROGRESS_PATH, encoding='utf-8') as f:
        content = f.read()

    by_name = {}
    by_arxiv = {}

    for line in content.split('\n'):
        line = line.strip()
        if not line.startswith('|'):
            continue
        cols = [c.strip() for c in line.split('|')]
        cols = [c for c in cols if c]
        if len(cols) < 2:
            continue
        if cols[0] in ('#', '---', '----', '-----') or re.match(r'^-+$', cols[0]):
            continue

        tag_m = _H_INDEX_RE.match(cols[0])
        if not tag_m:
            continue

        h_num = int(tag_m.group(1))
        paper_col = cols[1]

        for ax_m in _ARXIV_IN_MARKDOWN_CELL_RE.finditer(paper_col):
            ax = re.sub(r'v\d+$', '', ax_m.group(1).lower())
            by_arxiv[ax] = h_num

        paper_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', paper_col)
        paper_text = re.sub(r'[*_`\[\]]', '', paper_text)
        paper_text = paper_text.strip()
        if not paper_text:
            continue

        normalized = normalize_name(paper_text)
        if normalized and len(normalized) > 3:
            by_name[normalized] = h_num

    return by_name, by_arxiv


def match_high_impact_h_order(paper_title, paper_dir, arxiv_id, by_name, by_arxiv):
    """Resolve H# reading order for high-impact notes; ``None`` if unknown."""
    if arxiv_id:
        ax_key = arxiv_id.lower()
        if ax_key in by_arxiv:
            return by_arxiv[ax_key]
        if re.search(r'v\d+$', ax_key):
            ax_key = re.sub(r'v\d+$', '', ax_key)
            if ax_key in by_arxiv:
                return by_arxiv[ax_key]

    norm_title = normalize_name(paper_title)
    if norm_title and norm_title in by_name:
        return by_name[norm_title]

    norm_dir = normalize_name(paper_dir.replace('_', ' '))
    if norm_dir and norm_dir in by_name:
        return by_name[norm_dir]

    for key, h_num in by_name.items():
        if norm_title and (norm_title in key or key in norm_title):
            return h_num

    for key, h_num in by_name.items():
        if norm_dir and (norm_dir in key or key in norm_dir):
            return h_num

    return None


def match_paper_order(paper_title, paper_dir, progress_order):
    """Find the README order index for a paper. Lower = earlier in README."""
    # ⚡ Bolt Optimization: O(1) fast-path for exact matches before O(N) fuzzy search
    norm_title = normalize_name(paper_title)
    if norm_title and norm_title in progress_order:
        return progress_order[norm_title]

    norm_dir = normalize_name(paper_dir.replace('_', ' '))
    if norm_dir and norm_dir in progress_order:
        return progress_order[norm_dir]

    # Try matching by title
    for key, idx in progress_order.items():
        if norm_title and (norm_title in key or key in norm_title):
            return idx

    # Try matching by directory name
    for key, idx in progress_order.items():
        if norm_dir and (norm_dir in key or key in norm_dir):
            return idx

    # Not found - put at end
    return 99999


def check_stub(fpath, content):
    """Print ``[STUB]`` warning if a note looks like an unfilled skeleton.

    Delegates the actual rule to :func:`_common.stub_reason` so all maintenance
    scripts share a single source of truth.
    """
    reason = stub_reason(content)
    if reason:
        rel = os.path.relpath(fpath, BASE_DIR)
        print(f"  [STUB] {rel} ({reason})")


def process_papers():
    """Walk through papers directory and add front matter."""
    progress_order = parse_progress_order()
    hi_by_name, hi_by_arxiv = parse_high_impact_h_order()
    index_data = {}

    # Load existing papers.json to preserve metadata (subtitle, subcategories, zhname)
    existing_papers_json_path = os.path.join(BASE_DIR, '_data', 'papers.json')
    existing_papers_json = {}
    existing_paper_meta = {}  # title/path -> metadata from existing data
    if os.path.exists(existing_papers_json_path):
        try:
            with open(existing_papers_json_path, encoding='utf-8') as f:
                existing_papers_json = json.load(f)
            # Build metadata lookup from all papers (top-level and subcategory)
            for cat_data in existing_papers_json.values():
                for p in cat_data.get('papers', []):
                    existing_paper_meta[p.get('title')] = p
                    existing_paper_meta[p.get('path')] = p
                for sc in cat_data.get('subcategories', []):
                    for p in sc.get('papers', []):
                        existing_paper_meta[p.get('title')] = p
                        existing_paper_meta[p.get('path')] = p
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            pass

    if not os.path.exists(PAPERS_DIR):
        print(f"Papers directory not found: {PAPERS_DIR}")
        return

    for category_dir in sorted(os.listdir(PAPERS_DIR)):
        category_path = os.path.join(PAPERS_DIR, category_dir)
        if not os.path.isdir(category_path):
            continue
        if category_dir in SKIP_DIRS:
            continue

        category_display = get_category_name(category_dir)
        papers = []

        for paper_dir in sorted(os.listdir(category_path)):
            paper_path = os.path.join(category_path, paper_dir)
            if not os.path.isdir(paper_path):
                continue

            for fname in sorted(os.listdir(paper_path)):
                if not fname.endswith('.md'):
                    continue

                fpath = os.path.join(paper_path, fname)

                with open(fpath, encoding='utf-8') as f:
                    content = f.read()

                normalized, meta_changed = normalize_paper_meta_blockquotes(content)
                if meta_changed:
                    content = normalized
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  Normalized meta blockquotes: {fpath}")

                check_stub(fpath, content)

                title = extract_title(content) or paper_dir.replace('_', ' ')

                # Add front matter if not present
                if not has_frontmatter(content):
                    # Use json.dumps to safely escape title and category for YAML
                    safe_title = json.dumps(title, ensure_ascii=False)
                    safe_category = json.dumps(category_display, ensure_ascii=False)
                    frontmatter = f'---\nlayout: paper\ntitle: {safe_title}\ncategory: {safe_category}\n---\n\n'
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(frontmatter + content)
                    print(f"  Added front matter: {fpath}")
                else:
                    print(f"  Already has front matter: {fpath}")

                rel_path = os.path.relpath(fpath, BASE_DIR)
                url_path = '/' + rel_path.rsplit('.md', 1)[0] + '.html'

                # ⚡ Bolt Optimization: Extract front matter explicitly with O(1) parsing
                # instead of running multiple multi-line regexes over the whole file
                frontmatter_meta = parse_frontmatter(content)

                arxiv_for_order = extract_arxiv(content)

                order_idx = match_paper_order(title, paper_dir, progress_order)

                if category_dir == '03_High_Impact_Selection':
                    h_idx = match_high_impact_h_order(
                        title, paper_dir, arxiv_for_order, hi_by_name, hi_by_arxiv
                    )
                    if h_idx is not None:
                        order_idx = h_idx
                    elif 'paper_order' in frontmatter_meta:
                        try:
                            order_idx = int(frontmatter_meta['paper_order'])
                        except ValueError:
                            pass
                elif 'paper_order' in frontmatter_meta:
                    # Front-matter `paper_order: <n>` overrides PROGRESS.md matching.
                    # Used to put papers in README's recommended learning-path order
                    # even when their titles don't match the awesome-list table rows.
                    try:
                        order_idx = int(frontmatter_meta['paper_order'])
                    except ValueError:
                        pass

                # Extract subcategory from front matter if present
                paper_subcat = frontmatter_meta.get('subcategory')

                paper_entry = {
                    'title': title,
                    'path': rel_path,
                    'url': url_path,
                    'dir': paper_dir,
                    '_order': order_idx,
                    '_subcategory': paper_subcat
                }

                existing_meta_for_paper = existing_paper_meta.get(title) or existing_paper_meta.get(rel_path) or {}

                # Extract arXiv ID, preserving existing metadata when the note
                # uses a format the parser does not recognize.
                arxiv = arxiv_for_order or existing_meta_for_paper.get('arxiv')
                if arxiv:
                    paper_entry['arxiv'] = arxiv

                # Prefer zhname from front matter when present
                if 'zhname' in frontmatter_meta:
                    paper_entry['zhname'] = frontmatter_meta['zhname']
                # Otherwise restore zhname from existing data if available
                elif existing_meta_for_paper.get('zhname'):
                    paper_entry['zhname'] = existing_meta_for_paper['zhname']

                papers.append(paper_entry)

        # Sort: global categories by PROGRESS row order; High Impact uses H# from PROGRESS when matched
        papers.sort(key=lambda p: p['_order'])
        # Load existing category meta (subtitle, subcategories) from current papers.json
        existing_meta = existing_papers_json.get(category_dir, {})

        if papers:
            entry = {
                'display_name': category_display,
                'papers': papers
            }
        else:
            entry = {
                'display_name': category_display,
                'papers': []
            }

        # Preserve subtitle, i18n names, and subtitle_zh if exists
        if 'subtitle' in existing_meta:
            entry['subtitle'] = existing_meta['subtitle']
        if 'subtitle_zh' in existing_meta:
            entry['subtitle_zh'] = existing_meta['subtitle_zh']
        # Support both zhname (new) and display_name_zh (legacy) field names
        if 'zhname' in existing_meta:
            entry['zhname'] = existing_meta['zhname']
        elif 'display_name_zh' in existing_meta:
            entry['zhname'] = existing_meta['display_name_zh']

        # Distribute papers into subcategories if defined
        if 'subcategories' in existing_meta:
            subcats = [dict(s) for s in existing_meta['subcategories']]
            # Reset papers in each subcat and migrate name_zh -> zhname
            for s in subcats:
                s['papers'] = []
                if 'name_zh' in s:
                    s['zhname'] = s.pop('name_zh')
            subcat_map = {s['name']: s for s in subcats}
            ungrouped = []
            for paper in papers:
                paper_subcat = paper.get('_subcategory')
                if paper_subcat and paper_subcat in subcat_map:
                    subcat_map[paper_subcat]['papers'].append(paper)
                else:
                    ungrouped.append(paper)
            entry['subcategories'] = subcats
            # ungrouped papers stay in top-level papers list
            entry['papers'] = ungrouped

        # Remove internal fields
        for p in papers:
            if '_order' in p:
                del p['_order']
            if '_subcategory' in p:
                del p['_subcategory']

        index_data[category_dir] = entry

    # Ensure ALL category directories appear (even if empty)
    for category_dir in sorted(os.listdir(PAPERS_DIR)):
        category_path = os.path.join(PAPERS_DIR, category_dir)
        if category_dir in SKIP_DIRS:
            continue
        if os.path.isdir(category_path) and category_dir not in index_data:
            existing_meta = existing_papers_json.get(category_dir, {})
            entry = {
                'display_name': get_category_name(category_dir),
                'papers': []
            }
            if 'subtitle' in existing_meta:
                entry['subtitle'] = existing_meta['subtitle']
            if 'subtitle_zh' in existing_meta:
                entry['subtitle_zh'] = existing_meta['subtitle_zh']
            if 'zhname' in existing_meta:
                entry['zhname'] = existing_meta['zhname']
            elif 'display_name_zh' in existing_meta:
                entry['zhname'] = existing_meta['display_name_zh']
            if 'subcategories' in existing_meta:
                entry['subcategories'] = [dict(s, papers=[]) for s in existing_meta['subcategories']]
                for s in entry['subcategories']:
                    if 'name_zh' in s:
                        s['zhname'] = s.pop('name_zh')
            index_data[category_dir] = entry

    # Sort by category directory name prefix (01_, 02_, etc.)
    sorted_data = dict(sorted(index_data.items()))

    # Write index data
    data_dir = os.path.join(BASE_DIR, '_data')
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, 'papers.json'), 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    total = sum(
        len(v['papers']) + sum(len(s.get('papers', [])) for s in v.get('subcategories', []))
        for v in sorted_data.values()
    )
    print(f"\nGenerated _data/papers.json with {total} papers in {len(sorted_data)} categories")


if __name__ == '__main__':
    print("Preparing paper pages for Jekyll...\n")
    process_papers()
    print("\nDone!")
