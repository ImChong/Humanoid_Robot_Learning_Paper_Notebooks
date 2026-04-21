import json
import os
import glob

PROGRESS_FILE = 'progress.json'
PAPERS_DIR = 'papers'

def is_stub(content):
    lines = content.splitlines()
    if len(lines) < 80:
        return True
    if '## 🔧 方法详解' not in content:
        return True
    if content.count('🚧') >= 5:
        return True
    return False

def sync():
    with open(PROGRESS_FILE, 'r') as f:
        progress = json.load(f)

    # Index existing papers by folder or title
    papers_in_json = progress['papers']
    folder_map = {p['folder']: i for i, p in enumerate(papers_in_json) if 'folder' in p}
    title_map = {p['title']: i for i, p in enumerate(papers_in_json)}

    # Walk papers dir
    md_files = glob.glob(os.path.join(PAPERS_DIR, '**/*.md'), recursive=True)
    
    # Filter out PROGRESS.md if any
    md_files = [f for f in md_files if 'PROGRESS.md' not in f and 'todos' not in f]

    for md_path in md_files:
        with open(md_path, 'r') as f:
            content = f.read()
        
        # Simple front matter parser
        title = ""
        category = ""
        for line in content.splitlines():
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"')
            if line.startswith('category:'):
                category = line.split(':', 1)[1].strip().strip('"')
        
        folder = os.path.dirname(md_path)
        note_file = os.path.basename(md_path)
        
        idx = folder_map.get(folder)
        if idx is None:
            # Try matching by title (vague match)
            for t in title_map:
                if t in title or title in t:
                    idx = title_map[t]
                    break
        
        status = 'done' if not is_stub(content) else 'pending'
        
        if idx is not None:
            # Update existing
            papers_in_json[idx]['status'] = status
            papers_in_json[idx]['folder'] = folder
            papers_in_json[idx]['note_file'] = note_file
        else:
            # Add new
            new_entry = {
                "title": title,
                "folder": folder,
                "note_file": note_file,
                "status": status,
                "arxiv": "",
                "pdf_file": "",
                "route": category,
                "title_cn": ""
            }
            papers_in_json.append(new_entry)
            print(f"Added new entry to progress.json: {title}")

    # Save
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    sync()
