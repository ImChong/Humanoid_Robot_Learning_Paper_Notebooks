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

PROGRESS_PATH = os.path.join(PAPERS_DIR, "PROGRESS.md")

# Keep homepage category order aligned with
# https://github.com/YanjieZe/awesome-humanoid-robot-learning.
CATEGORY_ORDER = [
    "01_Foundational_RL",
    "02_Motion_Retargeting",
    "03_High_Impact_Selection",
    "04_Loco-Manipulation_and_WBC",
    "06_Manipulation",
    "07_Teleoperation",
    "05_Locomotion",
    "08_Navigation",
    "09_State_Estimation",
    "10_Sim-to-Real",
    "12_Hardware_Design",
    "11_Simulation_Benchmark",
    "13_Physics-Based_Animation",
    "14_Human_Motion",
]

# Canonical Chinese category names aligned with upstream section semantics.
CATEGORY_ZHNAME = {
    "01_Foundational_RL": "基础强化学习",
    "02_Motion_Retargeting": "运动重定向",
    "03_High_Impact_Selection": "高影响力精选",
    "04_Loco-Manipulation_and_WBC": "运动操作与全身控制",
    "05_Locomotion": "行走运动",
    "06_Manipulation": "灵巧操作",
    "07_Teleoperation": "遥操作",
    "08_Navigation": "导航",
    "09_State_Estimation": "状态估计",
    "10_Sim-to-Real": "仿真到现实",
    "11_Simulation_Benchmark": "仿真与基准",
    "12_Hardware_Design": "硬件设计",
    "13_Physics-Based_Animation": "物理动画",
    "14_Human_Motion": "人体动作分析与生成",
}

# Categories that keep curated reading order from PROGRESS / front matter
# instead of arXiv-based sorting.
#
# Other modules default to arXiv newest-first (新→旧). Motion retargeting and
# high-impact selection (including all subcategories) use oldest-first (旧→新).

# ⚡ Bolt Optimization: Globally pre-compile regular expressions used inside loops
# and high-frequency functions to prevent the regex engine from re-parsing the
# pattern on every iteration, reducing CPU overhead and allocation churn.
_EMPTY_TABLE_ROW_RE = re.compile(r"^\|[\s\-:|]+\|$")
_DASH_ROW_RE = re.compile(r"^-+$")
_LABEL_STARS_RE = re.compile(r"\*+")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_MD_CHARS_RE = re.compile(r"[*_`\[\]]")
_CATEGORY_PREFIX_RE = re.compile(r"^\d+_")
_ARXIV_ID_PARTS_RE = re.compile(r"^(\d{2})(\d{2})\.(\d{4,5})(?:v\d+)?$")
_ARXIV_VERSION_SUFFIX_RE = re.compile(r"v\d+$")
_ARXIV_FALLBACK_RE = re.compile(r"arxiv", re.IGNORECASE)
_ARXIV_PATTERNS = [
    re.compile(r"\|\s*(?:\*\*)?arXiv(?:\*\*)?\s*\|\s*\[?(\d{4}\.\d{4,5}(?:v\d+)?)", re.IGNORECASE),
    re.compile(r"(?:arXiv:|arxiv\.org/(?:abs|html|pdf)/)(\d{4}\.\d{4,5}(?:v\d+)?)", re.IGNORECASE),
]

CATEGORIES_PROGRESS_ORDER = frozenset({
    "01_Foundational_RL",
})

CATEGORIES_ARXIV_OLDEST_FIRST = frozenset({
    "02_Motion_Retargeting",
    "03_High_Impact_Selection",
})

CATEGORY_SORT_ORDER_HINT = {
    "01_Foundational_RL": {
        "en": "Paper tags ordered by recommended learning path",
        "zh": "论文标签按推荐阅读路线顺序排列",
    },
    "02_Motion_Retargeting": {
        "en": "Paper tags ordered by arXiv date, oldest first",
        "zh": "论文标签按 arXiv 发表时间旧→新排列",
    },
    "03_High_Impact_Selection": {
        "en": "Paper tags ordered by arXiv date, oldest first (same within subcategories)",
        "zh": "论文标签按 arXiv 发表时间旧→新排列（各子模块同理）",
    },
}

