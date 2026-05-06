"""Golden-file test for ``scripts.prepare_pages.process_papers``.

Builds a tiny isolated paper repository in a tmp dir, runs the side-effecting
``process_papers`` function against it (by monkey-patching its module-level
``BASE_DIR`` / ``PAPERS_DIR`` / ``PROGRESS_PATH``), and then asserts:

* front matter is added to notes that lack it,
* ``_data/papers.json`` is generated with the expected category & paper shape,
* notes that already have front matter are left untouched.
"""

import json
from pathlib import Path  # noqa: F401  -- imported for the type hint in _build_fixture_repo

import pytest

from scripts import prepare_pages

NOTE_WITH_METHOD = """# {title}

| **arXiv** | [1234.{idx:05d}](https://arxiv.org/abs/1234.{idx:05d}) |

## 🔧 方法详解

This is a fully written note. {body_padding}
"""


def _make_note_body(title: str, idx: int, lines: int = 200) -> str:
    body_padding = ("Lorem ipsum content. " * 5 + "\n") * lines
    return NOTE_WITH_METHOD.format(title=title, idx=idx, body_padding=body_padding)


def _build_fixture_repo(root: Path) -> None:
    papers = root / "papers"
    (papers / "01_Foundational_RL" / "PPO").mkdir(parents=True)
    (papers / "01_Foundational_RL" / "PPO" / "PPO.md").write_text(
        _make_note_body("Proximal Policy Optimization", 1), encoding="utf-8"
    )

    (papers / "02_Locomotion" / "WalkPaper").mkdir(parents=True)
    walk_md = (
        '---\nlayout: paper\ntitle: "Existing Title"\ncategory: "Locomotion"\n---\n\n'
        + _make_note_body("Walking", 2)
    )
    (papers / "02_Locomotion" / "WalkPaper" / "WalkPaper.md").write_text(
        walk_md, encoding="utf-8"
    )

    (papers / "todos").mkdir(parents=True)
    (papers / "todos" / "TODO_v1.md").write_text("ignored", encoding="utf-8")

    (papers / "PROGRESS.md").write_text(
        "| # | 论文 | 状态 |\n|---|------|------|\n"
        "| 1 | Proximal Policy Optimization | ✅ |\n"
        "| 2 | Walking | ⏳ |\n",
        encoding="utf-8",
    )


@pytest.fixture()
def fixture_repo(tmp_path, monkeypatch):
    """Build the fixture and re-point prepare_pages at it."""
    _build_fixture_repo(tmp_path)
    monkeypatch.setattr(prepare_pages, "BASE_DIR", str(tmp_path))
    monkeypatch.setattr(prepare_pages, "PAPERS_DIR", str(tmp_path / "papers"))
    monkeypatch.setattr(
        prepare_pages, "PROGRESS_PATH", str(tmp_path / "papers" / "PROGRESS.md")
    )
    return tmp_path


def test_process_papers_adds_frontmatter(fixture_repo, capsys):
    prepare_pages.process_papers()

    ppo_md = (fixture_repo / "papers" / "01_Foundational_RL" / "PPO" / "PPO.md").read_text(
        encoding="utf-8"
    )
    assert ppo_md.startswith("---\n"), "front matter must be prepended to notes that lack it"
    assert 'layout: paper' in ppo_md
    assert 'title: "Proximal Policy Optimization"' in ppo_md
    assert 'category: "Foundational RL"' in ppo_md


def test_process_papers_leaves_existing_frontmatter(fixture_repo):
    prepare_pages.process_papers()

    walk_md = (
        fixture_repo / "papers" / "02_Locomotion" / "WalkPaper" / "WalkPaper.md"
    ).read_text(encoding="utf-8")
    assert walk_md.startswith("---\n")
    fm_block = walk_md.split("---", 2)[1]
    assert fm_block.count("title:") == 1, "front matter should not be duplicated"
    assert 'title: "Existing Title"' in fm_block


def test_process_papers_emits_index(fixture_repo):
    prepare_pages.process_papers()

    papers_json = fixture_repo / "_data" / "papers.json"
    assert papers_json.exists(), "_data/papers.json must be generated"

    data = json.loads(papers_json.read_text(encoding="utf-8"))
    assert set(data.keys()) == {"01_Foundational_RL", "02_Locomotion"}, (
        "todos directory must be skipped"
    )

    assert data["01_Foundational_RL"]["display_name"] == "Foundational RL"
    assert data["02_Locomotion"]["display_name"] == "Locomotion"

    ppo_papers = data["01_Foundational_RL"]["papers"]
    assert len(ppo_papers) == 1
    assert ppo_papers[0]["title"] == "Proximal Policy Optimization"
    assert ppo_papers[0]["url"].endswith("/PPO.html")
    assert ppo_papers[0]["arxiv"] == "1234.00001"


def test_process_papers_is_idempotent(fixture_repo):
    """Running twice should not duplicate front matter or change papers.json."""
    prepare_pages.process_papers()
    first_json = (fixture_repo / "_data" / "papers.json").read_text(encoding="utf-8")
    first_ppo = (
        fixture_repo / "papers" / "01_Foundational_RL" / "PPO" / "PPO.md"
    ).read_text(encoding="utf-8")

    prepare_pages.process_papers()
    second_json = (fixture_repo / "_data" / "papers.json").read_text(encoding="utf-8")
    second_ppo = (
        fixture_repo / "papers" / "01_Foundational_RL" / "PPO" / "PPO.md"
    ).read_text(encoding="utf-8")

    assert first_json == second_json
    assert first_ppo == second_ppo


def test_process_papers_handles_quoted_title(tmp_path, monkeypatch):
    """Titles containing double quotes must remain valid YAML when re-emitted."""
    papers = tmp_path / "papers"
    (papers / "01_Test" / "Quoted").mkdir(parents=True)
    (papers / "01_Test" / "Quoted" / "Quoted.md").write_text(
        '# The "Groot" Model\n\n## 🔧 方法详解\n\n' + ("body line\n" * 200),
        encoding="utf-8",
    )
    (papers / "PROGRESS.md").write_text(
        "| # | 论文 | 状态 |\n|---|------|------|\n", encoding="utf-8"
    )

    monkeypatch.setattr(prepare_pages, "BASE_DIR", str(tmp_path))
    monkeypatch.setattr(prepare_pages, "PAPERS_DIR", str(papers))
    monkeypatch.setattr(prepare_pages, "PROGRESS_PATH", str(papers / "PROGRESS.md"))

    prepare_pages.process_papers()

    md = (papers / "01_Test" / "Quoted" / "Quoted.md").read_text(encoding="utf-8")
    head = md.split("---", 2)[1]
    # Title must use json-escaped quotes to remain valid YAML.
    assert '\\"Groot\\"' in head, f"YAML title must escape internal quotes; got: {head!r}"
