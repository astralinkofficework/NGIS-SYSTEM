/**
 * ============================================================
 * NGIS Global Modal & Popup UI System (Enterprise 2026)
 * - Focused modal experience with background blur (backdrop-filter)
 * - Viewport-wide dimming covering sidebar, topbar, and main content
 * - Background scroll lock with scrollbar jump compensation
 * - Smooth entrance (200ms) and exit (160ms) animations
 * - Keyboard accessibility: focus trap, Escape key, focus restoration
 * - Protection of unsaved form data
 * - Strictly NO BOLD FONTS (maximum font-weight: 500)
 * ============================================================
 */

(function (window, document) {
  "use strict";

  var activeModals = [];
  var lastActiveElement = null;
  var scrollbarWidth = null;
  var savedScrollY = 0;

  function getScrollbarWidth() {
    if (scrollbarWidth !== null) return scrollbarWidth;
    var outer = document.createElement("div");
    outer.style.visibility = "hidden";
    outer.style.overflow = "scroll";
    outer.style.msOverflowStyle = "scrollbar";
    document.body.appendChild(outer);
    var inner = document.createElement("div");
    outer.appendChild(inner);
    scrollbarWidth = outer.offsetWidth - inner.offsetWidth;
    outer.parentNode.removeChild(outer);
    return scrollbarWidth;
  }

  function lockScroll() {
    if (activeModals.length > 1) return; // already locked
    savedScrollY = window.scrollY || window.pageYOffset || 0;
    var sbWidth = getScrollbarWidth();
    var hasScrollbar = window.innerWidth > document.documentElement.clientWidth;

    document.documentElement.classList.add("ngis-modal-open");
    document.body.classList.add("ngis-modal-open");
    if (hasScrollbar && sbWidth > 0) {
      document.body.style.paddingRight = sbWidth + "px";
    }
  }

  function unlockScroll() {
    if (activeModals.length > 0) return; // other modals still open
    document.documentElement.classList.remove("ngis-modal-open");
    document.body.classList.remove("ngis-modal-open");
    document.body.style.paddingRight = "";
    if (typeof savedScrollY === "number" && savedScrollY > 0) {
      window.scrollTo(0, savedScrollY);
    }
  }

  function getFocusableElements(container) {
    if (!container) return [];
    var selectors = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled]):not([type="hidden"])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])'
    ];
    var nodes = Array.prototype.slice.call(container.querySelectorAll(selectors.join(',')));
    return nodes.filter(function (el) {
      return el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement;
    });
  }

  function handleTabKey(e, modalBox) {
    var focusables = getFocusableElements(modalBox);
    if (!focusables.length) {
      e.preventDefault();
      return;
    }
    var first = focusables[0];
    var last = focusables[focusables.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === first || !modalBox.contains(document.activeElement)) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last || !modalBox.contains(document.activeElement)) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  function snapshotForm(modalBox) {
    if (!modalBox) return;
    var inputs = modalBox.querySelectorAll('input:not([type="hidden"]):not([type="button"]):not([type="submit"]), textarea, select');
    for (var i = 0; i < inputs.length; i++) {
      var inp = inputs[i];
      if (inp.type === 'checkbox' || inp.type === 'radio') {
        inp.setAttribute('data-initial-checked', inp.checked ? '1' : '0');
      } else {
        inp.setAttribute('data-initial-val', inp.value || '');
      }
    }
  }

  function isFormDirty(modalBox) {
    if (!modalBox) return false;
    var inputs = modalBox.querySelectorAll('input:not([type="hidden"]):not([type="button"]):not([type="submit"]), textarea, select');
    for (var i = 0; i < inputs.length; i++) {
      var inp = inputs[i];
      if (inp.type === 'checkbox' || inp.type === 'radio') {
        var initChecked = inp.getAttribute('data-initial-checked');
        if (initChecked !== null) {
          if ((inp.checked ? '1' : '0') !== initChecked) return true;
        } else if (inp.checked !== inp.defaultChecked) {
          return true;
        }
      } else {
        var initVal = inp.getAttribute('data-initial-val');
        if (initVal !== null) {
          if (inp.value !== initVal) return true;
        } else if (inp.tagName === 'SELECT') {
          // select without snapshot is not dirty by default
          continue;
        } else {
          var def = inp.defaultValue || '';
          if (inp.value !== def && inp.value.trim() !== '') return true;
        }
      }
    }
    return false;
  }

  var NGISModalSystem = {
    /**
     * Mounts and animates an existing or newly created modal backdrop
     */
    open: function (backdropEl, options) {
      if (!backdropEl) return;
      options = options || {};

      lastActiveElement = document.activeElement;

      // Ensure backdrop is direct child of body so it is never trapped
      if (backdropEl.parentNode !== document.body) {
        document.body.appendChild(backdropEl);
      }

      backdropEl.classList.add("ngis-modal-backdrop-root");
      var modalBox = backdropEl.querySelector('.smx-modal, .rp-modal, .ngis-modal, .ngis-modal-box, .id-modal-container, .modal, [role="dialog"]');
      if (modalBox) {
        modalBox.classList.add("ngis-modal-box-root");
        snapshotForm(modalBox);
      }

      lockScroll();
      activeModals.push({ backdrop: backdropEl, box: modalBox, options: options });

      // Trigger smooth entrance animation with NGIS_MOTION or CSS fallback
      backdropEl.classList.remove("ngis-modal-exit");
      backdropEl.classList.add("ngis-modal-enter");

      if (window.NGIS_MOTION && typeof window.NGIS_MOTION.modalEnter === 'function') {
        window.NGIS_MOTION.modalEnter(backdropEl, modalBox, function () {
          backdropEl.classList.add("ngis-modal-active");
          backdropEl.classList.remove("ngis-modal-enter");
        });
      } else {
        void backdropEl.offsetWidth;
        requestAnimationFrame(function () {
          backdropEl.classList.add("ngis-modal-active");
          backdropEl.classList.remove("ngis-modal-enter");
        });
      }

      // Focus first interactive element or close button
      if (modalBox) {
        var focusables = getFocusableElements(modalBox);
        var firstInput = modalBox.querySelector('input:not([type="hidden"]), select, textarea');
        if (firstInput && !options.noAutoFocus) {
          firstInput.focus();
        } else if (focusables.length) {
          focusables[0].focus();
        } else {
          modalBox.focus();
        }
      }
    },

    /**
     * Gracefully closes and animates out the modal
     */
    close: function (backdropEl, force) {
      if (!backdropEl && activeModals.length > 0) {
        backdropEl = activeModals[activeModals.length - 1].backdrop;
      }
      if (!backdropEl) return;

      var entryIdx = -1;
      for (var i = 0; i < activeModals.length; i++) {
        if (activeModals[i].backdrop === backdropEl) {
          entryIdx = i;
          break;
        }
      }
      var entry = entryIdx !== -1 ? activeModals[entryIdx] : null;

      // Check for unsaved dirty changes if not forced
      if (!force && entry && entry.options && entry.options.confirmUnsaved && entry.box && isFormDirty(entry.box)) {
        if (window.NGIS_UX && typeof window.NGIS_UX.confirm === "function") {
          window.NGIS_UX.confirm({
            title: "Discard Unsaved Changes?",
            description: "You have unsaved edits in this form. Closing will discard your pending modifications.",
            consequence: "Unsaved form data will be permanently discarded.",
            confirmLabel: "Discard Changes",
            cancelLabel: "Keep Editing",
            isDestructive: true,
            isRecoverable: false,
            icon: "exclamation-triangle"
          }).then(function (confirmed) {
            if (confirmed) {
              close(backdropEl, true);
            }
          });
          return;
        } else {
          var leave = window.confirm("You have unsaved changes in this form. Discard changes and close?");
          if (!leave) return;
        }
      }

      if (entryIdx !== -1) {
        activeModals.splice(entryIdx, 1);
      }

      backdropEl.classList.remove("ngis-modal-active");
      backdropEl.classList.add("ngis-modal-exit");

      var cleanup = function () {
        if (backdropEl && backdropEl.parentNode) {
          backdropEl.parentNode.removeChild(backdropEl);
        }
        unlockScroll();

        // Restore focus
        if (lastActiveElement && typeof lastActiveElement.focus === "function") {
          try { lastActiveElement.focus(); } catch (err) {}
        }
      };

      if (window.NGIS_MOTION && typeof window.NGIS_MOTION.modalExit === 'function') {
        window.NGIS_MOTION.modalExit(backdropEl, entry ? entry.box : null, cleanup);
      } else {
        var prefersReducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        var duration = prefersReducedMotion ? 10 : 180;
        setTimeout(cleanup, duration);
      }
    },

    /**
     * Helper to check if any modal is currently open
     */
    isOpen: function () {
      return activeModals.length > 0;
    },

    /**
     * Top-most modal backdrop element
     */
    current: function () {
      return activeModals.length ? activeModals[activeModals.length - 1].backdrop : null;
    }
  };

  // Global keydown handler: Tab trapping & Escape to close
  document.addEventListener("keydown", function (e) {
    if (!activeModals.length) return;
    var current = activeModals[activeModals.length - 1];

    if (e.key === "Tab") {
      handleTabKey(e, current.box || current.backdrop);
    } else if (e.key === "Escape") {
      // Don't close if disabled in options
      if (current.options && current.options.disableEsc) return;
      e.preventDefault();
      NGISModalSystem.close(current.backdrop, false);
    }
  });

  window.NGIS_MODAL = NGISModalSystem;

})(window, document);