DEFAULT_SORT_ORDER_HINT = {
    "en": "Paper tags ordered by arXiv date, newest first",
    "zh": "论文标签按 arXiv 发表时间新→旧排列",
}

_SUBCATEGORY_SORT_ORDER_HINT = {
    "en": "Paper tags ordered by arXiv date, oldest first",
    "zh": "论文标签按 arXiv 发表时间旧→新排列",
}


def apply_sort_order_hint(entry, category_dir):
    """Attach bilingual sort-order hints for the homepage category block."""
    hint = CATEGORY_SORT_ORDER_HINT.get(category_dir, DEFAULT_SORT_ORDER_HINT)
    entry["sort_order_hint"] = hint["en"]
    entry["sort_order_hint_zh"] = hint["zh"]
    if category_dir in CATEGORIES_ARXIV_OLDEST_FIRST:
        for subcat in entry.get("subcategories", []):
            subcat["sort_order_hint"] = _SUBCATEGORY_SORT_ORDER_HINT["en"]
            subcat["sort_order_hint_zh"] = _SUBCATEGORY_SORT_ORDER_HINT["zh"]


_TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def extract_title(content):
    """Extract title from first H1 heading."""
    start_idx = 0
    # ⚡ Bolt Optimization: Use `find` to skip frontmatter without string copies,
    # and use `find('#')` as a fast pre-check before running the regex.
    if has_frontmatter(content):
        end_idx = content.find("---", 3)
        if end_idx != -1:
            start_idx = end_idx + 3

    if content.find("#", start_idx) != -1:
        match = _TITLE_RE.search(content, start_idx)
        if match:
            return match.group(1).strip()
    return None


# ``is_stub`` and ``normalize_name`` are now provided by ``_common``; we keep
# this module-level binding so ``from scripts.prepare_pages import normalize_name``
# (used by tests) still works.
_ = (is_stub, normalize_name)  # re-exported for backwards compatibility


_BASIC_INFO_SECTION_RE = re.compile(
    r"^##\s*📋\s*基本信息\s*$",
    re.MULTILINE,
)
_NEXT_H2_RE = re.compile(r"^##\s", re.MULTILINE)
_PUBLISH_DATE_LABEL_RE = re.compile(r"发布时间")
_CODE_ROW_LABEL_RE = re.compile(
    r"(?:代码|源码|GitHub|官方代码|算法代码)",
    re.IGNORECASE,
)
_CODE_ROW_EXCLUDE_LABEL_RE = re.compile(
    r"相关|许可|文档|主页|进阶|配套|同组|项目主页",
    re.IGNORECASE,
)
_NO_OPEN_SOURCE_VALUE_RE = re.compile(
    r"未开源|暂未开源|暂无公开|未见到.*(?:官方|独立)|未集中给出|原文未开源|"
    r"待官方释出|待确认公开|🚧|暂未完全公开|暂无公开仓库",
    re.IGNORECASE,
)
_GITHUB_REPO_URL_RE = re.compile(
    r"https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]+",
    re.IGNORECASE,
)


def _extract_basic_info_section(content):
    """Return markdown under the ``## 📋 基本信息`` heading, or ``None``."""
    # ⚡ Bolt Optimization: Use fast `in` operator to short-circuit regex execution
    # when the heading is absent, and scan for the next heading using the `pos`
    # parameter (`start`) to avoid a massive O(N) string allocation for `content[start:]`.
    if "基本信息" not in content:
        return None
    match = _BASIC_INFO_SECTION_RE.search(content)
    if not match:
        return None
    start = match.end()
    next_heading = _NEXT_H2_RE.search(content, start)
    end = next_heading.start() if next_heading else len(content)
    return content[start:end]


def _clean_table_cell_value(value):
    """Strip markdown links and HTML for plain-text metadata display."""
    value = _MD_LINK_RE.sub(r"\1", value)
    value = re.sub(r"<br\s*/?>", "; ", value, flags=re.IGNORECASE)
    value = _MD_CHARS_RE.sub("", value)
    return " ".join(value.split()).strip()


