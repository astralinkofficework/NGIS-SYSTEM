with open('assets/js/sticky-layout.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace SELECTORS and pickHeader
old_pick = '''  /* Ordered by authority: an explicit page header wins; the compact mobile
     app bar wins over the large hero header; the legacy topbar is the last
     fallback. */
  var SELECTORS = [
    '[data-ngis-sticky-header]',
    '.mobile-appbar',
    '[data-purpose="mobile-header"]',
    '.htb-topbar-mobile',
    'header.lg\\\\:hidden',
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
  }'''

new_pick = '''  /* Ordered by authority: desktop prioritises hero-topbar; mobile prioritises mobile-appbar. */
  var DESKTOP_SELECTORS = [
    '#heroBanner .hero-topbar',
    '.hero .hero-topbar',
    '.hero-topbar',
    '[data-ngis-sticky-header]:not(.lg\\\\:hidden):not(.md\\\\:hidden)',
    'header.topbar'
  ];

  var MOBILE_SELECTORS = [
    '.mobile-appbar',
    '[data-purpose="mobile-header"]',
    '.htb-topbar-mobile',
    'header.lg\\\\:hidden',
    'header.md\\\\:hidden',
    '[data-ngis-sticky-header]',
    '#heroBanner .hero-topbar',
    '.hero-topbar',
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
    var isDesktop = window.innerWidth >= 1024;
    var list = isDesktop ? DESKTOP_SELECTORS : MOBILE_SELECTORS;
    for (var i = 0; i < list.length; i++) {
      var nodes;
      try { nodes = document.querySelectorAll(list[i]); } catch (e) { continue; }
      for (var j = 0; j < nodes.length; j++) {
        if (isVisible(nodes[j])) return nodes[j];
      }
    }
    // Fallback search in remaining list
    var fallbackList = isDesktop ? MOBILE_SELECTORS : DESKTOP_SELECTORS;
    for (var i = 0; i < fallbackList.length; i++) {
      var nodes;
      try { nodes = document.querySelectorAll(fallbackList[i]); } catch (e) { continue; }
      for (var j = 0; j < nodes.length; j++) {
        if (isVisible(nodes[j])) return nodes[j];
      }
    }
    return null;
  }'''

if old_pick in code:
    code = code.replace(old_pick, new_pick)
    print("Replaced pickHeader successfully.")
else:
    print("Could not find exact old_pick, checking variations...")

# Replace updateStickiness and measure
old_measure_and_sticky = '''  function updateStickiness() {
    if (!header || !spacer || isFullscreen()) return;

    /* Keep the measured trigger point in document coordinates. The spacer
       never moves when the header is fixed, so this is stable while scrolling. */
    var triggerTop = spacer.getBoundingClientRect().top + window.pageYOffset;
    var shouldStick = window.pageYOffset >= triggerTop - 1;
    if (shouldStick === stuck) return;

    stuck = shouldStick;
    header.classList.toggle('ngis-sticky-fixed', shouldStick);
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

    /* Inline !important is the final guard against legacy global sheets that
       still force transparent headers on duplicate component loads. */
    var rootStyle = window.getComputedStyle(root);
    var surface = rootStyle.getPropertyValue('--ngis-sticky-surface').trim() || '#FFFFFF';
    header.style.setProperty('background-color', surface, 'important');
    header.style.setProperty('background-image', 'none', 'important');
    header.style.setProperty('backdrop-filter', 'none', 'important');
    header.style.setProperty('-webkit-backdrop-filter', 'none', 'important');

    root.style.setProperty('--ngis-sticky-h', height + 'px');
    root.style.setProperty('--ngis-sticky-left', left + 'px');
    root.style.setProperty('--ngis-sticky-width', width + 'px');
    applyFullscreenState();
    updateStickiness();
  }'''

new_measure_and_sticky = '''  function getPageBackground() {
    var bodyBg = window.getComputedStyle(body).backgroundColor;
    if (bodyBg && bodyBg !== 'transparent' && bodyBg !== 'rgba(0, 0, 0, 0)') {
      return bodyBg;
    }
    var htmlBg = window.getComputedStyle(root).backgroundColor;
    if (htmlBg && htmlBg !== 'transparent' && htmlBg !== 'rgba(0, 0, 0, 0)') {
      return htmlBg;
    }
    return (root.getAttribute('data-theme') === 'dark') ? '#0F172A' : '#F7F9F7';
  }

  function applyHeaderSurface(isStuck) {
    if (!header) return;
    if (isStuck) {
      var surface = getPageBackground();
      header.style.setProperty('background-color', surface, 'important');
      header.style.setProperty('background', surface, 'important');
    } else {
      header.style.setProperty('background-color', 'transparent', 'important');
      header.style.setProperty('background', 'transparent', 'important');
    }
    header.style.setProperty('background-image', 'none', 'important');
    header.style.setProperty('border', 'none', 'important');
    header.style.setProperty('border-bottom', 'none', 'important');
    header.style.setProperty('box-shadow', 'none', 'important');
    header.style.setProperty('backdrop-filter', 'none', 'important');
    header.style.setProperty('-webkit-backdrop-filter', 'none', 'important');
  }

  function updateStickiness() {
    if (!header || !spacer || isFullscreen()) return;

    /* Keep the measured trigger point in document coordinates. The spacer
       never moves when the header is fixed, so this is stable while scrolling. */
    var triggerTop = spacer.getBoundingClientRect().top + window.pageYOffset;
    var shouldStick = window.pageYOffset > (triggerTop + 1);
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

    /* Apply seamless surface: transparent in normal state, exact page background when scrolled */
    applyHeaderSurface(stuck);

    root.style.setProperty('--ngis-sticky-h', height + 'px');
    root.style.setProperty('--ngis-sticky-left', left + 'px');
    root.style.setProperty('--ngis-sticky-width', width + 'px');
    applyFullscreenState();
    updateStickiness();
  }'''

if old_measure_and_sticky in code:
    code = code.replace(old_measure_and_sticky, new_measure_and_sticky)
    print("Replaced measure and updateStickiness successfully.")
else:
    print("Could not find exact old_measure_and_sticky.")

with open('assets/js/sticky-layout.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated assets/js/sticky-layout.js.")
