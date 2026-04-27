#!/usr/bin/env python3
"""自动更新 README.md 中的 Papers 和 Notes badge 数字."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
PROGRESS = ROOT / "papers" / "PROGRESS.md"
PAPERS_DIR = ROOT / "papers"
PAPERS_JSON = ROOT / "_data" / "papers.json"


def count_papers() -> int:
    """统计 PROGRESS.md 中的论文总数（所有状态）."""
    text = PROGRESS.read_text(encoding="utf-8")
    return len(re.findall(r"[✅📖⏳]", text))


def count_notes() -> int:
    """统计 notes 数，优先使用 _data/papers.json（与主页列表同口径）。"""
    if PAPERS_JSON.exists():
        data = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
        total = 0
        for cat_data in data.values():
            total += len(cat_data.get("papers", []))
            for subcat in cat_data.get("subcategories", []):
                total += len(subcat.get("papers", []))
        return total

    # 回退：按目录结构统计论文笔记
    excluded_names = {"PROGRESS.md"}
    excluded_dirs = {"todos"}
    return sum(
        1
        for f in PAPERS_DIR.rglob("*.md")
        if f.name not in excluded_names
        and not f.name.startswith("TODO")
        and not any(part in excluded_dirs for part in f.relative_to(PAPERS_DIR).parts)
        and len(f.relative_to(PAPERS_DIR).parts) >= 3
    )


def update_badge(text: str, label: str, new_value: int) -> str:
    """替换 badge 中的数字, e.g. Papers-468-orange → Papers-500-orange."""
    pattern = rf"({re.escape(label)})-\d+(-\w+\.svg)"
    return re.sub(pattern, rf"\g<1>-{new_value}\2", text)


def main():
    papers = count_papers()
    notes = count_notes()

    text = README.read_text(encoding="utf-8")
    new_text = update_badge(text, "Papers", papers)
    new_text = update_badge(new_text, "Notes", notes)

    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print(f"✅ Updated: Papers={papers}, Notes={notes}")
    else:
        print(f"ℹ️  No change: Papers={papers}, Notes={notes}")


if __name__ == "__main__":
    main()
