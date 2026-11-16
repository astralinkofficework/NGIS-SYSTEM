/* ============================================================
   NGIS Shared Components — vanilla JS UI helpers
   Toast, confirm dialog, modal shell, dropdown initialization.
   No framework. Works alongside layout.js.
   ============================================================ */
(function () {
  "use strict";

  var doc = document;

  /* ── Escape helper ── */
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ── Ensure a container exists ── */
  function ensureContainer(id, cls, html) {
    var el = doc.getElementById(id);
    if (el) return el;
    el = doc.createElement("div");
    el.id = id;
    el.className = cls;
    el.innerHTML = html;
    doc.body.appendChild(el);
    return el;
  }

  /* ── Toast ── */
  var TOAST_ICONS = { success: "check_circle", error: "error", warning: "warning", info: "info" };
  var TOAST_COLOR = { success: "success", error: "danger", warning: "warning", info: "primary" };

  window.ngisToast = function (msg, kind, detail, options) {
    kind = kind || "info";
    options = options || {};
    var wrap = ensureContainer("ngisToastContainer", "", "");
    var color = TOAST_COLOR[kind] || "primary";
    var icon = TOAST_ICONS[kind] || TOAST_ICONS.info;
    var t = doc.createElement("div");
    t.className = "ngis-toast " + kind;
    t.setAttribute("role", "alert");
    t.setAttribute("aria-live", "polite");
    t.innerHTML =
      '<span class="material-symbols-outlined ngis-toast-icon" aria-hidden="true">' + esc(icon) + '</span>' +
      '<div class="ngis-toast-body">' +
      '<div class="ngis-toast-title">' + esc(msg) + '</div>' +
      (detail ? '<div class="ngis-toast-detail">' + esc(detail) + '</div>' : "") +
      "</div>" +
      '<button class="ngis-toast-close" aria-label="Dismiss" type="button">&times;</button>';
    wrap.appendChild(t);
    var closeBtn = t.querySelector(".ngis-toast-close");
    closeBtn.addEventListener("click", function () { dismissToast(t); });
    setTimeout(function () { dismissToast(t); }, options.duration !== undefined ? options.duration : 3000);
    return t;
  };

  function dismissToast(el) {
    if (!el || !el.parentNode) return;
    el.style.opacity = "0";
    el.style.transition = "opacity 220ms ease";
    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 220);
  }

  /* Keep the legacy window.toast working via the new component */
  window.toast = function (msg, kind, detail, options) {
    return window.ngisToast(msg, kind, detail, options);
  };

  /* ── Confirm dialog ── */
  function confirmDialog(options) {
    options = options || {};
    var kind = options.kind || "neutral"; // neutral | danger | warning | success | info
    var title = esc(options.title || "Confirm");
    var desc = esc(options.description || "");
    var confirmLabel = esc(options.confirmLabel || "Confirm");
    var cancelLabel = esc(options.cancelLabel || "Cancel");
    var confirmClass = options.confirmClass || "btn-" + (kind === "danger" ? "danger" : kind === "warning" ? "warning" : kind === "success" ? "success" : "primary");
    var overlay = doc.createElement("div");
    overlay.className = "modal-overlay confirm-dialog confirm-dialog--" + kind;
    overlay.innerHTML =
      '<div class="modal" role="dialog" aria-modal="true" aria-labelledby="confirmTitle">' +
      '<div class="modal-body">' +
      '<div class="confirm-icon" aria-hidden="true">' +
      (kind === "danger" ? "delete" : kind === "warning" ? "warning" : kind === "success" ? "check_circle" : "info") +
      "</div>" +
      '<h3 class="confirm-title" id="confirmTitle">' + title + "</h3>" +
      (desc ? '<p class="confirm-desc">' + desc + "</p>" : "") +
      "</div>" +
      '<div class="modal-footer">' +
      '<button type="button" class="btn btn-ghost confirm-cancel">' + cancelLabel + "</button>" +
      '<button type="button" class="btn ' + confirmClass + ' confirm-confirm">' + confirmLabel + "</button>" +
      "</div>" +
      "</div>" +
      "</div>";
    doc.body.appendChild(overlay);
    overlay.classList.add("open");

    return new Promise(function (resolve) {
      var cleanup = function () {
        overlay.classList.remove("open");
        setTimeout(function () {
          if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
        }, 220);
      };
      var cancelBtn = overlay.querySelector(".confirm-cancel");
      var confirmBtn = overlay.querySelector(".confirm-confirm");
      var onKey = function (e) {
        if (e.key === "Escape") { resolve(false); teardown(); }
        if (e.key === "Enter") { resolve(true); teardown(); }
      };
      doc.addEventListener("keydown", onKey);
      function teardown() {
        doc.removeEventListener("keydown", onKey);
        cancelBtn.removeEventListener("click", onCancel);
        confirmBtn.removeEventListener("click", onConfirm);
        cleanup();
      }
      function onCancel() { resolve(false); teardown(); }
      function onConfirm() { resolve(true); teardown(); }
      cancelBtn.addEventListener("click", onCancel);
      confirmBtn.addEventListener("click", onConfirm);
      overlay.addEventListener("click", function (e) {
        if (e.target === overlay) { resolve(false); teardown(); }
      });
    });
  }
  window.ngisConfirm = confirmDialog;

  /* ── Generic modal ── */
  window.ngisModal = function (options) {
    options = options || {};
    var overlay = doc.createElement("div");
    overlay.className = "modal-overlay";
    var footerHtml = "";
    if (options.footer) {
      footerHtml = '<div class="modal-footer">' + options.footer + "</div>";
    }
    overlay.innerHTML =
      '<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle">' +
      '<div class="modal-header">' +
      '<h3 class="modal-title" id="modalTitle">' + esc(options.title || "") + "</h3>" +
      '<button type="button" class="modal-close" aria-label="Close">&times;</button>' +
      "</div>" +
      '<div class="modal-body">' + (options.body || "") + "</div>" +
      footerHtml +
      "</div>" +
      "</div>";
    doc.body.appendChild(overlay);
    overlay.classList.add("open");

    var close = function () {
      overlay.classList.remove("open");
      setTimeout(function () {
        if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
      }, 220);
    };
    overlay.querySelector(".modal-close").addEventListener("click", close);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) close();
    });
    doc.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    return { element: overlay, close: close };
  };

  /* ── Dropdown (custom select) initialization ── */
  window.ngisDropdown = function (triggerSelector) {
    doc.querySelectorAll(triggerSelector || ".select-trigger").forEach(function (trigger) {
      var wrap = trigger.closest(".select-wrap");
      if (!wrap) return;
      var menu = wrap.querySelector(".select-menu");
      var valueEl = trigger.querySelector(".select-value");
      var chevron = trigger.querySelector(".select-chevron");
      var input = wrap.querySelector('input[type="hidden"]');
      var search = wrap.querySelector(".select-search");
      var options = Array.prototype.slice.call(menu.querySelectorAll(".select-option"));

      function setValue(val, label) {
        trigger.setAttribute("aria-checked", "true");
        if (valueEl) valueEl.textContent = label;
        if (input) input.value = val;
        options.forEach(function (o) {
          o.setAttribute("data-selected", o.getAttribute("data-value") === val ? "true" : "false");
        });
      }

      function open() {
        doc.querySelectorAll(".select-menu.open").forEach(function (m) { m.classList.remove("open"); });
        menu.classList.add("open");
        trigger.setAttribute("aria-expanded", "true");
        positionMenu();
        if (search) { search.focus(); search.value = ""; filterOptions(""); }
        doc.addEventListener("click", onDocClick);
      }
      function close() {
        menu.classList.remove("open");
        trigger.setAttribute("aria-expanded", "false");
        doc.removeEventListener("click", onDocClick);
      }
      function toggle() { return menu.classList.contains("open") ? close() : open(); }

      trigger.addEventListener("click", function (e) { e.stopPropagation(); toggle(); });
      trigger.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(); }
        if (e.key === "Escape") close();
      });

      options.forEach(function (o) {
        o.addEventListener("click", function (e) {
          e.stopPropagation();
          var val = o.getAttribute("data-value");
          var label = o.textContent.trim();
          setValue(val, label);
          close();
          if (trigger.onchange) trigger.onchange(val);
        });
        o.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); o.click(); }
          if (e.key === "Escape") { close(); trigger.focus(); }
        });
      });

      if (search) {
        search.addEventListener("input", function (e) { filterOptions(e.target.value); });
      }

      function filterOptions(q) {
        q = (q || "").toLowerCase();
        var any = false;
        options.forEach(function (o) {
          var show = o.textContent.toLowerCase().indexOf(q) !== -1;
          o.style.display = show ? "" : "none";
          if (show) any = true;
        });
        var nr = wrap.querySelector(".select-no-results");
        if (nr) {
          if (!any) {
            nr.style.display = "";
            nr.textContent = "No results";
          } else {
            nr.style.display = "none";
          }
        }
      }

      function positionMenu() {
        var rect = trigger.getBoundingClientRect();
        var spaceBelow = window.innerHeight - rect.bottom - 8;
        var spaceAbove = rect.top - 8;
        if (spaceBelow < 180 && spaceAbove > spaceBelow) {
          menu.style.top = "";
          menu.style.bottom = (window.innerHeight - rect.top + 8) + "px";
          menu.classList.add("menu-up");
        } else {
          menu.style.bottom = "";
          menu.style.top = (rect.bottom + 6) + "px";
          menu.classList.remove("menu-up");
        }
        menu.style.left = rect.left + "px";
        menu.style.width = rect.width + "px";
      }

      function onDocClick(e) {
        if (!wrap.contains(e.target)) close();
      }

      // Initialize selected value from data attribute
      var selected = menu.querySelector('.select-option[data-selected="true"]');
      if (selected && valueEl) {
        valueEl.textContent = selected.textContent.trim();
        if (input) input.value = selected.getAttribute("data-value");
      }
    });
  };

  /* Reposition open dropdowns on resize/scroll */
  window.addEventListener("resize", function () {
    doc.querySelectorAll(".select-menu.open").forEach(function (m) {
      var trigger = m.closest(".select-wrap").querySelector(".select-trigger");
      if (trigger) {
        var rect = trigger.getBoundingClientRect();
        m.style.left = rect.left + "px";
        m.style.width = rect.width + "px";
      }
    });
  });

  /* ── Show More / Show Less (Part 13) ── */
  window.ngisShowMore = function (containerSelector) {
    doc.querySelectorAll(containerSelector || ".show-more-wrap").forEach(function (wrap) {
      var btn = wrap.querySelector(".show-more-btn");
      if (!btn || wrap.dataset.smInitialized) return;
      wrap.dataset.smInitialized = "true";
      var content = wrap.querySelector(".show-more-content") || wrap;
      var maxH = wrap.style.maxHeight || "";
      var expanded = false;

      function update() {
        var cs = window.getComputedStyle(content);
        var contentHeight = content.scrollHeight;
        var wrapHeight = wrap.clientHeight;
        var shouldClamp = contentHeight > wrapHeight + 2;
        var show = wrap.dataset.smShow === "true";
        if (!shouldClamp) {
          btn.style.display = "none";
          wrap.style.maxHeight = "";
          wrap.classList.remove("expanded");
          return;
        }
        btn.style.display = "";
        if (!show) {
          wrap.classList.remove("expanded");
          wrap.style.maxHeight = "7.5em";
          wrap.setAttribute("aria-expanded", "false");
          btn.textContent = "Show More";
        } else {
          wrap.classList.add("expanded");
          wrap.style.maxHeight = "";
          wrap.setAttribute("aria-expanded", "true");
          btn.textContent = "Show Less";
        }
      }

      btn.setAttribute("aria-expanded", "false");
      btn.type = "button";
      btn.addEventListener("click", function () {
        expanded = !expanded;
        wrap.dataset.smShow = String(expanded);
        wrap.setAttribute("aria-expanded", String(expanded));
        wrap.classList.toggle("expanded", expanded);
        if (expanded) { wrap.style.maxHeight = ""; btn.textContent = "Show Less"; }
        else { wrap.style.maxHeight = "7.5em"; btn.textContent = "Show More"; }
      });

      update();
      window.addEventListener("resize", update);
    });
  };

  /* Auto-init on DOM ready */
  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", function () {
      window.ngisDropdown();
      window.ngisShowMore();
    });
  } else {
    window.ngisDropdown();
    window.ngisShowMore();
  }

})();
