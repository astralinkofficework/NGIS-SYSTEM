/**
 * ============================================================================
 * NGIS ERP — Global Standardized Pagination Component & Animation Controller
 * Universal Previous / Indicators / Next system with GSAP directional transitions,
 * state preservation, keyboard navigation, and responsive touch targets.
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // Escape helper
  function esc(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Detect reduced motion
  function isReducedMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  /**
   * Helper to compute windowed page array with ellipses
   * e.g. [1, "...", 4, 5, 6, "...", 20]
   */
  function computePageWindow(current, totalPages) {
    if (totalPages <= 7) {
      var arr = [];
      for (var i = 1; i <= totalPages; i++) arr.push(i);
      return arr;
    }
    var out = [1];
    var left = Math.max(2, current - 1);
    var right = Math.min(totalPages - 1, current + 1);

    if (current <= 3) {
      left = 2;
      right = 4;
    } else if (current >= totalPages - 2) {
      left = totalPages - 3;
      right = totalPages - 1;
    }

    if (left > 2) out.push("...");
    for (var p = left; p <= right; p++) out.push(p);
    if (right < totalPages - 1) out.push("...");
    out.push(totalPages);
    return out;
  }

  /**
   * Universal Pagination Instance
   */
  function PaginationController(options) {
    this.container = typeof options.container === "string"
      ? document.querySelector(options.container)
      : options.container;

    this.contentContainer = typeof options.contentContainer === "string"
      ? document.querySelector(options.contentContainer)
      : options.contentContainer;

    this.totalItems = Number(options.totalItems) || 0;
    this.pageSize = Math.max(1, Number(options.pageSize) || 10);
    this.currentPage = Math.max(1, Number(options.currentPage) || 1);
    this.mode = options.mode === "dots" ? "dots" : "numbers"; // "numbers" or "dots"
    this.showSummary = options.showSummary !== false;
    this.itemLabel = options.itemLabel || "records"; // e.g. "classes", "assignments", "accounts"
    this.onPageChange = typeof options.onPageChange === "function" ? options.onPageChange : null;
    this.isLoading = false;

    this.init();
  }

  PaginationController.prototype = {
    init: function () {
      if (!this.container) return;
      this.render();
      this.bindEvents();
    },

    getTotalPages: function () {
      return Math.max(1, Math.ceil(this.totalItems / this.pageSize));
    },

    /**
     * Update pagination state (e.g., when search filter changes)
     */
    update: function (data) {
      data = data || {};
      if (data.totalItems != null) this.totalItems = Math.max(0, Number(data.totalItems));
      if (data.pageSize != null) this.pageSize = Math.max(1, Number(data.pageSize));
      if (data.currentPage != null) {
        this.currentPage = Math.max(1, Number(data.currentPage));
      }

      var maxPages = this.getTotalPages();
      if (this.currentPage > maxPages) {
        this.currentPage = maxPages;
      }

      this.render();
    },

    /**
     * Reset to page 1 (call whenever user types a search query or switches filters)
     */
    reset: function (newTotalItems) {
      if (newTotalItems != null) {
        this.totalItems = Math.max(0, Number(newTotalItems));
      }
      this.currentPage = 1;
      this.render();
    },

    /**
     * Go to a specific page with directional animation
     */
    goToPage: function (targetPage) {
      var totalPages = this.getTotalPages();
      targetPage = Math.max(1, Math.min(totalPages, Number(targetPage) || 1));

      if (targetPage === this.currentPage && !this.isLoading) return;
      if (this.isLoading) return;

      var direction = targetPage > this.currentPage ? "forward" : "backward";
      var oldPage = this.currentPage;
      this.currentPage = targetPage;

      // Animate directional content transition
      this.animateContentTransition(direction);

      // Re-render controls
      this.render();

      // Trigger callback
      if (this.onPageChange) {
        this.isLoading = true;
        try {
          var res = this.onPageChange(this.currentPage, {
            pageSize: this.pageSize,
            direction: direction,
            oldPage: oldPage
          });
          if (res && typeof res.then === "function") {
            var self = this;
            res.finally(function () { self.isLoading = false; });
          } else {
            this.isLoading = false;
          }
        } catch (err) {
          this.isLoading = false;
          console.error("[NGIS Pagination] Error in onPageChange:", err);
        }
      }
    },

    nextPage: function () {
      if (this.currentPage < this.getTotalPages()) {
        this.goToPage(this.currentPage + 1);
      }
    },

    prevPage: function () {
      if (this.currentPage > 1) {
        this.goToPage(this.currentPage - 1);
      }
    },

    /**
     * GSAP Directional Transition on Content
     */
    animateContentTransition: function (direction) {
      if (!this.contentContainer || isReducedMotion()) return;

      var el = this.contentContainer;
      var offset = direction === "forward" ? 18 : -18;

      if (typeof gsap !== "undefined" && typeof gsap.fromTo === "function") {
        gsap.fromTo(el,
          { opacity: 0.2, x: offset },
          { opacity: 1, x: 0, duration: 0.22, ease: "power2.out", clearProps: "transform,opacity" }
        );
      } else {
        // CSS fallback
        el.style.transition = "transform 0.18s ease-out, opacity 0.18s ease-out";
        el.style.transform = "translateX(" + offset + "px)";
        el.style.opacity = "0.3";
        requestAnimationFrame(function () {
          el.style.transform = "translateX(0)";
          el.style.opacity = "1";
        });
      }
    },

    /**
     * Render the pagination bar HTML
     */
    render: function () {
      if (!this.container) return;

      var totalPages = this.getTotalPages();
      var isFirst = this.currentPage <= 1;
      var isLast = this.currentPage >= totalPages;

      // Calculate record range
      var startRecord = this.totalItems === 0 ? 0 : (this.currentPage - 1) * this.pageSize + 1;
      var endRecord = Math.min(this.totalItems, this.currentPage * this.pageSize);

      var summaryHtml = "";
      if (this.showSummary) {
        summaryHtml =
          '<div class="ngis-pagination-summary">' +
            (this.totalItems === 0
              ? 'No ' + esc(this.itemLabel) + ' found'
              : 'Showing <span class="font-medium">' + startRecord + '</span> to <span class="font-medium">' + endRecord + '</span> of <span class="font-medium">' + this.totalItems + '</span> ' + esc(this.itemLabel)) +
          '</div>';
      }

      // Middle controls: Numbers or Dots
      var middleHtml = "";
      if (this.mode === "dots") {
        // Progress Dots Mode (for 2–6 step flows)
        var dots = [];
        for (var d = 1; d <= totalPages; d++) {
          var isCurDot = d === this.currentPage;
          dots.push(
            '<button type="button" class="ngis-pag-dot' + (isCurDot ? ' is-active' : '') + '" ' +
                    'data-page="' + d + '" ' +
                    'aria-label="Step ' + d + ' of ' + totalPages + '" ' +
                    'aria-current="' + (isCurDot ? 'step' : 'false') + '">' +
            '</button>'
          );
        }
        middleHtml = '<div class="ngis-pagination-dots" role="tablist">' + dots.join("") + '</div>';
      } else {
        // Numerical Indicators Mode
        var pagesWindow = computePageWindow(this.currentPage, totalPages);
        var pageBtns = pagesWindow.map(function (p) {
          if (p === "...") {
            return '<span class="ngis-pag-ellipsis" aria-hidden="true">&hellip;</span>';
          }
          var isCur = p === this.currentPage;
          return (
            '<button type="button" class="ngis-pag-btn ngis-pag-number' + (isCur ? ' is-active' : '') + '" ' +
                    'data-page="' + p + '" ' +
                    'aria-label="Page ' + p + '" ' +
                    'aria-current="' + (isCur ? 'page' : 'false') + '">' +
              p +
            '</button>'
          );
        }.bind(this));
        middleHtml = '<div class="ngis-pagination-numbers" role="navigation" aria-label="Page selection">' + pageBtns.join("") + '</div>';
      }

      // Complete Component Shell
      this.container.innerHTML =
        '<div class="ngis-pagination-wrapper">' +
          summaryHtml +
          '<div class="ngis-pagination-controls" role="group" aria-label="Pagination">' +
            // 1. Previous Button (Neutral/White on left)
            '<button type="button" class="ngis-pag-btn ngis-pag-prev' + (isFirst ? ' is-disabled' : '') + '" ' +
                    'data-action="prev" ' +
                    (isFirst ? 'disabled aria-disabled="true"' : '') + ' ' +
                    'aria-label="Previous page">' +
              '<span class="ngis-pag-icon" data-ngis-icon="chevronLeft" aria-hidden="true">&lsaquo;</span>' +
              '<span class="ngis-pag-text">Previous</span>' +
            '</button>' +

            // 2. Middle Indicators
            middleHtml +

            // 3. Next Button (NGIS Primary Green on right)
            '<button type="button" class="ngis-pag-btn ngis-pag-next' + (isLast ? ' is-disabled' : '') + '" ' +
                    'data-action="next" ' +
                    (isLast ? 'disabled aria-disabled="true"' : '') + ' ' +
                    'aria-label="Next page">' +
              '<span class="ngis-pag-text">Next</span>' +
              '<span class="ngis-pag-icon" data-ngis-icon="chevronRight" aria-hidden="true">&rsaquo;</span>' +
            '</button>' +
          '</div>' +
        '</div>';

      // Hydrate official Bootstrap icons
      if (window.NGIS && typeof window.NGIS.hydrateIcons === "function") {
        window.NGIS.hydrateIcons(this.container);
      }
    },

    /**
     * Wire click and keyboard events
     */
    bindEvents: function () {
      var self = this;

      this.container.addEventListener("click", function (e) {
        var prevBtn = e.target.closest('[data-action="prev"]');
        if (prevBtn && !prevBtn.disabled) {
          e.preventDefault();
          self.prevPage();
          return;
        }

        var nextBtn = e.target.closest('[data-action="next"]');
        if (nextBtn && !nextBtn.disabled) {
          e.preventDefault();
          self.nextPage();
          return;
        }

        var pageBtn = e.target.closest("[data-page]");
        if (pageBtn) {
          e.preventDefault();
          var p = Number(pageBtn.getAttribute("data-page"));
          if (p) self.goToPage(p);
        }
      });

      // Keyboard navigation when container has focus
      this.container.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") {
          e.preventDefault();
          self.prevPage();
        } else if (e.key === "ArrowRight") {
          e.preventDefault();
          self.nextPage();
        }
      });
    }
  };

  /* ── FACTORY API ── */
  var PaginationEngine = {
    /**
     * Create a new pagination instance
     * @param {Object} options
     * @returns {PaginationController}
     */
    create: function (options) {
      return new PaginationController(options);
    },

    /**
     * Animate a directional transition on any container
     */
    animateTransition: function (container, direction) {
      if (!container || isReducedMotion()) return;
      var offset = direction === "forward" ? 18 : -18;
      if (typeof gsap !== "undefined" && typeof gsap.fromTo === "function") {
        gsap.fromTo(container,
          { opacity: 0.2, x: offset },
          { opacity: 1, x: 0, duration: 0.22, ease: "power2.out", clearProps: "transform,opacity" }
        );
      }
    }
  };

  window.NGIS_PAGINATION = PaginationEngine;
  if (!window.NGIS) window.NGIS = {};
  window.NGIS.pagination = PaginationEngine;

})(window, document);
