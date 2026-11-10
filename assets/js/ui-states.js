/**
 * ============================================================
 * NGIS ERP — Master UI States Engine v1.0
 * Provides all 10 essential UI states across every role portal:
 * 1. Empty State
 * 2. Loading State (Skeletons)
 * 3. Error State
 * 4. Offline State
 * 5. Slow Network State (Measurable progress & anti-duplicate)
 * 6. No Search Results
 * 7. Permission Denied
 * 8. Session Expired (Draft preservation)
 * 9. Form Validation (Inline & Accessible)
 * 10. Success State (Toasts & Confirmations)
 * ============================================================
 */

(function (window, document) {
  "use strict";

  // Prevent multiple initializations
  if (window.NGISUI) return;

  const NGISUI = {
    version: "1.0.0",

    /* ══════════════════════════════════════════════════════════
       1. EMPTY STATE
       ══════════════════════════════════════════════════════════ */
    renderEmptyState(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      const {
        icon = "ph-folder-open",
        title = "No Data Found",
        description = "There are no records to display at this time.",
        actionText = "",
        actionHref = "",
        onAction = null,
        fullWidth = false,
        className = ""
      } = options;

      const iconHtml = icon.startsWith("ph")
        ? `<i class="ph ${icon}"></i>`
        : `<span class="material-symbols-outlined">${icon}</span>`;

      let actionBtnHtml = "";
      if (actionText) {
        if (actionHref) {
          actionBtnHtml = `<a href="${actionHref}" class="ngis-btn-primary"><i class="ph ph-plus"></i><span>${actionText}</span></a>`;
        } else {
          actionBtnHtml = `<button type="button" class="ngis-btn-primary ngis-empty-action-btn"><i class="ph ph-plus"></i><span>${actionText}</span></button>`;
        }
      }

      const card = document.createElement("div");
      card.className = `ngis-state-card ngis-empty-state ${fullWidth ? "full-width" : ""} ${className}`;
      card.innerHTML = `
        <div class="ngis-state-icon neutral">
          ${iconHtml}
        </div>
        <h3 class="ngis-state-title">${title}</h3>
        <p class="ngis-state-desc">${description}</p>
        ${actionBtnHtml ? `<div class="ngis-state-actions">${actionBtnHtml}</div>` : ""}
      `;

      if (onAction && !actionHref) {
        const btn = card.querySelector(".ngis-empty-action-btn");
        if (btn) btn.addEventListener("click", onAction);
      }

      container.innerHTML = "";
      container.appendChild(card);
    },

    /* ══════════════════════════════════════════════════════════
       2. LOADING STATE (SKELETON LOADERS)
       ══════════════════════════════════════════════════════════ */
    showSkeleton(container, type = "list", count = 5) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      container.setAttribute("aria-busy", "true");

      // Save previous content in dataset if not already saved
      if (!container.dataset.ngisPrevContent) {
        container.dataset.ngisPrevContent = container.innerHTML || "";
      }

      if (window.NGISSkeleton && window.NGISSkeleton.templates && window.NGISSkeleton.templates[type]) {
        container.innerHTML = window.NGISSkeleton.templates[type](count);
        return;
      }

      let skeletonHtml = "";
      if (type === "table") {
        const rows = [];
        for (let i = 0; i < count; i++) {
          rows.push(`
            <tr class="ngis-skeleton-pulse ngis-skeleton-row">
              <td style="width: 40px;"><div class="ngis-skeleton-line sm" style="width: 20px;"></div></td>
              <td style="width: 180px;"><div class="ngis-skeleton-line" style="width: ${60 + (i % 3) * 15}%;"></div></td>
              <td><div class="ngis-skeleton-line" style="width: ${40 + (i % 4) * 12}%;"></div></td>
              <td style="width: 120px;"><div class="ngis-skeleton-line sm" style="width: 70px;"></div></td>
              <td style="width: 80px;"><div class="ngis-skeleton-line sm" style="width: 50px;"></div></td>
            </tr>
          `);
        }
        skeletonHtml = `
          <table class="ngis-skeleton-table">
            <tbody>${rows.join("")}</tbody>
          </table>
        `;
      } else if (type === "cards") {
        const cards = [];
        for (let i = 0; i < count; i++) {
          cards.push(`
            <div class="ngis-skeleton-card ngis-skeleton-pulse">
              <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
                <div class="ngis-skeleton-circle" style="width:40px; height:40px;"></div>
                <div style="flex:1;">
                  <div class="ngis-skeleton-line" style="width:65%;"></div>
                  <div class="ngis-skeleton-line sm" style="width:40%; margin-bottom:0;"></div>
                </div>
              </div>
              <div class="ngis-skeleton-line" style="width:90%;"></div>
              <div class="ngis-skeleton-line" style="width:75%; margin-bottom:16px;"></div>
              <div class="ngis-skeleton-line lg" style="width:100%; border-radius:8px;"></div>
            </div>
          `);
        }
        skeletonHtml = `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px;">${cards.join("")}</div>`;
      } else if (type === "stats") {
        const stats = [];
        for (let i = 0; i < count; i++) {
          stats.push(`
            <div class="ngis-skeleton-card ngis-skeleton-pulse" style="display:flex; justify-content:space-between; align-items:center;">
              <div style="flex:1;">
                <div class="ngis-skeleton-line sm" style="width:60px;"></div>
                <div class="ngis-skeleton-line lg" style="width:90px; margin-bottom:0;"></div>
              </div>
              <div class="ngis-skeleton-circle" style="width:44px; height:44px;"></div>
            </div>
          `);
        }
        skeletonHtml = `<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:16px;">${stats.join("")}</div>`;
      } else if (type === "list") {
        const items = [];
        for (let i = 0; i < count; i++) {
          items.push(`
            <div class="ngis-skeleton-pulse" style="display:flex; align-items:center; gap:14px; padding:12px 16px; border-bottom:1px solid #F3F3F5;">
              <div class="ngis-skeleton-circle" style="width:36px; height:36px;"></div>
              <div style="flex:1;">
                <div class="ngis-skeleton-line" style="width:45%;"></div>
                <div class="ngis-skeleton-line sm" style="width:30%; margin-bottom:0;"></div>
              </div>
              <div class="ngis-skeleton-line sm" style="width:50px;"></div>
            </div>
          `);
        }
        skeletonHtml = `<div>${items.join("")}</div>`;
      }

      container.innerHTML = skeletonHtml;
    },

    hideSkeleton(container) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      container.removeAttribute("aria-busy");

      if (container.dataset.ngisPrevContent !== undefined) {
        container.innerHTML = container.dataset.ngisPrevContent;
        delete container.dataset.ngisPrevContent;
      } else {
        container.innerHTML = "";
      }
    },

    /* ══════════════════════════════════════════════════════════
       3. ERROR STATE
       ══════════════════════════════════════════════════════════ */
    renderErrorState(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      if (window.NGISErrorState && typeof window.NGISErrorState.render === "function") {
        window.NGISErrorState.render(container, options);
        return;
      }

      const {
        title = "Unable to Load Data",
        message = "A problem occurred while retrieving information from the server.",
        onRetry = null,
        retryText = "Try Again",
        fullWidth = false,
        className = ""
      } = options;

      const card = document.createElement("div");
      card.className = `ngis-state-card ngis-error-state ${fullWidth ? "full-width" : ""} ${className}`;
      card.innerHTML = `
        <div class="ngis-state-icon error">
          <i class="ph ph-warning-circle"></i>
        </div>
        <h3 class="ngis-state-title">${title}</h3>
        <p class="ngis-state-desc">${message}</p>
        <div class="ngis-state-actions">
          ${onRetry ? `<button type="button" class="ngis-btn-primary ngis-retry-btn ngis-btn-retry"><i class="ph ph-arrow-clockwise"></i><span>${retryText}</span></button>` : ""}
          <button type="button" onclick="window.location.reload()" class="ngis-btn-secondary"><i class="ph ph-arrow-counter-clockwise"></i><span>Reload Page</span></button>
        </div>
      `;

      if (onRetry) {
        const btn = card.querySelector(".ngis-retry-btn");
        if (btn) btn.addEventListener("click", onRetry);
      }

      container.innerHTML = "";
      container.appendChild(card);
    },

    /* ══════════════════════════════════════════════════════════
       4. OFFLINE STATE
       ══════════════════════════════════════════════════════════ */
    initOfflineDetection() {
      let banner = document.getElementById("ngisOfflineBanner");
      if (!banner) {
        banner = document.createElement("div");
        banner.id = "ngisOfflineBanner";
        banner.className = "hidden";
        banner.innerHTML = `
          <div class="ngis-offline-content">
            <span class="ngis-offline-badge"><i class="ph ph-wifi-slash"></i> Offline</span>
            <span>You are currently offline. Changes are saved locally and will sync when connection returns.</span>
          </div>
          <button type="button" onclick="window.NGISUI.checkConnection()" class="ngis-btn-secondary" style="padding:4px 10px; font-size:11.5px; border-color:#E5E5E8;">
            <i class="ph ph-arrows-clockwise"></i> Check
          </button>
        `;
        document.body.prepend(banner);
      }

      const updateOnlineStatus = (evt) => {
        const isOffline = evt?.type === "offline" ? true : evt?.type === "online" ? false : !navigator.onLine;
        if (isOffline) {
          banner.classList.remove("hidden");
          this.toast.warning("Offline Mode Active", "Working with cached local data.");
        } else {
          banner.classList.add("hidden");
          this.toast.success("Back Online", "Internet connection restored. Synchronizing updates...");
        }
      };

      window.addEventListener("online", updateOnlineStatus);
      window.addEventListener("offline", updateOnlineStatus);

      // Initial check
      if (!navigator.onLine) {
        banner.classList.remove("hidden");
      }
    },

    checkConnection() {
      if (navigator.onLine) {
        this.toast.success("Connected", "Internet connection is active.");
        const banner = document.getElementById("ngisOfflineBanner");
        if (banner) banner.classList.add("hidden");
      } else {
        this.toast.warning("Still Offline", "No active internet connection detected.");
      }
    },

    /* ══════════════════════════════════════════════════════════
       5. SLOW NETWORK & DUPLICATE SUBMISSION GUARD
       ══════════════════════════════════════════════════════════ */
    async guardSubmit(button, asyncFn) {
      if (!button || button.disabled || button.getAttribute("aria-busy") === "true") {
        return;
      }

      const originalHtml = button.innerHTML;
      const originalText = button.innerText.trim();
      button.setAttribute("aria-busy", "true");
      button.disabled = true;
      button.classList.add("ngis-btn-submitting");

      // Replace label with neutral loading indicator
      button.innerHTML = `
        <span style="display:inline-block; width:12px; height:12px; border:2px solid currentColor; border-top-color:transparent; border-radius:50%; animation:spin 0.6s linear infinite; vertical-align:middle; margin-right:6px;"></span>
        <span>Processing...</span>
      `;

      // Set slow network fallback notice if operation takes > 3.0s
      let slowTimer = setTimeout(() => {
        if (button.getAttribute("aria-busy") === "true") {
          this.toast.info("Processing Request", "Operation is taking longer than usual. Please wait...");
        }
      }, 3000);

      try {
        const result = await asyncFn();
        return result;
      } catch (err) {
        this.toast.error("Operation Failed", err.message || "An error occurred while saving changes.");
        throw err;
      } finally {
        clearTimeout(slowTimer);
        button.removeAttribute("aria-busy");
        button.disabled = false;
        button.classList.remove("ngis-btn-submitting");
        button.innerHTML = originalHtml;
      }
    },

    // Measurable progress handler (Strictly real progress, no fake percentages)
    trackProgress(progressElement, current, total) {
      if (typeof progressElement === "string") progressElement = document.querySelector(progressElement);
      if (!progressElement || total <= 0) return;

      const pct = Math.min(100, Math.max(0, Math.round((current / total) * 100)));
      progressElement.setAttribute("aria-valuenow", String(pct));
      progressElement.style.width = pct + "%";
      let bar = progressElement.querySelector(".ngis-progress-bar");
      if (!bar) {
        progressElement.className = "ngis-progress-wrap";
        bar = document.createElement("div");
        bar.className = "ngis-progress-bar";
        progressElement.appendChild(bar);
      }
      bar.style.width = pct + "%";
      bar.setAttribute("aria-valuenow", String(pct));
      bar.setAttribute("aria-valuemin", "0");
      bar.setAttribute("aria-valuemax", "100");
    },

    /* ══════════════════════════════════════════════════════════
       6. NO SEARCH RESULTS
       ══════════════════════════════════════════════════════════ */
    renderNoResults(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      const {
        title = "",
        description = "",
        query = "",
        filterCategory = "",
        onClear = null,
        onReset = null,
        clearText = "",
        resetLabel = "",
        fullWidth = false,
        className = ""
      } = options;

      const handler = onReset || onClear;
      const btnLabel = resetLabel || clearText || "Clear Filters & Search";
      const finalTitle = title || ("No matching results" + (query ? ` for &ldquo;${query}&rdquo;` : ""));
      const finalDesc = description || (
        "We couldn&rsquo;t find any records matching your current filter criteria" +
        (filterCategory ? ` in ${filterCategory}` : "") +
        ". Please verify spelling or reset filters to view all entries."
      );

      const card = document.createElement("div");
      card.className = `ngis-state-card ngis-no-results-state ${fullWidth ? "full-width" : ""} ${className}`;
      card.innerHTML = `
        <div class="ngis-state-icon neutral">
          <i class="ph ph-magnifying-glass"></i>
        </div>
        <h3 class="ngis-state-title">${finalTitle}</h3>
        <p class="ngis-state-desc">${finalDesc}</p>
        ${handler ? `
          <div class="ngis-state-actions">
            <button type="button" class="ngis-btn-secondary ngis-clear-filter-btn ngis-btn-reset">
              <i class="ph ph-x-circle"></i>
              <span>${btnLabel}</span>
            </button>
          </div>
        ` : ""}
      `;

      if (handler) {
        const btn = card.querySelector(".ngis-clear-filter-btn");
        if (btn) btn.addEventListener("click", handler);
      }

      container.innerHTML = "";
      container.appendChild(card);
    },

    /* ══════════════════════════════════════════════════════════
       7. PERMISSION DENIED
       ══════════════════════════════════════════════════════════ */
    renderPermissionDenied(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      const {
        title = "Access Restricted",
        reason = "",
        message = "",
        requiredRole = "Administrator",
        currentRole = (window.NGISAuth ? window.NGISAuth.getRole() : "User"),
        returnUrl = ""
      } = options;

      const root = (window.location.pathname.indexOf("/pages/") !== -1) ? "../../" : "";
      const defaultReturn = returnUrl || `${root}pages/${currentRole}/${currentRole}.html`;
      const finalMsg = reason || message || `You are currently authenticated as <strong>${currentRole.toUpperCase()}</strong>. Access to this section requires <strong>${requiredRole}</strong> privileges.`;

      const card = document.createElement("div");
      card.className = "ngis-state-card ngis-denied-state";
      card.innerHTML = `
        <div class="ngis-state-icon permission">
          <i class="ph ph-shield-warning"></i>
        </div>
        <div class="ngis-badge-danger" style="margin-bottom:8px; display:inline-flex; align-items:center; gap:6px; font-size:11px; color:#92243D; background:rgba(239,68,68,0.08); padding:3px 10px; border-radius:999px;">
          <i class="ph ph-lock-key"></i> Restricted Access
        </div>
        <h3 class="ngis-state-title">${title}</h3>
        <p class="ngis-state-desc">${finalMsg}</p>
        <div class="ngis-state-actions">
          <a href="${defaultReturn}" class="ngis-btn-primary">
            <i class="ph ph-arrow-left"></i>
            <span>Return to Dashboard</span>
          </a>
          <button type="button" onclick="if(window.NGISAuth) NGISAuth.logout(); else window.location.href='${root}index.html';" class="ngis-btn-secondary">
            <i class="ph ph-sign-out"></i>
            <span>Switch Account</span>
          </button>
        </div>
      `;

      container.innerHTML = "";
      container.appendChild(card);
    },

    /* ══════════════════════════════════════════════════════════
       8. SESSION EXPIRED (WITH DRAFT PRESERVATION)
       ══════════════════════════════════════════════════════════ */
    saveDraft(formId = "mainForm") {
      const form = typeof formId === "string" ? document.getElementById(formId) : formId;
      if (!form) return;

      const data = {};
      const inputs = form.querySelectorAll("input, select, textarea");
      inputs.forEach(el => {
        if (!el.name && !el.id) return;
        const key = el.name || el.id;
        if (el.type === "checkbox") data[key] = el.checked;
        else if (el.type === "radio") { if (el.checked) data[key] = el.value; }
        else data[key] = el.value;
      });

      try {
        sessionStorage.setItem("ngis_draft_" + window.location.pathname, JSON.stringify(data));
      } catch (e) {}
    },

    restoreDraft(formId = "mainForm") {
      const form = typeof formId === "string" ? document.getElementById(formId) : formId;
      if (!form) return false;

      try {
        const raw = sessionStorage.getItem("ngis_draft_" + window.location.pathname);
        if (!raw) return false;
        const data = JSON.parse(raw);
        Object.keys(data).forEach(key => {
          const el = form.elements[key] || form.querySelector(`[name="${key}"], #${key}`);
          if (!el) return;
          if (el.type === "checkbox") el.checked = Boolean(data[key]);
          else el.value = data[key];
        });
        return true;
      } catch (e) {
        return false;
      }
    },

    showSessionExpiredModal(options = {}) {
      // 1. Preserve drafts from all forms on page
      document.querySelectorAll("form").forEach(f => this.saveDraft(f));

      let modal = document.getElementById("ngisSessionModal");
      if (!modal) {
        modal = document.createElement("div");
        modal.id = "ngisSessionModal";
        modal.className = "ngis-modal-backdrop";
        modal.innerHTML = `
          <div class="ngis-modal-box" role="dialog" aria-modal="true" aria-labelledby="ngisSessionModalTitle">
            <div style="text-align:center; margin-bottom:16px;">
              <div class="ngis-state-icon warning" style="margin:0 auto 12px;">
                <i class="ph ph-lock-key"></i>
              </div>
              <h3 id="ngisSessionModalTitle" class="ngis-state-title">Session Expired</h3>
              <p class="ngis-state-desc" style="margin-bottom:0;">
                Your security session has timed out. Any unsaved form drafts have been safely preserved in your browser.
              </p>
            </div>
            <div style="display:flex; flex-direction:column; gap:8px;">
              <button type="button" id="ngisResumeSessionBtn" class="ngis-btn-primary" style="justify-content:center; width:100%; padding:10px;">
                <i class="ph ph-key"></i>
                <span>Re-authenticate &amp; Restore</span>
              </button>
              <button type="button" onclick="if(window.NGISAuth) NGISAuth.logout(); else window.location.reload();" class="ngis-btn-secondary" style="justify-content:center; width:100%;">
                <span>Sign In with Different Account</span>
              </button>
            </div>
          </div>
        `;
        document.body.appendChild(modal);

        modal.querySelector("#ngisResumeSessionBtn").addEventListener("click", () => {
          if (window.NGISAuth) {
            const role = NGISAuth.getRole() || "teacher";
            NGISAuth.setDemoUser(role);
          }
          modal.classList.add("hidden");
          document.querySelectorAll("form").forEach(f => this.restoreDraft(f));
          this.toast.success("Session Restored", "Your workspace draft was recovered successfully.");
          if (typeof options.onReauth === "function") options.onReauth();
        });
      }

      modal.classList.remove("hidden");
    },

    /* ══════════════════════════════════════════════════════════
       9. FORM VALIDATION (INLINE, ACCESSIBLE, CLEAR ON EDIT)
       ══════════════════════════════════════════════════════════ */
    validateForm(form) {
      if (typeof form === "string") form = document.querySelector(form);
      if (!form) return true;

      let isValid = true;
      let firstInvalid = null;

      const fields = form.querySelectorAll("input:not([type='hidden']):not([type='submit']), select, textarea");
      fields.forEach(field => {
        const error = this.validateField(field);
        if (error) {
          isValid = false;
          if (!firstInvalid) firstInvalid = field;
        }
      });

      if (!isValid && firstInvalid) {
        firstInvalid.focus();
      }

      return isValid;
    },

    validateField(field) {
      if (!field || field.disabled) return null;

      const value = field.value.trim();
      let errorMsg = "";

      // Required validation
      if (field.hasAttribute("required") && !value) {
        const label = this.getFieldLabel(field);
        errorMsg = `${label} is required.`;
      }
      // Email validation
      else if (field.type === "email" && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        errorMsg = "Please enter a valid email address.";
      }
      // Min length
      else if (field.minLength > 0 && value && value.length < field.minLength) {
        errorMsg = `Must be at least ${field.minLength} characters.`;
      }
      // Max value for number
      else if (field.type === "number" && value && field.max && Number(value) > Number(field.max)) {
        errorMsg = `Value cannot exceed ${field.max}.`;
      }
      // Min value for number
      else if (field.type === "number" && value && field.min && Number(value) < Number(field.min)) {
        errorMsg = `Value must be at least ${field.min}.`;
      }

      if (errorMsg) {
        this.setFieldError(field, errorMsg);
        return errorMsg;
      } else {
        this.clearFieldError(field);
        return null;
      }
    },

    setFieldError(field, message) {
      field.classList.add("ngis-input-error");
      field.setAttribute("aria-invalid", "true");

      const errorId = field.id ? `error-${field.id}` : `error-${Math.random().toString(36).slice(2, 7)}`;
      field.setAttribute("aria-describedby", errorId);

      // Check if error message element already exists
      let errorEl = field.parentElement.querySelector(".ngis-field-error");
      if (!errorEl) {
        errorEl = document.createElement("div");
        errorEl.className = "ngis-field-error ngis-field-error-msg";
        errorEl.id = errorId;
        field.parentElement.appendChild(errorEl);
      }
      errorEl.innerHTML = `<i class="ph ph-warning-circle"></i><span>${message}</span>`;

      // Clear immediately when user edits
      const clearOnInput = () => {
        this.clearFieldError(field);
        field.removeEventListener("input", clearOnInput);
        field.removeEventListener("change", clearOnInput);
      };
      field.addEventListener("input", clearOnInput);
      field.addEventListener("change", clearOnInput);
    },

    clearFieldError(field) {
      field.classList.remove("ngis-input-error");
      field.setAttribute("aria-invalid", "false");
      field.removeAttribute("aria-describedby");
      const err = field.parentElement ? field.parentElement.querySelector(".ngis-field-error, .ngis-field-error-msg") : null;
      if (err) err.remove();
    },

    getFieldLabel(field) {
      if (field.id) {
        const labelEl = document.querySelector(`label[for="${field.id}"]`);
        if (labelEl) return labelEl.innerText.replace("*", "").trim();
      }
      return field.getAttribute("placeholder") || field.name || "This field";
    },

    setupInlineValidation(formSelector = "form") {
      document.querySelectorAll(formSelector).forEach(form => {
        form.querySelectorAll("input, select, textarea").forEach(field => {
          field.addEventListener("blur", () => {
            if (field.value.trim() || field.hasAttribute("required")) {
              this.validateField(field);
            }
          });
        });
      });
    },

    /* ══════════════════════════════════════════════════════════
       10. SUCCESS STATE & TOAST ENGINE
       ══════════════════════════════════════════════════════════ */
    toast: {
      getContainer() {
        let container = document.getElementById("ngisToastContainer");
        if (!container) {
          container = document.createElement("div");
          container.id = "ngisToastContainer";
          container.setAttribute("role", "region");
          container.setAttribute("aria-live", "polite");
          document.body.appendChild(container);
        }
        return container;
      },

      show(type, title, detail = "", options = {}) {
        const container = this.getContainer();
        const toast = document.createElement("div");
        toast.className = `ngis-toast ${type} ngis-toast-${type}`;
        toast.setAttribute("role", "alert");

        const icons = {
          success: "ph-check-circle",
          error: "ph-x-circle",
          warning: "ph-warning",
          info: "ph-info"
        };

        const iconClass = icons[type] || "ph-info";

        let actionHtml = "";
        if (options.actionText) {
          actionHtml = `<button type="button" class="ngis-toast-action">${options.actionText}</button>`;
        }

        toast.innerHTML = `
          <i class="ph ${iconClass} ngis-toast-icon"></i>
          <div class="ngis-toast-body">
            <div class="ngis-toast-title">${title}</div>
            ${detail ? `<div class="ngis-toast-detail">${detail}</div>` : ""}
            ${actionHtml}
          </div>
          <button type="button" class="ngis-toast-close" aria-label="Dismiss">&times;</button>
        `;

        if (options.onAction && options.actionText) {
          const actBtn = toast.querySelector(".ngis-toast-action");
          if (actBtn) {
            actBtn.addEventListener("click", () => {
              options.onAction();
              toast.remove();
            });
          }
        }

        const closeBtn = toast.querySelector(".ngis-toast-close");
        closeBtn.addEventListener("click", () => toast.remove());

        container.appendChild(toast);

        // Auto dismiss in 4 seconds unless duration is 0
        const duration = options.duration !== undefined ? options.duration : 4000;
        if (duration > 0) {
          setTimeout(() => {
            if (toast.parentElement) toast.remove();
          }, duration);
        }

        return toast;
      },

      success(title, detail = "", options = {}) {
        return this.show("success", title, detail, options);
      },

      error(title, detail = "", options = {}) {
        return this.show("error", title, detail, options);
      },

      warning(title, detail = "", options = {}) {
        return this.show("warning", title, detail, options);
      },

      info(title, detail = "", options = {}) {
        return this.show("info", title, detail, options);
      }
    },

    /* Rule 2: Honest 1-Tap Confirmation Dialog */
    confirmAction(options = {}) {
      if (window.NGISCancelDialog) {
        return window.NGISCancelDialog.open(options);
      }
      const proceed = window.confirm((options.title || "Confirm Action") + "\n\n" + (options.description || "") + "\n\nWhat happens next: " + (options.consequence || "Changes will be updated safely."));
      if (proceed && typeof options.onConfirm === "function") options.onConfirm();
      else if (!proceed && typeof options.onCancel === "function") options.onCancel();
    },

    /* Rule 1: Dedicated Screen Skeletons */
    showDashboardSkeleton(container) { return this.showSkeleton(container, "dashboard"); },
    showFeedSkeleton(container, count = 3) { return this.showSkeleton(container, "feed", count); },
    showListSkeleton(container, count = 6) { return this.showSkeleton(container, "list", count); },
    showDetailSkeleton(container) { return this.showSkeleton(container, "detail"); },
    showProfileSkeleton(container) { return this.showSkeleton(container, "profile"); },

    /* Global Initialization */
    init() {
      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => {
          this.initOfflineDetection();
          this.setupInlineValidation();
        });
      } else {
        this.initOfflineDetection();
        this.setupInlineValidation();
      }
    }
  };

  // Auto initialize
  NGISUI.init();

  // Export to window
  window.NGISUI = NGISUI;

})(window, document);
