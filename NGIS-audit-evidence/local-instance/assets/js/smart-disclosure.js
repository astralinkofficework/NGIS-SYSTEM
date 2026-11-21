/**
 * NGIS Smart Content Display & Progressive Disclosure System
 * Reusable vanilla JavaScript component for progressive disclosure across NGIS-SYSTEM.
 *
 * Capabilities:
 * 1. Show More / Show Less: Clamps long descriptions/paragraphs with smooth reveal.
 * 2. Accordions: Expandable sections for lengthy instructions, policies, and secondary info.
 * 3. Smart Tables: Truncates long table cells with clean ellipsis and full-detail popover.
 * 4. Detail Modals: Clean reading view for full text/JSON payloads.
 * 5. Auto-Discovery: Gracefully identifies walls of text without modifying short content.
 *
 * AGENTS.md Compliance:
 * - NO bold fonts (font-weight <= 500)
 * - Accessible aria-expanded and keyboard navigation
 * - Smooth 150-250ms transitions
 */

(function (window, document) {
  'use strict';

  var SmartDisclosure = {
    version: '1.0.0',
    initialized: false,
    popoverBackdrop: null,
    observer: null,
    debounceTimer: null,

    /**
     * Initialize the system across a container or entire document.
     */
    init: function (container) {
      var root = container || document.body;
      if (!root) return;

      this.ensureStylesLoaded();
      this.ensurePopoverElements();

      // 1. Process declarative elements
      this.processDeclarativeClamps(root);
      this.processDeclarativeAccordions(root);
      this.processSmartTables(root);

      // 2. Process auto-discovered long text & instructions
      this.autoDiscoverLongContent(root);

      // 3. Setup dynamic observer if not already running
      if (!this.observer && !container) {
        this.setupObserver();
      }

      this.initialized = true;
    },

    /**
     * Ensure smart-disclosure.css is injected if not already in document.
     */
    ensureStylesLoaded: function () {
      if (document.getElementById('smart-disclosure-css')) return;
      var existing = document.querySelector('link[href*="smart-disclosure.css"]');
      if (existing) return;

      var link = document.createElement('link');
      link.id = 'smart-disclosure-css';
      link.rel = 'stylesheet';
      link.href = (function () {
        var scripts = document.querySelectorAll('script[src*="smart-disclosure.js"], script[src*="layout.js"]');
        if (scripts.length > 0) {
          var src = scripts[0].getAttribute('src') || '';
          var base = src.substring(0, src.lastIndexOf('/'));
          return base ? base.replace('/js', '/css') + '/smart-disclosure.css' : '../../assets/css/smart-disclosure.css';
        }
        return '../../assets/css/smart-disclosure.css';
      })();
      document.head.appendChild(link);
    },

    /**
     * Process elements explicitly marked with [data-disclosure="clamp"] or .smart-clamp
     */
    processDeclarativeClamps: function (root) {
      var items = root.querySelectorAll('[data-disclosure="clamp"], .smart-clamp');
      for (var i = 0; i < items.length; i++) {
        var el = items[i];
        if (el.dataset.smartBound) continue;
        this.bindClampElement(el);
      }
    },

    /**
     * Wrap and bind a clamped element with a Show More/Less toggle.
     */
    bindClampElement: function (el, explicitLines) {
      if (el.dataset.smartBound) return;
      el.dataset.smartBound = 'true';

      var lines = explicitLines || parseInt(el.getAttribute('data-lines'), 10) || 3;
      el.style.setProperty('--smart-clamp-lines', lines);

      // Find or create content wrapper
      var contentEl = el.querySelector('[data-disclosure-content], .smart-clamp-content');
      if (!contentEl) {
        contentEl = document.createElement('div');
        contentEl.className = 'smart-clamp-content';
        while (el.firstChild) {
          contentEl.appendChild(el.firstChild);
        }
        el.appendChild(contentEl);
      }

      // Check if text actually overflows
      var originalDisplay = el.style.display;
      var isClamped = contentEl.scrollHeight > (contentEl.clientHeight + 4);
      
      // If content doesn't overflow, do not add an unnecessary button!
      var rawLength = (contentEl.textContent || '').trim().length;
      if (!isClamped && rawLength < 160) {
        return;
      }

      // Create accessible toggle button
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'smart-toggle-btn';
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-label', 'Reveal more details');

      var uniqueId = 'smart-clamp-' + Math.random().toString(36).substring(2, 9);
      contentEl.id = uniqueId;
      btn.setAttribute('aria-controls', uniqueId);

      btn.innerHTML = '<span class="smart-toggle-label">Show more</span><span class="material-symbols-outlined smart-toggle-icon">expand_more</span>';

      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var expanded = el.classList.toggle('is-expanded');
        btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        var label = btn.querySelector('.smart-toggle-label');
        if (label) {
          label.textContent = expanded ? 'Show less' : 'Show more';
        }
      });

      // Keyboard support
      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });

      el.appendChild(btn);
    },

    /**
     * Process declarative accordions: [data-disclosure="accordion"], .smart-accordion
     */
    processDeclarativeAccordions: function (root) {
      var accordions = root.querySelectorAll('[data-disclosure="accordion"], .smart-accordion');
      for (var i = 0; i < accordions.length; i++) {
        var acc = accordions[i];
        if (acc.dataset.smartBound) continue;
        this.bindAccordionElement(acc);
      }
    },

    /**
     * Bind accordion header click and keyboard events.
     */
    bindAccordionElement: function (acc) {
      if (acc.dataset.smartBound) return;
      acc.dataset.smartBound = 'true';

      var trigger = acc.querySelector('[data-accordion-trigger], .smart-accordion-header');
      var collapse = acc.querySelector('.smart-accordion-collapse');
      var body = acc.querySelector('.smart-accordion-body');

      // If markup was basic, construct structure
      if (!collapse && body) {
        collapse = document.createElement('div');
        collapse.className = 'smart-accordion-collapse';
        acc.insertBefore(collapse, body);
        collapse.appendChild(body);
      }

      if (!trigger) return;

      var isInitiallyOpen = acc.classList.contains('is-expanded') || acc.getAttribute('data-open') === 'true';
      trigger.setAttribute('aria-expanded', isInitiallyOpen ? 'true' : 'false');
      if (isInitiallyOpen) {
        acc.classList.add('is-expanded');
      }

      var uniqueId = 'smart-acc-' + Math.random().toString(36).substring(2, 9);
      if (body) body.id = uniqueId;
      trigger.setAttribute('aria-controls', uniqueId);

      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        var expanded = acc.classList.toggle('is-expanded');
        trigger.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      });

      trigger.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          trigger.click();
        }
      });
    },

    /**
     * Process tables with wide/long cell contents (e.g. audit logs, service notes, change remarks).
     */
    processSmartTables: function (root) {
      var tables = root.querySelectorAll('table.tbl, table.req-table, table.smx-table, table[data-disclosure="table"], .smart-table');
      for (var t = 0; t < tables.length; t++) {
        var table = tables[t];
        if (table.dataset.smartBound) continue;
        table.dataset.smartBound = 'true';

        var rows = table.querySelectorAll('tbody tr');
        for (var r = 0; r < rows.length; r++) {
          var cells = rows[r].querySelectorAll('td');
          for (var c = 0; c < cells.length; c++) {
            var cell = cells[c];
            // Skip action columns or cells with inputs/buttons
            if (cell.classList.contains('table-actions') || cell.querySelector('button, input, select, .action-group')) {
              continue;
            }

            var text = (cell.textContent || '').trim();
            // If cell content is long (> 95 characters) and not already wrapped
            if (text.length > 95 && !cell.querySelector('.smart-cell-wrap')) {
              this.truncateTableCell(cell, text);
            }
          }
        }
      }
    },

    /**
     * Truncate a table cell with an ellipsis and inline detail popup button.
     */
    truncateTableCell: function (cell, fullText) {
      var thIndex = cell.cellIndex;
      var table = cell.closest('table');
      var headerText = 'Detail Information';
      if (table) {
        var th = table.querySelectorAll('thead th')[thIndex];
        if (th) headerText = (th.textContent || '').trim();
      }

      var originalHtml = cell.innerHTML;
      cell.innerHTML = '';

      var wrap = document.createElement('div');
      wrap.className = 'smart-cell-wrap';

      var textSpan = document.createElement('span');
      textSpan.className = 'smart-cell-text';
      textSpan.textContent = fullText;
      textSpan.title = fullText;

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'smart-cell-more-btn';
      btn.textContent = 'More';
      btn.setAttribute('aria-label', 'View full ' + headerText);

      var self = this;
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        self.showDetailModal(headerText, fullText);
      });

      wrap.appendChild(textSpan);
      wrap.appendChild(btn);
      cell.appendChild(wrap);
    },

    /**
     * Auto-discover long paragraphs, announcement descriptions, and instruction callouts
     * that make the UI cluttered.
     */
    autoDiscoverLongContent: function (root) {
      // 1. Long paragraphs in descriptions, guides, and announcement cards
      var candidates = root.querySelectorAll(
        '.ann-notice-desc, .ann-card-desc, .news-card-desc, .lesson-desc, .candidate-desc, ' +
        '.module-desc, .task-desc, .feed-desc, .card-desc, .info-text, .alert-desc'
      );

      for (var i = 0; i < candidates.length; i++) {
        var item = candidates[i];
        if (item.dataset.smartBound || item.closest('.smart-clamp, [data-disclosure]')) continue;
        
        var text = (item.textContent || '').trim();
        if (text.length > 180) {
          item.classList.add('smart-clamp');
          this.bindClampElement(item, 3);
        }
      }

      // 2. Sprawling multi-paragraph instruction callouts
      var callouts = root.querySelectorAll('.art-callout, .instruction-box, .exam-guidelines-box, .guide-card');
      for (var k = 0; k < callouts.length; k++) {
        var box = callouts[k];
        if (box.dataset.smartBound || box.closest('.smart-accordion, [data-disclosure]')) continue;

        var heading = box.querySelector('h2, h3, h4, .art-callout-title, strong');
        var textLength = (box.textContent || '').trim().length;

        // If it's a sizeable instructions box with a clear heading, convert into an accordion
        if (heading && textLength > 240) {
          this.convertBoxToAccordion(box, heading);
        }
      }
    },

    /**
     * Turn a static instruction box into an accessible accordion.
     */
    convertBoxToAccordion: function (box, headingEl) {
      box.dataset.smartBound = 'true';
      box.classList.add('smart-accordion', 'minimal');

      var titleText = (headingEl.textContent || '').trim();
      var icon = 'info';
      if (box.classList.contains('warn') || box.classList.contains('warning')) icon = 'warning';
      if (box.classList.contains('urgent') || box.classList.contains('danger')) icon = 'priority_high';

      // Remove heading from original content flow
      headingEl.remove();

      var headerBtn = document.createElement('button');
      headerBtn.type = 'button';
      headerBtn.className = 'smart-accordion-header';
      headerBtn.setAttribute('aria-expanded', 'false');
      headerBtn.innerHTML =
        '<div class="smart-accordion-title-wrap">' +
          '<span class="smart-accordion-icon"><span class="material-symbols-outlined text-[16px]">' + icon + '</span></span>' +
          '<span class="smart-accordion-title">' + titleText + '</span>' +
          '<span class="smart-accordion-badge">Guidelines</span>' +
        '</div>' +
        '<span class="material-symbols-outlined smart-accordion-chevron">expand_more</span>';

      var collapse = document.createElement('div');
      collapse.className = 'smart-accordion-collapse';

      var body = document.createElement('div');
      body.className = 'smart-accordion-body';

      while (box.firstChild) {
        body.appendChild(box.firstChild);
      }

      collapse.appendChild(body);
      box.appendChild(headerBtn);
      box.appendChild(collapse);

      this.bindAccordionElement(box);
    },

    /**
     * Singleton Detail Popover Modal for viewing complete values and copying text.
     */
    ensurePopoverElements: function () {
      if (this.popoverBackdrop) return;

      var backdrop = document.createElement('div');
      backdrop.className = 'smart-popover-backdrop';
      backdrop.id = 'smartPopoverBackdrop';

      var card = document.createElement('div');
      card.className = 'smart-popover-card';
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-labelledby', 'smartPopoverTitle');

      card.innerHTML =
        '<div class="smart-popover-head">' +
          '<h4 class="smart-popover-title" id="smartPopoverTitle">' +
            '<span class="material-symbols-outlined text-emerald-700 text-[18px]">info</span>' +
            '<span class="title-text">Detail View</span>' +
          '</h4>' +
          '<button type="button" class="smart-popover-close" aria-label="Close dialog" id="smartPopoverClose">' +
            '<span class="material-symbols-outlined">close</span>' +
          '</button>' +
        '</div>' +
        '<div class="smart-popover-body" id="smartPopoverBody"></div>' +
        '<div class="smart-popover-foot">' +
          '<button type="button" class="smart-popover-copy-btn" id="smartPopoverCopy">' +
            '<span class="material-symbols-outlined text-[16px]">content_copy</span>' +
            '<span>Copy to Clipboard</span>' +
          '</button>' +
        '</div>';

      backdrop.appendChild(card);
      document.body.appendChild(backdrop);
      this.popoverBackdrop = backdrop;

      var self = this;
      var closeBtn = card.querySelector('#smartPopoverClose');
      closeBtn.addEventListener('click', function () {
        self.closeDetailModal();
      });

      backdrop.addEventListener('click', function (e) {
        if (e.target === backdrop) {
          self.closeDetailModal();
        }
      });

      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && backdrop.classList.contains('show')) {
          self.closeDetailModal();
        }
      });

      var copyBtn = card.querySelector('#smartPopoverCopy');
      copyBtn.addEventListener('click', function () {
        var body = card.querySelector('#smartPopoverBody');
        var text = (body.textContent || '').trim();
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            copyBtn.innerHTML = '<span class="material-symbols-outlined text-[16px]">check</span><span>Copied!</span>';
            setTimeout(function () {
              copyBtn.innerHTML = '<span class="material-symbols-outlined text-[16px]">content_copy</span><span>Copy to Clipboard</span>';
            }, 2000);
          });
        }
      });
    },

    /**
     * Show full content in modal preview.
     */
    showDetailModal: function (title, content) {
      this.ensurePopoverElements();
      var titleEl = this.popoverBackdrop.querySelector('.title-text');
      var bodyEl = this.popoverBackdrop.querySelector('#smartPopoverBody');

      if (titleEl) titleEl.textContent = title || 'Detail View';
      if (bodyEl) bodyEl.textContent = content || '';

      this.popoverBackdrop.classList.add('show');
      var closeBtn = this.popoverBackdrop.querySelector('#smartPopoverClose');
      if (closeBtn) closeBtn.focus();
    },

    /**
     * Close modal preview.
     */
    closeDetailModal: function () {
      if (this.popoverBackdrop) {
        this.popoverBackdrop.classList.remove('show');
      }
    },

    /**
     * Setup debounced MutationObserver for dynamic AJAX DOM changes.
     */
    setupObserver: function () {
      var self = this;
      this.observer = new MutationObserver(function (mutations) {
        clearTimeout(self.debounceTimer);
        self.debounceTimer = setTimeout(function () {
          for (var i = 0; i < mutations.length; i++) {
            var m = mutations[i];
            if (m.addedNodes && m.addedNodes.length > 0) {
              for (var j = 0; j < m.addedNodes.length; j++) {
                var node = m.addedNodes[j];
                if (node.nodeType === 1) { // ELEMENT_NODE
                  self.processDeclarativeClamps(node);
                  self.processDeclarativeAccordions(node);
                  self.processSmartTables(node);
                  self.autoDiscoverLongContent(node);
                }
              }
            }
          }
        }, 120);
      });

      this.observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
  };

  // Expose globally
  window.SmartDisclosure = SmartDisclosure;

  // Auto-init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      SmartDisclosure.init();
    });
  } else {
    SmartDisclosure.init();
  }

})(window, document);

