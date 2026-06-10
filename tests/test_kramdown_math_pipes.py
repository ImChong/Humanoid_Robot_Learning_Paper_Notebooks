"""Tests for kramdown GFM pipe-in-math normalization."""

from scripts._common import normalize_kramdown_math_pipes


def test_conditional_policy_not_split_as_table():
    content = (
        "**一行定位**：下层用 RL 学 $\\pi_\\phi(a|o,g)$ 跟踪参考。\n"
    )
    normalized, changed = normalize_kramdown_math_pipes(content)
    assert changed is True
    assert "$\\pi_\\phi(a \\mid o,g)$" in normalized
    assert "(a|o,g)" not in normalized


def test_latent_prior_conditional():
    content = "- 先验 $p(z|s)$ 采样\n"
    normalized, changed = normalize_kramdown_math_pipes(content)
    assert changed is True
    assert "$p(z \\mid s)$" in normalized


def test_absolute_value_uses_vert_delimiters():
    content = "$$\\tau = |v| < v_{x1}$$\n"
    normalized, changed = normalize_kramdown_math_pipes(content)
    assert changed is True
    assert "\\|v\\|" in normalized


def test_skips_markdown_table_rows():
    content = "| prior | $p(z|s)$ |\n"
    normalized, changed = normalize_kramdown_math_pipes(content)
    assert changed is False
    assert normalized == content


def test_skips_fenced_code_blocks():
    content = "```python\nexpr = 'a|b'\n```\n"
    normalized, changed = normalize_kramdown_math_pipes(content)
    assert changed is False
    assert normalized == content


def test_idempotent_when_already_escaped():
    content = "**一行定位**：$\\pi_\\phi(a \\mid o,g)$\n"
    normalized, changed = normalize_kramdown_math_pipes(content)
    assert changed is False
    assert normalized == content
