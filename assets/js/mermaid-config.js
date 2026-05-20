/**
 * Shared Mermaid render settings for paper flowcharts and the home roadmap.
 * Inline diagrams use MERMAID_RENDER_SCALE; the lightbox re-renders from source
 * at MERMAID_LIGHTBOX_SCALE for sharper zoom (especially htmlLabels).
 */
(function () {
  'use strict';

  /** Inline / page render density (was effectively ~1.0 with useMaxWidth). */
  var MERMAID_RENDER_SCALE = 1.4;
  /** Extra density when opening the fullscreen lightbox. */
  var MERMAID_LIGHTBOX_SCALE = 1.85;

  function scaledFlowchart(scale) {
    return {
      useMaxWidth: false,
      curve: 'basis',
      nodeSpacing: Math.round(50 * scale),
      rankSpacing: Math.round(50 * scale),
      wrappingWidth: Math.round(200 * scale),
      diagramPadding: Math.round(20 * scale),
    };
  }

  function initDirective(scale) {
    return {
      fontSize: Math.round(16 * scale),
      htmlLabels: true,
      flowchart: scaledFlowchart(scale),
    };
  }

  window.MERMAID_RENDER_SCALE = MERMAID_RENDER_SCALE;
  window.MERMAID_LIGHTBOX_SCALE = MERMAID_LIGHTBOX_SCALE;

  /**
   * Mermaid htmlLabels embed text in SVG foreignObject. Default DOMPurify strips
   * those nodes and leaves empty boxes in the lightbox / roadmap.
   */
  window.sanitizeMermaidSvg = function (svgString) {
    if (!svgString) return '';
    if (typeof DOMPurify === 'undefined') return svgString;
    return DOMPurify.sanitize(svgString, {
      USE_PROFILES: { svg: true, svgFilters: true },
      ADD_TAGS: ['foreignObject'],
    });
  };

  window.getMermaidSiteConfig = function (theme) {
    return {
      startOnLoad: false,
      theme: theme === 'dark' ? 'dark' : 'default',
      fontSize: Math.round(16 * MERMAID_RENDER_SCALE),
      htmlLabels: true,
      flowchart: scaledFlowchart(MERMAID_RENDER_SCALE),
      securityLevel: 'strict',
    };
  };

  /** Prepend a one-off init block for high-res lightbox renders. */
  window.buildMermaidLightboxGraph = function (source) {
    var text = (source || '').trim();
    if (!text) return '';
    return (
      '%%{init: ' +
      JSON.stringify(initDirective(MERMAID_LIGHTBOX_SCALE)) +
      '}%%\n' +
      text
    );
  };
})();
