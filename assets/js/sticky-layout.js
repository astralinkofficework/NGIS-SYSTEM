/* ============================================================================
   NGIS shared sticky layout controller
   ----------------------------------------------------------------------------
   Replaces competing sticky/fixed header implementations with one measured
   application header. The real rendered box is used for height, left and
   width, so sidebar collapse, resize, safe-area changes and fullscreen do not
   require hardcoded offsets.
   ========================================================================== */
(function (window, document) {
  'use strict';

  if (window.__NGIS_STICKY_LAYOUT__) return;
  window.__NGIS_STICKY_LAYOUT__ = true;

  var root = document.documentElement;
  var body = document.body;
  var header = null;
  var spacer = null;
  var stuck = false;
  var raf = 0;
  var attempts = 0;
  var lastHeight = -1;
  var resizeObserver = null;
  var mutationObserver = null;
  var bound = false;

  /* Ordered by authority: an explicit page header wins; the compact mobile
     app bar wins over the large hero header; the legacy topbar is the last
     fallback. */
  var SELECTORS = [
    '[data-ngis-sticky-header]',
    '.mobile-appbar',
    '[data-purpose="mobile-header"]',
    '.htb-topbar-mobile',
    'header.lg\\:hidden',
    '.hero .hero-topbar',
    '.hero-topbar',
    '#heroBanner .hero-topbar',
    'header.topbar'
  ];

  function isVisible(el) {
    if (!el || el.hidden || el.classList.contains('ngis-sticky-duplicate')) return false;
    if (el.getAttribute('aria-hidden') === 'true') return false;
    var style = window.getComputedStyle(el);
    if (!style || style.display === 'none' || style.visibility === 'hidden') return false;
    var rects = el.getClientRects();
    if (!rects.length) return false;
    var rect = el.getBoundingClientRect();
    return rect.width > 1 && rect.height > 1;
  }

  function pickHeader() {
    for (var i = 0; i < SELECTORS.length; i++) {
      var nodes;
      try { nodes = document.querySelectorAll(SELECTORS[i]); } catch (e) { continue; }
      for (var j = 0; j < nodes.length; j++) {
        if (isVisible(nodes[j])) return nodes[j];
      }
    }
    return null;
  }

  function isFullscreen() {
    var overlay = document.querySelector('[data-ngis-fullscreen-overlay]');
    return body.classList.contains('fullscreen-soc-mode') ||
      !!(overlay && !overlay.classList.contains('hidden'));
  }

  function schedule(fn) {
    if (raf) return;
    raf = window.requestAnimationFrame(function () {
      raf = 0;
      fn();
    });
  }

  function getPageBackground() {
    try {
      var bodyStyle = window.getComputedStyle(document.body);
      var bg = bodyStyle.backgroundColor;
      if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return bg;
      var main = document.querySelector('main, .main');
      if (main) {
        var mBg = window.getComputedStyle(main).backgroundColor;
        if (mBg && mBg !== 'rgba(0, 0, 0, 0)' && mBg !== 'transparent') return mBg;
      }
    } catch (e) {}
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    return isDark ? '#0F172A' : '#F7F9F7';
  }

  function applyHeaderSurface(isStuck) {
    if (!header) return;
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    var solidBg = isDark ? '#0F172A' : '#FFFFFF';
    header.style.setProperty('background-color', solidBg, 'important');
    header.style.setProperty('background', solidBg, 'important');
  }

  function updateStickiness() {
    if (!header || !spacer || isFullscreen()) return;

    /* Keep the measured trigger point in document coordinates. The spacer
       never moves when the header is fixed, so this is stable while scrolling. */
    var triggerTop = spacer.getBoundingClientRect().top + window.pageYOffset;
    /* Normal state when page is at the top (pageYOffset <= 8); sticks when scrolled */
    var shouldStick = window.pageYOffset > 8 && (window.pageYOffset >= triggerTop - 1);
    if (shouldStick === stuck) return;

    stuck = shouldStick;
    header.classList.toggle('ngis-sticky-fixed', shouldStick);
    applyHeaderSurface(shouldStick);
  }

  function retarget() {
    if (!header) return;
    if (resizeObserver) resizeObserver.disconnect();

    if (spacer && spacer.parentNode) spacer.parentNode.removeChild(spacer);
    header.classList.remove('ngis-sticky-active', 'ngis-sticky-fixed');
    ['background-color', 'background-image', 'backdrop-filter', '-webkit-backdrop-filter'].forEach(function (prop) {
      header.style.removeProperty(prop);
    });
    document.querySelectorAll('.ngis-sticky-duplicate').forEach(function (el) {
      el.classList.remove('ngis-sticky-duplicate');
    });

    header = null;
    spacer = null;
    stuck = false;
    lastHeight = -1;
    attempts = 0;
    boot();
  }

  function measure() {
    if (!header || !spacer) return;
    if (isFullscreen()) {
      applyFullscreenState();
      return;
    }
    if (!isVisible(header)) {
      retarget();
      return;
    }

    var height = Math.max(1, Math.round(header.getBoundingClientRect().height));
    var rect = spacer.getBoundingClientRect();
    var left = Math.round(rect.left + window.pageXOffset);
    var width = Math.round(rect.width);

    if (height !== lastHeight) {
      lastHeight = height;
      spacer.style.height = height + 'px';
    }

    header.style.setProperty('background-image', 'none', 'important');
    header.style.setProperty('backdrop-filter', 'none', 'important');
    header.style.setProperty('-webkit-backdrop-filter', 'none', 'important');

    root.style.setProperty('--ngis-sticky-h', height + 'px');
    root.style.setProperty('--ngis-sticky-left', left + 'px');
    root.style.setProperty('--ngis-sticky-width', width + 'px');
    applyFullscreenState();
    updateStickiness();
    applyHeaderSurface(stuck);
  }

  function applyFullscreenState() {
    if (!header) return;
    var fullscreen = isFullscreen();
    body.classList.toggle('ngis-sticky-suspended', fullscreen);

    if (fullscreen) {
      if (stuck) {
        stuck = false;
        header.classList.remove('ngis-sticky-fixed');
      }
      root.style.setProperty('--ngis-sticky-h', '0px');
    }
  }

  function hideDuplicateHeaders() {
    var all = [];
    SELECTORS.forEach(function (selector) {
      var nodes;
      try { nodes = document.querySelectorAll(selector); } catch (e) { return; }
      for (var i = 0; i < nodes.length; i++) {
        if (all.indexOf(nodes[i]) === -1) all.push(nodes[i]);
      }
    });

    all.forEach(function (el) {
      if (el === header || el.contains(header) || header.contains(el)) return;
      if (isVisible(el)) el.classList.add('ngis-sticky-duplicate');
    });
  }

  function bind() {
    if (bound) return;
    bound = true;

    window.addEventListener('scroll', function () { schedule(updateStickiness); }, { passive: true });
    window.addEventListener('resize', function () { schedule(measure); }, { passive: true });
    window.addEventListener('orientationchange', function () { schedule(measure); });
    window.addEventListener('load', function () { schedule(measure); });
    document.addEventListener('ngis:layout:changed', function () { schedule(measure); });

    if (window.visualViewport) {
      window.visualViewport.addEventListener('resize', function () { schedule(measure); });
    }

    if ('ResizeObserver' in window) {
      resizeObserver = new ResizeObserver(function () { schedule(measure); });
      resizeObserver.observe(header);
      resizeObserver.observe(spacer);
      var main = document.querySelector('.main');
      if (main) resizeObserver.observe(main);
    }

    if ('MutationObserver' in window) {
      mutationObserver = new MutationObserver(function () { schedule(measure); });
      mutationObserver.observe(body, { attributes: true, attributeFilter: ['class'] });
      mutationObserver.observe(root, { attributes: true, attributeFilter: ['data-theme'] });
      var overlay = document.querySelector('[data-ngis-fullscreen-overlay]');
      if (overlay) mutationObserver.observe(overlay, { attributes: true, attributeFilter: ['class', 'style'] });
    }
  }

  function boot() {
    if (!body) return;

    if (body.dataset.ngisNavbar === 'page' || document.getElementById('ngisGlobalNavbar')) {
      body.classList.add('ngis-sticky-suspended');
      var oldSpacers = document.querySelectorAll('.ngis-sticky-spacer');
      for (var s = 0; s < oldSpacers.length; s++) {
        oldSpacers[s].remove();
      }
      return;
    }

    header = pickHeader();
    if (!header) {
      /* hero.js and the shared layout engine mount asynchronously. */
      attempts++;
      if (attempts < 14) window.setTimeout(boot, 120);
      return;
    }

    body.setAttribute('data-ngis-sticky-booted', 'true');
    root.classList.add('ngis-sticky-ready');
    hideDuplicateHeaders();

    spacer = document.createElement('div');
    spacer.className = 'ngis-sticky-spacer';
    spacer.setAttribute('aria-hidden', 'true');
    header.parentNode.insertBefore(spacer, header);

    header.classList.add('ngis-sticky-active');
    bind();
    if (resizeObserver) {
      resizeObserver.observe(header);
      resizeObserver.observe(spacer);
      var mainEl = document.querySelector('.main');
      if (mainEl) resizeObserver.observe(mainEl);
    }
    measure();

    /* Late web-font and CDN layout changes alter header height on some pages. */
    window.setTimeout(function () { schedule(measure); }, 300);
    window.setTimeout(function () { schedule(measure); }, 1200);
  }

  window.NGISSticky = {
    refresh: function () { schedule(measure); },
    getHeader: function () { return header; }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(window, document);
