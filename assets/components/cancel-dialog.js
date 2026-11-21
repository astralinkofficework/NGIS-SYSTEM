/**
 * ============================================================
 * NGIS ERP — Reusable Cancel & Honest Action Dialog (Rule 2 Compliant)
 * Rule 2: No dark patterns. Cancelling/deleting must take one clear
 * action with honest copy.
 * - Shows exactly what happens next in plain language
 * - One confirmation tap at most; no multi-step funnels
 * - Equal visual visibility between confirming and cancelling
 * - Zero guilt/fear copy, zero countdown timers, zero forced steps
 * ============================================================
 */

(function (window, document) {
  "use strict";

  const NGISCancelDialog = {
    modalId: "ngisCancelDialogModal",

    /**
     * Open an honest, 1-tap confirmation dialog
     */
    open(options = {}) {
      if (window.NGIS_UX && typeof window.NGIS_UX.confirm === "function") {
        return window.NGIS_UX.confirm(options);
      }
      const {
        title = "Confirm Action",
        description = "Please confirm that you want to proceed.",
        consequence = "Your data will be updated accordingly.",
        confirmLabel = "Confirm",
        cancelLabel = "Cancel",
        isDestructive = false,
        onConfirm = null,
        onCancel = null
      } = options;

      let modal = document.getElementById(this.modalId);
      if (modal) modal.remove();

      modal = document.createElement("div");
      modal.id = this.modalId;
      modal.className = "ngis-modal-backdrop";
      modal.setAttribute("role", "dialog");
      modal.setAttribute("aria-modal", "true");
      modal.setAttribute("aria-labelledby", "ngisCancelDialogTitle");

      const confirmBtnClass = isDestructive ? "ngis-btn-danger" : "ngis-btn-primary";

      modal.innerHTML = `
        <div class="ngis-modal-box" style="background:var(--token-surface, #FFFFFF); border:1px solid var(--token-border, #E1E9E3); border-radius:14px; max-width:440px; width:92%; padding:24px; box-shadow:0 8px 30px rgba(0,0,0,0.12); margin:auto;">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:40px; height:40px; display:grid; place-items:center; color:${isDestructive ? 'var(--color-danger, #DC2626)' : 'var(--token-primary, #176B45)'}; font-size:20px; flex-shrink:0;">
              <i class="ph ${isDestructive ? 'ph-trash' : 'ph-question'}"></i>
            </div>
            <div>
              <h3 id="ngisCancelDialogTitle" style="font-size:16px; font-weight:500; color:var(--token-text-primary, #29352E); margin:0; line-height:1.2;">
                ${title}
              </h3>
            </div>
          </div>

          <div style="font-size:13.5px; color:var(--token-text-secondary, #555555); line-height:1.55; margin-bottom:16px;">
            <p style="margin:0 0 10px 0;">${description}</p>
            <div style="background:var(--token-canvas, #F7F9F7); border:1px solid var(--token-border, #E1E9E3); border-radius:8px; padding:10px 12px; font-size:12.5px; color:var(--token-text-primary, #29352E);">
              <span style="font-weight:500;">What happens next:</span> ${consequence}
            </div>
          </div>

          <div style="display:flex; gap:10px; justify-content:flex-end; align-items:center;">
            <button type="button" id="ngisDialogCancelBtn" class="ngis-btn-secondary" style="min-height:44px; padding:0 18px; border-radius:10px; font-size:13px; font-weight:500; cursor:pointer; background:var(--token-surface, #FFFFFF); border:1px solid var(--token-border, #E1E9E3); color:var(--token-text-primary, #29352E);">
              ${cancelLabel}
            </button>
            <button type="button" id="ngisDialogConfirmBtn" class="${confirmBtnClass}" style="min-height:44px; padding:0 20px; border-radius:10px; font-size:13px; font-weight:500; cursor:pointer; background:${isDestructive ? 'var(--color-danger, #DC2626)' : 'var(--token-primary, #176B45)'}; color:#FFFFFF; border:1px solid ${isDestructive ? 'var(--color-danger, #DC2626)' : 'var(--token-primary, #176B45)'};">
              ${confirmLabel}
            </button>
          </div>
        </div>
      `;

      if (window.NGIS_MODAL && typeof window.NGIS_MODAL.open === "function") {
        window.NGIS_MODAL.open(modal, { disableEsc: false });
      } else {
        document.body.appendChild(modal);
        document.body.classList.add("ngis-modal-open");
      }

      const cleanup = () => {
        if (window.NGIS_MODAL && typeof window.NGIS_MODAL.close === "function") {
          window.NGIS_MODAL.close(modal, true);
        } else {
          if (modal && modal.parentElement) modal.remove();
          document.body.classList.remove("ngis-modal-open");
        }
        document.removeEventListener("keydown", handleKey);
      };

      const handleKey = (e) => {
        if (e.key === "Escape") {
          cleanup();
          if (typeof onCancel === "function") onCancel();
        }
      };
      document.addEventListener("keydown", handleKey);

      modal.querySelector("#ngisDialogCancelBtn").addEventListener("click", () => {
        cleanup();
        if (typeof onCancel === "function") onCancel();
      });

      modal.querySelector("#ngisDialogConfirmBtn").addEventListener("click", () => {
        cleanup();
        if (typeof onConfirm === "function") onConfirm();
      });
    }
  };

  window.NGISCancelDialog = NGISCancelDialog;
})(window, document);

