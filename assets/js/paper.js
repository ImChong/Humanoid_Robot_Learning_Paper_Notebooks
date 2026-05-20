/* Paper-page client-side enhancements.
 *
 * This file is included once per paper layout and self-initialises. It expects
 * the surrounding HTML to provide:
 *
 *   - <script type="application/json" id="paper-nav-data">{ baseurl, papers }</script>
 *     (rendered server-side from _data/roadmap_order.yml + site.baseurl)
 *   - #paper-body, #paper-nav, #toc-sidebar, #toc-nav, #sidebar-paper-nav, #sidebar-overlay
 */

(function () {
  'use strict';

  // ─── Paper navigation (prev/next) ─────────────────────────────────────────
  function initPaperNav() {
    var dataEl = document.getElementById('paper-nav-data');
    if (!dataEl) return;
    var navData;
    try {
      navData = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }
    var paperOrder = (navData && navData.papers) || [];
    var listLink = (navData && navData.listLink) || '/';
    if (!paperOrder.length) return;

    var currentPath = window.location.pathname;
    var currentIdx = -1;
    for (var i = 0; i < paperOrder.length; i++) {
      var url = paperOrder[i].url;
      if (currentPath.indexOf(url) !== -1 || url.indexOf(currentPath) !== -1) {
        currentIdx = i;
        break;
      }
    }
    if (currentIdx === -1) return;

    var nav = document.getElementById('paper-nav');
    if (!nav) return;

    var prev = currentIdx > 0 ? paperOrder[currentIdx - 1] : null;
    var next = currentIdx < paperOrder.length - 1 ? paperOrder[currentIdx + 1] : null;
    var isFirst = currentIdx === 0;
    var backText = isFirst ? '← 返回论文列表' : '返回论文列表';

    nav.innerHTML = '';
    if (prev) {
      var prevLink = document.createElement('a');
      prevLink.href = prev.url;
      prevLink.className = 'prev-link';
      prevLink.textContent = '← ' + prev.short;
      nav.appendChild(prevLink);
    }

    var backLinkEl = document.createElement('a');
    backLinkEl.href = listLink;
    backLinkEl.className = 'back-link';
    backLinkEl.textContent = backText;
    nav.appendChild(backLinkEl);

    if (next) {
      var nextLink = document.createElement('a');
      nextLink.href = next.url;
      nextLink.className = 'next-link';
      nextLink.textContent = next.short + ' →';
      nav.appendChild(nextLink);
    }

    var sidebarNav = document.getElementById('sidebar-paper-nav');
    if (sidebarNav) {
      sidebarNav.innerHTML = '';
      if (prev) {
        var sidebarPrevLink = document.createElement('a');
        sidebarPrevLink.href = prev.url;
        sidebarPrevLink.className = 'right-sidebar-link';
        sidebarPrevLink.textContent = '← ' + prev.short;
        sidebarNav.appendChild(sidebarPrevLink);
      }
      if (next) {
        var sidebarNextLink = document.createElement('a');
        sidebarNextLink.href = next.url;
        sidebarNextLink.className = 'right-sidebar-link';
        sidebarNextLink.textContent = next.short + ' →';
        sidebarNav.appendChild(sidebarNextLink);
      }
    }
  }

  // ─── Wrap tables for horizontal scroll ───────────────────────────────────
  function initTableWrappers() {
    var body = document.getElementById('paper-body');
    if (!body) return;
    body.querySelectorAll('table').forEach(function (table) {
      if (table.parentElement && table.parentElement.classList.contains('table-wrapper')) return;
      var wrapper = document.createElement('div');
      wrapper.className = 'table-wrapper';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    });
  }

  // ─── Build TOC + scroll-spy active highlighting ───────────────────────────
  function initToc() {
    var body = document.getElementById('paper-body');
    var nav = document.getElementById('toc-nav');
    if (!body || !nav) return;

    var headings = body.querySelectorAll('h2, h3');
    if (headings.length === 0) {
      var emptySidebar = document.getElementById('toc-sidebar');
      if (emptySidebar) emptySidebar.style.display = 'none';
      return;
    }

    var ul = document.createElement('ul');
    ul.className = 'toc-list';

    headings.forEach(function (h, i) {
      if (!h.id) h.id = 'heading-' + i;
      var li = document.createElement('li');
      li.className = 'toc-item toc-' + h.tagName.toLowerCase();
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.className = 'toc-link';
      li.appendChild(a);
      ul.appendChild(li);
    });
    nav.appendChild(ul);

    var links = nav.querySelectorAll('.toc-link');
    var headingArr = Array.from(headings);
    var sidebar = document.getElementById('toc-sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    var mobileQuery = window.matchMedia('(max-width: 1200px)');

    function closeMobileSidebar() {
      if (sidebar) sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('show');
      document.body.style.overflow = '';
    }

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        var hash = link.getAttribute('href');
        if (!hash || hash.charAt(0) !== '#') return;
        var target = document.querySelector(hash);
        if (!target) return;
        e.preventDefault();
        if (mobileQuery.matches) closeMobileSidebar();
        window.history.replaceState(null, '', hash);
        var headerOffset = 90;
        var targetTop = target.getBoundingClientRect().top + window.scrollY - headerOffset;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
      });
    });

    var lastActive = -1;
    // ⚡ Bolt Optimization: Cache layout positions to prevent layout thrashing on scroll
    var cachedPositions = [];

    function updatePositions() {
      cachedPositions = headingArr.map(function(h) {
        return h.offsetTop;
      });
    }

    updatePositions();

    if (window.ResizeObserver) {
      var ro = new ResizeObserver(updatePositions);
      ro.observe(document.body);
    } else {
      window.addEventListener('resize', function() {
        clearTimeout(window.resizeTimeout);
        window.resizeTimeout = setTimeout(updatePositions, 150);
      });
    }

    function updateActive() {
      var scrollPos = window.scrollY + 100;
      var current = -1;
      for (var i = 0; i < cachedPositions.length; i++) {
        if (cachedPositions[i] <= scrollPos) current = i;
      }
      // Only update DOM if the active section actually changed.
      if (current !== lastActive) {
        links.forEach(function (link, idx) {
          link.classList.toggle('active', idx === current);
        });
        lastActive = current;
      }
    }

    var ticking = false;
    // Throttle scroll handler with requestAnimationFrame to avoid layout thrashing.
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          updateActive();
          ticking = false;
        });
        ticking = true;
      }
    });
    updateActive();
  }

  // ─── Mermaid block detection + line-numbered code rebuild ────────────────
  function buildMermaidDiv(source) {
    var code = source.trim();
    var div = document.createElement('div');
    div.className = 'mermaid';
    div.setAttribute('data-original-code', code);
    div.textContent = code;
    return div;
  }

  function transformMermaid() {
    document.querySelectorAll('pre > code.language-mermaid').forEach(function (codeEl) {
      var pre = codeEl.parentElement;
      if (!pre || pre.classList.contains('mermaid-processed')) return;
      var mermaidDiv = buildMermaidDiv(codeEl.textContent);
      pre.parentNode.insertBefore(mermaidDiv, pre);
      pre.style.display = 'none';
      pre.classList.add('mermaid-processed');
    });

    document.querySelectorAll('div.highlighter-rouge').forEach(function (outer) {
      var codeEl = outer.querySelector('code');
      if (!codeEl) return;
      var text = codeEl.textContent.trim();
      var isMermaid =
        outer.classList.contains('language-mermaid') ||
        codeEl.classList.contains('language-mermaid') ||
        codeEl.classList.contains('mermaid') ||
        text.startsWith('graph ') ||
        text.startsWith('flowchart ') ||
        text.startsWith('sequenceDiagram') ||
        text.startsWith('gantt') ||
        text.startsWith('classDiagram');
      if (isMermaid && !outer.classList.contains('mermaid-processed')) {
        var mermaidDiv = buildMermaidDiv(codeEl.textContent);
        outer.parentNode.insertBefore(mermaidDiv, outer);
        outer.style.display = 'none';
        outer.classList.add('mermaid-processed');
      }
    });
  }

  function splitByNewline(html) {
    var lines = [],
      cur = '',
      inTag = false;
    for (var i = 0; i < html.length; i++) {
      var c = html[i];
      if (c === '<') {
        inTag = true;
        cur += c;
      } else if (c === '>') {
        inTag = false;
        cur += c;
      } else if (c === '\n' && !inTag) {
        lines.push(cur);
        cur = '';
      } else {
        cur += c;
      }
    }
    if (cur !== '') lines.push(cur);
    return lines;
  }

  function rebuildWithLineNumbers() {
    transformMermaid();
    document.querySelectorAll('div.highlighter-rouge:not(.mermaid-processed)').forEach(function (outer) {
      var code = outer.querySelector('pre code');
      if (!code) return;
      var html = code.innerHTML;
      if (html.endsWith('\n')) html = html.slice(0, -1);
      var lines = splitByNewline(html);

      var wrapper = document.createElement('div');
      wrapper.className = 'code-block highlight';

      lines.forEach(function (lineHTML, i) {
        var row = document.createElement('div');
        row.className = 'code-row';
        var ln = document.createElement('span');
        ln.className = 'code-ln';
        ln.textContent = String(i + 1);
        var cell = document.createElement('span');
        cell.className = 'code-cell';
        cell.innerHTML = lineHTML;
        row.appendChild(ln);
        row.appendChild(cell);
        wrapper.appendChild(row);
      });

      outer.innerHTML = '';
      outer.appendChild(wrapper);
    });

    if (typeof mermaid !== 'undefined') {
      var theme = document.documentElement.getAttribute('data-theme') || 'light';
      if (typeof initMermaid === 'function') {
        initMermaid(theme);
      } else {
        mermaid.run();
      }
    }
  }

  // ─── Keep “（`fn`）” in headings on one line (mobile word-break splits otherwise) ─
  function wrapHeadingInlineCodePhrases() {
    var body = document.getElementById('paper-body');
    if (!body) return;
    body.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(function (h) {
      var codes = h.querySelectorAll(':scope > code');
      for (var i = 0; i < codes.length; i++) {
        var code = codes[i];
        if (code.closest('.heading-code-phrase')) continue;
        var prev = code.previousSibling;
        var next = code.nextSibling;
        if (!prev || prev.nodeType !== Node.TEXT_NODE) continue;
        if (!next || next.nodeType !== Node.TEXT_NODE) continue;
        var prevText = prev.textContent;
        var nextText = next.textContent;
        var openIdx = Math.max(prevText.lastIndexOf('（'), prevText.lastIndexOf('('));
        if (openIdx === -1) continue;
        var openChar = prevText.charAt(openIdx);
        var closeChar = openChar === '（' ? '）' : ')';
        if (!nextText.startsWith(closeChar)) continue;

        var span = document.createElement('span');
        span.className = 'heading-code-phrase';
        prev.textContent = prevText.slice(0, openIdx);
        span.appendChild(document.createTextNode(prevText.slice(openIdx)));
        span.appendChild(code);
        span.appendChild(document.createTextNode(closeChar));
        if (nextText.length > 1) {
          next.textContent = nextText.slice(1);
        } else {
          h.removeChild(next);
        }
        h.insertBefore(span, prev.nextSibling);
      }
    });
  }

  // ─── Insert <wbr> in long inline code so paths break at /, then ── ────────
  // Without these hints the mobile parent's ``word-break: break-word`` shatters
  // identifiers at arbitrary positions inside a filename. Two-stage hinting:
  //   1. ``/`` → preferred break (between path segments).
  //   2. ``.`` and ``_`` and ``-`` → secondary breaks only when a single segment
  //      between slashes is itself too long to fit.
  // Anything still longer than the line falls back to ``overflow-wrap: anywhere``
  // (any-character break) so it cannot overflow the viewport.
  function applyWbrSplit(code, parts) {
    while (code.firstChild) code.removeChild(code.firstChild);
    for (var j = 0; j < parts.length; j++) {
      if (j > 0) code.appendChild(document.createElement('wbr'));
      code.appendChild(document.createTextNode(parts[j]));
    }
    code.dataset.wbrApplied = '1';
  }

  function splitLongSegment(seg) {
    // For a single path segment with no slashes, allow secondary breaks at
    // ``.``, ``_``, ``-`` boundaries (kept with the next chunk).
    return seg.split(/(?=[._\-])/);
  }

  function addInlineCodeBreakHints() {
    var paperBody = document.getElementById('paper-body');
    if (!paperBody) return;
    var codes = paperBody.querySelectorAll('code');
    for (var i = 0; i < codes.length; i++) {
      var code = codes[i];
      // Skip code inside <pre> (block code) and skip if already processed.
      if (code.closest('pre')) continue;
      if (code.closest('.heading-code-phrase')) continue;
      if (code.closest('h1, h2, h3, h4, h5, h6')) continue;
      if (code.dataset.wbrApplied === '1') continue;
      var text = code.textContent;
      if (!text || text.length < 16) continue;
      // Only act when the token has no whitespace (paths, identifiers, URLs).
      if (/\s/.test(text)) continue;
      // Don't touch code that already contains child elements (syntax-highlighted spans).
      if (code.firstElementChild) continue;

      // Primary split at ``/`` (kept with the next chunk: ``foo/bar`` →
      // ``foo`` + ``<wbr>`` + ``/bar``). Path segments stay whole — a 28-char
      // filename folds to its own line before splitting internally. Only when
      // a single segment is longer than ~30 characters (true edge case, won't
      // fit on a mobile line) do we add secondary ``.``/``_``/``-`` breaks so
      // it can fold without overflowing.
      var slashParts = text.split(/(?=\/)/);
      var parts = [];
      for (var k = 0; k < slashParts.length; k++) {
        var seg = slashParts[k];
        if (seg.length > 30) {
          var sub = splitLongSegment(seg);
          for (var m = 0; m < sub.length; m++) parts.push(sub[m]);
        } else {
          parts.push(seg);
        }
      }
      if (parts.length < 2) continue;
      applyWbrSplit(code, parts);
    }
  }

  function init() {
    initPaperNav();
    initTableWrappers();
    initToc();
    rebuildWithLineNumbers();
    wrapHeadingInlineCodePhrases();
    addInlineCodeBreakHints();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