def extract_published_date(content):
    """Extract publication date from the basic-info table, if present."""
    section = _extract_basic_info_section(content)
    if not section:
        return None

    for line in section.split("\n"):
        line = line.strip()
        if not line.startswith("|") or _EMPTY_TABLE_ROW_RE.match(line):
            continue
        cols = [c.strip() for c in line.split("|")]
        cols = [c for c in cols if c]
        if len(cols) < 2:
            continue

        label = _LABEL_STARS_RE.sub("", cols[0]).strip()
        if not _PUBLISH_DATE_LABEL_RE.search(label):
            continue

        value = cols[-1] if len(cols) == 2 else " | ".join(cols[1:])
        cleaned = _clean_table_cell_value(value)
        return cleaned or None

    return None


def extract_has_open_source(content):
    """True when the basic-info table links to this paper's open-source code on GitHub."""
    section = _extract_basic_info_section(content)
    if not section:
        return False

    for line in section.split("\n"):
        line = line.strip()
        if not line.startswith("|") or _EMPTY_TABLE_ROW_RE.match(line):
            continue
        cols = [c.strip() for c in line.split("|")]
        cols = [c for c in cols if c]
        if len(cols) < 2:
            continue

        label = _LABEL_STARS_RE.sub("", cols[0]).strip()
        value = cols[-1] if len(cols) == 2 else " | ".join(cols[1:])

        if _CODE_ROW_EXCLUDE_LABEL_RE.search(label):
            continue
        if not _CODE_ROW_LABEL_RE.search(label):
            continue
        if _NO_OPEN_SOURCE_VALUE_RE.search(value):
            continue
        if _GITHUB_REPO_URL_RE.search(value):
            return True

    return False


def extract_arxiv(content):
    """Extract arXiv ID from common note metadata table formats."""
    # ⚡ Bolt Optimization: Avoid re.search and string lowercasing copies by
    # checking for the most common casing variants with the fast `in` operator.
    # Case-insensitive pre-check: the patterns below use IGNORECASE, so the
    # guard must not require the exact substrings ``arxiv`` / ``arXiv`` (e.g.
    # ``| ARXIV |`` or ``Arxiv:`` would otherwise be skipped and drop metadata).
    if (
        "arxiv" not in content
        and "arXiv" not in content
        and "Arxiv" not in content
        and "ARXIV" not in content
        and "ArXiv" not in content
    ):
        # Fallback to a case-insensitive regex check for unusual casings
        # to guarantee 100% correctness without regressions.
        if _ARXIV_FALLBACK_RE.search(content) is None:
            return None

    for pattern in _ARXIV_PATTERNS:
        match = pattern.search(content)
        if match:
            return match.group(1)
    return None


def get_category_name(category_dir):
    """Clean category directory name for display."""
    name = _CATEGORY_PREFIX_RE.sub("", category_dir)
    name = name.replace("_", " ")
    return name


def parse_progress_order():
    """
    Parse PROGRESS.md to extract paper ordering within each section.
    Returns a dict: { normalized_paper_name: order_index }
    We use the paper title/name from the PROGRESS.md table rows.
    """
    if not os.path.exists(PROGRESS_PATH):
        return {}

    with open(PROGRESS_PATH, encoding="utf-8") as f:
        content = f.read()

    # Extract all paper names mentioned in table rows (| # | paper_name | ... |)
    # This captures the order they appear in README
    order = {}
    idx = 0

    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip header/separator rows
        cols = [c.strip() for c in line.split("|")]
        cols = [c for c in cols if c]  # remove empty
        if len(cols) < 2:
            continue
        if cols[0] in ("#", "---", "----", "-----") or _DASH_ROW_RE.match(cols[0]):
            continue
        # First col is usually the number, second is paper name/title
        paper_col = cols[1] if len(cols) > 1 else cols[0]

        # Extract the key text (remove markdown links, bold, etc.)
        paper_text = _MD_LINK_RE.sub(r"\1", paper_col)
        paper_text = _MD_CHARS_RE.sub("", paper_text)
        paper_text = paper_text.strip()

        if not paper_text or paper_text in ("论文", "---", "笔记", "状态", "日期", "路线"):
            continue

        # Normalize for matching: lowercase, remove special chars
        normalized = normalize_name(paper_text)
        if normalized and len(normalized) > 3:
            order[normalized] = idx
            idx += 1

    return order


