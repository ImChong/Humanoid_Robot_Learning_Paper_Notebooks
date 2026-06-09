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

  function isMobileViewport() {
    return (
      typeof window !== 'undefined' &&
      window.matchMedia &&
      window.matchMedia('(max-width: 600px)').matches
    );
  }

  function scaledFlowchart(scale) {
    var mobile = isMobileViewport();
    return {
      useMaxWidth: false,
      curve: 'basis',
      nodeSpacing: Math.round((mobile ? 36 : 50) * scale),
      rankSpacing: Math.round((mobile ? 40 : 50) * scale),
      wrappingWidth: mobile ? 150 : Math.round(200 * scale),
      diagramPadding: Math.round((mobile ? 12 : 20) * scale),
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

  /** Preserve <br> line breaks when snapshotting Mermaid source from built HTML. */
  window.readMermaidBlockSource = function (el) {
    if (!el) return '';
    var stored = el.getAttribute('data-original-code');
    if (stored) return stored;
    var clone = el.cloneNode(true);
    clone.querySelectorAll('br').forEach(function (br) {
      br.replaceWith(document.createTextNode('\n'));
    });
    return clone.textContent.trim();
  };

  window.writeMermaidBlockSource = function (el, source) {
    if (!el) return;
    el.textContent = source || '';
  };

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
          ALLOWED_TAGS: ['div', 'span', 'p', 'br', 'b', 'i', 'em', 'strong'],
          ALLOWED_ATTR: ['style', 'class', 'xmlns'],
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
    var mobile = isMobileViewport();
    var scale = mobile ? 1.05 : MERMAID_RENDER_SCALE;
    return {
      startOnLoad: false,
      theme: theme === 'dark' ? 'dark' : 'default',
      fontSize: Math.round((mobile ? 14 : 16) * scale),
      htmlLabels: true,
      flowchart: scaledFlowchart(scale),
      securityLevel: 'strict',
      // Site already loads KaTeX CSS; use CSS-based math for consistent flowchart labels.
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
