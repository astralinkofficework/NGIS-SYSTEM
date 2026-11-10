/**
 * ============================================================
 * NGIS ERP — Reusable ErrorState Component (Rule 5 Compliant)
 * Rule 5: Users never see backend errors, stack traces, SQL,
 * request URLs, or raw JSON.
 * 
 * Every error state includes:
 * - Empathetic institutional message
 * - Confirmation that data is safe
 * - Clear primary "Try Again" action
 * - Internal tracking Request ID (never exposing backend internals)
 * - Dedicated Offline and Timeout modes
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISErrorState = {
    /**
     * Render an accessible, polished error card into a target container
     */
    render(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      // Resolve friendly copy via centralized NGISErrors if raw error provided
      let errorDetails = {};
      if (options.error) {
        errorDetails = window.NGISErrors ? window.NGISErrors.resolve(options.error, options.context) : {};
      }

      const title = options.title || errorDetails.title || "Unable to Load Content";
      const message = options.message || errorDetails.description || "A temporary issue occurred while loading this section. Your data is safe.";
      const retryText = options.retryText || errorDetails.actionText || "Try Again";
      const onRetry = options.onRetry || null;
      const type = options.type || errorDetails.type || "error";
      const requestId = options.requestId || errorDetails.requestId || (window.NGISErrors ? window.NGISErrors.generateRequestId() : "REQ-" + Date.now().toString(36).toUpperCase());
      const showHomeBtn = options.showHomeBtn !== false;
      const fullWidth = options.fullWidth || false;

      // Icon determination based on error mode
      let icon = "ph-warning-circle";
      let iconColor = "#92243D";
      let badgeLabel = "System Notice";

      if (type === "offline" || !navigator.onLine) {
        icon = "ph-wifi-slash";
        iconColor = "#202F63";
        badgeLabel = "Offline Mode";
      } else if (type === "timeout") {
        icon = "ph-clock-countdown";
        iconColor = "#202F63";
        badgeLabel = "Connection Timeout";
      } else if (type === "not_found") {
        icon = "ph-magnifying-glass";
        iconColor = "#555555";
        badgeLabel = "Not Found";
      }

      const root = (window.location.pathname.indexOf("/pages/") !== -1) ? "../../" : "";
      const homeUrl = options.homeUrl || `${root}index.html`;

      const card = document.createElement("div");
      card.className = `ngis-state-card ngis-error-state ${fullWidth ? "full-width" : ""}`;
      card.setAttribute("role", "alert");
      card.setAttribute("aria-live", "assertive");

      card.innerHTML = `
        <div class="ngis-state-icon" style="background:#F3F3F5; color:${iconColor}; border:1px solid #E5E5E8; width:52px; height:52px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:14px;">
          <i class="ph ${icon}"></i>
        </div>
        <div style="margin-bottom:8px;">
          <span style="font-size:11px; font-weight:500; text-transform:uppercase; letter-spacing:0.05em; color:#555555; background:#F3F3F5; border:1px solid #E5E5E8; padding:3px 10px; border-radius:999px;">
            ${badgeLabel}
          </span>
        </div>
        <h3 class="ngis-state-title" style="font-size:16px; font-weight:500; color:#000000; margin-bottom:8px;">
          ${title}
        </h3>
        <p class="ngis-state-desc" style="font-size:13.5px; font-weight:400; color:#555555; max-width:440px; margin:0 auto 20px; line-height:1.55;">
          ${message}
        </p>
        <div class="ngis-state-actions" style="display:flex; justify-content:center; align-items:center; gap:10px; flex-wrap:wrap;">
          ${onRetry ? `
            <button type="button" class="ngis-btn-primary ngis-retry-action-btn" style="min-height:44px; padding:0 20px; border-radius:10px; display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:500; cursor:pointer;">
              <i class="ph ph-arrow-clockwise"></i>
              <span>${retryText}</span>
            </button>
          ` : `
            <button type="button" onclick="window.location.reload()" class="ngis-btn-primary" style="min-height:44px; padding:0 20px; border-radius:10px; display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:500; cursor:pointer;">
              <i class="ph ph-arrow-counter-clockwise"></i>
              <span>Refresh Page</span>
            </button>
          `}
          ${showHomeBtn ? `
            <a href="${homeUrl}" class="ngis-btn-secondary" style="min-height:44px; padding:0 18px; border-radius:10px; display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:500; border:1px solid #E5E5E8; background:#FFFFFF; color:#333333; text-decoration:none;">
              <i class="ph ph-house"></i>
              <span>Portal Home</span>
            </a>
          ` : ""}
        </div>
        <div style="margin-top:20px; font-size:11px; color:#888890; font-family:monospace;">
          Ref: ${requestId}
        </div>
      `;

      if (onRetry) {
        const btn = card.querySelector(".ngis-retry-action-btn");
        if (btn) btn.addEventListener("click", onRetry);
      }

      container.innerHTML = "";
      container.appendChild(card);
    }
  };

  // Custom Web Component: <ngis-error-state title="..." message="..." type="error|offline|timeout"></ngis-error-state>
  if (typeof customElements !== "undefined" && !customElements.get("ngis-error-state")) {
    customElements.define("ngis-error-state", class extends HTMLElement {
      connectedCallback() {
        const title = this.getAttribute("title");
        const message = this.getAttribute("message");
        const type = this.getAttribute("type") || "error";
        NGISErrorState.render(this, { title, message, type });
      }
    });
  }

  window.NGISErrorState = NGISErrorState;
})(window, document);