_H_INDEX_RE = re.compile(r"^H(\d+)$", re.IGNORECASE)
_ARXIV_IN_MARKDOWN_CELL_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|html|pdf)/|arxiv:)(\d{4}\.\d{4,5}(?:v\d+)?)",
    re.IGNORECASE,
)


def _arxiv_sort_key(arxiv_id):
    """Return sortable key for arXiv IDs (newest first when reversed).

    Supports modern IDs such as ``2603.12686``; unknown formats sort last.
    """
    if not arxiv_id:
        return (-1, -1, -1)
    m = _ARXIV_ID_PARTS_RE.match(str(arxiv_id).strip())
    if not m:
        return (-1, -1, -1)
    yy, mm, seq = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return (yy, mm, seq)


def _order_tiebreaker(paper, *, newest_first: bool):
    """Secondary sort key from PROGRESS / front-matter ``paper_order``."""
    order_val = paper.get("_order")
    if not isinstance(order_val, int):
        order_val = 10**9
    return -order_val if newest_first else order_val


def sort_papers_by_arxiv(papers, *, newest_first: bool):
    """Sort papers by arXiv ID; ``newest_first`` controls direction."""
    papers.sort(
        key=lambda p: (
            _arxiv_sort_key(p.get("arxiv")),
            _order_tiebreaker(p, newest_first=newest_first),
        ),
        reverse=newest_first,
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

    with open(PROGRESS_PATH, encoding="utf-8") as f:
        content = f.read()

    by_name = {}
    by_arxiv = {}

    for line in content.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.split("|")]
        cols = [c for c in cols if c]
        if len(cols) < 2:
            continue
        if cols[0] in ("#", "---", "----", "-----") or _DASH_ROW_RE.match(cols[0]):
            continue

        tag_m = _H_INDEX_RE.match(cols[0])
        if not tag_m:
            continue

        h_num = int(tag_m.group(1))
        paper_col = cols[1]

        for ax_m in _ARXIV_IN_MARKDOWN_CELL_RE.finditer(paper_col):
            ax = _ARXIV_VERSION_SUFFIX_RE.sub("", ax_m.group(1).lower())
            by_arxiv[ax] = h_num

        paper_text = _MD_LINK_RE.sub(r"\1", paper_col)
        paper_text = _MD_CHARS_RE.sub("", paper_text)
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
        if _ARXIV_VERSION_SUFFIX_RE.search(ax_key):
            ax_key = _ARXIV_VERSION_SUFFIX_RE.sub("", ax_key)
            if ax_key in by_arxiv:
                return by_arxiv[ax_key]

    norm_title = normalize_name(paper_title)
    if norm_title and norm_title in by_name:
        return by_name[norm_title]

    norm_dir = normalize_name(paper_dir.replace("_", " "))
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

    norm_dir = normalize_name(paper_dir.replace("_", " "))
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
    existing_papers_json_path = os.path.join(BASE_DIR, "_data", "papers.json")
    existing_papers_json = {}
    existing_paper_meta = {}  # title/path -> metadata from existing data
    if os.path.exists(existing_papers_json_path):
        try:
            with open(existing_papers_json_path, encoding="utf-8") as f:
                existing_papers_json = json.load(f)
            # Build metadata lookup from all papers (top-level and subcategory)
            for cat_data in existing_papers_json.values():
                for p in cat_data.get("papers", []):
                    existing_paper_meta[p.get("title")] = p
                    existing_paper_meta[p.get("path")] = p
                for sc in cat_data.get("subcategories", []):
                    for p in sc.get("papers", []):
                        existing_paper_meta[p.get("title")] = p
                        existing_paper_meta[p.get("path")] = p
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
                if not fname.endswith(".md"):
                    continue

                fpath = os.path.join(paper_path, fname)

                with open(fpath, encoding="utf-8") as f:
                    content = f.read()

                normalized, meta_changed = normalize_paper_meta_blockquotes(content)
                if meta_changed:
                    content = normalized
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"  Normalized meta blockquotes: {fpath}")

                check_stub(fpath, content)

                title = extract_title(content) or paper_dir.replace("_", " ")

                # Add front matter if not present
                if not has_frontmatter(content):
                    # Use json.dumps to safely escape title and category for YAML
                    safe_title = json.dumps(title, ensure_ascii=False)
                    safe_category = json.dumps(category_display, ensure_ascii=False)
                    frontmatter = f"---\nlayout: paper\ntitle: {safe_title}\ncategory: {safe_category}\n---\n\n"
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(frontmatter + content)
                    print(f"  Added front matter: {fpath}")
                else:
                    print(f"  Already has front matter: {fpath}")

                rel_path = os.path.relpath(fpath, BASE_DIR)
                url_path = "/" + rel_path.rsplit(".md", 1)[0] + ".html"

                # ⚡ Bolt Optimization: Extract front matter explicitly with O(1) parsing
                # instead of running multiple multi-line regexes over the whole file
                frontmatter_meta = parse_frontmatter(content)

                arxiv_for_order = extract_arxiv(content)

                order_idx = match_paper_order(title, paper_dir, progress_order)

                if category_dir == "03_High_Impact_Selection":
                    h_idx = match_high_impact_h_order(title, paper_dir, arxiv_for_order, hi_by_name, hi_by_arxiv)
                    if h_idx is not None:
                        order_idx = h_idx
                    elif "paper_order" in frontmatter_meta:
                        try:
                            order_idx = int(frontmatter_meta["paper_order"])
                        except ValueError:
                            pass
                elif "paper_order" in frontmatter_meta:
                    # Front-matter `paper_order: <n>` overrides PROGRESS.md matching.
                    # Used to put papers in README's recommended learning-path order
                    # even when their titles don't match the awesome-list table rows.
                    try:
                        order_idx = int(frontmatter_meta["paper_order"])
                    except ValueError:
                        pass

                # Extract subcategory from front matter if present
                paper_subcat = frontmatter_meta.get("subcategory")

                paper_entry = {
                    "title": title,
                    "path": rel_path,
                    "url": url_path,
                    "dir": paper_dir,
                    "_order": order_idx,
                    "_subcategory": paper_subcat,
                }

                existing_meta_for_paper = existing_paper_meta.get(title) or existing_paper_meta.get(rel_path) or {}

                # Extract arXiv ID, preserving existing metadata when the note
                # uses a format the parser does not recognize.
                arxiv = arxiv_for_order or existing_meta_for_paper.get("arxiv")
                if arxiv:
                    paper_entry["arxiv"] = arxiv

                if extract_has_open_source(content):
                    paper_entry["has_open_source"] = True

                published_date = extract_published_date(content) or existing_meta_for_paper.get(
                    "published_date"
                )
                if published_date:
                    paper_entry["published_date"] = published_date

                # Prefer zhname from front matter when present
                if "zhname" in frontmatter_meta:
                    paper_entry["zhname"] = frontmatter_meta["zhname"]
                # Otherwise restore zhname from existing data if available
                elif existing_meta_for_paper.get("zhname"):
                    paper_entry["zhname"] = existing_meta_for_paper["zhname"]

                papers.append(paper_entry)

        if category_dir in CATEGORIES_PROGRESS_ORDER:
            papers.sort(key=lambda p: p["_order"])
        elif category_dir in CATEGORIES_ARXIV_OLDEST_FIRST:
            sort_papers_by_arxiv(papers, newest_first=False)
        else:
            sort_papers_by_arxiv(papers, newest_first=True)
        # Load existing category meta (subtitle, subcategories) from current papers.json
        existing_meta = existing_papers_json.get(category_dir, {})

        if papers:
            entry = {"display_name": category_display, "papers": papers}
        else:
            entry = {"display_name": category_display, "papers": []}

        # Preserve subtitle, i18n names, and subtitle_zh if exists
        if "subtitle" in existing_meta:
            entry["subtitle"] = existing_meta["subtitle"]
        if "subtitle_zh" in existing_meta:
            entry["subtitle_zh"] = existing_meta["subtitle_zh"]
        # Support both zhname (new) and display_name_zh (legacy) field names
        if category_dir in CATEGORY_ZHNAME:
            entry["zhname"] = CATEGORY_ZHNAME[category_dir]
        elif "zhname" in existing_meta:
            entry["zhname"] = existing_meta["zhname"]
        elif "display_name_zh" in existing_meta:
            entry["zhname"] = existing_meta["display_name_zh"]

        # Distribute papers into subcategories if defined
        if "subcategories" in existing_meta:
            subcats = [dict(s) for s in existing_meta["subcategories"]]
            # Reset papers in each subcat and migrate name_zh -> zhname
            for s in subcats:
                s["papers"] = []
                if "name_zh" in s:
                    s["zhname"] = s.pop("name_zh")
            subcat_map = {s["name"]: s for s in subcats}
            ungrouped = []
            for paper in papers:
                paper_subcat = paper.get("_subcategory")
                if paper_subcat and paper_subcat in subcat_map:
                    subcat_map[paper_subcat]["papers"].append(paper)
                else:
                    ungrouped.append(paper)
            entry["subcategories"] = subcats
            # ungrouped papers stay in top-level papers list
            entry["papers"] = ungrouped
            if category_dir in CATEGORIES_ARXIV_OLDEST_FIRST:
                for sc in entry["subcategories"]:
                    sort_papers_by_arxiv(sc["papers"], newest_first=False)

        apply_sort_order_hint(entry, category_dir)

        # Remove internal fields
        for p in papers:
            if "_order" in p:
                del p["_order"]
            if "_subcategory" in p:
                del p["_subcategory"]

        index_data[category_dir] = entry

    # Ensure ALL category directories appear (even if empty)
    for category_dir in sorted(os.listdir(PAPERS_DIR)):
        category_path = os.path.join(PAPERS_DIR, category_dir)
        if category_dir in SKIP_DIRS:
            continue
        if os.path.isdir(category_path) and category_dir not in index_data:
            existing_meta = existing_papers_json.get(category_dir, {})
            entry = {"display_name": get_category_name(category_dir), "papers": []}
            if "subtitle" in existing_meta:
                entry["subtitle"] = existing_meta["subtitle"]
            if "subtitle_zh" in existing_meta:
                entry["subtitle_zh"] = existing_meta["subtitle_zh"]
            if category_dir in CATEGORY_ZHNAME:
                entry["zhname"] = CATEGORY_ZHNAME[category_dir]
            elif "zhname" in existing_meta:
                entry["zhname"] = existing_meta["zhname"]
            elif "display_name_zh" in existing_meta:
                entry["zhname"] = existing_meta["display_name_zh"]
            if "subcategories" in existing_meta:
                entry["subcategories"] = [dict(s, papers=[]) for s in existing_meta["subcategories"]]
                for s in entry["subcategories"]:
                    if "name_zh" in s:
                        s["zhname"] = s.pop("name_zh")
            apply_sort_order_hint(entry, category_dir)
            index_data[category_dir] = entry

    # Sort by upstream awesome-list order first; unknown folders keep lexical tail order.
    rank = {name: i for i, name in enumerate(CATEGORY_ORDER)}
    sorted_data = dict(
        sorted(
            index_data.items(),
            key=lambda kv: (rank.get(kv[0], len(CATEGORY_ORDER)), kv[0]),
        )
    )

    # Write index data
    data_dir = os.path.join(BASE_DIR, "_data")
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, "papers.json"), "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    total = sum(
        len(v["papers"]) + sum(len(s.get("papers", [])) for s in v.get("subcategories", []))
        for v in sorted_data.values()
    )
    print(f"\nGenerated _data/papers.json with {total} papers in {len(sorted_data)} categories")


if __name__ == "__main__":
    print("Preparing paper pages for Jekyll...\n")
    process_papers()
    print("\nDone!")
