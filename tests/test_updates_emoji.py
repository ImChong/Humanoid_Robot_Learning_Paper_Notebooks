"""Update Log seasonal emoji: date rules + markup hooks."""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMOJI_JS = ROOT / "assets" / "js" / "updates-emoji.js"
INDEX = ROOT / "index.html"
UPDATES = ROOT / "updates.html"
LAYOUT = ROOT / "_layouts" / "default.html"


def test_updates_emoji_markup_hooks():
    index = INDEX.read_text(encoding="utf-8")
    updates = UPDATES.read_text(encoding="utf-8")
    layout = LAYOUT.read_text(encoding="utf-8")

    assert 'class="js-updates-emoji"' in index
    assert 'class="js-updates-emoji"' in updates
    assert "assets/js/updates-emoji.js" in layout
    # Emoji is separated from i18n text so language toggle does not wipe it.
    assert 'data-en="Update Log"' in updates
    assert 'data-zh="更新记录"' in updates
    assert 'data-en="📅 Update Log"' not in updates


def test_updates_emoji_calendar_via_node():
    """Resolve a few fixed dates through the shipped JS (viewer-local calendar)."""
    script = f"""
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync({str(EMOJI_JS)!r}, 'utf8');
const sandbox = {{
  window: {{}},
  document: {{
    readyState: 'complete',
    querySelectorAll: () => [],
    addEventListener: () => {{}},
  }},
}};
sandbox.window = sandbox;
sandbox.global = sandbox;
vm.createContext(sandbox);
vm.runInContext(code, sandbox);

function d(y, m, day) {{ return new Date(y, m - 1, day); }}
const cases = [
  [d(2026, 1, 1), '🎊'],
  [d(2026, 2, 14), '💝'],
  [d(2026, 4, 1), '🃏'],
  [d(2026, 7, 21), '🌊'],  // July month fallback
  [d(2026, 10, 31), '🎃'],
  [d(2026, 12, 25), '🎄'],
  [d(2026, 2, 10), '🧧'],  // February month (Spring Festival season)
];
for (const [date, expect] of cases) {{
  const got = sandbox.getUpdatesEmoji(date);
  if (got !== expect) {{
    console.error('mismatch', date.toISOString().slice(0, 10), 'got', got, 'want', expect);
    process.exit(1);
  }}
}}
if (sandbox.__UPDATES_EMOJI_DEFAULT__ !== '📅') process.exit(2);
console.log('ok');
"""
    result = subprocess.run(
        ["node", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "ok" in result.stdout
