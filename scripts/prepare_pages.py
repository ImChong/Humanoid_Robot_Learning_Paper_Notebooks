#!/usr/bin/env python3
"""
Prepare paper markdown files for Jekyll:
1. Add minimal front matter if not present (Jekyll requires it to process files)
2. Generate index data (category -> papers mapping)
"""

import os
import re
import json

PAPERS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'papers')
FRONTMATTER_MARKER = '---'


def has_frontmatter(content):
    """Check if file already has Jekyll front matter."""
    return content.startswith('---\n') or content.startswith('---\r\n')


def extract_title(content):
    """Extract title from first H1 heading."""
    # Remove front matter first if present
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
    name = category_dir
    # Remove leading number prefix like "01_"
    name = re.sub(r'^\d+_', '', name)
    # Replace underscores with spaces
    name = name.replace('_', ' ')
    return name


def process_papers():
    """Walk through papers directory and add front matter."""
    index_data = {}
    
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
            
            for fname in os.listdir(paper_path):
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
                
                # Build relative URL
                rel_path = os.path.relpath(fpath, os.path.dirname(PAPERS_DIR))
                # Remove .md extension for URL
                url_path = '/' + rel_path.rsplit('.md', 1)[0] + '.html'
                
                papers.append({
                    'title': title,
                    'path': rel_path,
                    'url': url_path,
                    'dir': paper_dir
                })
        
        if papers:
            index_data[category_dir] = {
                'display_name': category_display,
                'papers': papers
            }
    
    # Write index data for Jekyll to use
    data_dir = os.path.join(os.path.dirname(PAPERS_DIR), '_data')
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, 'papers.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nGenerated _data/papers.json with {sum(len(v['papers']) for v in index_data.values())} papers in {len(index_data)} categories")


if __name__ == '__main__':
    print("Preparing paper pages for Jekyll...\n")
    process_papers()
    print("\nDone!")
