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

    var html = '';
    if (prev) html += '<a href="' + prev.url + '" class="prev-link">← ' + prev.short + '</a>';
    html += '<a href="' + listLink + '" class="back-link">' + backText + '</a>';
    if (next) html += '<a href="' + next.url + '" class="next-link">' + next.short + ' →</a>';
    nav.innerHTML = html;

    var sidebarNav = document.getElementById('sidebar-paper-nav');
    if (sidebarNav) {
      var sidebarHtml = '';
      if (prev) sidebarHtml += '<a href="' + prev.url + '" class="right-sidebar-link">← ' + prev.short + '</a>';
      if (next) sidebarHtml += '<a href="' + next.url + '" class="right-sidebar-link">' + next.short + ' →</a>';
      sidebarNav.innerHTML = sidebarHtml;
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
    function updateActive() {
      var scrollPos = window.scrollY + 100;
      var current = -1;
      for (var i = 0; i < headingArr.length; i++) {
        if (headingArr[i].offsetTop <= scrollPos) current = i;
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

  function init() {
    initPaperNav();
    initTableWrappers();
    initToc();
    rebuildWithLineNumbers();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
