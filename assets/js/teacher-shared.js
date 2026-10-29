/**
 * NGIS Teacher Portal — Shared Application Layer
 * Pure Vanilla JS, robust error handling, honest states, no fake data.
 */

(function (window) {
  "use strict";

  // Prevent multiple instantiations
  if (window.TeacherPortal) return;

  const API_ROOT = "";

  /**
   * Safe HTML Escaper
   */
  function esc(str) {
    if (str === null || str === undefined) return "";
    return String(str).replace(/[&<>"']/g, function (c) {
      return {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
      }[c];
    });
  }

  /**
   * Formatting Utilities
   */
  const format = {
    esc: esc,

    formatDate(dateStr) {
      if (!dateStr) return "—";
      try {
        const d = new Date(dateStr);
        if (isNaN(d.getTime())) return String(dateStr);
        return d.toLocaleDateString("en-GB", {
          weekday: "short",
          day: "numeric",
          month: "short",
          year: "numeric"
        });
      } catch (e) {
        return String(dateStr);
      }
    },

    formatTime(dateStr) {
      if (!dateStr) return "—";
      try {
        const d = new Date(dateStr);
        if (isNaN(d.getTime())) return String(dateStr);
        return d.toLocaleTimeString("en-GB", {
          hour: "2-digit",
          minute: "2-digit"
        });
      } catch (e) {
        return String(dateStr);
      }
    },

    relativeTime(isoStr) {
      if (!isoStr) return "—";
      try {
        const d = new Date(isoStr);
        if (isNaN(d.getTime())) return String(isoStr);
        const now = new Date();
        const diffMs = now - d;
        const diffSecs = Math.floor(diffMs / 1000);
        const diffMins = Math.floor(diffSecs / 60);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffSecs < 60) return "Just now";
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays === 1) return "Yesterday";
        if (diffDays < 7) return `${diffDays}d ago`;
        return d.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
      } catch (e) {
        return String(isoStr);
      }
    },

    formatGrade(score, maxScore) {
      if (score === null || score === undefined || score === "") return "—";
      if (maxScore !== undefined && maxScore !== null) {
        return `${score} / ${maxScore}`;
      }
      return String(score);
    }
  };

  /**
   * Backend API Service
   */
  const api = {
    async getMe() {
      return await window.NGISAuth.api("/api/teacher/me");
    },

    async getClasses() {
      const res = await window.NGISAuth.api("/api/teacher/classes");
      return res.data || [];
    },

    async getClassWorkspace(classId) {
      const res = await window.NGISAuth.api(`/api/teacher/classes/${encodeURIComponent(classId)}/workspace`);
      return res.data || {};
    },

    async getClassStudents(classId) {
      const res = await window.NGISAuth.api(`/api/teacher/classes/${encodeURIComponent(classId)}/students`);
      return res.data || [];
    },

    async getClassSubmissions(classId) {
      const res = await window.NGISAuth.api(`/api/teacher/classes/${encodeURIComponent(classId)}/submissions`);
      return res.data || [];
    },

    async saveAttendance(classId, date, records) {
      // records: [{ student_id, status, notes }]
      return await window.NGISAuth.api("/api/academic/attendance", {
        method: "POST",
        body: JSON.stringify({
          class_id: classId,
          attendance_date: date,
          records: records
        })
      });
    },

    async getAttendanceByClass(classId, date) {
      return await window.NGISAuth.api(`/api/academic/attendance?class_id=${encodeURIComponent(classId)}&date=${encodeURIComponent(date)}`);
    },

    async getGradebook(classId, subjectId, termId) {
      let q = `/api/academic/gradebook?class_id=${encodeURIComponent(classId)}`;
      if (subjectId) q += `&subject_id=${encodeURIComponent(subjectId)}`;
      if (termId) q += `&term_id=${encodeURIComponent(termId)}`;
      const res = await window.NGISAuth.api(q);
      return res.data || {};
    },

    async saveGradebookBatch(batch) {
      // batch: [{ student_id, assessment_id, score, comment }]
      return await window.NGISAuth.api("/api/academic/gradebook/batch", {
        method: "POST",
        body: JSON.stringify({ batch })
      });
    },

    async getExams() {
      const res = await window.NGISAuth.api("/api/teacher/exams");
      return res.data || {};
    },

    async getReports(classId, term) {
      let q = `/api/academic/report-cards?class_id=${encodeURIComponent(classId)}`;
      if (term) q += `&term_id=${encodeURIComponent(term)}`;
      const res = await window.NGISAuth.api(q);
      return res.data || [];
    },

    async gradeSubmission(asgnId, submission) {
      return await window.NGISAuth.api(`/api/assignments/${encodeURIComponent(asgnId)}/grade`, {
        method: "POST",
        body: JSON.stringify(submission)
      });
    }
  };

  /**
   * UI Component Helpers
   */
  const ui = {
    badge(text, kind, icon) {
      kind = kind || "neutral";
      let iconHtml = icon ? `<span class="material-symbols-outlined text-[14px] leading-none">${icon}</span>` : "";
      return `<span class="tp-badge tp-badge-${kind}">${iconHtml}<span>${esc(text)}</span></span>`;
    },

    getAttendanceBadge(status) {
      const s = String(status || "").toLowerCase();
      if (s === "present" || s === "p") {
        return ui.badge("Present", "success", "check");
      }
      if (s === "absent" || s === "a") {
        return ui.badge("Absent", "danger", "close");
      }
      if (s === "late" || s === "l" || s === "tardy") {
        return ui.badge("Late", "warning", "schedule");
      }
      if (s === "excused" || s === "e") {
        return ui.badge("Excused", "neutral", "info");
      }
      return ui.badge("Unrecorded", "neutral", "help");
    },

    getSubmissionBadge(status) {
      const s = String(status || "").toLowerCase();
      if (s === "graded" || s === "reviewed") {
        return ui.badge("Reviewed", "success", "check");
      }
      if (s === "submitted" || s === "needs_review") {
        return ui.badge("Needs review", "warning", "pending");
      }
      if (s === "late") {
        return ui.badge("Late", "danger", "warning");
      }
      if (s === "new") {
        return ui.badge("New", "info", "fiber_new");
      }
      return ui.badge("Not submitted", "neutral", "remove");
    },

    getGradeStatusBadge(status) {
      const s = String(status || "").toLowerCase();
      if (s === "saved") {
        return ui.badge("Saved", "success", "check");
      }
      if (s === "edited") {
        return ui.badge("Edited", "warning", "edit");
      }
      if (s === "invalid") {
        return ui.badge("Invalid", "danger", "error");
      }
      if (s === "saving") {
        return ui.badge("Saving…", "info", "sync");
      }
      return ui.badge("—", "neutral");
    },

    renderEmptyState(container, opts) {
      const icon = opts.icon || "inbox";
      const title = opts.title || "No items found";
      const desc = opts.desc || "There are currently no items to display.";
      const actionText = opts.actionText || "";
      const onAction = opts.onAction || null;

      container.innerHTML = `
        <div class="tp-empty-state">
          <div class="tp-state-icon">
            <span class="material-symbols-outlined">${esc(icon)}</span>
          </div>
          <h3 class="tp-state-title">${esc(title)}</h3>
          <p class="tp-state-desc">${esc(desc)}</p>
          ${actionText ? `<button type="button" class="tp-btn tp-btn-secondary tp-btn-sm" id="emptyStateActionBtn">${esc(actionText)}</button>` : ""}
        </div>
      `;

      if (actionText && onAction) {
        const btn = container.querySelector("#emptyStateActionBtn");
        if (btn) btn.addEventListener("click", onAction);
      }
    },

    renderErrorState(container, opts) {
      const title = opts.title || "Something went wrong";
      const message = opts.message || "We couldn't load the requested data. Check your connection and try again.";
      const onRetry = opts.onRetry || null;

      container.innerHTML = `
        <div class="tp-error-state">
          <div class="tp-state-icon" style="background:#fef2f2;color:#b42332;">
            <span class="material-symbols-outlined">error_outline</span>
          </div>
          <h3 class="tp-state-title">${esc(title)}</h3>
          <p class="tp-state-desc">${esc(message)}</p>
          ${onRetry ? `<button type="button" class="tp-btn tp-btn-primary tp-btn-sm" id="errorStateRetryBtn"><span class="material-symbols-outlined text-[16px]">refresh</span><span>Try again</span></button>` : ""}
        </div>
      `;

      if (onRetry) {
        const btn = container.querySelector("#errorStateRetryBtn");
        if (btn) btn.addEventListener("click", onRetry);
      }
    },

    renderSkeleton(rows = 5, cols = 4) {
      let str = '<div class="p-6 space-y-4">';
      for (let r = 0; r < rows; r++) {
        str += '<div class="flex items-center gap-4">';
        for (let c = 0; c < cols; c++) {
          const w = c === 0 ? "w-24" : c === 1 ? "w-48" : "flex-1";
          str += `<div class="h-6 ${w} tp-skeleton"></div>`;
        }
        str += '</div>';
      }
      str += '</div>';
      return str;
    },

    toast(message, kind = "success") {
      if (typeof window.toast === "function") {
        window.toast(message, kind);
        return;
      }
      let wrap = document.getElementById("toasts");
      if (!wrap) {
        wrap = document.createElement("div");
        wrap.id = "toasts";
        wrap.className = "toast-wrap";
        document.body.appendChild(wrap);
      }
      const icons = { success: "check_circle", error: "error", warning: "warning", info: "info" };
      const t = document.createElement("div");
      t.className = "toast";
      t.setAttribute("role", "alert");
      t.innerHTML = `<span class="material-symbols-outlined">${icons[kind] || "info"}</span><span>${esc(message)}</span>`;
      wrap.appendChild(t);
      setTimeout(() => {
        t.style.opacity = "0";
        t.style.transition = "opacity 0.2s ease";
        setTimeout(() => t.remove(), 250);
      }, kind === "error" ? 6000 : 4000);
    },

    confirm(opts) {
      return new Promise((resolve) => {
        let backdrop = document.getElementById("tpConfirmModal");
        if (!backdrop) {
          backdrop = document.createElement("div");
          backdrop.id = "tpConfirmModal";
          backdrop.className = "tp-modal-backdrop";
          backdrop.innerHTML = `
            <div class="tp-modal" role="dialog" aria-modal="true">
              <div class="tp-modal-header">
                <h3 class="tp-modal-title" id="tpModalTitle">Confirm</h3>
              </div>
              <div class="tp-modal-body" id="tpModalMsg">Are you sure?</div>
              <div class="tp-modal-footer">
                <button type="button" class="tp-btn tp-btn-secondary" id="tpModalCancel">Cancel</button>
                <button type="button" class="tp-btn tp-btn-primary" id="tpModalConfirm">Confirm</button>
              </div>
            </div>
          `;
          document.body.appendChild(backdrop);
        }

        const titleEl = backdrop.querySelector("#tpModalTitle");
        const msgEl = backdrop.querySelector("#tpModalMsg");
        const cancelBtn = backdrop.querySelector("#tpModalCancel");
        const confirmBtn = backdrop.querySelector("#tpModalConfirm");

        titleEl.textContent = opts.title || "Confirm Action";
        msgEl.textContent = opts.message || "Are you sure you want to proceed?";
        cancelBtn.textContent = opts.cancelText || "Cancel";
        confirmBtn.textContent = opts.confirmText || "Confirm";

        if (opts.isDanger) {
          confirmBtn.className = "tp-btn tp-btn-danger";
        } else {
          confirmBtn.className = "tp-btn tp-btn-primary";
        }

        const cleanup = () => {
          backdrop.classList.remove("open");
          document.body.classList.remove("modal-open");
          cancelBtn.onclick = null;
          confirmBtn.onclick = null;
        };

        cancelBtn.onclick = () => {
          cleanup();
          resolve(false);
        };
        confirmBtn.onclick = () => {
          cleanup();
          resolve(true);
        };

        backdrop.classList.add("open");
        document.body.classList.add("modal-open");
        cancelBtn.focus();
      });
    },

    drawer: {
      open(opts) {
        let wrap = document.getElementById("tpDrawerWrap");
        if (!wrap) {
          wrap = document.createElement("div");
          wrap.id = "tpDrawerWrap";
          wrap.className = "tp-drawer-backdrop";
          wrap.innerHTML = `
            <div class="tp-drawer" role="dialog" aria-modal="true">
              <div class="tp-drawer-header">
                <h3 class="text-base font-medium text-slate-900 m-0" id="tpDrawerTitle">Details</h3>
                <button type="button" class="tp-btn tp-btn-subtle tp-btn-sm p-1 min-w-[32px] h-[32px]" id="tpDrawerCloseBtn" aria-label="Close drawer">
                  <span class="material-symbols-outlined text-[20px]">close</span>
                </button>
              </div>
              <div class="tp-drawer-body" id="tpDrawerBody"></div>
              <div class="tp-drawer-footer" id="tpDrawerFooter"></div>
            </div>
          `;
          document.body.appendChild(wrap);
        }

        const titleEl = wrap.querySelector("#tpDrawerTitle");
        const bodyEl = wrap.querySelector("#tpDrawerBody");
        const footEl = wrap.querySelector("#tpDrawerFooter");
        const closeBtn = wrap.querySelector("#tpDrawerCloseBtn");

        titleEl.textContent = opts.title || "Details";
        bodyEl.innerHTML = opts.bodyHtml || "";
        footEl.innerHTML = opts.footerHtml || "";

        const close = () => {
          wrap.classList.remove("open");
          document.body.classList.remove("drawer-open");
          if (opts.onClose) opts.onClose();
        };

        closeBtn.onclick = close;
        wrap.onclick = (e) => {
          if (e.target === wrap) close();
        };

        const onEsc = (e) => {
          if (e.key === "Escape") {
            close();
            document.removeEventListener("keydown", onEsc);
          }
        };
        document.addEventListener("keydown", onEsc);

        wrap.classList.add("open");
        document.body.classList.add("drawer-open");

        if (opts.onRender) opts.onRender(wrap);
        return { close };
      }
    }
  };

  /**
   * Unsaved Changes Protection
   */
  const unsaved = {
    hasChanges: false,
    set(isDirty) {
      unsaved.hasChanges = Boolean(isDirty);
      const indicator = document.getElementById("tpUnsavedIndicator");
      if (indicator) {
        indicator.style.display = unsaved.hasChanges ? "inline-flex" : "none";
      }
      const saveBtn = document.getElementById("tpSaveBtn");
      if (saveBtn && saveBtn.dataset.dirtyControlled) {
        saveBtn.disabled = !unsaved.hasChanges;
      }
    },
    init() {
      window.addEventListener("beforeunload", function (e) {
        if (unsaved.hasChanges) {
          e.preventDefault();
          e.returnValue = "You have unsaved changes. If you leave now, they will be lost.";
          return e.returnValue;
        }
      });
    },
    async guard(nextAction) {
      if (!unsaved.hasChanges) {
        return nextAction();
      }
      const discard = await ui.confirm({
        title: "Unsaved Changes",
        message: "You have unsaved changes. If you leave now, they will be lost.",
        confirmText: "Discard changes",
        cancelText: "Keep editing",
        isDanger: true
      });
      if (discard) {
        unsaved.set(false);
        return nextAction();
      }
    }
  };

  unsaved.init();

  /**
   * Search Debouncer
   */
  function debounce(fn, delay = 260) {
    let t = null;
    return function (...args) {
      if (t) clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  /**
   * Sync active class across tabs and URLs
   */
  function getActiveParamClassId() {
    const params = new URLSearchParams(window.location.search);
    return params.get("classId") || params.get("class") || localStorage.getItem("ngis_teacher_active_class") || "cls-10a";
  }

  function setActiveClassId(classId) {
    if (!classId) return;
    localStorage.setItem("ngis_teacher_active_class", classId);
    const url = new URL(window.location.href);
    url.searchParams.set("classId", classId);
    window.history.replaceState({}, "", url.toString());
  }

  /**
   * Update live review badge in sidebar
   */
  async function refreshReviewBadge() {
    try {
      const classes = await api.getClasses();
      const totalPending = classes.reduce((sum, c) => sum + (c.pendingSubmissions || 0), 0);
      document.querySelectorAll('[data-id="submissions"] .pill, [data-tab="submissions"] .mob-bn-dot').forEach(el => {
        if (totalPending > 0) {
          el.textContent = totalPending > 99 ? "99+" : String(totalPending);
          el.style.display = "";
        } else {
          el.style.display = "none";
        }
      });
    } catch (e) {
      // Ignore background badge errors
    }
  }

  // Refresh review badge on window focus
  window.addEventListener("focus", refreshReviewBadge);
  document.addEventListener("DOMContentLoaded", () => {
    setTimeout(refreshReviewBadge, 500);
  });

  window.TeacherPortal = {
    api,
    ui,
    format,
    unsaved,
    debounce,
    getActiveParamClassId,
    setActiveClassId,
    refreshReviewBadge
  };

})(window);
