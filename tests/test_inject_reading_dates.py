"""Tests for ``inject_reading_dates`` helpers."""

import os
import subprocess

from scripts.inject_reading_dates import git_last_modified_date, replace_reading_date


def test_replace_reading_date_swaps_iso_value():
    content = "# Title\n\n> 📅 阅读日期: 2026-05-17\n>\n> 🏷️ 板块: x\n"
    new, changed = replace_reading_date(content, "2026-06-17")
    assert changed
    assert "> 📅 阅读日期: 2026-06-17" in new
    assert "2026-05-17" not in new


def test_replace_reading_date_drops_trailing_annotation():
    content = "> 📅 阅读日期: 2026-05-20（2026-05-16 扩充：补全官方训练命令）\n"
    new, changed = replace_reading_date(content, "2026-06-20")
    assert changed
    assert new == "> 📅 阅读日期: 2026-06-20\n"


def test_replace_reading_date_fills_dash_placeholder():
    content = "> 📅 阅读日期: -\n"
    new, changed = replace_reading_date(content, "2026-06-01")
    assert changed
    assert new == "> 📅 阅读日期: 2026-06-01\n"


def test_replace_reading_date_idempotent_when_equal():
    content = "> 📅 阅读日期: 2026-06-17\n"
    new, changed = replace_reading_date(content, "2026-06-17")
    assert not changed
    assert new == content


def test_replace_reading_date_no_line_is_noop():
    content = "# Title\n\nNo reading date here.\n"
    new, changed = replace_reading_date(content, "2026-06-17")
    assert not changed
    assert new == content


def test_replace_reading_date_only_touches_header_blockquote():
    # A non-blockquote prose mention of 阅读日期 must stay intact.
    content = "> 📅 阅读日期: 2026-05-17\n\n正文也提到阅读日期: 2025-01-01，不应改动。\n"
    new, changed = replace_reading_date(content, "2026-06-17")
    assert changed
    assert "> 📅 阅读日期: 2026-06-17" in new
    assert "正文也提到阅读日期: 2025-01-01" in new


def _git(args, cwd, env=None):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True, env=env)


def test_git_last_modified_date_returns_committer_date(tmp_path):
    repo = tmp_path
    _git(["init"], repo)
    _git(["config", "user.email", "t@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)
    note = repo / "note.md"
    note.write_text("> 📅 阅读日期: 2020-01-01\n", encoding="utf-8")
    _git(["add", "note.md"], repo)
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": "2026-06-15T12:00:00",
        "GIT_COMMITTER_DATE": "2026-06-15T12:00:00",
    }
    _git(["-c", "commit.gpgsign=false", "commit", "-m", "add note"], repo, env=env)
    assert git_last_modified_date(str(note)) == "2026-06-15"


def test_git_last_modified_date_outside_repo_returns_none(tmp_path):
    note = tmp_path / "loose.md"
    note.write_text("no repo here\n", encoding="utf-8")
    assert git_last_modified_date(str(note)) is None
