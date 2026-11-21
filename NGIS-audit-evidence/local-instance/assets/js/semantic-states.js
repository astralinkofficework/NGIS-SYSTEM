/**
 * NGIS Semantic States — Central Urgency Classification
 * Phase 4 of the Master Urgency & Deadline Color spec.
 *
 * ONE deadline calculation for the whole app. Modules pass their REAL
 * record fields; this module derives the urgency level from the actual
 * business state (submission status, due date, late permission) — never
 * from label text. Thresholds are configurable per module because
 * assignment urgency ≠ administrative approval urgency.
 *
 * Levels (mirrored by .ngis-state--* / .ngis-dot--* / button classes
 * in semantic-states.css):
 *   overdue      — deadline passed, action still required (red)
 *   urgent       — critical window open, e.g. due within urgentHours (red)
 *   approaching  — deadline approaching, action time-sensitive (orange)
 *   normal       — no time pressure (neutral / brand)
 *   complete     — user's required action already done (green, never urgent)
 *   closed       — cancelled / withdrawn / not applicable (neutral)
 */
(function () {
  "use strict";

  /* Status vocabularies seen across NGIS modules (student assignments,
     services, admin approvals, attendance, exams). Anything unknown is
     treated as "pending action" only when paired with a due date. */
  var COMPLETE_STATUSES = {
    graded: 1, submitted: 1, approved: 1, completed: 1, resolved: 1,
    returned: 1, published: 1, present: 1, done: 1, paid: 1,
    "on-time": 1, verified: 1, collected: 1,
    late: 1  /* "late" = submitted AFTER the deadline: action is done,
                the penalty is informational — never render urgent UI */
  };
  var CLOSED_STATUSES = {
    cancelled: 1, canceled: 1, closed: 1, withdrawn: 1, expired: 1,
    archived: 1, rejected: 1, denied: 1, excused: 1
  };
  /* Statuses meaning the USER still owes an action. */
  var ACTION_STATUSES = {
    pending: 1, open: 1, missing: 1, unsubmitted: 1, "not-submitted": 1,
    awaiting: 1, "awaiting-submission": 1, draft: 1, "in-progress": 1,
    reviewing: 1, review: 1, overdue: 1
  };

  var DEFAULT_THRESHOLDS = { urgentHours: 6, warnHours: 24 };

  function parseDate(value) {
    if (!value) return null;
    if (value instanceof Date) return isNaN(value.getTime()) ? null : value;
    var str = String(value).trim();
    if (!str || str === "—") return null;
    /* ISO "YYYY-MM-DD[THH:MM]" → treat as LOCAL school time (NGIS runs
       single-campus on ICT, UTC+7; server dates carry no zone suffix).
       Explicit Z/GMT offsets are honored by Date.parse. */
    if (/^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?)?$/.test(str)) {
      str = str.replace(" ", "T");
      var dt = new Date(str);
      return isNaN(dt.getTime()) ? null : dt;
    }
    var parsed = new Date(str);
    return isNaN(parsed.getTime()) ? null : parsed;
  }

  /**
   * classify(record, options) → level string.
   * @param {Object} record
   *   status      {string}  real submission/approval/attendance status
   *   dueDate     {string|Date|null} deadline (null → no urgency signal)
   *   lateAllowed {boolean} portal still accepts late submissions
   *   actionDone  {boolean} explicit override: the user's action is done
   *   actionable  {boolean} explicit override: action still required
   * @param {Object} [options] { urgentHours, warnHours }
   */
  function classify(record, options) {
    record = record || {};
    options = options || {};
    var thresholds = {
      urgentHours: options.urgentHours != null ? options.urgentHours : DEFAULT_THRESHOLDS.urgentHours,
      warnHours: options.warnHours != null ? options.warnHours : DEFAULT_THRESHOLDS.warnHours
    };
    var raw = String(record.status || "").toLowerCase().trim();

    if (record.actionDone || COMPLETE_STATUSES[raw]) return "complete";
    if (CLOSED_STATUSES[raw]) return "closed";
    if (record.actionable === false) return "complete";
    if (record.actionable === true) {
      /* caller asserts action is required — fall through to date logic */
    } else if (!ACTION_STATUSES[raw]) {
      /* Unknown/empty status with no date signal → normal. */
      var dueOnly = parseDate(record.dueDate);
      if (!dueOnly) return "normal";
    }

    var due = parseDate(record.dueDate);
    var now = new Date();

    if (due && due.getTime() <= now.getTime()) {
      /* Deadline passed. */
      if (record.actionDone || COMPLETE_STATUSES[raw]) return "complete";
      if (CLOSED_STATUSES[raw]) return "closed";
      var owesAction = record.actionable === true || ACTION_STATUSES[raw] || !record.status;
      if (!owesAction) return "complete";           /* already submitted — no misleading urgency */
      if (record.lateAllowed === false) return "closed"; /* window shut → nothing to do */
      return "overdue";
    }

    if (due) {
      var hoursLeft = (due.getTime() - now.getTime()) / 3600000;
      if (hoursLeft <= thresholds.urgentHours) return "urgent";
      if (hoursLeft <= thresholds.warnHours) return "approaching";
    }
    return "normal";
  }

  /** Map a level to the CSS modifier suffix. */
  function levelClass(level) {
    return "ngis-state--" + level;
  }

  /** Apply a level to an element: data attribute + state classes. */
  function apply(el, level) {
    if (!el) return level;
    el.setAttribute("data-ngis-state", level);
    ["overdue", "urgent", "approaching", "complete", "info", "normal", "neutral", "closed"].forEach(function (lv) {
      el.classList.remove("ngis-state--" + lv, "ngis-state-chip--" + lv, "ngis-dot--" + lv);
    });
    el.classList.add("ngis-state--" + level);
    return level;
  }

  /** Human-readable default labels — color is never the only signal. */
  var LABELS = {
    overdue: "Overdue — Action Required",
    urgent: "Due Very Soon",
    approaching: "Due Soon",
    normal: "Scheduled",
    complete: "Completed",
    closed: "Closed"
  };

  /** Style an action button to match the record's urgency. */
  function styleButton(btn, level) {
    if (!btn) return;
    btn.classList.remove("ngis-btn-urgent", "ngis-btn-warning");
    if (level === "overdue" || level === "urgent") btn.classList.add("ngis-btn-urgent");
    else if (level === "approaching") btn.classList.add("ngis-btn-warning");
    /* normal/complete keep the module's existing primary styling */
  }

  /** Convenience: classify + apply in one call. */
  function mark(el, record, options) {
    var level = classify(record, options);
    apply(el, level);
    return level;
  }

  window.NGISStates = {
    classify: classify,
    apply: apply,
    mark: mark,
    styleButton: styleButton,
    label: function (level) { return LABELS[level] || level; },
    levels: LABELS,
    parseDate: parseDate,
    version: "1.0.0"
  };
})();
