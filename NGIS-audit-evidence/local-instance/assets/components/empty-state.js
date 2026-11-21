/**
 * ============================================================
 * NGIS ERP — Reusable EmptyState Component
 * Standards:
 * - Clear explanation of why the state is currently empty
 * - Accessible iconography
 * - Optional primary CTA
 * - Adheres strictly to 60-30-10 palette & 44px touch targets
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISEmptyState = {
    render(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      const {
        icon = "ph-folder-open",
        title = "No Records Available",
        description = "There are no records to display under the selected filter or category.",
        actionText = "",
        actionHref = "",
        onAction = null,
        fullWidth = false,
        className = ""
      } = options;

      const iconHtml = icon.startsWith("ph")
        ? `<i class="ph ${icon}"></i>`
        : `<span class="material-symbols-outlined">${icon}</span>`;

      let actionHtml = "";
      if (actionText) {
        if (actionHref) {
          actionHtml = `
            <a href="${actionHref}" class="ngis-btn-primary" style="min-height:44px; padding:0 20px; border-radius:10px; display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:500; text-decoration:none;">
              <i class="ph ph-plus"></i>
              <span>${actionText}</span>
            </a>
          `;
        } else {
          actionHtml = `
            <button type="button" class="ngis-btn-primary ngis-empty-cta-btn" style="min-height:44px; padding:0 20px; border-radius:10px; display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:500; cursor:pointer;">
              <i class="ph ph-plus"></i>
              <span>${actionText}</span>
            </button>
          `;
        }
      }

      const card = document.createElement("div");
      card.className = `ngis-state-card ngis-empty-state ${fullWidth ? "full-width" : ""} ${className}`;
      card.innerHTML = `
        <div class="ngis-state-icon neutral" style="background:#F3F3F5; color:#333333; border:1px solid #E5E5E8; width:52px; height:52px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:14px;">
          ${iconHtml}
        </div>
        <h3 class="ngis-state-title" style="font-size:16px; font-weight:500; color:#000000; margin-bottom:8px;">
          ${title}
        </h3>
        <p class="ngis-state-desc" style="font-size:13.5px; font-weight:400; color:#555555; max-width:440px; margin:0 auto 20px; line-height:1.55;">
          ${description}
        </p>
        ${actionHtml ? `<div class="ngis-state-actions" style="display:flex; justify-content:center; align-items:center;">${actionHtml}</div>` : ""}
      `;

      if (onAction && !actionHref) {
        const btn = card.querySelector(".ngis-empty-cta-btn");
        if (btn) btn.addEventListener("click", onAction);
      }

      container.innerHTML = "";
      container.appendChild(card);
    }
  };

  // Custom Web Component: <ngis-empty-state icon="..." title="..." description="..." action-text="..." action-href="..."></ngis-empty-state>
  if (typeof customElements !== "undefined" && !customElements.get("ngis-empty-state")) {
    customElements.define("ngis-empty-state", class extends HTMLElement {
      connectedCallback() {
        const icon = this.getAttribute("icon") || "ph-folder-open";
        const title = this.getAttribute("title") || "No Records Available";
        const description = this.getAttribute("description") || "There are no records to display.";
        const actionText = this.getAttribute("action-text") || "";
        const actionHref = this.getAttribute("action-href") || "";
        NGISEmptyState.render(this, { icon, title, description, actionText, actionHref });
      }
    });
  }

  window.NGISEmptyState = NGISEmptyState;
})(window, document);

