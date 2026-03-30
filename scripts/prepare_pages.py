#!/usr/bin/env python3
"""
Prepare paper markdown files for Jekyll:
1. Add minimal front matter if not present (Jekyll requires it to process files)
2. Generate index data (category -> papers mapping) ordered by README appearance
"""

import os
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS_DIR = os.path.join(BASE_DIR, 'papers')
PROGRESS_PATH = os.path.join(PAPERS_DIR, 'PROGRESS.md')


def has_frontmatter(content):
    """Check if file already has Jekyll front matter."""
    return content.startswith('---\n') or content.startswith('---\r\n')


def extract_title(content):
    """Extract title from first H1 heading."""
    text = content
    if has_frontmatter(text):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            text = parts[2]
    match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if match:
        return match.group(1).strip()
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

    with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
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


def normalize_name(name):
    """Normalize a name for fuzzy matching."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def match_paper_order(paper_title, paper_dir, progress_order):
    """Find the README order index for a paper. Lower = earlier in README."""
    # Try matching by title
    norm_title = normalize_name(paper_title)
    for key, idx in progress_order.items():
        if norm_title and (norm_title in key or key in norm_title):
            return idx

    # Try matching by directory name
    norm_dir = normalize_name(paper_dir.replace('_', ' '))
    for key, idx in progress_order.items():
        if norm_dir and (norm_dir in key or key in norm_dir):
            return idx

    # Not found - put at end
    return 99999


def process_papers():
    """Walk through papers directory and add front matter."""
    progress_order = parse_progress_order()
    index_data = {}

    # Load existing papers.json to preserve metadata (subtitle, subcategories)
    existing_papers_json_path = os.path.join(BASE_DIR, '_data', 'papers.json')
    existing_papers_json = {}
    if os.path.exists(existing_papers_json_path):
        try:
            with open(existing_papers_json_path, 'r', encoding='utf-8') as f:
                existing_papers_json = json.load(f)
        except Exception:
            pass

    if not os.path.exists(PAPERS_DIR):
        print(f"Papers directory not found: {PAPERS_DIR}")
        return

    for category_dir in sorted(os.listdir(PAPERS_DIR)):
        category_path = os.path.join(PAPERS_DIR, category_dir)
        if not os.path.isdir(category_path):
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

                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()

                title = extract_title(content) or paper_dir.replace('_', ' ')

                # Add front matter if not present
                if not has_frontmatter(content):
                    frontmatter = f'---\nlayout: paper\ntitle: "{title}"\ncategory: "{category_display}"\n---\n\n'
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(frontmatter + content)
                    print(f"  Added front matter: {fpath}")
                else:
                    print(f"  Already has front matter: {fpath}")

                rel_path = os.path.relpath(fpath, BASE_DIR)
                url_path = '/' + rel_path.rsplit('.md', 1)[0] + '.html'

                order_idx = match_paper_order(title, paper_dir, progress_order)

                papers.append({
                    'title': title,
                    'path': rel_path,
                    'url': url_path,
                    'dir': paper_dir,
                    '_order': order_idx
                })

        # Sort by README order
        papers.sort(key=lambda p: p['_order'])
        # Remove internal _order field
        for p in papers:
            del p['_order']

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

        # Preserve subtitle and i18n name if exists
        if 'subtitle' in existing_meta:
            entry['subtitle'] = existing_meta['subtitle']
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
                # Read paper front matter to get subcategory
                paper_subcat = None
                try:
                    with open(os.path.join(BASE_DIR, paper['path']), 'r', encoding='utf-8') as pf:
                        pcontent = pf.read()
                    fm_match = re.search(r'^subcategory:\s*["\']?(.+?)["\']?\s*$', pcontent, re.MULTILINE)
                    if fm_match:
                        paper_subcat = fm_match.group(1).strip()
                except Exception:
                    pass
                if paper_subcat and paper_subcat in subcat_map:
                    subcat_map[paper_subcat]['papers'].append(paper)
                else:
                    ungrouped.append(paper)
            entry['subcategories'] = subcats
            # ungrouped papers stay in top-level papers list
            entry['papers'] = ungrouped

        index_data[category_dir] = entry

    # Ensure ALL category directories appear (even if empty)
    for category_dir in sorted(os.listdir(PAPERS_DIR)):
        category_path = os.path.join(PAPERS_DIR, category_dir)
        if os.path.isdir(category_path) and category_dir not in index_data:
            existing_meta = existing_papers_json.get(category_dir, {})
            entry = {
                'display_name': get_category_name(category_dir),
                'papers': []
            }
            if 'subtitle' in existing_meta:
                entry['subtitle'] = existing_meta['subtitle']
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

    total = sum(len(v['papers']) for v in sorted_data.values())
    print(f"\nGenerated _data/papers.json with {total} papers in {len(sorted_data)} categories")


if __name__ == '__main__':
    print("Preparing paper pages for Jekyll...\n")
    process_papers()
    print("\nDone!")
