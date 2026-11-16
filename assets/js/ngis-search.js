/* NGIS Shared Search Enhancer
   Adds a consistent layout, accessible label and clear action to existing
   search inputs. It does NOT replace page filtering logic or issue requests. */
(function (window, document) {
  'use strict';

  var READY = 'ngisSearchReady';
  var WRAPPER_SELECTOR = '.ngis-search, .htb-search-wrap, .search, .sb-search-box, ' +
    '.sb-search-wrap, .hpd-search-input-wrap, .ann-search-input-wrap, ' +
    '.dir-search-input-wrap, .smx-search, .search-input-with-icon, ' +
    '[data-purpose="filtering-controls"], .filter-bar';
  var CLEAR_SELECTOR = '.ngis-search-clear, [aria-label*="Clear" i], ' +
    '[title*="Clear" i], #clearSearch, #clearDeptSearch, #clearSearchBtn, ' +
    '#lfClearSearchBtn, #campusSearchClear, #searchClearBtn, #mobileClearSearchBtn';

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

    /* Legacy pages wrap the glyph in an unlabelled span: <span><i class="ph
       ph-magnifying-glass"></i></span> or <span><svg>...</svg></span>. */
    var glyph = node.querySelector ? node.querySelector('i, svg, span') : null;
    if (!glyph) return false;
    var glyphCls = classNameOf(glyph);
    if (/search|magnifying/i.test(glyphCls)) return true;
    return !text && /^(I|SVG|SPAN)$/.test(glyph.tagName);
  }

  function isClearButton(node) {
    if (!node || node.nodeType !== 1) return false;
    var label = String(node.getAttribute('aria-label') || '');
    var cls = String(node.className || '');
    var id = String(node.id || '');
    return /clear/i.test(label) || /clear/i.test(cls) || /clear/i.test(id);
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
    icon.className = 'material-symbols-outlined ngis-search-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = 'search';
    return icon;
  }

  function makeClear(input) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ngis-search-clear';
    button.setAttribute('aria-label', 'Clear search');
    button.title = 'Clear search';
    button.innerHTML = '&times;';
    button.addEventListener('click', function () {
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

    /* Prefer an existing clear control from the page so its original handler
       stays authoritative. Only add one when none exists in the shell or its
       immediate parent (the common Tailwind "relative" wrapper pattern). */
    var existingClear = wrapper.querySelector(CLEAR_SELECTOR);
    if (!existingClear && wrapper.parentElement) {
      existingClear = wrapper.parentElement.querySelector(CLEAR_SELECTOR);
    }
    if (existingClear) {
      existingClear.classList.add('ngis-search-clear');
    } else {
      var kbd = findKbd(wrapper);
      wrapper.insertBefore(makeClear(input), kbd);
    }

    function sync() {
      wrapper.classList.toggle('has-value', Boolean(String(input.value || '').length));
    }
    input.addEventListener('input', sync);
    input.addEventListener('change', sync);
    sync();

    input.dataset[READY] = 'true';
  }

  function candidates() {
    return document.querySelectorAll(
      'input[type="search"],' +
      'input[placeholder*="Search" i],' +
      'input[id*="search" i],' +
      'input[class*="search" i]'
    );
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
