/**
 * ============================================================================
 * NGIS ERP — Centralized Status Indicator System
 * Standardized status definitions across 5 base semantic variants:
 * Default (gray), Processing (blue), Success (green), Warning (amber), Error (red).
 * Official Bootstrap Icons, compact 12-13px typography (strict no-bold),
 * flat & badge styling, and GSAP micro-interaction transitions.
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // Escape helper for safe HTML interpolation
  function esc(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ── 1. CANONICAL STATUS REGISTRY (Mapped to 5 Base Semantic Variants) ── */
  var STATUS_DEFINITIONS = {
    // ── Variant 1: DEFAULT (Neutral Gray) ──
    draft: {
      key: "draft",
      label: "Draft",
      variant: "default",
      icon: "pencil",
      color: "gray",
      textClass: "text-slate-600 dark:text-slate-400",
      bgClass: "bg-slate-100 dark:bg-slate-800",
      borderClass: "border-slate-200 dark:border-slate-700",
      tint: "#f1f5f9",
      colorCode: "#64748b"
    },
    not_assigned: {
      key: "not_assigned",
      label: "Not Assigned",
      variant: "default",
      icon: "dash-circle",
      color: "gray",
      textClass: "text-slate-600 dark:text-slate-400",
      bgClass: "bg-slate-100 dark:bg-slate-800",
      borderClass: "border-slate-200 dark:border-slate-700",
      tint: "#f1f5f9",
      colorCode: "#64748b"
    },
    inactive: {
      key: "inactive",
      label: "Inactive",
      variant: "default",
      icon: "pause-circle",
      color: "gray",
      textClass: "text-slate-600 dark:text-slate-400",
      bgClass: "bg-slate-100 dark:bg-slate-800",
      borderClass: "border-slate-200 dark:border-slate-700",
      tint: "#f1f5f9",
      colorCode: "#64748b"
    },
    archived: {
      key: "archived",
      label: "Archived",
      variant: "default",
      icon: "archive",
      color: "gray",
      textClass: "text-slate-600 dark:text-slate-400",
      bgClass: "bg-slate-100 dark:bg-slate-800",
      borderClass: "border-slate-200 dark:border-slate-700",
      tint: "#f1f5f9",
      colorCode: "#64748b"
    },

    // ── Variant 2: PROCESSING (Blue) ──
    processing: {
      key: "processing",
      label: "Processing",
      variant: "processing",
      icon: "arrow-repeat",
      color: "blue",
      textClass: "text-blue-700 dark:text-blue-300",
      bgClass: "bg-blue-50 dark:bg-blue-950/40",
      borderClass: "border-blue-200 dark:border-blue-900",
      tint: "#eff6ff",
      colorCode: "#2563eb"
    },
    in_review: {
      key: "in_review",
      label: "In Review",
      variant: "processing",
      icon: "clock-history",
      color: "blue",
      textClass: "text-blue-700 dark:text-blue-300",
      bgClass: "bg-blue-50 dark:bg-blue-950/40",
      borderClass: "border-blue-200 dark:border-blue-900",
      tint: "#eff6ff",
      colorCode: "#2563eb"
    },
    in_progress: {
      key: "in_progress",
      label: "In Progress",
      variant: "processing",
      icon: "circle-half",
      color: "blue",
      textClass: "text-blue-700 dark:text-blue-300",
      bgClass: "bg-blue-50 dark:bg-blue-950/40",
      borderClass: "border-blue-200 dark:border-blue-900",
      tint: "#eff6ff",
      colorCode: "#2563eb"
    },

    // ── Variant 3: WARNING (Amber) ──
    pending: {
      key: "pending",
      label: "Pending",
      variant: "warning",
      icon: "clock",
      color: "amber",
      textClass: "text-amber-700 dark:text-amber-300",
      bgClass: "bg-amber-50 dark:bg-amber-950/40",
      borderClass: "border-amber-200 dark:border-amber-900",
      tint: "#fffbeb",
      colorCode: "#d97706"
    },
    late: {
      key: "late",
      label: "Late",
      variant: "warning",
      icon: "exclamation-triangle",
      color: "amber",
      textClass: "text-amber-700 dark:text-amber-300",
      bgClass: "bg-amber-50 dark:bg-amber-950/40",
      borderClass: "border-amber-200 dark:border-amber-900",
      tint: "#fffbeb",
      colorCode: "#d97706"
    },
    needs_correction: {
      key: "needs_correction",
      label: "Needs Correction",
      variant: "warning",
      icon: "pencil-square",
      color: "amber",
      textClass: "text-amber-700 dark:text-amber-300",
      bgClass: "bg-amber-50 dark:bg-amber-950/40",
      borderClass: "border-amber-200 dark:border-amber-900",
      tint: "#fffbeb",
      colorCode: "#d97706"
    },
    due_soon: {
      key: "due_soon",
      label: "Due Soon",
      variant: "warning",
      icon: "bell",
      color: "amber",
      textClass: "text-amber-700 dark:text-amber-300",
      bgClass: "bg-amber-50 dark:bg-amber-950/40",
      borderClass: "border-amber-200 dark:border-amber-900",
      tint: "#fffbeb",
      colorCode: "#d97706"
    },

    // ── Variant 4: SUCCESS (Green) ──
    active: {
      key: "active",
      label: "Active",
      variant: "success",
      icon: "circle-fill",
      color: "green",
      textClass: "text-emerald-700 dark:text-emerald-300",
      bgClass: "bg-emerald-50 dark:bg-emerald-950/40",
      borderClass: "border-emerald-200 dark:border-emerald-900",
      tint: "#ecfdf5",
      colorCode: "#059669"
    },
    approved: {
      key: "approved",
      label: "Approved",
      variant: "success",
      icon: "check-circle",
      color: "green",
      textClass: "text-emerald-700 dark:text-emerald-300",
      bgClass: "bg-emerald-50 dark:bg-emerald-950/40",
      borderClass: "border-emerald-200 dark:border-emerald-900",
      tint: "#ecfdf5",
      colorCode: "#059669"
    },
    published: {
      key: "published",
      label: "Published",
      variant: "success",
      icon: "check-circle",
      color: "green",
      textClass: "text-emerald-700 dark:text-emerald-300",
      bgClass: "bg-emerald-50 dark:bg-emerald-950/40",
      borderClass: "border-emerald-200 dark:border-emerald-900",
      tint: "#ecfdf5",
      colorCode: "#059669"
    },
    completed: {
      key: "completed",
      label: "Completed",
      variant: "success",
      icon: "check-circle-fill",
      color: "green",
      textClass: "text-emerald-700 dark:text-emerald-300",
      bgClass: "bg-emerald-50 dark:bg-emerald-950/40",
      borderClass: "border-emerald-200 dark:border-emerald-900",
      tint: "#ecfdf5",
      colorCode: "#059669"
    },
    present: {
      key: "present",
      label: "Present",
      variant: "success",
      icon: "check2-circle",
      color: "green",
      textClass: "text-emerald-700 dark:text-emerald-300",
      bgClass: "bg-emerald-50 dark:bg-emerald-950/40",
      borderClass: "border-emerald-200 dark:border-emerald-900",
      tint: "#ecfdf5",
      colorCode: "#059669"
    },

    // ── Variant 5: ERROR (Red) ──
    rejected: {
      key: "rejected",
      label: "Rejected",
      variant: "error",
      icon: "x-circle",
      color: "red",
      textClass: "text-red-700 dark:text-red-300",
      bgClass: "bg-red-50 dark:bg-red-950/40",
      borderClass: "border-red-200 dark:border-red-900",
      tint: "#fef2f2",
      colorCode: "#dc2626"
    },
    absent: {
      key: "absent",
      label: "Absent",
      variant: "error",
      icon: "x-lg",
      color: "red",
      textClass: "text-red-700 dark:text-red-300",
      bgClass: "bg-red-50 dark:bg-red-950/40",
      borderClass: "border-red-200 dark:border-red-900",
      tint: "#fef2f2",
      colorCode: "#dc2626"
    },
    overdue: {
      key: "overdue",
      label: "Overdue",
      variant: "error",
      icon: "exclamation-circle",
      color: "red",
      textClass: "text-red-700 dark:text-red-300",
      bgClass: "bg-red-50 dark:bg-red-950/40",
      borderClass: "border-red-200 dark:border-red-900",
      tint: "#fef2f2",
      colorCode: "#dc2626"
    },
    restricted: {
      key: "restricted",
      label: "Restricted",
      variant: "error",
      icon: "slash-circle",
      color: "red",
      textClass: "text-red-700 dark:text-red-300",
      bgClass: "bg-red-50 dark:bg-red-950/40",
      borderClass: "border-red-200 dark:border-red-900",
      tint: "#fef2f2",
      colorCode: "#dc2626"
    }
  };

  /* ── 2. BACKEND STATUS ALIAS MAPPER ── */
  var ALIAS_MAP = {
    // Default aliases
    unassigned: "not_assigned",
    "not-assigned": "not_assigned",
    disabled: "inactive",
    paused: "inactive",

    // Processing aliases
    inprogress: "in_progress",
    "in-progress": "in_progress",
    ongoing: "in_progress",
    drafting: "in_progress",
    syncing: "processing",
    updating: "processing",

    // In Review aliases
    inreview: "in_review",
    "in-review": "in_review",
    under_review: "in_review",
    "under-review": "in_review",
    submitted: "in_review",
    awaiting_review: "in_review",

    // Warning aliases
    waiting: "pending",
    queued: "pending",
    needs_action: "needs_correction",
    correction: "needs_correction",
    delayed: "late",
    tardy: "late",
    duesoon: "due_soon",
    "due-soon": "due_soon",
    urgent: "due_soon",
    approaching: "due_soon",

    // Completed aliases
    done: "completed",
    graded: "completed",
    resolved: "completed",
    passed: "completed",

    // Approved aliases
    verified: "approved",
    endorsed: "approved",

    // Published aliases
    released: "published",
    broadcast: "published",

    // Active aliases
    open: "active",
    enabled: "active",
    enrolled: "active",
    online: "active",

    // Present aliases
    here: "present",
    attended: "present",

    // Rejected aliases
    declined: "rejected",
    failed: "rejected",
    dismissed: "rejected",
    unapproved: "rejected",

    // Absent aliases
    missing: "absent",
    truant: "absent",

    // Overdue aliases
    missed: "overdue",
    expired: "overdue",

    // Restricted aliases
    suspended: "restricted",
    blocked: "restricted",
    locked: "restricted",
    frozen: "restricted",

    // Archived aliases
    closed: "archived",
    withdrawn: "archived",
    deleted: "archived",
    historical: "archived"
  };

  /**
   * Resolve a status string to its canonical definition
   */
  function resolveStatus(raw) {
    if (!raw) return STATUS_DEFINITIONS.draft;
    var normalized = String(raw).trim().toLowerCase().replace(/[\s-]+/g, "_");
    if (STATUS_DEFINITIONS[normalized]) {
      return STATUS_DEFINITIONS[normalized];
    }
    var mapped = ALIAS_MAP[normalized] || ALIAS_MAP[String(raw).trim().toLowerCase()];
    if (mapped && STATUS_DEFINITIONS[mapped]) {
      return STATUS_DEFINITIONS[mapped];
    }
    // Default fallback
    return {
      key: normalized,
      label: String(raw).charAt(0).toUpperCase() + String(raw).slice(1),
      variant: "default",
      icon: "circle",
      color: "gray",
      textClass: "text-slate-600 dark:text-slate-400",
      bgClass: "bg-slate-100 dark:bg-slate-800",
      borderClass: "border-slate-200 dark:border-slate-700",
      tint: "#f1f5f9",
      colorCode: "#64748b"
    };
  }

  /**
   * Render HTML for a standardized status indicator
   * @param {string} status - status key e.g. "approved", "pending"
   * @param {Object} [options]
   * @param {string} [options.variant="flat"] - "flat" (default for dense tables) or "badge" (soft tint) or "dot"
   * @param {string} [options.customLabel] - optional custom text override
   * @param {string} [options.extraClass] - optional extra CSS classes
   * @returns {string}
   */
  function renderStatusHtml(status, options) {
    options = options || {};
    var def = resolveStatus(status);
    var label = options.customLabel || def.label;
    var variant = options.variant || "flat";
    var extraClass = options.extraClass || "";

    if (variant === "flat") {
      return (
        '<span class="ngis-status-indicator ngis-status-flat ngis-status--' + def.variant + ' ngis-status--' + def.color + ' ' + esc(extraClass) + '" ' +
              'data-status="' + esc(def.key) + '" data-semantic-variant="' + esc(def.variant) + '">' +
          '<span class="ngis-status-icon" aria-hidden="true" data-ngis-icon="' + esc(def.icon) + '"></span>' +
          '<span class="ngis-status-label">' + esc(label) + '</span>' +
        '</span>'
      );
    }

    if (variant === "dot") {
      return (
        '<span class="ngis-status-indicator ngis-status-dot ngis-status--' + def.variant + ' ngis-status--' + def.color + ' ' + esc(extraClass) + '" ' +
              'data-status="' + esc(def.key) + '" data-semantic-variant="' + esc(def.variant) + '">' +
          '<span class="ngis-status-dot-glyph" aria-hidden="true"></span>' +
          '<span class="ngis-status-label">' + esc(label) + '</span>' +
        '</span>'
      );
    }

    // Badge variant (subtle tinted background)
    return (
      '<span class="ngis-status-indicator ngis-status-badge ngis-status--' + def.variant + ' ngis-status--' + def.color + ' ' + esc(extraClass) + '" ' +
            'data-status="' + esc(def.key) + '" data-semantic-variant="' + esc(def.variant) + '">' +
        '<span class="ngis-status-icon" aria-hidden="true" data-ngis-icon="' + esc(def.icon) + '"></span>' +
        '<span class="ngis-status-label">' + esc(label) + '</span>' +
      '</span>'
    );
  }

  /**
   * Transition an existing status element to a new status with GSAP micro-interaction
   */
  function transitionStatus(element, newStatus, options) {
    if (!element) return;
    options = options || {};
    var def = resolveStatus(newStatus);
    var label = options.customLabel || def.label;
    var variant = options.variant || (element.classList.contains("ngis-status-badge") ? "badge" : "flat");

    // Animate transition with GSAP if available and motion is not reduced
    var prefersReduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (window.gsap && !prefersReduced) {
      window.gsap.to(element, {
        scale: 0.94,
        opacity: 0.5,
        duration: 0.12,
        ease: "power1.in",
        onComplete: function () {
          element.outerHTML = renderStatusHtml(newStatus, { variant: variant, customLabel: label, extraClass: options.extraClass });
          var updatedEl = document.querySelector('[data-status="' + esc(def.key) + '"]');
          if (updatedEl) {
            window.gsap.fromTo(
              updatedEl,
              { scale: 1.06, opacity: 0.7 },
              { scale: 1, opacity: 1, duration: 0.22, ease: "back.out(2)" }
            );
            if (window.NGIS && window.NGIS.hydrateIcons) {
              window.NGIS.hydrateIcons(updatedEl);
            }
          }
        }
      });
    } else {
      element.outerHTML = renderStatusHtml(newStatus, { variant: variant, customLabel: label, extraClass: options.extraClass });
      if (window.NGIS && window.NGIS.hydrateIcons) {
        window.NGIS.hydrateIcons(document.body);
      }
    }
  }

  /* ── 3. EXPORTS ── */
  var NGIS_STATUS = {
    version: "2.0.0",
    definitions: STATUS_DEFINITIONS,
    aliases: ALIAS_MAP,
    resolve: resolveStatus,
    render: renderStatusHtml,
    transition: transitionStatus
  };

  window.NGIS_STATUS = NGIS_STATUS;
  if (!window.NGIS) window.NGIS = {};
  window.NGIS.status = NGIS_STATUS;

  // Hydrate any static markup with data-ngis-status attribute on DOM ready
  function autoHydrate() {
    var targets = document.querySelectorAll("[data-ngis-status]");
    targets.forEach(function (el) {
      var statusKey = el.getAttribute("data-ngis-status");
      var variant = el.getAttribute("data-status-variant") || (el.classList.contains("badge") ? "badge" : "flat");
      var customLabel = el.getAttribute("data-status-label") || el.textContent.trim();
      var rendered = renderStatusHtml(statusKey, { variant: variant, customLabel: customLabel || undefined });
      var temp = document.createElement("div");
      temp.innerHTML = rendered;
      var newEl = temp.firstElementChild;
      if (newEl && el.parentNode) {
        el.parentNode.replaceChild(newEl, el);
        if (window.NGIS && window.NGIS.hydrateIcons) {
          window.NGIS.hydrateIcons(newEl);
        }
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", autoHydrate);
  } else {
    autoHydrate();
  }

})(window, document);
