/* ==========================================================================
   NGIS Shared Search Enhancer
   Guarantees a unified, accessible layout, single visual boundary, and working
   clear action for all search inputs across NGIS-SYSTEM.
   Does NOT alter page-level search filtering logic, pagination, or query params.
   ========================================================================== */
(function (window, document) {
  'use strict';

  var READY = 'ngisSearchReady';
  var WRAPPER_SELECTOR = '.ngis-search, .htb-search-wrap, .search, .sb-search-box, ' +
    '.sb-search-wrap, .hpd-search-input-wrap, .ann-search-input-wrap, ' +
    '.dir-search-wrap, .dir-search-input-wrap, .smx-search, .search-input-with-icon, ' +
    '[data-purpose="filtering-controls"], .filter-bar, .oak-filter-search-wrap';

  var CLEAR_SELECTOR = '.ngis-search-clear, [aria-label*="Clear"], [aria-label*="clear"], ' +
    '[title*="Clear"], [title*="clear"], #clearSearch, #clearDeptSearch, #clearSearchBtn, ' +
    '#lfClearSearchBtn, #campusSearchClear, #searchClearBtn, #mobileClearSearchBtn';

  var CONFLICTING_CLASSES = [
    'bg-white', 'bg-slate-50', 'bg-slate-100', 'border', 'border-slate-200',
    'border-[#E1E9E3]', 'border-slate-300', 'rounded-lg', 'rounded-xl', 'rounded-md',
    'rounded-full', 'shadow-xs', 'shadow-2xs', 'min-h-[40px]', 'min-h-[38px]',
    'focus:ring-1', 'focus:ring-2', 'focus:ring-[#176B45]', 'focus:ring-[#0F5132]',
    'focus:border-[#176B45]', 'focus:border-[#0F5132]', 'focus:outline-none'
  ];

  var TRANSFER_WIDTH_CLASSES = [
    'w-full', 'sm:w-56', 'w-56', 'w-64', 'w-72', 'w-80', 'max-w-xs',
    'max-w-sm', 'max-w-md', 'max-w-lg', 'max-w-xl', 'max-w-2xl', 'flex-1'
  ];

  function classNameOf(node) {
    if (!node) return '';
    if (node.className && typeof node.className === 'object' && 'baseVal' in node.className) {
      return String(node.className.baseVal || '');
    }
    return String(node.className || '');
  }

  function isIcon(node) {
    if (!node || node.nodeType !== 1) return false;
    if (/^(INPUT|BUTTON|TEXTAREA|SELECT|LABEL|KBD)$/.test(node.tagName)) return false;
    if (node.hasAttribute && node.hasAttribute('data-ngis-search')) return false;

    var cls = classNameOf(node);
    var text = String(node.textContent || '').trim();
    if (/search|magnifying|ngis-search-icon/i.test(cls) || text === 'search') return true;

    var glyph = node.querySelector ? node.querySelector('i, svg, span') : null;
    if (!glyph) return false;
    var glyphCls = classNameOf(glyph);
    if (/search|magnifying/i.test(glyphCls)) return true;
    return !text && /^(I|SVG|SPAN)$/.test(glyph.tagName);
  }

  function findIcon(wrapper) {
    var direct = Array.prototype.slice.call(wrapper.children).filter(isIcon);
    return direct[0] || wrapper.querySelector('.ngis-search-icon');
  }

  function findKbd(wrapper) {
    return Array.prototype.slice.call(wrapper.children).filter(function (node) {
      return node && node.tagName === 'KBD';
    })[0] || null;
  }

  function makeIcon() {
    var icon = document.createElement('span');
    icon.className = 'ngis-search-icon';
    icon.setAttribute('data-ngis-icon', 'search');
    icon.setAttribute('aria-hidden', 'true');
    if (window.NGIS && typeof window.NGIS.icon === 'function') {
      icon.innerHTML = window.NGIS.icon('search');
    } else {
      icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/></svg>';
    }
    return icon;
  }

  function makeClear(input) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ngis-search-clear';
    button.setAttribute('aria-label', 'Clear search');
    button.title = 'Clear search';
    if (window.NGIS && typeof window.NGIS.icon === 'function') {
      button.innerHTML = window.NGIS.icon('close');
    } else {
      button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293z"/></svg>';
    }
    button.addEventListener('click', function (e) {
      e.preventDefault();
      input.value = '';
      input.focus();
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
    return button;
  }

  function enhance(input) {
    if (!input || input.getAttribute('data-ngis-search-skip') === 'true' ||
        input.dataset[READY] || input.type === 'hidden') return;

    // Do not touch searchable dropdown menus or select-menus
    if (input.classList.contains('select-search') ||
        input.classList.contains('ngis-combobox-search-input') ||
        (input.closest && (input.closest('.select-menu') || input.closest('.ngis-combobox')))) {
      input.dataset[READY] = 'true';
      return;
    }

    var parent = input.parentElement;
    if (!parent) return;

    var wrapper;
    var parentIsSearchShell = parent.matches(WRAPPER_SELECTOR);
    var parentHasIcon = Array.prototype.slice.call(parent.children).some(isIcon);

    if (parentIsSearchShell || (parentHasIcon && parent.children.length <= 5)) {
      wrapper = parent;
    } else {
      wrapper = document.createElement('div');
      wrapper.className = 'ngis-search';
      parent.insertBefore(wrapper, input);
      wrapper.appendChild(input);

      // Transfer inline width constraints so toolbars maintain exact sizing
      if (input.style.width) {
        wrapper.style.width = input.style.width;
        input.style.width = '100%';
      }
      if (input.style.maxWidth) {
        wrapper.style.maxWidth = input.style.maxWidth;
        input.style.maxWidth = '100%';
      }
      if (input.style.minWidth) {
        wrapper.style.minWidth = input.style.minWidth;
        input.style.minWidth = '0';
      }

      // Transfer layout utility classes to the wrapper
      TRANSFER_WIDTH_CLASSES.forEach(function (cls) {
        if (input.classList.contains(cls)) {
          wrapper.classList.add(cls);
          input.classList.remove(cls);
        }
      });
    }

    wrapper.classList.add('ngis-search');

    if (wrapper.classList.contains('htb-search-wrap') ||
        wrapper.classList.contains('search') ||
        wrapper.classList.contains('hpd-search-input-wrap')) {
      wrapper.classList.add('ngis-search--hero');
    }
    if (wrapper.classList.contains('sb-search-box') ||
        wrapper.classList.contains('sb-search-wrap')) {
      wrapper.classList.add('ngis-search--compact');
    }

    // Strip duplicate or conflicting inline Tailwind classes from input
    CONFLICTING_CLASSES.forEach(function (cls) {
      input.classList.remove(cls);
    });

    input.classList.add('ngis-search-input');
    input.setAttribute('data-ngis-search', 'true');

    if (!input.getAttribute('aria-label') && !(input.labels && input.labels.length)) {
      input.setAttribute('aria-label', String(input.placeholder || 'Search').trim());
    }

    var icon = findIcon(wrapper);
    if (!icon) {
      wrapper.insertBefore(makeIcon(), input);
    } else {
      icon.classList.add('ngis-search-icon');
      icon.setAttribute('aria-hidden', 'true');
    }

    // Ensure icon engine hydrates if present
    if (window.NGIS && typeof window.NGIS.hydrateIcons === 'function') {
      window.NGIS.hydrateIcons(wrapper);
    }

    /* Wire or adopt clear button */
    var existingClear = null;
    try {
      existingClear = wrapper.querySelector(CLEAR_SELECTOR);
    } catch (_) {}
    if (!existingClear && wrapper.parentElement) {
      try {
        existingClear = wrapper.parentElement.querySelector(CLEAR_SELECTOR);
      } catch (_) {}
      if (existingClear && !wrapper.contains(existingClear)) {
        wrapper.appendChild(existingClear);
      }
    }

    if (existingClear) {
      existingClear.classList.add('ngis-search-clear');
      existingClear.classList.remove('hidden'); // Let .has-value manage visibility
      existingClear.addEventListener('click', function () {
        input.value = '';
        input.focus();
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        sync();
      });
    } else {
      var kbd = findKbd(wrapper);
      wrapper.insertBefore(makeClear(input), kbd);
    }

    function sync() {
      var hasVal = Boolean(String(input.value || '').length);
      wrapper.classList.toggle('has-value', hasVal);
    }

    input.addEventListener('input', sync);
    input.addEventListener('change', sync);
    sync();

    input.dataset[READY] = 'true';
  }

  function candidates() {
    var sel = 'input[type="search"],' +
      'input[placeholder*="Search"], input[placeholder*="search"],' +
      'input[id*="search"], input[id*="Search"],' +
      'input[class*="search"], .search input, .ngis-search input';
    try {
      return document.querySelectorAll(sel);
    } catch (_) {
      return document.getElementsByTagName('input');
    }
  }

  function needsWork() {
    var list = candidates();
    for (var i = 0; i < list.length; i += 1) {
      if (!list[i].dataset[READY] && list[i].getAttribute('data-ngis-search-skip') !== 'true' &&
          list[i].type !== 'hidden') return true;
    }
    return false;
  }

  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () {
      scheduled = false;
      if (needsWork()) init();
    });
  }

  function init() {
    Array.prototype.forEach.call(candidates(), enhance);
  }

  window.NGISSearch = {
    refresh: function () { init(); },
    setLoading: function (input, loading) {
      if (!input) return;
      var wrapper = input.closest('.ngis-search') || input.parentElement;
      if (wrapper) wrapper.classList.toggle('is-loading', Boolean(loading));
    },
    clear: function (input) {
      if (!input) return;
      input.value = '';
      input.dispatchEvent(new Event('input', { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      init();
      if (window.MutationObserver) {
        var observer = new MutationObserver(schedule);
        observer.observe(document.body, { childList: true, subtree: true });
      }
    });
  } else {
    init();
    if (window.MutationObserver) {
      var observer = new MutationObserver(schedule);
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }
})(window, document);
