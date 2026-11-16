/**
 * ============================================================
 * NGIS ERP — Shared UI Component Kit (Single Source of Truth)
 * Implements reusable, framework-free accessible UI patterns:
 * - Button        (consistent icons + labels, 40-44px target)
 * - Field         (label above full-width input + inline errors)
 * - FormStepper   ("Step X of Y" + progress bar)
 * - SettingsGroup (clean grouped profile/settings cards)
 * - FilterSheet   (mobile bottom drawer with live result count)
 * - confirmAction (clean dialog replacement for window.confirm)
 * ============================================================
 */
(function (global, doc) {
  "use strict";

  function esc(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function copyT(path, vars, fallback) {
    if (global.NGIS_COPY && typeof global.NGIS_COPY.t === "function") {
      return global.NGIS_COPY.t(path, vars, fallback);
    }
    var txt = fallback || path;
    if (vars && typeof txt === "string") {
      Object.keys(vars).forEach(function (k) {
        txt = txt.replace(new RegExp("\\{" + k + "\\}", "g"), String(vars[k]));
      });
    }
    return txt;
  }

  /* ── 1. Inline Field Errors (Rule 6: never clear user input) ── */
  function setFieldError(field, message) {
    if (!field) return;
    if (typeof field === "string") field = doc.getElementById(field) || doc.querySelector(field);
    if (!field) return;

    if (global.NGISUI && typeof global.NGISUI.setFieldError === "function") {
      global.NGISUI.setFieldError(field, message);
      return;
    }

    field.classList.add("ngis-input-error");
    field.setAttribute("aria-invalid", "true");
    var parent = field.closest(".ngis-field, .smx-field, .cms-form-group, div") || field.parentElement;
    if (!parent) return;

    var errId = field.id ? "error-" + field.id : "error-" + Math.random().toString(36).slice(2, 7);
    field.setAttribute("aria-describedby", errId);

    var errEl = parent.querySelector(".ngis-field-error");
    if (!errEl) {
      errEl = doc.createElement("div");
      errEl.className = "ngis-field-error ngis-field-error-msg";
      errEl.id = errId;
      errEl.setAttribute("role", "alert");
      parent.appendChild(errEl);
    }
    errEl.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">error</span><span>' + esc(message) + "</span>";

    if (!field.dataset.ngisErrBound) {
      field.dataset.ngisErrBound = "1";
      var clearFn = function () {
        clearFieldError(field);
      };
      field.addEventListener("input", clearFn);
      field.addEventListener("change", clearFn);
    }
  }

  function clearFieldError(field) {
    if (!field) return;
    if (typeof field === "string") field = doc.getElementById(field) || doc.querySelector(field);
    if (!field) return;

    if (global.NGISUI && typeof global.NGISUI.clearFieldError === "function") {
      global.NGISUI.clearFieldError(field);
      return;
    }

    field.classList.remove("ngis-input-error");
    field.setAttribute("aria-invalid", "false");
    field.removeAttribute("aria-describedby");
    var parent = field.closest(".ngis-field, .smx-field, .cms-form-group, div") || field.parentElement;
    var err = parent ? parent.querySelector(".ngis-field-error, .ngis-field-error-msg") : null;
    if (err) err.remove();
  }

  function clearContainerErrors(container) {
    if (!container) return;
    container.querySelectorAll(".ngis-input-error").forEach(function (el) {
      clearFieldError(el);
    });
    container.querySelectorAll(".ngis-field-error, .ngis-field-error-msg").forEach(function (el) {
      el.remove();
    });
  }

  /* ── 2. Button HTML Builder (Rule 3: Icons always have text labels) ── */
  function Button(opts) {
    var o = opts || {};
    var variant = o.variant || "secondary";
    var cls = "ngis-btn ngis-btn-" + variant + (o.className ? " " + o.className : "");
    var idAttr = o.id ? ' id="' + esc(o.id) + '"' : "";
    var typeAttr = ' type="' + esc(o.type || "button") + '"';
    var iconHtml = "";
    if (o.icon) {
      iconHtml = o.icon.indexOf("ph") === 0
        ? '<i class="ph ' + esc(o.icon) + '" aria-hidden="true"></i>'
        : '<span class="material-symbols-outlined" aria-hidden="true">' + esc(o.icon) + "</span>";
    }
    var extra = o.attrs ? " " + o.attrs : "";
    return "<button" + typeAttr + idAttr + ' class="' + esc(cls) + '"' + extra + ">" +
      iconHtml + "<span>" + esc(o.label || "") + "</span></button>";
  }

  /* ── 3. Field Wrapper Builder (Rule 4: Label above full-width input) ── */
  function Field(opts) {
    var o = opts || {};
    var reqMark = o.required ? ' <span class="ngis-req" aria-hidden="true">*</span>' : "";
    var forAttr = o.forId ? ' for="' + esc(o.forId) + '"' : "";
    var hintHtml = o.hint ? '<div class="ngis-field-hint">' + esc(o.hint) + "</div>" : "";
    var errHtml = o.error
      ? '<div class="ngis-field-error ngis-field-error-msg" role="alert"><span class="material-symbols-outlined" aria-hidden="true">error</span><span>' + esc(o.error) + "</span></div>"
      : "";
    return '<div class="ngis-field' + (o.className ? " " + esc(o.className) : "") + '">' +
      '<label class="ngis-field-label"' + forAttr + ">" + esc(o.label || "") + reqMark + "</label>" +
      '<div class="ngis-field-control">' + (o.inputHtml || "") + "</div>" +
      hintHtml +
      errHtml +
      "</div>";
  }

  /* ── 4. FormStepper Component (Rule 5: Step X of Y + Progress Bar) ── */
  function FormStepper(opts) {
    var o = opts || {};
    var current = Math.max(1, Number(o.current) || 1);
    var total = Math.max(1, Number(o.total) || 1);
    var pct = Math.min(100, Math.max(0, Math.round((current / total) * 100)));
    var counterLabel = copyT("common.stepProgress", { current: current, total: total }, "Step " + current + " of " + total);
    var stepInfo = Array.isArray(o.steps) && o.steps[current - 1] ? o.steps[current - 1] : null;
    var title = o.title || (stepInfo && stepInfo.title) || "";
    var sub = o.subtitle || (stepInfo && stepInfo.sub) || "";

    var dotsHtml = "";
    if (total <= 6) {
      dotsHtml = '<div class="ngis-stepper-dots" aria-hidden="true">';
      for (var i = 1; i <= total; i++) {
        var stateCls = i < current ? "is-done" : (i === current ? "is-active" : "");
        dotsHtml += '<span class="ngis-stepper-seg ' + stateCls + '"></span>';
      }
      dotsHtml += "</div>";
    }

    return '<div class="ngis-stepper" role="region" aria-label="' + esc(counterLabel) + '">' +
      '<div class="ngis-stepper-top">' +
        '<span class="ngis-stepper-count">' + esc(counterLabel) + "</span>" +
        '<span class="ngis-stepper-pct">' + pct + "%</span>" +
      "</div>" +
      '<div class="ngis-stepper-track" role="progressbar" aria-valuemin="1" aria-valuemax="' + total + '" aria-valuenow="' + current + '">' +
        '<div class="ngis-stepper-fill" style="width:' + pct + '%"></div>' +
      "</div>" +
      dotsHtml +
      (title ? '<div class="ngis-stepper-heading">' + esc(title) + "</div>" : "") +
      (sub ? '<p class="ngis-stepper-sub">' + esc(sub) + "</p>" : "") +
      "</div>";
  }

  /* ── 5. SettingsGroup Card Builder (Rule 14: Clean Grouped Account Rows) ── */
  function SettingsGroup(opts) {
    var o = opts || {};
    var rows = (o.items || []).map(function (it) {
      return '<div class="ngis-sg-row">' +
        '<span class="ngis-sg-label">' + esc(it.label || "") + "</span>" +
        '<div class="ngis-sg-val">' + (it.html != null ? it.html : esc(it.value || "—")) + "</div>" +
        "</div>";
    }).join("");
    return '<section class="ngis-settings-group">' +
      (o.title ? '<header class="ngis-sg-head"><h4 class="ngis-sg-title">' + esc(o.title) + "</h4>" +
        (o.description ? '<p class="ngis-sg-desc">' + esc(o.description) + "</p>" : "") + "</header>" : "") +
      '<div class="ngis-sg-body">' + rows + "</div>" +
      "</section>";
  }

  /* ── 6. Mobile FilterSheet Bottom Sheet with Live Count CTA (Rule 16) ── */
  var activeSheet = null;

  function renderFilterSheetHtml(o) {
    var sections = (o.sections || []).map(function (sec) {
      var optsHtml = (sec.options || []).map(function (opt) {
        var sel = String(sec.value || "") === String(opt.value) ? " selected" : "";
        return '<option value="' + esc(opt.value) + '"' + sel + ">" + esc(opt.label) + "</option>";
      }).join("");
      var selectHtml = '<select class="ngis-sheet-select" data-sheet-filter="' + esc(sec.key) + '">' + optsHtml + "</select>";
      return Field({ label: sec.label, forId: "sheet-filter-" + sec.key, inputHtml: selectHtml });
    }).join("");

    var countVal = Number(o.count || 0);
    var ctaText = copyT("common.showResults", { count: countVal }, "Show Results (" + countVal + ")");
    return '<div class="ngis-sheet-panel" role="dialog" aria-modal="true" aria-labelledby="ngisFilterSheetTitle">' +
      '<div class="ngis-sheet-grab" aria-hidden="true"></div>' +
      '<div class="ngis-sheet-head">' +
        '<button type="button" class="ngis-btn ngis-btn-ghost ngis-sheet-cancel" data-filter-cancel>' +
          '<span class="material-symbols-outlined" aria-hidden="true">close</span>' +
          "<span>" + esc(copyT("common.cancel", null, "Cancel")) + "</span>" +
        "</button>" +
        '<h3 id="ngisFilterSheetTitle" class="ngis-sheet-title">' + esc(o.title || copyT("common.filters", null, "Filters")) + "</h3>" +
        '<button type="button" class="ngis-btn ngis-btn-ghost ngis-sheet-reset" data-filter-reset>' +
          "<span>" + esc(copyT("common.clearAll", null, "Clear All")) + "</span>" +
        "</button>" +
      "</div>" +
      '<div class="ngis-sheet-body">' + sections + "</div>" +
      '<div class="ngis-sheet-footer">' +
        '<button type="button" class="ngis-btn ngis-btn-primary ngis-sheet-apply" data-filter-apply>' +
          '<span data-filter-apply-label>' + esc(ctaText) + "</span>" +
        "</button>" +
      "</div>" +
      "</div>";
  }

  var FilterSheet = {
    open: function (options) {
      var o = options || {};
      this.close();

      var host = doc.createElement("div");
      host.className = "ngis-filter-sheet open";
      host.id = "ngisFilterSheet";
      host.innerHTML = renderFilterSheetHtml(o);
      doc.body.appendChild(host);
      doc.body.classList.add("ngis-sheet-open");

      activeSheet = { host: host, options: o };

      host.addEventListener("click", function (e) {
        if (e.target === host || e.target.closest("[data-filter-cancel]")) {
          if (typeof o.onCancel === "function") o.onCancel();
          FilterSheet.close();
          return;
        }
        if (e.target.closest("[data-filter-reset]")) {
          if (typeof o.onReset === "function") o.onReset();
          host.querySelectorAll("[data-sheet-filter]").forEach(function (sel) {
            if (sel.options.length > 0) sel.selectedIndex = 0;
          });
          return;
        }
        if (e.target.closest("[data-filter-apply]")) {
          if (typeof o.onApply === "function") o.onApply();
          FilterSheet.close();
        }
      });

      host.querySelectorAll("[data-sheet-filter]").forEach(function (sel) {
        sel.addEventListener("change", function () {
          if (typeof o.onChange === "function") {
            o.onChange(sel.dataset.sheetFilter, sel.value);
          }
        });
      });

      var onKey = function (ev) {
        if (ev.key === "Escape") {
          FilterSheet.close();
          doc.removeEventListener("keydown", onKey);
        }
      };
      doc.addEventListener("keydown", onKey);
    },
    updateCount: function (count) {
      if (!activeSheet || !activeSheet.host) return;
      var lbl = activeSheet.host.querySelector("[data-filter-apply-label]");
      if (lbl) {
        var n = Number(count || 0);
        lbl.textContent = copyT("common.showResults", { count: n }, "Show Results (" + n + ")");
      }
    },
    close: function () {
      var el = doc.getElementById("ngisFilterSheet");
      if (el) el.remove();
      doc.body.classList.remove("ngis-sheet-open");
      activeSheet = null;
    }
  };

  /* ── 7. Accessible Confirmation Dialog (replaces window.confirm) ── */
  function confirmAction(opts) {
    var o = opts || {};
    if (global.NGISCancelDialog && typeof global.NGISCancelDialog.open === "function") {
      global.NGISCancelDialog.open({
        title: o.title || "Confirm Action",
        description: o.description || "Please confirm you want to continue.",
        consequence: o.consequence || "This update will be applied to the current workspace.",
        confirmLabel: o.confirmLabel || "Confirm",
        cancelLabel: o.cancelLabel || copyT("common.cancel", null, "Cancel"),
        isDestructive: Boolean(o.isDestructive),
        onConfirm: o.onConfirm,
        onCancel: o.onCancel
      });
      return;
    }

    var existing = doc.getElementById("ngisConfirmSheetModal");
    if (existing) existing.remove();
    var backdrop = doc.createElement("div");
    backdrop.id = "ngisConfirmSheetModal";
    backdrop.className = "ngis-modal-backdrop";
    backdrop.innerHTML =
      '<div class="ngis-modal-box ngis-confirm-box" role="dialog" aria-modal="true">' +
        '<h3 class="ngis-confirm-title">' + esc(o.title || "Confirm Action") + "</h3>" +
        '<p class="ngis-confirm-desc">' + esc(o.description || "") + "</p>" +
        '<div class="ngis-confirm-actions">' +
          '<button type="button" class="ngis-btn ngis-btn-secondary" data-ngis-cancel>' + esc(o.cancelLabel || "Cancel") + "</button>" +
          '<button type="button" class="ngis-btn ' + (o.isDestructive ? "ngis-btn-danger" : "ngis-btn-primary") + '" data-ngis-ok>' + esc(o.confirmLabel || "Confirm") + "</button>" +
        "</div>" +
      "</div>";
    doc.body.appendChild(backdrop);

    backdrop.addEventListener("click", function (e) {
      if (e.target === backdrop || e.target.closest("[data-ngis-cancel]")) {
        backdrop.remove();
        if (typeof o.onCancel === "function") o.onCancel();
      } else if (e.target.closest("[data-ngis-ok]")) {
        backdrop.remove();
        if (typeof o.onConfirm === "function") o.onConfirm();
      }
    });
  }

  /* ── 8. Semantic Badge Builder (Rule 9: Green, Amber, Red, Blue, Neutral) ── */
  var VALID_STATUSES = {
    success: "badge-success",
    active: "badge-success",
    completed: "badge-success",
    published: "badge-success",
    approved: "badge-success",
    warning: "badge-warning",
    pending: "badge-warning",
    review: "badge-warning",
    draft: "badge-warning",
    "on-hold": "badge-warning",
    danger: "badge-danger",
    failed: "badge-danger",
    urgent: "badge-danger",
    overdue: "badge-danger",
    expired: "badge-danger",
    inactive: "badge-danger",
    rejected: "badge-danger",
    info: "badge-info",
    new: "badge-info",
    scheduled: "badge-info",
    neutral: "badge-neutral",
    archived: "badge-neutral",
    default: "badge-neutral"
  };

  function Badge(opts) {
    var o = opts || {};
    var rawStatus = String(o.status || "neutral").toLowerCase();
    var statusClass = VALID_STATUSES[rawStatus] || "badge-neutral";
    var iconHtml = "";
    if (o.icon) {
      iconHtml = o.icon.indexOf("ph") === 0
        ? '<i class="ph ' + esc(o.icon) + '" aria-hidden="true"></i> '
        : '<span class="material-symbols-outlined" style="font-size:14px" aria-hidden="true">' + esc(o.icon) + "</span> ";
    }
    return '<span class="badge ' + statusClass + (o.className ? " " + esc(o.className) : "") + '">' +
      iconHtml + esc(o.label || "") + "</span>";
  }

  /* ── 9. Button Loading Controller & 6-State Manager (Rule 11) ── */
  function setButtonLoading(btn, isLoading, loadingText) {
    if (!btn) return;
    if (typeof btn === "string") btn = doc.getElementById(btn) || doc.querySelector(btn);
    if (!btn) return;
    if (isLoading) {
      if (btn.dataset.ngisLoading === "true") return;
      btn.dataset.ngisLoading = "true";
      btn.dataset.prevHtml = btn.innerHTML;
      btn.classList.add("is-loading");
      btn.setAttribute("aria-busy", "true");
      btn.disabled = true;
      if (loadingText) btn.setAttribute("data-loading-text", loadingText);
    } else {
      btn.dataset.ngisLoading = "false";
      btn.classList.remove("is-loading");
      btn.removeAttribute("aria-busy");
      btn.disabled = false;
      if (btn.dataset.prevHtml) {
        btn.innerHTML = btn.dataset.prevHtml;
        delete btn.dataset.prevHtml;
      }
    }
  }

  /* ── 10. Sanitized Toast Notification System (Rule 12: Zero Filler Words) ── */
  function sanitizeCopy(text) {
    if (!text || typeof text !== "string") return text;
    return text
      .replace(/\b(successfully|has been successfully|was successfully)\b/gi, "")
      .replace(/\bhas been\s+/gi, "")
      .replace(/\bhave been\s+/gi, "")
      .replace(/\bplease note that\s+/gi, "")
      .replace(/\s{2,}/g, " ")
      .trim();
  }

  function Toast(message, type, duration) {
    var rawMsg = typeof message === "object" ? message.message : message;
    var cleanMsg = sanitizeCopy(rawMsg);
    var tType = (typeof message === "object" ? message.type : type) || "info";
    var dur = (typeof message === "object" ? message.duration : duration) || 3200;

    var container = doc.getElementById("ngisToastContainer");
    if (!container) {
      container = doc.createElement("div");
      container.id = "ngisToastContainer";
      container.className = "ngis-toast-container";
      container.setAttribute("role", "status");
      container.setAttribute("aria-live", "polite");
      doc.body.appendChild(container);
    }

    var toastEl = doc.createElement("div");
    toastEl.className = "ngis-toast ngis-toast-" + esc(tType);
    var iconName = tType === "success" ? "check_circle" : (tType === "error" || tType === "danger" ? "error" : (tType === "warning" ? "warning" : "info"));
    toastEl.innerHTML = '<span class="material-symbols-outlined" aria-hidden="true">' + iconName + '</span><span class="ngis-toast-text">' + esc(cleanMsg) + '</span>';
    container.appendChild(toastEl);

    setTimeout(function () {
      toastEl.classList.add("is-leaving");
      setTimeout(function () {
        if (toastEl.parentElement) toastEl.remove();
      }, 300);
    }, dur);
  }

  /* ── 11. Accessible Empty State Builder ── */
  function EmptyState(opts) {
    var o = opts || {};
    var icon = o.icon || "inbox";
    var title = o.title || "No items found";
    var desc = o.description || "There are no records to display at this time.";
    var actionHtml = "";
    if (o.actionLabel) {
      actionHtml = '<button type="button" class="btn btn-primary mt-4" data-empty-action>' +
        '<span class="material-symbols-outlined text-sm" aria-hidden="true">add</span>' +
        '<span>' + esc(o.actionLabel) + '</span></button>';
    }
    return '<div class="empty-state p-8 text-center bg-white border border-[#E1E9E3] rounded-2xl flex flex-col items-center justify-center my-4' + (o.className ? ' ' + esc(o.className) : '') + '">' +
      '<div class="w-12 h-12 rounded-full bg-[#E8F3ED] text-[#176B45] flex items-center justify-center mb-3">' +
      '<span class="material-symbols-outlined text-2xl" aria-hidden="true">' + esc(icon) + '</span></div>' +
      '<h4 class="text-sm font-medium text-[#29352E] mb-1">' + esc(title) + '</h4>' +
      '<p class="text-xs text-[#64746A] max-w-sm">' + esc(desc) + '</p>' +
      actionHtml +
      '</div>';
  }

  /* ── 12. Skeleton Loading Builder (Delegates to NGIS_SKELETON) ── */
  function Skeleton(opts) {
    if (global.NGIS_SKELETON) {
      var t = (opts && opts.type) || "table";
      if (typeof global.NGIS_SKELETON[t] === "function") {
        return global.NGIS_SKELETON[t](opts);
      }
      return global.NGIS_SKELETON.table(opts);
    }
    var o = opts || {};
    var count = Math.max(1, Number(o.count || 3));
    var type = o.type || "table";
    var html = '<div class="ngis-skeleton-group" aria-busy="true" aria-label="Loading content">';
    if (type === "card") {
      for (var i = 0; i < count; i++) {
        html += '<div class="ngis-sk-card mb-3">' +
          '<span class="ngis-sk-text ngis-sk-shimmer mb-3" style="width:33%;height:14px;"></span>' +
          '<span class="ngis-sk-text ngis-sk-shimmer mb-2" style="width:66%;height:12px;"></span>' +
          '<span class="ngis-sk-text ngis-sk-shimmer" style="width:50%;height:12px;"></span></div>';
      }
    } else {
      for (var j = 0; j < count; j++) {
        html += '<div class="ngis-sk-row">' +
          '<span class="ngis-sk-avatar ngis-sk-shimmer"></span>' +
          '<div class="flex-1">' +
            '<span class="ngis-sk-text ngis-sk-shimmer mb-1.5" style="width:25%;height:14px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:50%;height:11px;"></span>' +
          '</div>' +
          '<span class="ngis-sk-badge ngis-sk-shimmer w-16"></span></div>';
      }
    }
    html += '</div>';
    return html;
  }

  /* ── 13. Searchable Select / Combobox Component (Rule 6) ──────── */
  function createSearchableSelect(targetEl, opts) {
    var selectEl = typeof targetEl === 'string' ? doc.querySelector(targetEl) : targetEl;
    if (!selectEl) return null;
    var o = opts || {};
    var placeholder = o.placeholder || selectEl.getAttribute('data-placeholder') || 'Search or select...';
    
    // Read options from native select
    var options = [];
    if (selectEl.tagName === 'SELECT') {
      Array.prototype.forEach.call(selectEl.options, function (opt) {
        options.push({
          value: opt.value,
          label: opt.text,
          selected: opt.selected,
          disabled: opt.disabled
        });
      });
      selectEl.style.display = 'none';
    } else {
      options = o.options || [];
    }

    var selectedOpt = options.filter(function (opt) { return opt.selected; })[0] || options[0] || { value: '', label: placeholder };

    // Create wrapper
    var wrap = doc.createElement('div');
    wrap.className = 'ngis-combobox' + (o.className ? ' ' + o.className : '');
    
    wrap.innerHTML = 
      '<button type="button" class="ngis-combobox-trigger" aria-haspopup="listbox" aria-expanded="false">' +
        '<span class="ngis-combobox-label truncate">' + esc(selectedOpt ? selectedOpt.label : placeholder) + '</span>' +
        '<span class="material-symbols-outlined text-[18px] text-slate-400 shrink-0">expand_more</span>' +
      '</button>' +
      '<div class="ngis-combobox-dropdown" role="listbox">' +
        '<div class="ngis-combobox-search-box">' +
          '<span class="material-symbols-outlined ngis-combobox-search-icon">search</span>' +
          '<input type="text" class="ngis-combobox-search-input" placeholder="' + esc(placeholder) + '" aria-label="Filter options">' +
        '</div>' +
        '<div class="ngis-combobox-list"></div>' +
      '</div>';

    var trigger = wrap.querySelector('.ngis-combobox-trigger');
    var labelEl = wrap.querySelector('.ngis-combobox-label');
    var dropdown = wrap.querySelector('.ngis-combobox-dropdown');
    var searchInput = wrap.querySelector('.ngis-combobox-search-input');
    var listEl = wrap.querySelector('.ngis-combobox-list');

    function renderOptions(filterText) {
      var query = (filterText || '').toLowerCase().trim();
      var filtered = options.filter(function (opt) {
        return !query || opt.label.toLowerCase().indexOf(query) !== -1;
      });

      if (!filtered.length) {
        listEl.innerHTML = '<div class="ngis-combobox-empty">No matching options found</div>';
        return;
      }

      listEl.innerHTML = filtered.map(function (opt) {
        var isSel = selectEl.value === opt.value;
        return '<div class="ngis-combobox-option' + (isSel ? ' is-selected' : '') + '" data-val="' + esc(opt.value) + '" role="option" aria-selected="' + isSel + '">' +
          '<span class="truncate">' + esc(opt.label) + '</span>' +
          (isSel ? '<span class="material-symbols-outlined text-[16px] text-[#176B45]">check</span>' : '') +
          '</div>';
      }).join('');
    }

    function openDropdown() {
      wrap.classList.add('is-open');
      trigger.setAttribute('aria-expanded', 'true');
      renderOptions('');
      searchInput.value = '';
      setTimeout(function () { searchInput.focus(); }, 50);
    }

    function closeDropdown() {
      wrap.classList.remove('is-open');
      trigger.setAttribute('aria-expanded', 'false');
    }

    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      if (wrap.classList.contains('is-open')) {
        closeDropdown();
      } else {
        openDropdown();
      }
    });

    searchInput.addEventListener('input', function () {
      renderOptions(searchInput.value);
    });

    listEl.addEventListener('click', function (e) {
      var optEl = e.target.closest('.ngis-combobox-option');
      if (!optEl) return;
      var val = optEl.getAttribute('data-val');
      var matched = options.filter(function (o) { return String(o.value) === String(val); })[0];
      if (matched) {
        labelEl.textContent = matched.label;
        if (selectEl.tagName === 'SELECT') {
          selectEl.value = matched.value;
          var evt = new Event('change', { bubbles: true });
          selectEl.dispatchEvent(evt);
        }
        if (typeof o.onChange === 'function') {
          o.onChange(matched.value, matched);
        }
      }
      closeDropdown();
      trigger.focus();
    });

    doc.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) {
        closeDropdown();
      }
    });

    wrap.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeDropdown();
        trigger.focus();
      }
    });

    if (selectEl.parentNode) {
      selectEl.parentNode.insertBefore(wrap, selectEl.nextSibling);
    }

    return {
      wrap: wrap,
      setValue: function (val) {
        var m = options.filter(function (o) { return String(o.value) === String(val); })[0];
        if (m) {
          labelEl.textContent = m.label;
          if (selectEl.tagName === 'SELECT') selectEl.value = m.value;
        }
      },
      close: closeDropdown,
      open: openDropdown
    };
  }

  /* ── 14. Compact Multi-Select Chips Component (Rule 10) ────────── */
  function createMultiSelectChips(containerEl, opts) {
    var cEl = typeof containerEl === 'string' ? doc.querySelector(containerEl) : containerEl;
    if (!cEl) return null;
    var o = opts || {};
    var isMulti = o.multi !== false; // default true
    var items = o.items || [];
    var selected = Array.isArray(o.selected) ? o.selected.slice() : (o.selected ? [o.selected] : []);

    cEl.classList.add('chip-group', 'ngis-chip-group');

    function render() {
      cEl.innerHTML = items.map(function (it) {
        var val = it.value != null ? it.value : it;
        var label = it.label != null ? it.label : it;
        var icon = it.icon || '';
        var isSel = selected.indexOf(String(val)) !== -1;
        var iconHtml = icon ? '<span class="material-symbols-outlined text-[15px]">' + esc(icon) + '</span>' : '';
        return '<button type="button" class="filter-chip' + (isSel ? ' is-active' : '') + '" data-chip-val="' + esc(val) + '" role="checkbox" aria-checked="' + isSel + '">' +
          iconHtml +
          '<span class="chip-label">' + esc(label) + '</span>' +
          '<span class="material-symbols-outlined chip-check text-[14px]">check</span>' +
          '</button>';
      }).join('');
    }

    cEl.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-chip-val]');
      if (!btn) return;
      var val = String(btn.getAttribute('data-chip-val'));
      var idx = selected.indexOf(val);
      if (isMulti) {
        if (idx !== -1) {
          selected.splice(idx, 1);
        } else {
          selected.push(val);
        }
      } else {
        selected = [val];
      }
      render();
      if (typeof o.onChange === 'function') {
        o.onChange(isMulti ? selected : (selected[0] || ''));
      }
    });

    render();
    return {
      getSelected: function () { return isMulti ? selected.slice() : (selected[0] || ''); },
      setSelected: function (newSel) {
        selected = Array.isArray(newSel) ? newSel.map(String) : [String(newSel)];
        render();
      }
    };
  }

  /* ── 15. Phone Number Input Mask & Guidance (Rule 7) ──────────── */
  function applyPhoneMask(inputEl) {
    var el = typeof inputEl === 'string' ? doc.querySelector(inputEl) : inputEl;
    if (!el || el.dataset.phoneMaskBound) return;
    el.dataset.phoneMaskBound = '1';

    el.setAttribute('placeholder', 'e.g. 012 345 678');

    el.addEventListener('input', function () {
      var raw = el.value.replace(/[^\d+]/g, '');
      if (raw.indexOf('+855') === 0) {
        // International format: +855 12 345 678
        var sub = raw.slice(4);
        var formatted = '+855';
        if (sub.length > 0) formatted += ' ' + sub.slice(0, 2);
        if (sub.length > 2) formatted += ' ' + sub.slice(2, 5);
        if (sub.length > 5) formatted += ' ' + sub.slice(5, 9);
        el.value = formatted;
      } else {
        // Standard domestic Cambodian format: 012 345 678
        var d = raw.replace(/\D/g, '');
        var formatted = '';
        if (d.length > 0) formatted += d.slice(0, 3);
        if (d.length > 3) formatted += ' ' + d.slice(3, 6);
        if (d.length > 6) formatted += ' ' + d.slice(6, 10);
        el.value = formatted;
      }
    });
  }

  /* ── 16. Semantic Delete Confirmation Dialog (Rule 4) ──────────── */
  function confirmDelete(opts) {
    var o = opts || {};
    var title = o.title || 'Delete Record';
    var desc = o.description || 'Are you sure you want to delete this record?';
    var consequence = o.consequence || 'This action cannot be undone and will permanently remove this record from the system.';
    var confirmLabel = o.confirmLabel || 'Delete Record';
    var cancelLabel = o.cancelLabel || 'Cancel';

    if (global.NGISCancelDialog && typeof global.NGISCancelDialog.open === 'function') {
      global.NGISCancelDialog.open({
        title: title,
        description: desc,
        consequence: consequence,
        confirmLabel: confirmLabel,
        cancelLabel: cancelLabel,
        isDestructive: true,
        onConfirm: o.onConfirm,
        onCancel: o.onCancel
      });
    } else {
      if (window.confirm(title + '\n\n' + desc + '\n\n' + consequence)) {
        if (typeof o.onConfirm === 'function') o.onConfirm();
      } else {
        if (typeof o.onCancel === 'function') o.onCancel();
      }
    }
  }

  /* ── 17. Universal DOM Auto-Enhancer ───────────────────────────── */
  function autoEnhanceUI(root) {
    var scope = root || doc;
    
    // Auto phone masks
    scope.querySelectorAll('input[type="tel"], input[data-phone-mask]').forEach(function (inp) {
      applyPhoneMask(inp);
    });

    // Auto delete confirmation bindings
    scope.querySelectorAll('[data-confirm-delete]').forEach(function (btn) {
      if (btn.dataset.confirmBound) return;
      btn.dataset.confirmBound = '1';
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var itemTitle = btn.getAttribute('data-item-title') || 'this item';
        confirmDelete({
          title: 'Delete ' + itemTitle,
          description: 'Are you sure you want to permanently delete ' + itemTitle + '?',
          consequence: 'This record will be permanently deleted from the database and cannot be recovered.',
          confirmLabel: 'Delete ' + itemTitle,
          onConfirm: function () {
            if (btn.form) {
              btn.form.submit();
            } else if (btn.getAttribute('data-delete-url')) {
              window.location.href = btn.getAttribute('data-delete-url');
            } else {
              var customFn = btn.getAttribute('data-delete-handler');
              if (customFn && typeof global[customFn] === 'function') {
                global[customFn](btn);
              }
            }
          }
        });
      });
    });
  }

  // Auto-run on DOM ready
  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', function () { autoEnhanceUI(doc); });
  } else {
    autoEnhanceUI(doc);
  }

  global.NGISKit = {
    Button: Button,
    Field: Field,
    Badge: Badge,
    Toast: Toast,
    EmptyState: EmptyState,
    Skeleton: Skeleton,
    setButtonLoading: setButtonLoading,
    FormStepper: FormStepper,
    SettingsGroup: SettingsGroup,
    FilterSheet: FilterSheet,
    setFieldError: setFieldError,
    clearFieldError: clearFieldError,
    clearContainerErrors: clearContainerErrors,
    confirmAction: confirmAction,
    createSearchableSelect: createSearchableSelect,
    createMultiSelectChips: createMultiSelectChips,
    applyPhoneMask: applyPhoneMask,
    confirmDelete: confirmDelete,
    autoEnhanceUI: autoEnhanceUI
  };
})(window, document);

