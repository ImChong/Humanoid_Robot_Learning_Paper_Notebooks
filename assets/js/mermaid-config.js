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

  function isIos() {
    if (typeof navigator === 'undefined') return false;
    return (
      /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
    );
  }

  /** iOS Safari paints KaTeX-in-foreignObject unreliably; use plain labels instead. */
  window.shouldUsePlainMermaidMath = function () {
    return isIos();
  };

  window.mermaidMathToPlain = function (tex) {
    return tex
      .replace(/\\pi_\{\\theta_\{old\}\}\s*\\leftarrow\s*\\pi_\\theta/g, 'π_old ← π_θ')
      .replace(/\\pi_\\theta,\s*\\,?\s*V_\\phi/g, 'π_θ, V_φ')
      .replace(
        /r_t\(\\theta\)=\\frac\{([^}]+)\}\{([^}]+)\}/g,
        'r_t(θ)=$1/$2'
      )
      .replace(
        /L\^\{CLIP\}=\\min\(r_t\\hat\{A\}_t,\\,\\mathrm\{clip\}\(r_t,0\.8,1\.2\)\\hat\{A\}_t\)/g,
        'L^CLIP=min(r_t·Â_t, clip·Â_t)'
      )
      .replace(/\\hat\{A\}_t/g, 'Â_t')
      .replace(/\\delta_t/g, 'δ_t')
      .replace(/\\gamma\\lambda/g, 'γλ')
      .replace(/\\gamma/g, 'γ')
      .replace(/\\lambda/g, 'λ')
      .replace(/N \\times T/g, 'N×T')
      .replace(/\\min\(/g, 'min(')
      .replace(/\\mathrm\{clip\}/g, 'clip')
      .replace(/\\mid/g, '|')
      .replace(/\\leftarrow/g, '←')
      .replace(/\\theta/g, 'θ')
      .replace(/\\phi/g, 'φ')
      .replace(/\\pi/g, 'π')
      .replace(/\\,/g, ' ')
      .replace(/[{}]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  };

  window.prepareMermaidRenderSource = function (source) {
    if (!source || !window.shouldUsePlainMermaidMath()) return source;
    return source.replace(/\$\$([\s\S]*?)\$\$/g, function (_match, tex) {
      return window.mermaidMathToPlain(tex.trim());
    });
  };

  window.patchMermaidForeignObjects = function (root) {
    if (!isIos() && !isMobileViewport()) return;
    var scope = root && root.querySelectorAll ? root : document;
    scope.querySelectorAll('.mermaid svg foreignObject').forEach(function (fo) {
      var inner = fo.querySelector('.nodeLabel > div, .edgeLabel > div, .labelBkg');
      if (!inner) return;
      inner.style.setProperty('display', 'block', 'important');
      inner.style.setProperty('white-space', 'normal', 'important');
      inner.style.setProperty('max-width', 'min(280px, calc(100vw - 3rem))', 'important');
      inner.style.setProperty('box-sizing', 'border-box', 'important');
      var w = inner.scrollWidth;
      var h = inner.scrollHeight;
      if (w > 0) fo.setAttribute('width', String(Math.ceil(w)));
      if (h > 0) fo.setAttribute('height', String(Math.ceil(h)));
    });
  };

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
    var ios = isIos();
    var scale = mobile ? 1.05 : MERMAID_RENDER_SCALE;
    return {
      startOnLoad: false,
      theme: theme === 'dark' ? 'dark' : 'default',
      fontSize: Math.round((mobile ? 14 : 16) * scale),
      htmlLabels: true,
      flowchart: scaledFlowchart(scale),
      securityLevel: 'strict',
      // iOS Safari: native MathML; other platforms use KaTeX CSS in foreignObject.
      forceLegacyMathML: !ios,
    };
  };

  /** Prepend a one-off init block for high-res lightbox renders. */
  window.buildMermaidLightboxGraph = function (source) {
    var text = (source || '').trim();
    if (!text) return '';
    text =
      typeof window.prepareMermaidRenderSource === 'function'
        ? window.prepareMermaidRenderSource(text)
        : text;
    return (
      '%%{init: ' +
      JSON.stringify(initDirective(MERMAID_LIGHTBOX_SCALE)) +
      '}%%\n' +
      text
    );
  };

  if (typeof document !== 'undefined' && isIos()) {
    document.documentElement.classList.add('ios');
  }
})();
