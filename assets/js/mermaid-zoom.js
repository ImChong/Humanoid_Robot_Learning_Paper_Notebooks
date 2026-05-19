/**
 * Click any rendered Mermaid diagram to open a fullscreen lightbox.
 * Pan with left mouse button (or touch drag); close with Esc, backdrop, or ×.
 */
(function () {
  'use strict';

  var lightbox = null;
  var viewport = null;
  var stage = null;
  var state = {
    scale: 1,
    x: 0,
    y: 0,
    dragging: false,
    pointerId: null,
    lastClientX: 0,
    lastClientY: 0,
  };

  function ensureLightbox() {
    if (lightbox) return lightbox;

    lightbox = document.createElement('div');
    lightbox.className = 'mermaid-lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', 'Mermaid diagram viewer');
    lightbox.hidden = true;

    var backdrop = document.createElement('div');
    backdrop.className = 'mermaid-lightbox__backdrop';
    backdrop.setAttribute('data-mermaid-lightbox-close', '');

    var panel = document.createElement('div');
    panel.className = 'mermaid-lightbox__panel';

    var closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'mermaid-lightbox__close';
    closeBtn.setAttribute('data-mermaid-lightbox-close', '');
    closeBtn.setAttribute('aria-label', '关闭');
    closeBtn.textContent = '×';

    var hint = document.createElement('p');
    hint.className = 'mermaid-lightbox__hint';
    hint.textContent = '拖拽平移 · Esc 关闭';

    viewport = document.createElement('div');
    viewport.className = 'mermaid-lightbox__viewport';

    stage = document.createElement('div');
    stage.className = 'mermaid-lightbox__stage';
    viewport.appendChild(stage);

    panel.appendChild(closeBtn);
    panel.appendChild(hint);
    panel.appendChild(viewport);
    lightbox.appendChild(backdrop);
    lightbox.appendChild(panel);
    document.body.appendChild(lightbox);

    closeBtn.addEventListener('click', close);
    backdrop.addEventListener('click', close);

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) close();
    });

    panel.addEventListener('click', function (e) {
      e.stopPropagation();
    });

    viewport.addEventListener('pointerdown', onPointerDown);
    viewport.addEventListener('pointermove', onPointerMove);
    viewport.addEventListener('pointerup', onPointerUp);
    viewport.addEventListener('pointercancel', onPointerUp);

    document.addEventListener('keydown', onKeyDown);

    return lightbox;
  }

  function applyTransform() {
    if (!stage) return;
    stage.style.transform =
      'translate(calc(-50% + ' +
      state.x +
      'px), calc(-50% + ' +
      state.y +
      'px)) scale(' +
      state.scale +
      ')';
  }

  function measureSvg(svg) {
    var viewBox = svg.viewBox && svg.viewBox.baseVal;
    if (viewBox && viewBox.width > 0 && viewBox.height > 0) {
      return { width: viewBox.width, height: viewBox.height };
    }
    var rect = svg.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0) {
      return { width: rect.width, height: rect.height };
    }
    var w = parseFloat(svg.getAttribute('width'));
    var h = parseFloat(svg.getAttribute('height'));
    if (w > 0 && h > 0) return { width: w, height: h };
    return { width: 800, height: 600 };
  }

  /** Mermaid often sets width="100%" + max-width; that collapses to 0×0 outside .mermaid. */
  function cloneSvgForLightbox(svg) {
    var clone = svg.cloneNode(true);
    var size = measureSvg(svg);
    clone.removeAttribute('width');
    clone.removeAttribute('height');
    clone.style.cssText = '';
    clone.style.width = size.width + 'px';
    clone.style.height = size.height + 'px';
    clone.style.maxWidth = 'none';
    clone.classList.add('mermaid-lightbox__svg');
    return clone;
  }

  function fitToViewport(svg) {
    var size = measureSvg(svg);
    var pad = 48;
    var vw = Math.max(viewport.clientWidth - pad, 200);
    var vh = Math.max(viewport.clientHeight - pad, 200);
    var fit = Math.min(vw / size.width, vh / size.height);
    state.scale = Math.min(Math.max(fit, 0.25), 3);
    state.x = 0;
    state.y = 0;
    applyTransform();
  }

  function open(sourceEl) {
    var svg = sourceEl.querySelector('svg');
    if (!svg) return;

    ensureLightbox();
    stage.innerHTML = '';
    var clone = cloneSvgForLightbox(svg);
    stage.appendChild(clone);

    state.dragging = false;
    state.pointerId = null;
    lightbox.hidden = false;
    lightbox.classList.add('is-open');
    document.body.classList.add('mermaid-lightbox-open');

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        fitToViewport(clone);
      });
    });
  }

  function close() {
    if (!lightbox || lightbox.hidden) return;
    lightbox.hidden = true;
    lightbox.classList.remove('is-open');
    document.body.classList.remove('mermaid-lightbox-open');
    state.dragging = false;
    state.pointerId = null;
    if (viewport) viewport.classList.remove('is-dragging');
    if (stage) stage.innerHTML = '';
  }

  function onKeyDown(e) {
    if (e.key === 'Escape' && lightbox && !lightbox.hidden) {
      e.preventDefault();
      close();
    }
  }

  function onPointerDown(e) {
    if (!lightbox || lightbox.hidden) return;
    if (e.button !== 0 && e.pointerType === 'mouse') return;
    state.dragging = true;
    state.pointerId = e.pointerId;
    state.lastClientX = e.clientX;
    state.lastClientY = e.clientY;
    viewport.classList.add('is-dragging');
    viewport.setPointerCapture(e.pointerId);
    e.preventDefault();
  }

  function onPointerMove(e) {
    if (!state.dragging || e.pointerId !== state.pointerId) return;
    var dx = e.clientX - state.lastClientX;
    var dy = e.clientY - state.lastClientY;
    state.lastClientX = e.clientX;
    state.lastClientY = e.clientY;
    state.x += dx;
    state.y += dy;
    applyTransform();
    e.preventDefault();
  }

  function onPointerUp(e) {
    if (!state.dragging || e.pointerId !== state.pointerId) return;
    state.dragging = false;
    state.pointerId = null;
    viewport.classList.remove('is-dragging');
    try {
      viewport.releasePointerCapture(e.pointerId);
    } catch (err) {
      /* ignore */
    }
  }

  function findMermaidTarget(target) {
    if (!target || !target.closest) return null;
    var el = target.closest('.mermaid');
    if (!el || !el.querySelector('svg')) return null;
    return el;
  }

  document.addEventListener(
    'click',
    function (e) {
      if (lightbox && !lightbox.hidden) return;
      var mermaid = findMermaidTarget(e.target);
      if (!mermaid) return;
      e.preventDefault();
      open(mermaid);
    },
    true
  );

  new MutationObserver(function () {
    if (lightbox && !lightbox.hidden) close();
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme'],
  });
})();
