"""Tests for iOS plain-label Mermaid math fallback."""

from scripts.adapt_mermaid_blocks import escape_pipes_in_node_labels

# Re-use inline logic until extracted; test via exec of mermaid-config patterns in JS is harder.
# Python-side: verify PPO full flowchart source has no $$ after manual check.


def test_ppo_full_flowchart_has_no_display_math_delimiters():
    from pathlib import Path

    path = Path("papers/01_Foundational_RL/PPO_Proximal_Policy_Optimization/PPO_Proximal_Policy_Optimization.md")
    text = path.read_text(encoding="utf-8")
    start = text.index("### 完整流程图")
    end = text.index("### ", start + 1)
    block = text[start:end]
    assert "$$" not in block, "完整流程图应使用 Unicode 纯文本，避免 iOS foreignObject 公式重叠"


def test_escape_pipes_still_works():
    src = 'R["pi(a|s)"]'
    out = escape_pipes_in_node_labels(src)
    assert "#124;" in out
