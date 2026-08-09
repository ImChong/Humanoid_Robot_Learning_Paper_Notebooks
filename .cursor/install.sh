#!/usr/bin/env bash
# Idempotent Cloud Agent install for the Jekyll paper-notebook site.
# Safe to run repeatedly and against a cached/prebuilt snapshot.
set -euo pipefail

cd "$(dirname "$0")/.."

# --- System toolchain: Ruby (for Jekyll 4.3) + build deps for native gems ---
if ! command -v ruby >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    ruby-full ruby-bundler build-essential zlib1g-dev
fi

# --- Ruby gems for the static site (Jekyll + plugins) ---
# Gems install system-wide under /var/lib/gems, hence sudo (see AGENTS.md).
sudo bundle install

# --- Python tooling: lint (ruff), tests (pytest), and the HTML sanitizer deps ---
# Installed system-wide so `ruff`/`pytest` are on the default PATH for every shell.
sudo pip3 install --break-system-packages -r requirements-dev.txt

# --- Preprocess Markdown -> YAML front matter + _data/papers.json ---
# Required before any Jekyll build; idempotent (skips notes already prepared).
python3 scripts/prepare_pages.py
