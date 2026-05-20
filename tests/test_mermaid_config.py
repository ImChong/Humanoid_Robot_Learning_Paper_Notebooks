"""Mermaid site config: higher render scale and lightbox re-render helpers."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_JS = ROOT / "assets" / "js" / "mermaid-config.js"
DEFAULT_LAYOUT = ROOT / "_layouts" / "default.html"
ZOOM_JS = ROOT / "assets" / "js" / "mermaid-zoom.js"


def test_mermaid_config_uses_higher_render_scale():
    text = CONFIG_JS.read_text(encoding="utf-8")
    assert "MERMAID_RENDER_SCALE" in text
    assert "MERMAID_LIGHTBOX_SCALE" in text
    assert "useMaxWidth: false" in text
    assert "buildMermaidLightboxGraph" in text


def test_default_layout_loads_mermaid_config():
    text = DEFAULT_LAYOUT.read_text(encoding="utf-8")
    assert "mermaid-config.js" in text
    assert "getMermaidSiteConfig" in text


def test_lightbox_rerenders_from_source():
    text = ZOOM_JS.read_text(encoding="utf-8")
    assert "buildMermaidLightboxGraph" in text
    assert "mermaid.render" in text
