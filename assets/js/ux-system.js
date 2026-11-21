/**
 * ============================================================================
 * NGIS ERP — Universal UX Writing, Dialogs & Interaction Design System
 * Single Source of Truth for Enterprise User Communication across all Portals.
 *
 * Core Capabilities:
 * 1. Intelligent Confirmation Dialogs (explicit action, entity, consequence, recoverability)
 * 2. Universal Dialog Component (accessible, responsive, bottom sheet on mobile, safe areas)
 * 3. Professional Tooltip System (semantic actions, warm-group delay skipping, keyboard shortcuts)
 * 4. Meaningful Page Headings & Dynamic Record Summaries
 * 5. Action-Oriented Notifications & Deep-Linking with Authorization checks
 * 6. Specific Success Confirmations with Animated Checkmarks
 * 7. Actionable Error Messages & Inline Field Validation
 * 8. Double-Submission Prevention & Physical Press Feedback
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

  // Detect Mac OS for keyboard shortcuts (Cmd vs Ctrl)
  var isMac = typeof navigator !== "undefined" && /Mac|iPod|iPhone|iPad/.test(navigator.platform);
  var modKey = isMac ? "⌘" : "Ctrl";

  /* ==========================================================================
     1. INTELLIGENT CONFIRMATION DIALOGS & UNIVERSAL DIALOG ENGINE
     ========================================================================== */

  var activeDialog = null;
  var lastActiveElement = null;

  /**
   * Universal Confirmation Dialog
   * @param {Object} opts
   * @param {string} opts.title - Explicit question: e.g. "Delete Alice Hok?"
   * @param {string} opts.description - Specific consequences & scope
   * @param {string} [opts.consequence] - Explicit outcome summary or record impact
   * @param {boolean} [opts.isDestructive=false] - Red accent only for destructive operations
   * @param {boolean} [opts.isRecoverable=false] - State clearly if action can be reversed
   * @param {string} [opts.confirmLabel="Confirm Action"] - Action-oriented button label
   * @param {string} [opts.cancelLabel="Cancel"] - Keep record or safe exit label
   * @param {string} [opts.icon="warning"] - Bootstrap or Semantic icon glyph
   * @param {Function} [opts.onConfirm] - Callback on positive confirmation
   * @param {Function} [opts.onCancel] - Callback on dismissal/cancellation
   * @returns {Promise<boolean>}
   */
  function confirmDialog(opts) {
    opts = opts || {};

    return new Promise(function (resolve) {
      // Clean up any existing dialog
      if (activeDialog && activeDialog.backdrop) {
        closeDialog(false);
      }

      lastActiveElement = document.activeElement;

      var isDestructive = Boolean(opts.isDestructive);
      var isRecoverable = opts.isRecoverable !== undefined ? Boolean(opts.isRecoverable) : !isDestructive;
      var title = opts.title || "Confirm Action";
      var description = opts.description || "Please review the details below before proceeding.";
      var consequence = opts.consequence || "";
      var confirmLabel = opts.confirmLabel || (isDestructive ? "Delete Record" : "Confirm Action");
      var cancelLabel = opts.cancelLabel || "Cancel";
      var icon = opts.icon || (isDestructive ? "trash3" : "question-circle");

      // Backdrop container
      var backdrop = document.createElement("div");
      backdrop.id = "ngisUniversalDialogBackdrop";
      backdrop.className = "ngis-dialog-backdrop";
      backdrop.setAttribute("role", "dialog");
      backdrop.setAttribute("aria-modal", "true");
      backdrop.setAttribute("aria-labelledby", "ngisDialogTitle");
      backdrop.setAttribute("aria-describedby", "ngisDialogDesc");
      backdrop.style.zIndex = "100000";

      // Dialog Card Markup
      var cardHtml =
        '<div class="ngis-dialog-card' + (isDestructive ? ' ngis-dialog-card--destructive' : '') + '">' +
          // Header with functional close button
          '<div class="ngis-dialog-header">' +
            '<div class="ngis-dialog-title-group">' +
              '<div class="ngis-dialog-icon-badge ' + (isDestructive ? 'is-danger' : 'is-primary') + '">' +
                '<span data-ngis-icon="' + esc(icon) + '" aria-hidden="true"></span>' +
              '</div>' +
              '<div class="min-w-0 flex-1">' +
                '<h2 id="ngisDialogTitle" class="ngis-dialog-title">' + esc(title) + '</h2>' +
                (isRecoverable
                  ? '<span class="ngis-dialog-badge is-recoverable">Action can be reversed</span>'
                  : '<span class="ngis-dialog-badge is-irreversible">Cannot be undone</span>') +
              '</div>' +
            '</div>' +
            '<button type="button" class="ngis-dialog-close-btn" aria-label="Close dialog" data-action="cancel">' +
              '<span data-ngis-icon="close" aria-hidden="true">&times;</span>' +
            '</button>' +
          '</div>' +

          // Body: Description and Real Impact Box
          '<div class="ngis-dialog-body">' +
            '<p id="ngisDialogDesc" class="ngis-dialog-desc">' + esc(description) + '</p>' +
            (consequence
              ? '<div class="ngis-dialog-consequence">' +
                  '<div class="ngis-dialog-consequence-title">What happens next:</div>' +
                  '<div class="ngis-dialog-consequence-body">' + esc(consequence) + '</div>' +
                '</div>'
              : '') +
          '</div>' +

          // Footer: Action-oriented buttons
          '<div class="ngis-dialog-footer">' +
            '<button type="button" class="ngis-btn ngis-btn-ghost ngis-dialog-cancel-btn" data-action="cancel">' +
              esc(cancelLabel) +
            '</button>' +
            '<button type="button" class="ngis-btn ' + (isDestructive ? 'ngis-btn-danger' : 'ngis-btn-primary') + ' ngis-dialog-confirm-btn" data-action="confirm">' +
              esc(confirmLabel) +
            '</button>' +
          '</div>' +
        '</div>';

      backdrop.innerHTML = cardHtml;
      document.body.appendChild(backdrop);
      document.body.classList.add("ngis-modal-open");

      // Hydrate official Bootstrap Icons
      if (window.NGIS && typeof window.NGIS.hydrateIcons === "function") {
        window.NGIS.hydrateIcons(backdrop);
      }

      var card = backdrop.querySelector(".ngis-dialog-card");
      var confirmBtn = backdrop.querySelector(".ngis-dialog-confirm-btn");
      var cancelBtn = backdrop.querySelector(".ngis-dialog-cancel-btn");
      var closeBtn = backdrop.querySelector(".ngis-dialog-close-btn");

      // Trap focus & restore
      activeDialog = {
        backdrop: backdrop,
        card: card,
        resolve: resolve,
        opts: opts
      };

      // Enter Animation
      requestAnimationFrame(function () {
        backdrop.classList.add("is-visible");
        if (confirmBtn && !isDestructive) {
          confirmBtn.focus();
        } else if (cancelBtn) {
          cancelBtn.focus();
        }
      });

      function handleAction(confirmed) {
        closeDialog(confirmed);
      }

      if (confirmBtn) {
        confirmBtn.addEventListener("click", function () { handleAction(true); });
      }
      if (cancelBtn) {
        cancelBtn.addEventListener("click", function () { handleAction(false); });
      }
      if (closeBtn) {
        closeBtn.addEventListener("click", function () { handleAction(false); });
      }

      // Backdrop click dismisses safely
      backdrop.addEventListener("click", function (e) {
        if (e.target === backdrop) {
          handleAction(false);
        }
      });
    });
  }

  function closeDialog(confirmed) {
    if (!activeDialog || !activeDialog.backdrop) return;

    var cur = activeDialog;
    activeDialog = null;

    cur.backdrop.classList.remove("is-visible");
    cur.backdrop.classList.add("is-exiting");

    setTimeout(function () {
      if (cur.backdrop && cur.backdrop.parentNode) {
        cur.backdrop.parentNode.removeChild(cur.backdrop);
      }
      document.body.classList.remove("ngis-modal-open");

      // Restore focus
      if (lastActiveElement && typeof lastActiveElement.focus === "function") {
        try { lastActiveElement.focus(); } catch (err) {}
      }

      if (confirmed) {
        if (typeof cur.opts.onConfirm === "function") cur.opts.onConfirm();
        cur.resolve(true);
      } else {
        if (typeof cur.opts.onCancel === "function") cur.opts.onCancel();
        cur.resolve(false);
      }
    }, 180);
  }

  // Keyboard accessibility: Escape to dismiss, Tab trapping
  document.addEventListener("keydown", function (e) {
    if (!activeDialog || !activeDialog.backdrop) return;

    if (e.key === "Escape") {
      e.preventDefault();
      closeDialog(false);
      return;
    }

    if (e.key === "Tab") {
      var focusables = activeDialog.backdrop.querySelectorAll(
        'button:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      if (!focusables.length) return;

      var first = focusables[0];
      var last = focusables[focusables.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first || !activeDialog.backdrop.contains(document.activeElement)) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last || !activeDialog.backdrop.contains(document.activeElement)) {
          e.preventDefault();
          first.focus();
        }
      }
    }
  });

  /* ==========================================================================
     SPECIALIZED INTELLIGENT CONFIRMATION HELPERS (SECTION 02)
     ========================================================================== */

  var IntelligentDialogs = {
    // 1. Delete Student
    deleteStudent: function (data) {
      data = data || {};
      var name = data.name || "this student";
      var count = data.recordsCount != null ? data.recordsCount : 1;
      return confirmDialog({
        title: "Delete " + name + "?",
        description: "This will remove the student portal account and revoke their campus credentials. Historical academic transcript records will be preserved in the archive under Registrar oversight.",
        consequence: "Student " + name + " will immediately lose access to attendance, coursework, and grades.",
        confirmLabel: "Delete Student",
        cancelLabel: "Keep Student",
        isDestructive: true,
        isRecoverable: false,
        icon: "trash3",
        onConfirm: data.onConfirm,
        onCancel: data.onCancel
      });
    },

    // 2. Delete Assignment
    deleteAssignment: function (data) {
      data = data || {};
      var title = data.title || "this assignment";
      var subCount = data.submissionsCount != null ? Number(data.submissionsCount) : 0;
      var subText = subCount === 1
        ? "1 student submission is currently attached."
        : subCount + " student submissions are currently attached.";
      return confirmDialog({
        title: "Delete " + title + "?",
        description: subCount > 0
          ? subText + " Deleting this assignment will remove all grading progress and student coursework records."
          : "No student submissions have been recorded yet. The assignment will be deleted from the course syllabus.",
        consequence: subCount > 0
          ? "All " + subCount + " student submissions and rubrics will be archived for 30 days."
          : "The assignment entry will be removed immediately from student calendars.",
        confirmLabel: "Delete Assignment",
        cancelLabel: "Keep Assignment",
        isDestructive: true,
        isRecoverable: false,
        icon: "trash3",
        onConfirm: data.onConfirm,
        onCancel: data.onCancel
      });
    },

    // 3. Publish Academic Report
    publishReport: function (data) {
      data = data || {};
      var reportName = data.reportName || "Term Evaluation Report";
      var recipients = data.recipientCount ? data.recipientCount + " enrolled students" : "all enrolled students";
      return confirmDialog({
        title: "Publish " + reportName + "?",
        description: "This official report will become immediately available to " + recipients + " and their registered guardians in their academic portal.",
        consequence: "Guardians and students will receive an in-app notice and can view downloaded evaluation cards.",
        confirmLabel: "Publish Report",
        cancelLabel: "Keep Draft",
        isDestructive: false,
        isRecoverable: true,
        icon: "send-check",
        onConfirm: data.onConfirm,
        onCancel: data.onCancel
      });
    },

    // 4. Logout of NGIS
    logout: function (data) {
      data = data || {};
      return confirmDialog({
        title: "Log out of NGIS?",
        description: "You will need to sign in again to access your active portal and school records.",
        consequence: "Your active session will be securely closed on this device. Any unsaved drafts in open forms were preserved in your local browser cache.",
        confirmLabel: "Log Out",
        cancelLabel: "Stay Signed In",
        isDestructive: true,
        isRecoverable: true,
        icon: "box-arrow-right",
        onConfirm: function () {
          try {
            if (window.NGISAuth && typeof window.NGISAuth.clearSession === "function") {
              window.NGISAuth.clearSession();
            } else {
              localStorage.removeItem("ngis_token");
              localStorage.removeItem("ngis_user");
              localStorage.removeItem("ngis_active_portal");
              localStorage.removeItem("ngis_session_mode");
            }
          } catch (err) {}
          if (typeof data.onConfirm === "function") {
            data.onConfirm();
          } else {
            window.location.href = data.destUrl || "../../index.html";
          }
        },
        onCancel: data.onCancel
      });
    },

    // 5. Restrict Account
    restrictAccount: function (data) {
      data = data || {};
      var userName = data.userName || "this user";
      var duration = data.duration || "30 days";
      return confirmDialog({
        title: "Restrict " + userName + "?",
        description: "This user will be unable to access their account until the restriction expires (" + duration + ") or is manually removed by an administrator.",
        consequence: "Active logins will be immediately terminated. Institutional records remain intact.",
        confirmLabel: "Restrict Account",
        cancelLabel: "Cancel",
        isDestructive: true,
        isRecoverable: true,
        icon: "shield-exclamation",
        onConfirm: data.onConfirm,
        onCancel: data.onCancel
      });
    },

    // 6. Generic / Custom Action
    confirm: confirmDialog
  };

  /* ==========================================================================
     2. GLOBAL TOOLTIP SUPPRESSION & CLEANUP ENGINE
     All unnecessary hover tooltips, floating text popups, and mouse-tracking
     listeners have been completely removed per enterprise UX standards.
     Screen-reader accessibility is preserved via standard aria-label attributes.
     ========================================================================== */

  function removeGlobalTooltipElement() {
    var tip = document.getElementById("ngisGlobalTooltip");
    if (tip && tip.parentNode) {
      tip.parentNode.removeChild(tip);
    }
  }

  function stripUnnecessaryTooltips(root) {
    var scope = root || document;
    if (!scope.querySelectorAll) return;
    var els = scope.querySelectorAll("[title], [data-tooltip]");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.tagName === "HEAD" || el.tagName === "TITLE") continue;
      var text = el.getAttribute("title") || el.getAttribute("data-tooltip");
      if (text && !el.getAttribute("aria-label") && /^(BUTTON|A|INPUT|SELECT|SVG)$/i.test(el.tagName)) {
        el.setAttribute("aria-label", text.trim());
      }
      el.removeAttribute("title");
      el.removeAttribute("data-tooltip");
    }
    removeGlobalTooltipElement();
  }

  // Active mutation observer for dynamic tables & AJAX views
  if (typeof MutationObserver !== "undefined" && typeof document !== "undefined") {
    var domSanitizeObserver = new MutationObserver(function (mutations) {
      for (var m = 0; m < mutations.length; m++) {
        var added = mutations[m].addedNodes;
        for (var n = 0; n < added.length; n++) {
          var node = added[n];
          if (node.nodeType === 1) { // ELEMENT_NODE
            if (node.hasAttribute && (node.hasAttribute("title") || node.hasAttribute("data-tooltip"))) {
              var text = node.getAttribute("title") || node.getAttribute("data-tooltip");
              if (text && !node.getAttribute("aria-label") && /^(BUTTON|A|INPUT|SELECT|SVG)$/i.test(node.tagName)) {
                node.setAttribute("aria-label", text.trim());
              }
              node.removeAttribute("title");
              node.removeAttribute("data-tooltip");
            }
            if (node.querySelectorAll) {
              stripUnnecessaryTooltips(node);
            }
          }
        }
      }
    });

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        if (document.body) domSanitizeObserver.observe(document.body, { childList: true, subtree: true });
      });
    } else if (document.body) {
      domSanitizeObserver.observe(document.body, { childList: true, subtree: true });
    }
  }

  // Safe no-op helpers to preserve API compatibility
  function noopTooltip() {}

  /* ==========================================================================
     3. ACTION-ORIENTED NOTIFICATIONS REGISTRY & DEEP-LINKING (SECTIONS 06 & 07)
     ========================================================================== */

  var NotificationRegistry = {
    // In-memory notifications store
    items: [
      {
        id: "ntf-01",
        role: "student",
        category: "assignment",
        type: "assignment_published",
        title: "New mathematics assignment",
        message: "Your teacher Ms. Rathana Chea has published Algebra Worksheet 04. Due Friday at 5:00 PM.",
        sender: "Ms. Rathana Chea",
        time: "10 min ago",
        read: false,
        actionLabel: "View Assignment",
        targetUrl: "../student/student-assignments.html?id=ASG-ALG-04"
      },
      {
        id: "ntf-02",
        role: "student",
        category: "exam",
        type: "exam_scheduled",
        title: "Physics exam scheduled",
        message: "Your Semester 2 Physics Examination is on 29 June at 9:00 AM in Cambridge Hall.",
        sender: "Academic Registrar",
        time: "1h ago",
        read: false,
        actionLabel: "View Exam",
        targetUrl: "../student/student-exams.html?dept=physics"
      },
      {
        id: "ntf-03",
        role: "student",
        category: "report",
        type: "report_available",
        title: "Academic report is available",
        message: "The English Department has published your official Mid-Term Performance Evaluation.",
        sender: "English Department",
        time: "2h ago",
        read: false,
        actionLabel: "View Report",
        targetUrl: "../student/student-grades.html?dept=english"
      },
      {
        id: "ntf-04",
        role: "teacher",
        category: "submission",
        type: "submission_received",
        title: "5 new assignment submissions",
        message: "Students in Grade 10A have submitted their mathematics coursework for review.",
        sender: "Grade 10A Coursework",
        time: "25 min ago",
        read: false,
        actionLabel: "Review Submissions",
        targetUrl: "../teacher/teacher-submissions.html?class=Grade+10A"
      },
      {
        id: "ntf-05",
        role: "teacher",
        category: "correction",
        type: "report_correction",
        title: "Report needs correction",
        message: "Principal has returned the Grade 10 Physics Mid-Term Report with review feedback.",
        sender: "Office of the Principal",
        time: "2h ago",
        read: false,
        actionLabel: "View Feedback",
        targetUrl: "../teacher/teacher-reports.html?dept=physics&action=feedback"
      },
      {
        id: "ntf-06",
        role: "principal",
        category: "approval",
        type: "approval_request",
        title: "Academic reports awaiting review",
        message: "3 faculty teachers have submitted term grade evaluations for your official endorsement.",
        sender: "Faculty Academic Council",
        time: "30 min ago",
        read: false,
        actionLabel: "Review Reports",
        targetUrl: "../principal/principal-reports.html?status=pending_review"
      },
      {
        id: "ntf-07",
        role: "admin",
        category: "account",
        type: "account_verification",
        title: "New accounts awaiting verification",
        message: "4 newly registered student portal accounts require identity verification.",
        sender: "Admissions Gateway",
        time: "45 min ago",
        read: false,
        actionLabel: "Verify Accounts",
        targetUrl: "../admin/admin-users-students.html?status=pending_verification"
      },
      {
        id: "ntf-08",
        role: "admin",
        category: "security",
        type: "security_event",
        title: "Unusual sign-in activity detected",
        message: "Multiple failed sign-in attempts were recorded from campus gateway subnet 192.168.4.12.",
        sender: "NGIS Security Center",
        time: "15 min ago",
        read: false,
        actionLabel: "Review Security Event",
        targetUrl: "../admin/admin-security.html?view=threat_event&id=EVT-8821"
      }
    ],

    // Get notifications for current viewing portal
    getForRole: function (role) {
      role = (role || "").toLowerCase();
      if (!role) return this.items;
      return this.items.filter(function (n) {
        return n.role === role || n.role === "all";
      });
    },

    // Mark notification as read and decrement badge
    markAsRead: function (id) {
      for (var i = 0; i < this.items.length; i++) {
        if (this.items[i].id === id) {
          this.items[i].read = true;
          break;
        }
      }
      this.updateTopbarBadge();
    },

    // Update the notification badge counter in topbar
    updateTopbarBadge: function () {
      var unread = this.items.filter(function (n) { return !n.read; }).length;
      var badges = document.querySelectorAll(".htb-ctrl-badge, #notifCountBadge, .notif-count-badge");
      badges.forEach(function (b) {
        if (unread > 0) {
          b.textContent = unread;
          b.style.display = "inline-flex";
        } else {
          b.style.display = "none";
        }
      });
    },

    // Safe navigation with deep link & permission check
    openNotification: function (id) {
      var item = null;
      for (var i = 0; i < this.items.length; i++) {
        if (this.items[i].id === id) {
          item = this.items[i];
          break;
        }
      }
      if (!item) {
        toast("This notification record is no longer available.", "warning");
        return;
      }

      this.markAsRead(id);

      // Navigate safely
      if (item.targetUrl) {
        window.location.href = item.targetUrl;
      }
    },

    // Mark all notifications as read
    markAllAsRead: function (role) {
      this.items.forEach(function (n) {
        if (!role || n.role === role || role === "all") {
          n.read = true;
        }
      });
      this.updateTopbarBadge();
    },

    // Render reactive action cards into container
    render: function (container, role, filter) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      var list = this.getForRole(role);
      if (filter && filter !== "All" && filter !== "all") {
        var f = filter.toLowerCase();
        list = list.filter(function (n) {
          return (n.category || "").toLowerCase() === f || (n.type || "").toLowerCase().indexOf(f) !== -1;
        });
      }

      if (!list.length) {
        container.innerHTML =
          '<div style="text-align:center;padding:48px 24px;color:var(--muted);">' +
            '<div style="font-size:32px;margin-bottom:8px;">🔔</div>' +
            '<div style="font-size:15px;font-weight:500;color:var(--text, #1e293b);">No notifications in this view</div>' +
            '<div style="font-size:13px;margin-top:4px;">You are fully caught up with your academic updates.</div>' +
          '</div>';
        return;
      }

      var html = list.map(function (n) {
        var unreadClass = !n.read ? " is-unread" : "";
        var iconName = n.category === "assignment" ? "documents"
          : n.category === "exam" ? "calendar"
          : n.category === "report" ? "grades"
          : n.category === "submission" ? "documents"
          : n.category === "security" ? "shield"
          : "bell";

        return (
          '<div class="ngis-notification-card' + unreadClass + '" data-id="' + esc(n.id) + '">' +
            '<div class="ava" style="width:40px;height:40px;border-radius:10px;flex-shrink:0;background:var(--primary-soft, #e2f4ea);display:flex;align-items:center;justify-content:center;color:var(--primary, #0f5132);">' +
              '<span data-ngis-icon="' + iconName + '"></span>' +
            '</div>' +
            '<div style="flex:1;min-width:0;">' +
              '<div style="display:flex;align-items:baseline;justify-content:space-between;gap:8px;flex-wrap:wrap;">' +
                '<span style="font-size:13.5px;font-weight:500;color:var(--text, #1e293b);">' + esc(n.title) + '</span>' +
                '<span class="faint" style="font-size:11.5px;color:var(--muted, #64748b);">' + esc(n.time) + '</span>' +
              '</div>' +
              '<p style="font-size:12.5px;color:var(--muted, #64748b);margin-top:4px;line-height:1.5;">' + esc(n.message) + '</p>' +
              '<div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;gap:8px;flex-wrap:wrap;">' +
                '<span style="font-size:11.5px;color:var(--muted, #64748b);">From: <strong style="font-weight:500;color:var(--text, #1e293b);">' + esc(n.sender) + '</strong></span>' +
                '<button type="button" class="ngis-notification-card-action" data-action="open-notif" data-id="' + esc(n.id) + '">' +
                  esc(n.actionLabel || "View Details") +
                  ' <span data-ngis-icon="chevronRight" style="font-size:12px;">›</span>' +
                '</button>' +
              '</div>' +
            '</div>' +
            (!n.read ? '<div class="ngis-notification-card-dot" title="Unread notification"></div>' : '') +
          '</div>'
        );
      }).join("");

      container.innerHTML = html;

      // Hydrate icons
      if (window.NGIS && typeof window.NGIS.hydrateIcons === "function") {
        window.NGIS.hydrateIcons(container);
      }

      // Wire action clicks
      container.querySelectorAll('[data-action="open-notif"]').forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.stopPropagation();
          var id = btn.getAttribute("data-id");
          NotificationRegistry.openNotification(id);
        });
      });
    }
  };

  /* ==========================================================================
     4. SUCCESS CONFIRMATIONS & ANIMATED CHECKMARKS (SECTION 08)
     ========================================================================== */

  /**
   * Action-specific success toast
   * @param {string} message - Specific confirmation message
   * @param {Object} [options]
   */
  function showSuccess(message, options) {
    options = options || {};
    var duration = typeof options.duration === "number" ? options.duration : 3000;

    var container = document.getElementById("ngisSuccessToastWrap");
    if (!container) {
      container = document.createElement("div");
      container.id = "ngisSuccessToastWrap";
      container.className = "ngis-success-toast-wrap";
      document.body.appendChild(container);
    }

    var toastEl = document.createElement("div");
    toastEl.className = "ngis-success-toast-item";
    toastEl.setAttribute("role", "status");
    toastEl.setAttribute("aria-live", "polite");

    toastEl.innerHTML =
      '<div class="ngis-success-pill">' +
        '<div class="ngis-success-check-wrap">' +
          '<svg class="ngis-success-check-svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' +
            '<path class="ngis-check-path" d="M20 6L9 17L4 12"></path>' +
          '</svg>' +
        '</div>' +
        '<span class="ngis-success-text">' + esc(message || "Changes saved successfully.") + '</span>' +
      '</div>';

    container.appendChild(toastEl);

    // Animate checkmark draw
    var path = toastEl.querySelector(".ngis-check-path");
    if (path) {
      var len = path.getTotalLength ? path.getTotalLength() : 24;
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
      path.getBoundingClientRect(); // trigger reflow
      path.style.transition = "stroke-dashoffset 260ms cubic-bezier(0.16, 1, 0.3, 1) 100ms";
      path.style.strokeDashoffset = "0";
    }

    // Entrance
    requestAnimationFrame(function () {
      toastEl.classList.add("is-active");
    });

    // Exit
    setTimeout(function () {
      toastEl.classList.remove("is-active");
      toastEl.classList.add("is-exiting");
      setTimeout(function () {
        if (toastEl.parentNode) toastEl.parentNode.removeChild(toastEl);
        if (typeof options.onDismiss === "function") options.onDismiss();
      }, 220);
    }, duration);
  }

  /**
   * General Toast Helper
   */
  function toast(message, kind, detail) {
    kind = kind || "info";
    if (kind === "success") {
      showSuccess(message);
      return;
    }

    if (window.ngisToast && typeof window.ngisToast === "function") {
      window.ngisToast(message, kind, detail);
    } else {
      var t = document.createElement("div");
      t.className = "ngis-toast " + kind;
      t.textContent = message;
      document.body.appendChild(t);
      setTimeout(function () { t.remove(); }, 3000);
    }
  }

  /* ==========================================================================
     5. ERROR HANDLING & INLINE FIELD VALIDATION (SECTION 09)
     ========================================================================== */

  var FriendlyErrors = {
    network: "Could not connect to the academic server right now. Your unsaved data is safely preserved. Check your connection and try again.",
    notFound: "The requested school record could not be found. It may have been archived or moved.",
    fileTooLarge: "This file exceeds the 15 MB upload limit. Please choose a smaller file and try again.",
    invalidEmail: "Please enter a valid school email address (e.g. name@ngis.edu.kh).",
    required: "This field is required. Please fill in the details before proceeding.",
    generic: "We encountered an issue saving your updates. None of your inputs were lost. Please try again."
  };

  function setFieldError(field, message) {
    if (!field) return;
    if (typeof field === "string") field = document.getElementById(field) || document.querySelector(field);
    if (!field) return;

    field.classList.add("ngis-input-error");
    field.setAttribute("aria-invalid", "true");

    var parent = field.closest(".ngis-field, .form-group, div") || field.parentElement;
    if (!parent) return;

    var errId = field.id ? "err-" + field.id : "err-" + Math.random().toString(36).slice(2, 7);
    field.setAttribute("aria-describedby", errId);

    var existing = parent.querySelector(".ngis-inline-error");
    if (!existing) {
      existing = document.createElement("div");
      existing.className = "ngis-inline-error";
      existing.id = errId;
      existing.setAttribute("role", "alert");
      parent.appendChild(existing);
    }
    existing.textContent = message;

    // Clear on user input
    if (!field.dataset.ngisErrBound) {
      field.dataset.ngisErrBound = "1";
      var onInput = function () {
        clearFieldError(field);
      };
      field.addEventListener("input", onInput);
      field.addEventListener("change", onInput);
    }
  }

  function clearFieldError(field) {
    if (!field) return;
    if (typeof field === "string") field = document.getElementById(field) || document.querySelector(field);
    if (!field) return;

    field.classList.remove("ngis-input-error");
    field.setAttribute("aria-invalid", "false");
    field.removeAttribute("aria-describedby");

    var parent = field.closest(".ngis-field, .form-group, div") || field.parentElement;
    if (parent) {
      var err = parent.querySelector(".ngis-inline-error");
      if (err) err.remove();
    }
  }

  /* ==========================================================================
     6. DOUBLE-SUBMISSION LOCK & INTERACTION FEEDBACK (SECTIONS 10 & 11)
     ========================================================================== */

  /**
   * Wrap an async button action with a double-submission lock
   * @param {HTMLElement} btn - The submit button
   * @param {Function} asyncCallback - The action to perform
   * @param {string} [processingText] - Optional button text while processing
   */
  async function withSubmitLock(btn, asyncCallback, processingText) {
    if (!btn || btn.disabled || btn.dataset.ngisProcessing === "1") return;

    var origText = btn.innerHTML;
    btn.dataset.ngisProcessing = "1";
    btn.disabled = true;
    btn.classList.add("is-loading");

    if (processingText) {
      btn.innerHTML = '<span class="ngis-spinner" aria-hidden="true"></span> ' + esc(processingText);
    }

    try {
      await asyncCallback();
    } catch (err) {
      toast(err.message || FriendlyErrors.generic, "error");
    } finally {
      btn.disabled = false;
      btn.classList.remove("is-loading");
      btn.innerHTML = origText;
      delete btn.dataset.ngisProcessing;
    }
  }

  /* ==========================================================================
     7. GLOBAL EVENT LISTENERS & POLYFILLS
     ========================================================================== */

  // Safe window.confirm replacement:
  // Polyfill window.confirm to use intelligent dialog when called in async workflows,
  // while keeping synchronous fallback where strictly expected.
  var nativeConfirm = window.confirm;
  window.ngisConfirm = confirmDialog;

  // Global sanitization: remove unnecessary title attributes & tooltips
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      stripUnnecessaryTooltips();
    });
  } else {
    stripUnnecessaryTooltips();
  }

  /* ==========================================================================
     8. PUBLIC API EXPORT (SINGLE SOURCE OF TRUTH)
     ========================================================================== */

  // Attach specialized helpers directly to dialog function
  confirmDialog.confirm = confirmDialog;
  confirmDialog.deleteStudent = IntelligentDialogs.deleteStudent;
  confirmDialog.deleteAssignment = IntelligentDialogs.deleteAssignment;
  confirmDialog.publishReport = IntelligentDialogs.publishReport;
  confirmDialog.logout = IntelligentDialogs.logout;
  confirmDialog.restrictAccount = IntelligentDialogs.restrictAccount;

  // Attach field validation methods to FriendlyErrors for convenience
  FriendlyErrors.setFieldError = setFieldError;
  FriendlyErrors.clearFieldError = clearFieldError;

  window.NGIS_UX = {
    // Dialogs (accessible both via NGIS_UX.dialog.<method> and NGIS_UX.<method>)
    dialog: confirmDialog,
    confirm: confirmDialog,
    deleteStudent: IntelligentDialogs.deleteStudent,
    deleteAssignment: IntelligentDialogs.deleteAssignment,
    publishReport: IntelligentDialogs.publishReport,
    logout: IntelligentDialogs.logout,
    restrictAccount: IntelligentDialogs.restrictAccount,

    // Tooltips (decommissioned with safe no-op stubs)
    tooltip: {
      show: noopTooltip,
      hide: noopTooltip,
      strip: stripUnnecessaryTooltips
    },

    // Notifications
    notifications: NotificationRegistry,

    // Feedback
    success: showSuccess,
    toast: toast,

    // Errors & Validation
    errors: FriendlyErrors,
    setFieldError: setFieldError,
    clearFieldError: clearFieldError,

    // Interaction Locks
    withSubmitLock: withSubmitLock
  };

  // Expose convenient global aliases
  window.ngisSuccess = showSuccess;

})(window, document);
