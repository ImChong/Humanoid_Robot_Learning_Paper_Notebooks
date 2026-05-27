"""Tests for ``extract_has_open_source`` in ``prepare_pages``."""

from scripts.prepare_pages import extract_has_open_source

_BASIC_INFO = """# Sample

## 📋 基本信息

| 项目 | 链接 |
|------|------|
{rows}

---

## 🔧 方法详解

Body.
"""


def _note(*rows):
    body = '\n'.join(f'| {label} | {value} |' for label, value in rows)
    return _BASIC_INFO.format(rows=body)


def test_detects_github_in_code_row():
    content = _note(
        ('**arXiv**', '[1234.56789](https://arxiv.org/abs/1234.56789)'),
        ('**源码**', '[org/repo](https://github.com/org/repo)'),
    )
    assert extract_has_open_source(content) is True


def test_ignores_related_code_row():
    content = _note(
        ('**相关代码**', '原文未开源；参见 [other/repo](https://github.com/other/repo)'),
    )
    assert extract_has_open_source(content) is False


def test_ignores_when_marked_not_open():
    content = _note(
        (
            '**源码**',
            '未集中给出官方仓库；可参考 [BFM-Zero](https://github.com/LeCAR-Lab/BFM-Zero)',
        ),
    )
    assert extract_has_open_source(content) is False


def test_ignores_pending_or_stub_rows():
    content = _note(('**代码**', '🚧 暂无公开仓库'))
    assert extract_has_open_source(content) is False


def test_false_without_basic_info_section():
    assert extract_has_open_source('# Title only\n\nNo table here.\n') is False
