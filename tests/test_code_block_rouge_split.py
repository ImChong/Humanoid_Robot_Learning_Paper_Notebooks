"""Regression: Rouge HTML newlines must not split syntax spans across code rows."""

import re
import subprocess
from pathlib import Path

ROUGE_NL_BEFORE_CLOSE = re.compile(r"\n(\s*</span>)")


def _normalize_rouge_line_breaks(html: str) -> str:
    return ROUGE_NL_BEFORE_CLOSE.sub(r"\1\n", html)


def _split_by_newline(html: str) -> list[str]:
    lines: list[str] = []
    last_idx = 0
    in_tag = False
    i = 0
    while i < len(html):
        if not in_tag:
            next_tag = html.find("<", i)
            next_nl = html.find("\n", i)
            if next_nl != -1 and (next_tag == -1 or next_nl < next_tag):
                lines.append(html[last_idx:next_nl])
                last_idx = next_nl + 1
                i = next_nl + 1
            elif next_tag != -1:
                in_tag = True
                i = next_tag + 1
            else:
                break
        else:
            next_end = html.find(">", i)
            if next_end != -1:
                in_tag = False
                i = next_end + 1
            else:
                break
    if last_idx < len(html):
        lines.append(html[last_idx:])
    return lines


def test_rouge_newline_inside_span_does_not_break_tag_across_rows():
    sample = (
        '<span class="c1"># mimickit/learning/ppo_model.py\n'
        '</span><span class="k">class</span> Foo:'
    )
    broken = _split_by_newline(sample)
    assert broken[0].endswith("ppo_model.py")
    assert broken[0].startswith("<span")
    assert "</span>" not in broken[0]

    fixed = _normalize_rouge_line_breaks(sample)
    ok = _split_by_newline(fixed)
    assert ok[0] == '<span class="c1"># mimickit/learning/ppo_model.py</span>'
    assert ok[1] == '<span class="k">class</span> Foo:'


def test_paper_js_exports_normalize_before_split():
    """Keep Python mirror in sync with assets/js/paper.js."""
    paper_js = (Path(__file__).resolve().parents[1] / "assets/js/paper.js").read_text(
        encoding="utf-8"
    )
    assert "function normalizeRougeLineBreaks(html)" in paper_js
    assert "normalizeRougeLineBreaks(code.innerHTML)" in paper_js


def test_node_split_matches_python_mirror():
    repo = Path(__file__).resolve().parents[1]
    script = """
function normalizeRougeLineBreaks(html) {
  return html.replace(/\\n(\\s*<\\/span>)/g, '$1\\n');
}
const sample = '<span class="c1"># foo\\n</span><span class="k">def</span> bar';
const lines = sample.replace(/\\n(\\s*<\\/span>)/g, '$1\\n').split('\\n');
console.log(JSON.stringify(lines));
"""
    out = subprocess.run(
        ["node", "-e", script],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == '["<span class=\\"c1\\"># foo</span>","<span class=\\"k\\">def</span> bar"]'
