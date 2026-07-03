"""Tests for ``generate_updates_data`` helpers."""

import json
import os
import subprocess

from scripts.generate_updates_data import (
    build_updates_payload,
    collect_note_events,
    load_note_meta,
    run_git_log,
)

NOTE_A = "papers/01_Foundational_RL/PPO/PPO.md"
NOTE_B = "papers/05_Locomotion/HOMIE/HOMIE.md"


def _log(*chunks):
    return "\n".join(chunks) + "\n"


def test_collect_note_events_groups_by_day():
    log_text = _log(
        "\x012026-07-02",
        "",
        f"M\t{NOTE_A}",
        f"A\t{NOTE_B}",
        "\x012026-07-01",
        "",
        f"A\t{NOTE_A}",
    )
    touched, added = collect_note_events(log_text, [NOTE_A, NOTE_B])
    assert touched == {
        "2026-07-02": {NOTE_A, NOTE_B},
        "2026-07-01": {NOTE_A},
    }
    assert added == {NOTE_A: "2026-07-01", NOTE_B: "2026-07-02"}


def test_collect_note_events_ignores_unknown_and_non_note_paths():
    log_text = _log(
        "\x012026-07-02",
        "",
        "M\tpapers/PROGRESS.md",
        "M\tpapers/01_Foundational_RL/PPO/PPO.pdf",
        f"M\t{NOTE_A}",
    )
    touched, _added = collect_note_events(log_text, [NOTE_A])
    assert touched == {"2026-07-02": {NOTE_A}}


def test_collect_note_events_follows_renames():
    old = "papers/01_Foundational_RL/PPO_old/PPO_old.md"
    log_text = _log(
        "\x012026-07-03",
        "",
        f"M\t{NOTE_A}",
        "\x012026-07-02",
        "",
        f"R095\t{old}\t{NOTE_A}",
        "\x012026-07-01",
        "",
        f"A\t{old}",
    )
    touched, added = collect_note_events(log_text, [NOTE_A])
    assert touched == {
        "2026-07-03": {NOTE_A},
        "2026-07-02": {NOTE_A},
        "2026-07-01": {NOTE_A},
    }
    assert added == {NOTE_A: "2026-07-01"}


def test_collect_note_events_stops_at_deletion_of_dead_namesake():
    # NOTE_A was deleted and later re-created; history older than the deletion
    # belongs to a dead file and must not count.
    log_text = _log(
        "\x012026-07-03",
        "",
        f"A\t{NOTE_A}",
        "\x012026-07-02",
        "",
        f"D\t{NOTE_A}",
        "\x012026-07-01",
        "",
        f"A\t{NOTE_A}",
    )
    touched, added = collect_note_events(log_text, [NOTE_A])
    assert touched == {"2026-07-03": {NOTE_A}}
    assert added == {NOTE_A: "2026-07-03"}


def test_build_updates_payload_splits_added_and_maintained():
    touched = {
        "2026-07-01": {NOTE_A},
        "2026-07-02": {NOTE_A, NOTE_B},
    }
    added = {NOTE_A: "2026-07-01", NOTE_B: "2026-07-02"}
    meta = {
        NOTE_A: {"t": "PPO", "u": "/papers/01_Foundational_RL/PPO/PPO.html"},
        NOTE_B: {"t": "HOMIE", "u": "/papers/05_Locomotion/HOMIE/HOMIE.html"},
    }
    payload = build_updates_payload(touched, added, meta)

    assert [n["t"] for n in payload["notes"]] == ["PPO", "HOMIE"]
    assert payload["days"] == [
        {"d": "2026-07-02", "a": [1], "m": [0]},
        {"d": "2026-07-01", "a": [0]},
    ]


def test_build_updates_payload_falls_back_to_oldest_touch_as_added():
    touched = {"2026-07-01": {NOTE_A}, "2026-07-02": {NOTE_A}}
    payload = build_updates_payload(touched, {}, {})
    assert payload["days"] == [
        {"d": "2026-07-02", "m": [0]},
        {"d": "2026-07-01", "a": [0]},
    ]
    # Fallback metadata is derived from the file name.
    assert payload["notes"][0]["t"] == "PPO"
    assert payload["notes"][0]["u"] == "/papers/01_Foundational_RL/PPO/PPO.html"


def test_load_note_meta_indexes_top_level_and_subcategory_papers(tmp_path):
    papers_json = tmp_path / "papers.json"
    papers_json.write_text(
        json.dumps(
            {
                "01_Foundational_RL": {
                    "display_name": "Foundational RL",
                    "zhname": "基础强化学习",
                    "papers": [
                        {
                            "title": "PPO",
                            "zh_title": "近端策略优化",
                            "path": NOTE_A,
                            "url": "/papers/01_Foundational_RL/PPO/PPO.html",
                        }
                    ],
                    "subcategories": [
                        {
                            "name": "Sub",
                            "papers": [
                                {
                                    "title": "HOMIE",
                                    "path": NOTE_B,
                                    "url": "/papers/05_Locomotion/HOMIE/HOMIE.html",
                                }
                            ],
                        }
                    ],
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    meta = load_note_meta(str(papers_json))
    assert meta[NOTE_A] == {
        "t": "PPO",
        "u": "/papers/01_Foundational_RL/PPO/PPO.html",
        "z": "近端策略优化",
        "c": "Foundational RL",
        "cz": "基础强化学习",
    }
    assert meta[NOTE_B]["t"] == "HOMIE"
    assert "z" not in meta[NOTE_B]


def test_load_note_meta_missing_file_returns_empty(tmp_path):
    assert load_note_meta(str(tmp_path / "missing.json")) == {}


def _git(args, cwd, env=None):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True, env=env)


def _commit_all(repo, message, date):
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": f"{date}T12:00:00",
        "GIT_COMMITTER_DATE": f"{date}T12:00:00",
    }
    _git(["add", "-A"], repo)
    _git(["-c", "commit.gpgsign=false", "commit", "-m", message], repo, env=env)


def test_run_git_log_end_to_end(tmp_path):
    repo = tmp_path
    _git(["init"], repo)
    _git(["config", "user.email", "t@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)

    note_dir = repo / "papers" / "01_Foundational_RL" / "PPO"
    note_dir.mkdir(parents=True)
    note = note_dir / "PPO.md"
    note.write_text("# PPO\n", encoding="utf-8")
    _commit_all(repo, "add note", "2026-07-01")

    note.write_text("# PPO\nmore\n", encoding="utf-8")
    _commit_all(repo, "update note", "2026-07-02")

    log_text = run_git_log(str(repo))
    touched, added = collect_note_events(log_text, [NOTE_A])
    assert added == {NOTE_A: "2026-07-01"}
    assert touched == {
        "2026-07-01": {NOTE_A},
        "2026-07-02": {NOTE_A},
    }
