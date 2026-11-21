/**
 * ============================================================================
 * NGIS ERP — Global Empty States & Data State System
 * Standardized empty table states, contextual messaging, role-aware CTAs,
 * search empty states, missing cell values, error recovery, and GSAP motion.
 * Conforms strictly to NGIS System Guidelines (no bold, 60-30-10 palette, 44px touch targets).
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // Prevent multiple initializations
  if (window.NGIS_EMPTY) return;

  function esc(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ── 1. ROLE RESOLUTION ── */
  function getAuthRole() {
    try {
      if (window.PAGE && window.PAGE.role) return String(window.PAGE.role).toLowerCase();
      var raw = localStorage.getItem("ngis_user") || localStorage.getItem("auth_user");
      if (raw) {
        var u = JSON.parse(raw);
        if (u && (u.portal || u.role)) return String(u.portal || u.role).toLowerCase();
      }
      var bodyRole = document.body.getAttribute("data-role") || document.body.getAttribute("data-portal");
      if (bodyRole) return String(bodyRole).toLowerCase();
    } catch (e) {}
    return "student";
  }

  function userHasPermission(allowedRoles) {
    if (!allowedRoles || !allowedRoles.length) return false;
    var currentRole = getAuthRole();
    if (currentRole === "super_admin") currentRole = "superadmin";
    if (currentRole === "editor") currentRole = "admin";

    // Students must NEVER see administrative creation or upload controls
    if (currentRole === "student" && allowedRoles.indexOf("student") === -1) {
      return false;
    }
    return allowedRoles.some(function (r) {
      var nr = String(r).toLowerCase();
      if (nr === "super_admin") nr = "superadmin";
      if (nr === "editor") nr = "admin";
      return nr === currentRole;
    });
  }

  /* ── 2. MINIMAL MONOCHROME SVG ILLUSTRATIONS ── */
  var SVG_FILING_CABINET =
    '<svg class="ngis-empty-illustration-svg" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<!-- Outer Cabinet Frame -->' +
      '<rect x="26" y="20" width="68" height="80" rx="4" class="text-slate-300 dark:text-slate-700" stroke="currentColor" fill="none"/>' +
      '<!-- Upper Drawer -->' +
      '<line x1="26" y1="52" x2="94" y2="52" class="text-slate-300 dark:text-slate-700" stroke="currentColor"/>' +
      '<rect x="52" y="32" width="16" height="5" rx="1.5" class="text-slate-400 dark:text-slate-600" stroke="currentColor" fill="none"/>' +
      '<line x1="44" y1="42" x2="76" y2="42" stroke-dasharray="2 3" class="text-slate-300 dark:text-slate-700" stroke="currentColor"/>' +
      '<!-- Lower Drawer Pulled-Out Perspective -->' +
      '<path d="M 22 76 L 36 60 L 84 60 L 98 76 Z" class="text-slate-100 dark:text-slate-800" fill="currentColor" stroke="none"/>' +
      '<path d="M 22 76 L 36 60 L 84 60 L 98 76 Z" class="text-slate-400 dark:text-slate-500" stroke="currentColor" fill="none"/>' +
      '<rect x="22" y="76" width="76" height="24" rx="3" class="text-slate-400 dark:text-slate-500" stroke="currentColor" fill="none"/>' +
      '<rect x="52" y="85" width="16" height="5" rx="1.5" class="text-slate-400 dark:text-slate-500" stroke="currentColor" fill="none"/>' +
      '<!-- Clean Empty Folder Tab Outlines -->' +
      '<path d="M 42 66 L 46 60 L 58 60 L 62 66" class="text-slate-400 dark:text-slate-600" stroke="currentColor" fill="none"/>' +
      '<line x1="38" y1="71" x2="82" y2="71" stroke-dasharray="3 3" class="text-slate-300 dark:text-slate-600" stroke="currentColor"/>' +
    '</svg>';

  var SVG_NO_SEARCH =
    '<svg class="ngis-empty-illustration-svg" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<circle cx="44" cy="44" r="24" class="text-slate-300 dark:text-slate-600" stroke="currentColor" fill="none"/>' +
      '<line x1="62" y1="62" x2="78" y2="78" class="text-slate-400 dark:text-slate-500" stroke="currentColor" stroke-width="2"/>' +
      '<path d="M 36 44 A 8 8 0 0 1 44 36" class="text-slate-400 dark:text-slate-500" stroke="currentColor"/>' +
      '<line x1="22" y1="78" x2="32" y2="78" stroke-dasharray="2 3" class="text-slate-300 dark:text-slate-700" stroke="currentColor"/>' +
      '<line x1="68" y1="24" x2="76" y2="24" stroke-dasharray="2 3" class="text-slate-300 dark:text-slate-700" stroke="currentColor"/>' +
    '</svg>';

  var SVG_ERROR_FAILED =
    '<svg class="ngis-empty-illustration-svg" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<rect x="20" y="24" width="56" height="48" rx="6" class="text-slate-300 dark:text-slate-700" stroke="currentColor" fill="none"/>' +
      '<line x1="20" y1="44" x2="76" y2="44" class="text-slate-300 dark:text-slate-700" stroke="currentColor"/>' +
      '<circle cx="32" cy="34" r="2.5" class="text-slate-400 dark:text-slate-500" fill="currentColor"/>' +
      '<circle cx="42" cy="34" r="2.5" class="text-slate-400 dark:text-slate-500" fill="currentColor"/>' +
      '<line x1="48" y1="52" x2="48" y2="60" class="text-rose-500" stroke="currentColor" stroke-width="2"/>' +
      '<circle cx="48" cy="65" r="1.2" class="text-rose-500" fill="currentColor"/>' +
    '</svg>';

  var SVG_RESTRICTED =
    '<svg class="ngis-empty-illustration-svg" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M 48 18 L 74 28 C 74 54 58 68 48 76 C 38 68 22 54 22 28 Z" class="text-slate-300 dark:text-slate-700" stroke="currentColor" fill="none"/>' +
      '<rect x="40" y="42" width="16" height="14" rx="2" class="text-slate-400 dark:text-slate-500" stroke="currentColor" fill="none"/>' +
      '<path d="M 44 42 V 37 A 4 4 0 0 1 52 37 V 42" class="text-slate-400 dark:text-slate-500" stroke="currentColor" fill="none"/>' +
    '</svg>';

  /* ── 3. CONTEXTUAL REGISTRY ── */
  var CONTEXTUAL_STATES = {
    students: {
      heading: "No students yet",
      description: "There are currently no student accounts registered in this cohort or filter.",
      actionText: "Add Student",
      actionPermission: ["admin", "superadmin", "principal"],
      actionEvent: "add-student",
      actionHref: "admin-students.html?action=new"
    },
    teachers: {
      heading: "No teachers yet",
      description: "There are currently no faculty members assigned to this department or campus.",
      actionText: "Add Teacher",
      actionPermission: ["admin", "superadmin", "principal"],
      actionEvent: "add-teacher",
      actionHref: "admin-teachers.html?action=new"
    },
    attendance: {
      heading: "No attendance records",
      description: "Attendance has not been recorded yet for the selected class and date range.",
      actionText: "Record Attendance",
      actionPermission: ["teacher", "admin", "principal"],
      actionEvent: "record-attendance"
    },
    assignments: {
      heading: "No assignments yet",
      description: "No coursework or homework assignments have been scheduled for this class.",
      actionText: "Create Assignment",
      actionPermission: ["teacher", "admin"],
      actionEvent: "create-assignment"
    },
    lessons: {
      heading: "No lessons available",
      description: "Lesson plans and syllabus modules have not been uploaded for this term.",
      actionText: "Upload Lesson",
      actionPermission: ["teacher", "admin", "principal"],
      actionEvent: "upload-lesson"
    },
    exams: {
      heading: "No upcoming exams",
      description: "No examination schedules or assessment notices are queued for this evaluation period.",
      actionText: "Create Exam Notice",
      actionPermission: ["teacher", "principal", "admin"],
      actionEvent: "create-exam"
    },
    reports: {
      heading: "No reports available",
      description: "Academic reports and term performance summaries have not been published yet.",
      actionText: "Upload Report",
      actionPermission: ["teacher", "principal", "admin"],
      actionEvent: "upload-report"
    },
    announcements: {
      heading: "No announcements yet",
      description: "Important school notices, news bulletins, and campus alerts will appear here.",
      actionText: "Create Announcement",
      actionPermission: ["admin", "principal", "superadmin"],
      actionEvent: "create-announcement"
    },
    timetable: {
      heading: "No timetable available",
      description: "Master schedules and room allocations have not been uploaded for this semester.",
      actionText: "Upload Timetable",
      actionPermission: ["admin", "principal", "superadmin"],
      actionEvent: "upload-timetable"
    },
    services: {
      heading: "No service requests",
      description: "No maintenance, IT, or facility assistance requests are currently active.",
      actionText: "Create Request",
      actionPermission: ["student", "teacher", "principal", "admin", "superadmin"],
      actionEvent: "create-request"
    },
    lost_found: {
      heading: "No items reported",
      description: "No lost or found personal belongings are currently registered on campus.",
      actionText: "Report Item",
      actionPermission: ["student", "teacher", "principal", "admin", "superadmin"],
      actionEvent: "report-item"
    },
    notifications: {
      heading: "You\u2019re all caught up",
      description: "There are no unread system notifications or pending action items.",
      actionText: null
    },
    security_events: {
      heading: "No security events recorded",
      description: "Authentication checkpoints, access logs, and security monitors report zero anomalies.",
      actionText: null
    },
    audit_logs: {
      heading: "No activity recorded",
      description: "No administrative operations or data modifications were logged during this window.",
      actionText: null
    },
    classes: {
      heading: "No classes found",
      description: "No class cohorts or course sections are currently active.",
      actionText: "Create Class",
      actionPermission: ["admin", "principal", "superadmin"],
      actionEvent: "create-class"
    },
    departments: {
      heading: "No departments available",
      description: "Academic departments and faculty divisions will appear here.",
      actionText: "Add Department",
      actionPermission: ["admin", "principal", "superadmin"],
      actionEvent: "add-department"
    },
    generic: {
      heading: "No records available",
      description: "There are currently no items to display in this view.",
      actionText: null
    }
  };

  /* ── 4. MOTION & GSAP INTEGRATION ── */
  function animateEntrance(element) {
    if (!element) return;
    try {
      if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        element.style.opacity = "1";
        return;
      }
      if (window.gsap && typeof window.gsap.fromTo === "function") {
        window.gsap.fromTo(
          element,
          { opacity: 0, y: 8 },
          { opacity: 1, y: 0, duration: 0.28, ease: "power2.out", clearProps: "transform" }
        );
      } else {
        element.style.opacity = "1";
      }
    } catch (e) {
      element.style.opacity = "1";
    }
  }

  /* ── 5. CORE BUILDERS ── */
  function buildEmptyHtml(options) {
    var opts = options || {};
    var heading = opts.heading || "No records available";
    var description = opts.description || "There are no items to display.";
    var illustration = opts.illustration || SVG_FILING_CABINET;
    var actionText = opts.actionText || "";
    var actionHref = opts.actionHref || "";
    var actionPermission = opts.actionPermission || [];
    var actionEvent = opts.actionEvent || "";
    var actionClass = opts.actionClass || "ngis-empty-action-primary";
    var actionIcon = opts.actionIcon || "plus";

    // Permission Check
    var showAction = Boolean(actionText);
    if (showAction && actionPermission && actionPermission.length > 0) {
      showAction = userHasPermission(actionPermission);
    }

    var actionHtml = "";
    if (showAction) {
      var iconGlyph = '<svg class="w-4 h-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2z"/></svg>';
      if (actionIcon === "arrow-clockwise") {
        iconGlyph = '<svg class="w-4 h-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/><path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/></svg>';
      } else if (actionIcon === "x-circle") {
        iconGlyph = '<svg class="w-4 h-4" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/></svg>';
      }

      if (actionHref) {
        actionHtml =
          '<div class="ngis-empty-actions">' +
            '<a href="' + esc(actionHref) + '" class="ngis-empty-btn ' + esc(actionClass) + '" role="button">' +
              iconGlyph +
              '<span>' + esc(actionText) + '</span>' +
            '</a>' +
          '</div>';
      } else {
        actionHtml =
          '<div class="ngis-empty-actions">' +
            '<button type="button" class="ngis-empty-btn ' + esc(actionClass) + '"' +
              (actionEvent ? ' data-action="' + esc(actionEvent) + '"' : "") + '>' +
              iconGlyph +
              '<span>' + esc(actionText) + '</span>' +
            '</button>' +
          '</div>';
      }
    }

    return (
      '<div class="ngis-empty-state-wrap" role="status" aria-live="polite">' +
        '<div class="ngis-empty-illustration">' + illustration + '</div>' +
        '<h3 class="ngis-empty-heading">' + esc(heading) + '</h3>' +
        '<p class="ngis-empty-desc">' + esc(description) + '</p>' +
        actionHtml +
      '</div>'
    );
  }

  function resolveOptions(contextKeyOrOpts) {
    if (typeof contextKeyOrOpts === "string") {
      var entry = CONTEXTUAL_STATES[contextKeyOrOpts] || CONTEXTUAL_STATES.generic;
      return Object.assign({}, entry);
    }
    if (typeof contextKeyOrOpts === "object" && contextKeyOrOpts !== null) {
      var key = contextKeyOrOpts.key || contextKeyOrOpts.type || "";
      var base = key && CONTEXTUAL_STATES[key] ? CONTEXTUAL_STATES[key] : {};
      return Object.assign({}, base, contextKeyOrOpts);
    }
    return Object.assign({}, CONTEXTUAL_STATES.generic);
  }

  function getColspan(target) {
    if (!target) return 6;
    var table = target.tagName === "TABLE" ? target : target.closest("table");
    if (!table) return 6;
    var ths = table.querySelectorAll("thead tr th, thead tr td");
    if (ths.length > 0) return ths.length;
    var headerRow = table.querySelector("thead tr");
    if (headerRow && headerRow.children.length > 0) return headerRow.children.length;
    return 6;
  }

  /* ── 6. PUBLIC API ── */
  var NGIS_EMPTY = {
    version: "2.0.0",

    /* Contextual config dictionary */
    contexts: CONTEXTUAL_STATES,

    /* SVGs dictionary */
    svgs: {
      filingCabinet: SVG_FILING_CABINET,
      noSearch: SVG_NO_SEARCH,
      errorFailed: SVG_ERROR_FAILED,
      restricted: SVG_RESTRICTED
    },

    /**
     * Build HTML string for empty state
     */
    buildHtml: function (contextKeyOrOpts) {
      var opts = resolveOptions(contextKeyOrOpts);
      return buildEmptyHtml(opts);
    },

    /**
     * Build HTML string for an empty table row (<tr class="ngis-empty-row"><td colspan="X">...</td></tr>)
     */
    buildTableRow: function (colspan, contextKeyOrOpts) {
      var html = NGIS_EMPTY.buildHtml(contextKeyOrOpts);
      return '<tr class="ngis-empty-row"><td colspan="' + (colspan || 6) + '" class="ngis-empty-cell">' + html + '</td></tr>';
    },

    /**
     * Render contextual empty state into a table, tbody, or container.
     */
    render: function (container, contextKeyOrOpts) {
      var el = typeof container === "string" ? document.querySelector(container) : container;
      if (!el) return;

      var opts = resolveOptions(contextKeyOrOpts);
      var html = buildEmptyHtml(opts);

      var isTable = el.tagName === "TABLE";
      var isTbody = el.tagName === "TBODY";

      if (isTable || isTbody) {
        var tbody = isTable ? el.querySelector("tbody") || el : el;
        var cols = opts.colspan || getColspan(el);
        tbody.innerHTML =
          '<tr class="ngis-empty-row">' +
            '<td colspan="' + cols + '" class="ngis-empty-cell">' +
              html +
            '</td>' +
          '</tr>';
        animateEntrance(tbody.querySelector(".ngis-empty-state-wrap"));
        if (opts.onAction) {
          var btn = tbody.querySelector(".ngis-empty-btn");
          if (btn) btn.addEventListener("click", opts.onAction);
        }
      } else {
        el.innerHTML = html;
        animateEntrance(el.querySelector(".ngis-empty-state-wrap"));
        if (opts.onAction) {
          var btnEl = el.querySelector(".ngis-empty-btn");
          if (btnEl) btnEl.addEventListener("click", opts.onAction);
        }
      }
    },

    /**
     * Render No Search Results State.
     */
    renderNoResults: function (container, options) {
      var o = options || {};
      var opts = {
        heading: o.heading || "No matching results",
        description: o.description || "We couldn\u2019t find anything matching your filters or search terms. Try resetting or adjusting your criteria.",
        illustration: SVG_NO_SEARCH,
        actionText: o.actionText || "Clear Filters",
        actionPermission: ["student", "teacher", "principal", "admin", "superadmin"],
        actionEvent: o.actionEvent || "clear-filters",
        actionClass: "ngis-empty-btn-secondary",
        actionIcon: "x-circle",
        colspan: o.colspan,
        onAction: o.onAction
      };
      NGIS_EMPTY.render(container, opts);
    },

    /**
     * Render Request Failed / Network Error State.
     */
    renderError: function (container, options) {
      var o = options || {};
      var opts = {
        heading: o.heading || "Unable to load records",
        description: o.description || "A network error or server interruption occurred while fetching this data.",
        illustration: SVG_ERROR_FAILED,
        actionText: o.actionText || "Retry",
        actionPermission: ["student", "teacher", "principal", "admin", "superadmin"],
        actionEvent: o.actionEvent || "retry",
        actionClass: "ngis-empty-btn-secondary",
        actionIcon: "arrow-clockwise",
        colspan: o.colspan,
        onAction: o.onAction
      };
      NGIS_EMPTY.render(container, opts);
    },

    /**
     * Render Permission Restricted State.
     */
    renderRestricted: function (container, options) {
      var o = options || {};
      var opts = {
        heading: o.heading || "Access restricted",
        description: o.description || "You do not have the required permissions to view this section or dataset.",
        illustration: SVG_RESTRICTED,
        actionText: null,
        colspan: o.colspan
      };
      NGIS_EMPTY.render(container, opts);
    },

    /**
     * Render Skeletons in a Table.
     */
    renderSkeleton: function (container, options) {
      var el = typeof container === "string" ? document.querySelector(container) : container;
      if (!el) return;
      var o = options || {};
      var cols = o.cols || getColspan(el);
      var rows = Math.max(3, Number(o.rows || 5));

      var isTable = el.tagName === "TABLE";
      var isTbody = el.tagName === "TBODY";

      if (isTable || isTbody) {
        var tbody = isTable ? el.querySelector("tbody") || el : el;
        var rowsHtml = "";
        for (var i = 0; i < rows; i++) {
          rowsHtml += '<tr class="ngis-skeleton-row animate-pulse">';
          for (var c = 0; c < cols; c++) {
            var width = c === 0 ? "70%" : c === cols - 1 ? "40%" : "60%";
            rowsHtml +=
              '<td class="px-4 py-3.5 border-b border-slate-100 dark:border-slate-800">' +
                '<span class="inline-block bg-slate-200 dark:bg-slate-700 rounded h-3.5" style="width:' + width + ';"></span>' +
              '</td>';
          }
          rowsHtml += "</tr>";
        }
        tbody.innerHTML = rowsHtml;
      } else {
        if (window.NGIS_SKELETON && typeof window.NGIS_SKELETON.table === "function") {
          el.innerHTML = window.NGIS_SKELETON.table({ rows: rows, cols: cols });
        }
      }
    },

    /**
     * Missing Individual Table Values Formatter.
     * Distinguishes entirely empty table from records with missing values.
     * Prevents undefined, null, NaN, or broken placeholders.
     * Preserves valid numeric 0!
     */
    cellValue: function (val, type) {
      // Preserve numeric zero!
      if (val === 0 || val === "0") return "0";

      // If value is present, return escaped
      if (val != null && String(val).trim() !== "" && !Number.isNaN(val)) {
        return esc(val);
      }

      // Contextual missing values
      if (type === "assignment") {
        return '<span class="ngis-missing-val" title="Not assigned">Not assigned</span>';
      }
      if (type === "document") {
        return '<span class="ngis-missing-val" title="Not uploaded">Not uploaded</span>';
      }
      if (type === "personal") {
        return '<span class="ngis-missing-val" title="Not provided">Not provided</span>';
      }
      // Neutral em dash fallback
      return '<span class="ngis-missing-dash text-slate-400 dark:text-slate-500" aria-label="Not available">&mdash;</span>';
    }
  };

  /* ── 7. BACKWARDS COMPATIBILITY WRAPPERS ── */
  window.NGIS_EMPTY = NGIS_EMPTY;
  if (!window.NGIS) window.NGIS = {};
  window.NGIS.empty = NGIS_EMPTY;
  window.NGIS.cellValue = NGIS_EMPTY.cellValue;

  // Legacy NGISEmptyState wrapper
  window.NGISEmptyState = {
    render: function (container, options) {
      var o = options || {};
      NGIS_EMPTY.render(container, {
        heading: o.title || o.heading,
        description: o.description,
        actionText: o.actionText,
        actionHref: o.actionHref,
        onAction: o.onAction,
        colspan: o.colspan
      });
    }
  };

  // Wire into NGISUI if present or create mock
  if (!window.NGISUI) window.NGISUI = {};
  window.NGISUI.renderEmptyState = function (container, options) {
    NGIS_EMPTY.render(container, options);
  };
  window.NGISUI.renderNoResults = function (container, options) {
    NGIS_EMPTY.renderNoResults(container, options);
  };
  window.NGISUI.renderErrorState = function (container, options) {
    NGIS_EMPTY.renderError(container, options);
  };
  window.NGISUI.renderPermissionDenied = function (container, options) {
    NGIS_EMPTY.renderRestricted(container, options);
  };

  // Custom Web Component: <ngis-empty-state context="..." heading="..." description="..."></ngis-empty-state>
  if (typeof customElements !== "undefined" && !customElements.get("ngis-empty-state")) {
    customElements.define(
      "ngis-empty-state",
      class extends HTMLElement {
        connectedCallback() {
          var context = this.getAttribute("context") || this.getAttribute("type") || "generic";
          var heading = this.getAttribute("heading") || this.getAttribute("title");
          var description = this.getAttribute("description");
          var actionText = this.getAttribute("action-text");
          var actionHref = this.getAttribute("action-href");
          var opts = { actionHref: actionHref };
          if (heading) opts.heading = heading;
          if (description) opts.description = description;
          if (actionText) opts.actionText = actionText;
          NGIS_EMPTY.render(this, Object.assign({}, NGIS_EMPTY.contexts[context] || {}, opts));
        }
      }
    );
  }

})(window, document);
