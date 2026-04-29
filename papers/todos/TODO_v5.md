# Implementation Plan: Code Quality & Script Infrastructure (v5)

## Overview
Based on the code review findings from `code-review-and-quality`, this plan aims to improve the robustness, consistency, and security of the project's maintenance scripts. It focuses on unifying the logic between `prepare_pages.py` and `sync_progress.py`, securing metadata handling, and improving architectural clarity.

## Architecture Decisions
- **Source of Truth Consistency**: Align `is_stub` logic across all scripts to ensure consistent status reporting.
- **Defensive Metadata Handling**: Implement proper escaping for YAML frontmatter to prevent parsing errors.
- **Modularization**: Extract shared logic (normalization, stub detection) into a common module if possible, or at least synchronize implementations.

## Task List

### Phase 1: Correctness & Security (High Priority)
- [ ] **Task 1: Secure YAML Frontmatter Generation**
    - **Description**: Fix the potential JSON/YAML injection in `prepare_pages.py` by properly escaping paper titles.
    - **Acceptance criteria**:
        - Titles containing double quotes (e.g., `The "Groot" Model`) are correctly escaped in the output `.md` files.
        - Frontmatter remains valid YAML.
    - **Verification**:
        - Manual check of a file with a quoted title.
        - Run `python3 scripts/prepare_pages.py` and ensure no crashes.
    - **Files**: `scripts/prepare_pages.py`
    - **Scope**: Small

- [ ] **Task 2: Unify Stub Detection Logic**
    - **Description**: Synchronize the `is_stub` / `check_stub` criteria between `prepare_pages.py` and `sync_progress.py`.
    - **Acceptance criteria**:
        - Both scripts use the same thresholds (lines, required headings, marker counts).
        - No file is reported as `done` in one script and `stub` in another.
    - **Verification**:
        - Run both scripts and compare outputs/logs.
    - **Files**: `scripts/prepare_pages.py`, `scripts/sync_progress.py`
    - **Scope**: Small

### Phase 2: Readability & Refactoring
- [ ] **Task 3: Refactor `process_papers` in `prepare_pages.py`**
    - **Description**: Break down the monolithic 150-line function into logical sub-functions.
    - **Acceptance criteria**:
        - Function is split into `extract_metadata`, `handle_frontmatter`, `generate_paper_entry`, etc.
        - No change in output `_data/papers.json` content.
    - **Verification**:
        - `diff` the generated `papers.json` before and after refactoring.
    - **Files**: `scripts/prepare_pages.py`
    - **Scope**: Medium

- [ ] **Task 4: Add UTF-8 Encoding to `sync_progress.py`**
    - **Description**: Explicitly set `encoding='utf-8'` in all file open operations in `sync_progress.py`.
    - **Acceptance criteria**:
        - Script runs correctly on systems where the default encoding is not UTF-8.
    - **Verification**:
        - Script execution succeeds.
    - **Files**: `scripts/sync_progress.py`
    - **Scope**: XS

### Phase 3: Infrastructure & Documentation (R2 from v4)
- [ ] **Task 5: Add Local Jekyll Setup Instructions**
    - **Description**: Document how to install `bundle`, `jekyll`, and other dependencies.
    - **Acceptance criteria**:
        - Clear instructions added to `README.md` or a new `SETUP.md`.
    - **Files**: `README.md`
    - **Scope**: Small

## Checkpoint: Foundation & Quality
- [ ] `prepare_pages.py` and `sync_progress.py` produce consistent status reports.
- [ ] Metadata extraction is robust against special characters.
- [ ] Code is modular and follows PEP8.

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Refactoring breaks `papers.json` structure | High | Backup `papers.json` and use `diff` to verify zero-change output. |
| YAML escaping issues with complex titles | Med | Use simple `replace('"', '\\"')` or a dedicated library if needed. |

## Open Questions
- Should we create a `scripts/utils.py` for shared logic like normalization and stub checking? (Recommended for Phase 2)
