/**
 * ============================================================
 * NGIS ERP — Reusable PrimaryButton & Tap Engine (Rule 3 Compliant)
 * Rule 3: Every tap gets an instant response within 100 ms.
 * - Pressed active feedback <100ms
 * - Double-submit protection built-in
 * - State management: default, loading, success, disabled
 * - Accessible touch target >= 44px
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISButton = {
    /**
     * Set a button to its loading / in-progress state
     */
    setLoading(button, loadingText = "Processing...") {
      if (!button) return;
      if (!button.dataset.originalHtml) {
        button.dataset.originalHtml = button.innerHTML;
        button.dataset.originalWidth = button.getBoundingClientRect().width + "px";
      }

      button.style.minWidth = button.dataset.originalWidth;
      button.setAttribute("aria-busy", "true");
      button.setAttribute("disabled", "true");
      button.classList.add("ngis-btn-loading");

      button.innerHTML = `
        <span class="ngis-btn-spinner" aria-hidden="true"></span>
        <span>${loadingText}</span>
      `;
    },

    /**
     * Set a button to a temporary success confirmation state
     */
    setSuccess(button, successText = "Saved Successfully", revertDelay = 1500) {
      if (!button) return;
      const originalHtml = button.dataset.originalHtml || button.innerHTML;

      button.removeAttribute("aria-busy");
      button.classList.remove("ngis-btn-loading");
      button.classList.add("ngis-btn-success-state");

      button.innerHTML = `
        <i class="ph ph-check" style="font-size:16px;"></i>
        <span>${successText}</span>
      `;

      if (revertDelay > 0) {
        setTimeout(() => {
          this.reset(button);
        }, revertDelay);
      }
    },

    /**
     * Restore button to original state
     */
    reset(button) {
      if (!button) return;
      button.removeAttribute("aria-busy");
      button.removeAttribute("disabled");
      button.classList.remove("ngis-btn-loading", "ngis-btn-success-state");
      if (button.dataset.originalHtml) {
        button.innerHTML = button.dataset.originalHtml;
        delete button.dataset.originalHtml;
      }
    },

    /**
     * Wrap an async operation with automated instant response, double-submit protection,
     * loading state, success state, and rollback on failure.
     */
    async execute(button, asyncFn, options = {}) {
      if (!button || button.disabled || button.getAttribute("aria-busy") === "true") {
        return;
      }

      const {
        loadingText = "Processing...",
        successText = "Saved!",
        autoSuccess = true,
        revertMs = 1500,
        onError = null
      } = options;

      this.setLoading(button, loadingText);

      try {
        const result = await asyncFn();
        if (autoSuccess) {
          this.setSuccess(button, successText, revertMs);
        } else {
          this.reset(button);
        }
        return result;
      } catch (err) {
        this.reset(button);
        if (typeof onError === "function") {
          onError(err);
        } else if (window.NGISUI && window.NGISUI.toast) {
          window.NGISUI.toast.error("Action Could Not Complete", err.message || "Please check inputs and retry.");
        }
        throw err;
      }
    },

    /**
     * Initialize global tap feedback & double-click guard across the entire DOM
     */
    initGlobalTapEngine() {
      // 1. Instant <100ms tactile pressed feedback
      const handlePressStart = (e) => {
        const target = e.target.closest("button, .btn, .ngis-btn-primary, .ngis-btn-secondary, a[role='button']");
        if (!target || target.disabled || target.getAttribute("aria-busy") === "true") return;
        target.classList.add("ngis-tap-active");
      };

      const handlePressEnd = (e) => {
        const target = e.target.closest("button, .btn, .ngis-btn-primary, .ngis-btn-secondary, a[role='button']");
        if (target) {
          target.classList.remove("ngis-tap-active");
        }
      };

      document.addEventListener("mousedown", handlePressStart, { passive: true });
      document.addEventListener("mouseup", handlePressEnd, { passive: true });
      document.addEventListener("touchstart", handlePressStart, { passive: true });
      document.addEventListener("touchend", handlePressEnd, { passive: true });
      document.addEventListener("touchcancel", handlePressEnd, { passive: true });

      // 2. Automated double-submit guard for all forms and submit buttons
      document.addEventListener("submit", (e) => {
        const form = e.target;
        if (!form) return;

        const submitBtn = form.querySelector("button[type='submit'], input[type='submit']");
        if (submitBtn) {
          if (submitBtn.getAttribute("aria-busy") === "true") {
            e.preventDefault();
            return false;
          }
          // Mark busy for 800ms debounce
          submitBtn.setAttribute("aria-busy", "true");
          setTimeout(() => {
            if (submitBtn && submitBtn.getAttribute("aria-busy") === "true" && !submitBtn.classList.contains("ngis-btn-loading")) {
              submitBtn.removeAttribute("aria-busy");
            }
          }, 800);
        }
      });
    }
  };

  // Custom Web Component: <ngis-button variant="primary|secondary|danger">...</ngis-button>
  if (typeof customElements !== "undefined" && !customElements.get("ngis-button")) {
    customElements.define("ngis-button", class extends HTMLElement {
      connectedCallback() {
        const variant = this.getAttribute("variant") || "primary";
        const btnClass = variant === "secondary" ? "ngis-btn-secondary" : "ngis-btn-primary";
        this.classList.add(btnClass);
        if (!this.getAttribute("tabindex")) this.setAttribute("tabindex", "0");
        if (!this.getAttribute("role")) this.setAttribute("role", "button");
      }
    });
  }

  // Initialize global engine on load
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => NGISButton.initGlobalTapEngine());
  } else {
    NGISButton.initGlobalTapEngine();
  }

  window.NGISButton = NGISButton;
})(window, document);

