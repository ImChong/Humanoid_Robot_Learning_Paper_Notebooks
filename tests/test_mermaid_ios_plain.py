"""Tests for iOS plain-label Mermaid math fallback."""

from pathlib import Path

from scripts.adapt_mermaid_blocks import escape_pipes_in_node_labels

# The iOS foreignObject-overlap workaround happens at runtime:
# prepareMermaidRenderSource() downgrades $$...$$ to Unicode plain text on iOS
# only. The markdown source must keep KaTeX math so desktop/Android render it.


def _ppo_full_flowchart_block() -> str:
    path = Path(
        "papers/01_Foundational_RL/PPO_Proximal_Policy_Optimization/PPO_Proximal_Policy_Optimization.md"
    )
    text = path.read_text(encoding="utf-8")
    start = text.index("### 完整流程图")
    end = text.index("### ", start + 1)
    return text[start:end]


def test_ppo_full_flowchart_keeps_katex_math_in_source():
    block = _ppo_full_flowchart_block()
    assert "$$" in block, "完整流程图源码应保留 $$..$$ KaTeX 公式（iOS 降级由前端运行时处理）"
    assert r"\hat{A}_t" in block
    assert r"\pi_{\theta_{old}}" in block


def test_ios_runtime_fallback_covers_full_flowchart_formulas():
    config_js = Path("assets/js/mermaid-config.js").read_text(encoding="utf-8")
    assert "prepareMermaidRenderSource" in config_js
    assert "shouldUsePlainMermaidMath" in config_js
    # Plain-text replacements exist for each formula used in the flowchart.
    assert "mermaidMathToPlain" in config_js
    assert r"\\hat\{A\}_t" in config_js
    assert "L\\^\\{CLIP\\}" in config_js


def test_escape_pipes_still_works():
    src = 'R["pi(a|s)"]'
    out = escape_pipes_in_node_labels(src)
    assert "#124;" in out
