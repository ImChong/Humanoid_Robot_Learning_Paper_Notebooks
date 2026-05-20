"""Tests for paper header meta blockquote normalization."""

from scripts._common import normalize_paper_meta_blockquotes


def _sample_note(meta_lines: list[str]) -> str:
    body = '\n'.join(meta_lines)
    return (
        '---\nlayout: paper\ntitle: "Test"\n---\n\n'
        '# Title\n'
        '**subtitle**\n\n'
        f'{body}\n\n'
        '---\n\n'
        '## 📋 基本信息\n'
    )


def test_normalize_inserts_empty_blockquote_between_meta_lines():
    content = _sample_note([
        '> 📅 阅读日期: 2026-05-01',
        '> 🏷️ 板块: Sim-to-Real',
    ])
    normalized, changed = normalize_paper_meta_blockquotes(content)
    assert changed is True
    assert '> 📅 阅读日期: 2026-05-01\n>\n> 🏷️ 板块: Sim-to-Real' in normalized


def test_normalize_strips_trailing_spaces_on_meta_lines():
    content = _sample_note([
        '> 📅 阅读日期: 2026-03-11  ',
        '>',
        '> 🏷️ 板块: RL',
    ])
    normalized, changed = normalize_paper_meta_blockquotes(content)
    assert changed is True
    assert '> 📅 阅读日期: 2026-03-11\n' in normalized
    assert '  \n' not in normalized.split('## 📋')[0]


def test_normalize_idempotent_when_already_separated():
    content = _sample_note([
        '> 📅 阅读日期: 2026-03-11',
        '>',
        '> 🏷️ 板块: RL',
    ])
    normalized, changed = normalize_paper_meta_blockquotes(content)
    assert changed is False
    assert normalized == content


def test_normalize_separates_extra_header_blockquote_lines():
    content = _sample_note([
        '> 📅 阅读日期: 2026-04-21',
        '> 🏷️ 板块: 扩散 + 控制',
        '> 🚧 本笔记待细化。',
    ])
    normalized, changed = normalize_paper_meta_blockquotes(content)
    assert changed is True
    assert normalized.count('\n>\n') >= 2
