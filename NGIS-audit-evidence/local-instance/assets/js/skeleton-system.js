/**
 * ============================================================
 * NGIS ERP — Global Skeleton Loading System
 * Reusable, responsive, accessible skeleton placeholders.
 * Replaces generic spinners, blocking overlays, and jarring loaders.
 * Zero layout shifts (CLS prevention), prefers-reduced-motion safe.
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

  var NGIS_SKELETON = {
    version: "1.0",

    /* ── Primitive Builders ──────────────────────────────────── */
    text: function (opts) {
      var o = opts || {};
      var w = o.width || "100%";
      var sizeCls = o.size ? " ngis-sk-text-" + o.size : "";
      var cls = "ngis-sk-text ngis-sk-shimmer" + sizeCls + (o.className ? " " + o.className : "");
      return '<span class="' + esc(cls) + '" style="width:' + esc(w) + '" aria-hidden="true"></span>';
    },

    avatar: function (opts) {
      var o = opts || {};
      var sizeCls = o.size ? " ngis-sk-avatar-" + o.size : "";
      var cls = "ngis-sk-avatar ngis-sk-shimmer" + sizeCls + (o.className ? " " + o.className : "");
      return '<span class="' + esc(cls) + '" aria-hidden="true"></span>';
    },

    badge: function (opts) {
      var o = opts || {};
      var w = o.width || "72px";
      var cls = "ngis-sk-badge ngis-sk-shimmer" + (o.className ? " " + o.className : "");
      return '<span class="' + esc(cls) + '" style="width:' + esc(w) + '" aria-hidden="true"></span>';
    },

    button: function (opts) {
      var o = opts || {};
      var w = o.width || "96px";
      var cls = "ngis-sk-btn ngis-sk-shimmer" + (o.className ? " " + o.className : "");
      return '<span class="' + esc(cls) + '" style="width:' + esc(w) + '" aria-hidden="true"></span>';
    },

    /* ── 1. Dashboard Skeleton ───────────────────────────────── */
    dashboard: function (opts) {
      var o = opts || {};
      var cardCount = Math.max(2, Number(o.kpis || 4));
      var kpisHtml = '<div class="ngis-sk-kpi-grid">';
      for (var i = 0; i < cardCount; i++) {
        kpisHtml +=
          '<div class="ngis-sk-kpi-card">' +
            '<div class="flex items-center justify-between">' +
              '<span class="ngis-sk-text ngis-sk-shimmer" style="width:45%;height:12px;"></span>' +
              '<span class="ngis-sk-avatar-sm ngis-sk-shimmer"></span>' +
            '</div>' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:35%;height:28px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:65%;height:10px;"></span>' +
          '</div>';
      }
      kpisHtml += '</div>';

      var mainGridHtml =
        '<div class="ngis-sk-dash-content-grid">' +
          '<div class="ngis-sk-card" style="min-height:280px;">' +
            '<div class="flex items-center justify-between mb-4">' +
              '<span class="ngis-sk-text ngis-sk-shimmer" style="width:30%;height:16px;"></span>' +
              '<span class="ngis-sk-badge ngis-sk-shimmer"></span>' +
            '</div>' +
            '<div class="flex items-end justify-between gap-3 h-44 pt-6 px-4">' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:45%;"></span>' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:70%;"></span>' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:90%;"></span>' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:60%;"></span>' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:80%;"></span>' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:50%;"></span>' +
              '<span class="ngis-sk-shimmer rounded-t-lg w-full" style="height:65%;"></span>' +
            '</div>' +
          '</div>' +
          '<div class="ngis-sk-card" style="min-height:280px;">' +
            '<div class="flex items-center justify-between mb-4">' +
              '<span class="ngis-sk-text ngis-sk-shimmer" style="width:45%;height:16px;"></span>' +
            '</div>' +
            '<div class="flex flex-col gap-3">' +
              '<div class="p-3 rounded-xl border border-slate-100 flex items-center gap-3">' +
                '<span class="ngis-sk-avatar ngis-sk-shimmer"></span>' +
                '<div class="flex-1 flex flex-col gap-1.5">' +
                  '<span class="ngis-sk-text ngis-sk-shimmer" style="width:70%;height:12px;"></span>' +
                  '<span class="ngis-sk-text ngis-sk-shimmer" style="width:40%;height:10px;"></span>' +
                '</div>' +
              '</div>' +
              '<div class="p-3 rounded-xl border border-slate-100 flex items-center gap-3">' +
                '<span class="ngis-sk-avatar ngis-sk-shimmer"></span>' +
                '<div class="flex-1 flex flex-col gap-1.5">' +
                  '<span class="ngis-sk-text ngis-sk-shimmer" style="width:60%;height:12px;"></span>' +
                  '<span class="ngis-sk-text ngis-sk-shimmer" style="width:35%;height:10px;"></span>' +
                '</div>' +
              '</div>' +
              '<div class="p-3 rounded-xl border border-slate-100 flex items-center gap-3">' +
                '<span class="ngis-sk-avatar ngis-sk-shimmer"></span>' +
                '<div class="flex-1 flex flex-col gap-1.5">' +
                  '<span class="ngis-sk-text ngis-sk-shimmer" style="width:65%;height:12px;"></span>' +
                  '<span class="ngis-sk-text ngis-sk-shimmer" style="width:45%;height:10px;"></span>' +
                '</div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>';

      return (
        '<div class="ngis-sk-dashboard-wrap" role="status" aria-busy="true" aria-label="Loading dashboard metrics">' +
          kpisHtml +
          mainGridHtml +
        '</div>'
      );
    },

    /* ── 2. Table & Directory Skeleton ───────────────────────── */
    table: function (opts) {
      var o = opts || {};
      var rowsCount = Math.max(3, Number(o.rows || 6));
      var colsCount = Math.max(3, Number(o.cols || 5));

      var toolbarHtml =
        '<div class="ngis-sk-toolbar">' +
          '<div class="ngis-sk-toolbar-left">' +
            '<span class="ngis-sk-shimmer rounded-xl" style="height:38px;width:260px;"></span>' +
            '<span class="ngis-sk-shimmer rounded-xl hidden sm:block" style="height:38px;width:130px;"></span>' +
            '<span class="ngis-sk-shimmer rounded-xl hidden md:block" style="height:38px;width:110px;"></span>' +
          '</div>' +
          '<div class="ngis-sk-toolbar-right">' +
            '<span class="ngis-sk-shimmer rounded-xl" style="height:38px;width:110px;"></span>' +
          '</div>' +
        '</div>';

      var headHtml =
        '<div class="ngis-sk-table-head">' +
          '<span class="ngis-sk-text ngis-sk-shimmer flex-1" style="max-width:240px;height:12px;"></span>' +
          '<span class="ngis-sk-text ngis-sk-shimmer hidden sm:block w-36" style="height:12px;"></span>' +
          '<span class="ngis-sk-text ngis-sk-shimmer hidden md:block w-28" style="height:12px;"></span>' +
          '<span class="ngis-sk-text ngis-sk-shimmer w-20" style="height:12px;"></span>' +
          '<span class="ngis-sk-text ngis-sk-shimmer w-16 text-right" style="height:12px;"></span>' +
        '</div>';

      var rowsHtml = "";
      for (var i = 0; i < rowsCount; i++) {
        rowsHtml +=
          '<div class="ngis-sk-row">' +
            '<div class="flex items-center gap-3 flex-1 min-w-[180px]">' +
              '<span class="ngis-sk-avatar ngis-sk-shimmer"></span>' +
              '<div class="flex flex-col gap-1.5 flex-1">' +
                '<span class="ngis-sk-text ngis-sk-shimmer" style="width:' + (55 + (i % 3) * 15) + '%;height:13px;"></span>' +
                '<span class="ngis-sk-text ngis-sk-shimmer" style="width:30%;height:10px;"></span>' +
              '</div>' +
            '</div>' +
            '<span class="ngis-sk-text ngis-sk-shimmer hidden sm:block w-36" style="height:12px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer hidden md:block w-28" style="height:12px;"></span>' +
            '<span class="ngis-sk-badge ngis-sk-shimmer w-20"></span>' +
            '<div class="flex items-center justify-end gap-2 w-16">' +
              '<span class="ngis-sk-shimmer rounded-lg w-7 h-7"></span>' +
              '<span class="ngis-sk-shimmer rounded-lg w-7 h-7"></span>' +
            '</div>' +
          '</div>';
      }

      var paginationHtml =
        '<div class="ngis-sk-pagination">' +
          '<span class="ngis-sk-text ngis-sk-shimmer" style="width:140px;height:12px;"></span>' +
          '<div class="flex items-center gap-2">' +
            '<span class="ngis-sk-shimmer rounded-xl w-24 h-8"></span>' +
            '<span class="ngis-sk-shimmer rounded-xl w-24 h-8"></span>' +
          '</div>' +
        '</div>';

      return (
        '<div class="ngis-sk-table-container" role="status" aria-busy="true" aria-label="Loading table records">' +
          toolbarHtml +
          headHtml +
          rowsHtml +
          paginationHtml +
        '</div>'
      );
    },

    /* ── 3. Form Skeleton ────────────────────────────────────── */
    form: function (opts) {
      var o = opts || {};
      var fieldCount = Math.max(2, Number(o.fields || 6));
      var fieldsHtml = '<div class="ngis-sk-form-grid">';
      for (var i = 0; i < fieldCount; i++) {
        fieldsHtml +=
          '<div class="ngis-sk-field-group">' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:30%;height:12px;"></span>' +
            '<span class="ngis-sk-shimmer rounded-xl w-full" style="height:42px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:45%;height:10px;"></span>' +
          '</div>';
      }
      fieldsHtml += '</div>';

      return (
        '<div class="ngis-sk-form-container" role="status" aria-busy="true" aria-label="Loading form details">' +
          '<div class="flex flex-col gap-2 pb-4 border-b border-slate-100">' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:35%;height:18px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer" style="width:60%;height:12px;"></span>' +
          '</div>' +
          fieldsHtml +
          '<div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">' +
            '<span class="ngis-sk-shimmer rounded-xl w-24 h-10"></span>' +
            '<span class="ngis-sk-shimmer rounded-xl w-32 h-10"></span>' +
          '</div>' +
        '</div>'
      );
    },

    /* ── 4. Profile Skeleton ─────────────────────────────────── */
    profile: function (opts) {
      return (
        '<div class="w-full flex flex-col gap-6" role="status" aria-busy="true" aria-label="Loading profile records">' +
          '<div class="ngis-sk-profile-header">' +
            '<span class="ngis-sk-avatar-lg ngis-sk-shimmer"></span>' +
            '<div class="ngis-sk-profile-meta">' +
              '<div class="flex items-center gap-3">' +
                '<span class="ngis-sk-text ngis-sk-shimmer" style="width:200px;height:20px;"></span>' +
                '<span class="ngis-sk-badge ngis-sk-shimmer"></span>' +
              '</div>' +
              '<span class="ngis-sk-text ngis-sk-shimmer" style="width:260px;height:12px;"></span>' +
              '<div class="flex items-center gap-4 pt-1">' +
                '<span class="ngis-sk-text ngis-sk-shimmer" style="width:100px;height:11px;"></span>' +
                '<span class="ngis-sk-text ngis-sk-shimmer" style="width:120px;height:11px;"></span>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center gap-3 border-b border-slate-200 pb-2 px-1">' +
            '<span class="ngis-sk-shimmer rounded-lg w-24 h-7"></span>' +
            '<span class="ngis-sk-shimmer rounded-lg w-24 h-7"></span>' +
            '<span class="ngis-sk-shimmer rounded-lg w-24 h-7"></span>' +
          '</div>' +
          NGIS_SKELETON.form({ fields: 4 }) +
        '</div>'
      );
    },

    /* ── 5. Cards & Content Grid Skeleton ────────────────────── */
    cards: function (opts) {
      var o = opts || {};
      var count = Math.max(1, Number(o.count || 6));
      var cardsHtml = '<div class="ngis-sk-card-grid">';
      for (var i = 0; i < count; i++) {
        cardsHtml +=
          '<div class="ngis-sk-card" style="min-height:220px;">' +
            '<span class="ngis-sk-shimmer rounded-xl w-full mb-3" style="height:110px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer mb-2" style="width:75%;height:15px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer mb-1" style="width:90%;height:11px;"></span>' +
            '<span class="ngis-sk-text ngis-sk-shimmer mb-4" style="width:60%;height:11px;"></span>' +
            '<div class="flex items-center justify-between mt-auto pt-2 border-t border-slate-100">' +
              '<span class="ngis-sk-badge ngis-sk-shimmer"></span>' +
              '<span class="ngis-sk-btn ngis-sk-shimmer" style="width:70px;height:30px;"></span>' +
            '</div>' +
          '</div>';
      }
      cardsHtml += '</div>';

      return (
        '<div class="w-full" role="status" aria-busy="true" aria-label="Loading content items">' +
          cardsHtml +
        '</div>'
      );
    },

    /* ── 6. Smart Rendering & Wrapping API ───────────────────── */
    render: function (container, type, opts) {
      var el = typeof container === "string" ? doc.querySelector(container) : container;
      if (!el) return;
      var builder = NGIS_SKELETON[type] || NGIS_SKELETON.table;
      el.setAttribute("aria-busy", "true");
      el.dataset.skeletonActive = "true";
      el.innerHTML = builder(opts);
    },

    wrap: function (container, fetchPromise, renderContentFn, type, opts) {
      var el = typeof container === "string" ? doc.querySelector(container) : container;
      if (!el) return;

      NGIS_SKELETON.render(el, type, opts);

      if (!fetchPromise || typeof fetchPromise.then !== "function") {
        return;
      }

      fetchPromise
        .then(function (data) {
          el.removeAttribute("aria-busy");
          delete el.dataset.skeletonActive;
          if (typeof renderContentFn === "function") {
            renderContentFn(data, el);
          }
        })
        .catch(function (err) {
          el.removeAttribute("aria-busy");
          delete el.dataset.skeletonActive;
          var errMsg = (err && err.message) || "We could not load this content right now. Your data is safe.";
          el.innerHTML =
            '<div class="p-8 text-center bg-white border border-[#E1E9E3] rounded-2xl my-4">' +
              '<div class="w-12 h-12 rounded-full bg-red-50 text-red-600 flex items-center justify-center mx-auto mb-3">' +
                '<span class="material-symbols-outlined text-2xl">error</span>' +
              '</div>' +
              '<h4 class="text-sm font-medium text-[#29352E] mb-1">Could not load content</h4>' +
              '<p class="text-xs text-[#64746A] max-w-sm mx-auto mb-4">' + esc(errMsg) + '</p>' +
              '<button type="button" class="btn btn-primary" data-sk-retry>' +
                '<span class="material-symbols-outlined text-sm">refresh</span>' +
                '<span>Try Again</span>' +
              '</button>' +
            '</div>';

          var retryBtn = el.querySelector("[data-sk-retry]");
          if (retryBtn) {
            retryBtn.onclick = function () {
              if (opts && typeof opts.onRetry === "function") {
                opts.onRetry();
              } else {
                location.reload();
              }
            };
          }
        });
    },

    /* ── 7. Auto-Upgrader for Legacy Loading Spinners ────────── */
    autoUpgradeLegacySpinners: function () {
      try {
        // Upgrade admin-system fallback blocks
        doc.querySelectorAll(".flex.items-center.justify-center.py-16, .flex.items-center.justify-center.py-20, .flex.items-center.justify-center.py-24").forEach(function (block) {
          if (block.querySelector(".animate-spin, .animate-ping")) {
            var parent = block.parentElement;
            if (parent && !parent.dataset.skUpgraded) {
              parent.dataset.skUpgraded = "true";
              var isForm = parent.id && parent.id.indexOf("setting") !== -1;
              block.outerHTML = isForm ? NGIS_SKELETON.form({ fields: 6 }) : NGIS_SKELETON.table({ rows: 5 });
            }
          }
        });

        // Upgrade legacy CMS loading boxes
        doc.querySelectorAll(".cms-loading").forEach(function (cmsBox) {
          if (!cmsBox.dataset.skUpgraded) {
            cmsBox.dataset.skUpgraded = "true";
            cmsBox.outerHTML = NGIS_SKELETON.table({ rows: 3 });
          }
        });
      } catch (e) {
        // Safe fallback
      }
    }
  };

  /* Expose globally and on NGISKit */
  global.NGIS_SKELETON = NGIS_SKELETON;
  if (global.NGISKit) {
    global.NGISKit.Skeleton = NGIS_SKELETON;
  }

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", NGIS_SKELETON.autoUpgradeLegacySpinners);
  } else {
    NGIS_SKELETON.autoUpgradeLegacySpinners();
  }
})(window, document);

