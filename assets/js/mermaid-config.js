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
   * XHTML inside foreignObject (leaving bare text and wrong dark-theme colors in
   * the lightbox). Sanitize SVG structure and foreignObject inner HTML separately.
   */
  window.sanitizeMermaidSvg = function (svgString) {
    if (!svgString) return '';
    if (typeof DOMPurify === 'undefined') return '';

    var foreignObjects = [];
    var protectedSvg = svgString.replace(
      /<foreignObject([^>]*)>([\s\S]*?)<\/foreignObject>/gi,
      function (_match, attrs, inner) {
        var id = foreignObjects.length;
        var safeInner = DOMPurify.sanitize(inner, {
          USE_PROFILES: { html: true },
          ALLOWED_TAGS: [
            'div',
            'span',
            'p',
            'br',
            'b',
            'i',
            'em',
            'strong',
            // KaTeX (Mermaid forceLegacyMathML) inside foreignObject labels
            'annotation',
            'semantics',
            'math',
            'mrow',
            'mi',
            'mo',
            'mn',
            'msup',
            'msub',
            'msubsup',
            'mfrac',
            'mtext',
            'mspace',
            'mstyle',
            'mpadded',
            'menclose',
            'msqrt',
            'mroot',
            'munderover',
            'mover',
            'munder',
            'mtable',
            'mtr',
            'mtd',
            'mphantom',
            'svg',
            'path',
            'line',
            'rect',
            'g',
          ],
          ALLOWED_ATTR: [
            'style',
            'class',
            'xmlns',
            'aria-hidden',
            'encoding',
            'display',
            'd',
            'viewBox',
            'fill',
            'stroke',
            'stroke-width',
            'width',
            'height',
            'x',
            'y',
            'x1',
            'y1',
            'x2',
            'y2',
          ],
        });
        foreignObjects.push({ attrs: attrs, inner: safeInner, id: id });
        return '<foreignObject data-fo-placeholder="' + id + '"></foreignObject>';
      }
    );

    var sanitized = DOMPurify.sanitize(protectedSvg, {
      USE_PROFILES: { svg: true, svgFilters: true },
      ADD_TAGS: ['foreignObject'],
      ADD_ATTR: ['data-fo-placeholder'],
    });

    foreignObjects.forEach(function (fo) {
      sanitized = sanitized.replace(
        new RegExp(
          '<foreignObject[^>]*data-fo-placeholder="' + fo.id + '"[^>]*></foreignObject>',
          'i'
        ),
        '<foreignObject' + fo.attrs + '>' + fo.inner + '</foreignObject>'
      );
    });

    return sanitized;
  };

  window.getMermaidSiteConfig = function (theme) {
    return {
      startOnLoad: false,
      theme: theme === 'dark' ? 'dark' : 'default',
      fontSize: Math.round(16 * MERMAID_RENDER_SCALE),
      htmlLabels: true,
      flowchart: scaledFlowchart(MERMAID_RENDER_SCALE),
      securityLevel: 'strict',
      // Site already loads KaTeX CSS; use it for consistent math in flowcharts.
      // Wrap LaTeX in node labels with $$...$$ (see mermaid.js.org/config/math.html).
      forceLegacyMathML: true,
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
