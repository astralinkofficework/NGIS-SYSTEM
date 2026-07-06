/* ============================================================
   NGIS App.js — Interactive Layer
   Auto-loaded by layout.js after mount. Wires:
     1. Attendance P/L/A toggle groups
     2. Live table search
     3. Editable grade cells with auto-recalc
     4. Form field localStorage persistence
     5. Table row selection highlight
     6. Sortable table columns
   ============================================================ */
(function () {
  "use strict";

  /* ── tiny store ── */
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch(e) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch(e) {} },
    del: k => { try { localStorage.removeItem(k); } catch(e) {} },
  };

  const pageKey = window.location.pathname.split("/").pop().replace(".html","") || "index";

  /* ── inject dynamic CSS once ── */
  function injectCSS() {
    if (document.getElementById("ngis-app-css")) return;
    const s = document.createElement("style");
    s.id = "ngis-app-css";
    s.textContent = `
      .row-sel { background: var(--accent-soft) !important; }
      .tbl tbody tr { cursor: pointer; }
      .tbl th[data-sort] { cursor: pointer; user-select: none; }
      .tbl th[data-sort]:hover { color: var(--accent); }
      .tbl th[data-sort]::after { content: " ↕"; opacity: .35; font-size: .7em; }
      .tbl th[data-sort].asc::after  { content: " ↑"; opacity: 1; color: var(--accent); }
      .tbl th[data-sort].desc::after { content: " ↓"; opacity: 1; color: var(--accent); }
      .grade-input { width:56px; text-align:center; border:1px solid var(--border);
        border-radius:6px; padding:4px 6px; font-size:13px; font-family:inherit;
        background:var(--surface); color:var(--text); outline:none; }
      .grade-input:focus { border-color:var(--accent); box-shadow:0 0 0 3px var(--accent-soft); }
      .attend-row { transition: background .15s; }
      .attend-row.present-row { background: #f0fdf4; }
      .attend-row.late-row    { background: #fffbeb; }
      .attend-row.absent-row  { background: #fef2f2; }
      [data-theme="dark"] .attend-row.present-row { background: rgba(34,197,94,.07); }
      [data-theme="dark"] .attend-row.late-row    { background: rgba(234,179, 8,.07); }
      [data-theme="dark"] .attend-row.absent-row  { background: rgba(239, 68,68,.07); }
    `;
    document.head.appendChild(s);
  }

  /* ══════════════════════════════════════════════════
     1. ATTENDANCE TOGGLE GROUPS
     Detects any flex container holding 3 buttons
     with text Present / Late / Absent.
     ══════════════════════════════════════════════════ */
  function wireAttendance() {
    const groups = [];

    document.querySelectorAll("div").forEach(div => {
      const btns = Array.from(div.children).filter(c => c.tagName === "BUTTON");
      if (btns.length !== 3) return;
      const texts = btns.map(b => b.textContent.trim());
      if (!texts.includes("Present") || !texts.includes("Late") || !texts.includes("Absent")) return;
      groups.push({ div, btns });
    });

    groups.forEach(({ div, btns }) => {
      const row = div.closest("[style*='border-radius:10px'], [style*='border-radius: 10px']");

      function activate(btn) {
        const status = btn.textContent.trim();

        /* reset all 3 */
        btns.forEach(b => {
          b.style.background = "";
          b.style.color      = "";
          b.style.border     = "";
          b.classList.remove("btn-primary");
          b.classList.add("btn-ghost");
        });

        /* style the active one */
        btn.classList.remove("btn-ghost");
        let rowCls = "";
        if (status === "Present") {
          btn.style.background = "var(--success)";
          btn.style.color      = "#fff";
          rowCls = "present-row";
        } else if (status === "Late") {
          btn.style.background = "var(--warning)";
          btn.style.color      = "#fff";
          rowCls = "late-row";
        } else {
          btn.style.background = "var(--danger)";
          btn.style.color      = "#fff";
          rowCls = "absent-row";
        }

        /* row highlight */
        if (row) {
          row.classList.remove("attend-row", "present-row", "late-row", "absent-row");
          row.classList.add("attend-row", rowCls);
        }

        /* persist */
        const name = row ? (row.querySelector("b")?.textContent?.trim() || "") : "";
        store.set(`${pageKey}-attend-${name}`, status);

        /* toast */
        if (window.toast) window.toast(`${name || "Student"} marked ${status}`, status === "Present" ? "success" : status === "Late" ? "warning" : "error");
      }

      btns.forEach(btn => {
        btn.onclick = null;          /* strip inline handler */
        btn.addEventListener("click", () => activate(btn));
      });

      /* restore saved state */
      const name = row ? (row.querySelector("b")?.textContent?.trim() || "") : "";
      const saved = store.get(`${pageKey}-attend-${name}`);
      if (saved) {
        const match = btns.find(b => b.textContent.trim() === saved);
        if (match) activate(match);
      } else {
        /* keep pre-existing visual state but mark the active btn */
        const alreadyActive = btns.find(b => b.style.background && !b.classList.contains("btn-ghost"));
        if (alreadyActive) {
          /* just ensure the row class is set */
          const status = alreadyActive.textContent.trim();
          if (row) {
            row.classList.add("attend-row", status === "Present" ? "present-row" : status === "Late" ? "late-row" : "absent-row");
          }
        }
      }
    });

    /* "Mark All Present" button */
    document.querySelectorAll("button").forEach(btn => {
      if (!btn.textContent.includes("Mark All Present")) return;
      btn.onclick = null;
      btn.addEventListener("click", () => {
        groups.forEach(({ btns }) => {
          const presentBtn = btns.find(b => b.textContent.trim() === "Present");
          if (presentBtn) presentBtn.click();
        });
        /* don't double-toast — group clicks already toasted per student */
      });
    });

    /* Attendance stats updater — refresh summary card numbers */
    wireAttendanceSummary(groups);
  }

  function wireAttendanceSummary(groups) {
    function refresh() {
      let p = 0, l = 0, a = 0;
      groups.forEach(({ btns }) => {
        btns.forEach(btn => {
          if (btn.style.background === "var(--success)") p++;
          else if (btn.style.background === "var(--warning)") l++;
          else if (btn.style.background === "var(--danger)")  a++;
        });
      });
      /* Try to update stat cards labelled Present/Late/Absent */
      document.querySelectorAll(".stat").forEach(stat => {
        const lbl = stat.querySelector(".stat-label")?.textContent?.toLowerCase() || "";
        const val = stat.querySelector(".stat-val");
        if (!val) return;
        if (lbl.includes("present")) val.textContent = p;
        else if (lbl.includes("late"))    val.textContent = l;
        else if (lbl.includes("absent"))  val.textContent = a;
      });
    }
    groups.forEach(({ div }) => div.addEventListener("click", () => setTimeout(refresh, 50)));
  }

  /* ══════════════════════════════════════════════════
     2. LIVE TABLE SEARCH
     Any input[placeholder*="search"] (case-insensitive)
     near a <table> gets auto-wired.
     ══════════════════════════════════════════════════ */
  function wireSearch() {
    document.querySelectorAll("input").forEach(input => {
      if (input.type === "checkbox" || input.type === "radio" || input.type === "password") return;
      const ph = (input.placeholder || "").toLowerCase();
      if (!ph.includes("search") && input.type !== "search") return;

      /* find nearest table — walk up DOM tree */
      let tbl = null;
      let el = input.parentElement;
      for (let i = 0; i < 8 && el && !tbl; i++) {
        tbl = el.querySelector("table");
        el = el.parentElement;
      }
      if (!tbl) return;

      let noResultRow = null;

      input.addEventListener("input", () => {
        const q = input.value.toLowerCase().trim();
        let visible = 0;
        tbl.querySelectorAll("tbody tr").forEach(row => {
          if (row === noResultRow) return;
          const match = !q || row.textContent.toLowerCase().includes(q);
          row.style.display = match ? "" : "none";
          if (match) visible++;
        });

        /* no-result placeholder */
        if (!noResultRow) {
          noResultRow = document.createElement("tr");
          noResultRow.innerHTML = `<td colspan="20" style="text-align:center;padding:24px;color:var(--muted);font-size:13px">
            <span class="material-symbols-outlined" style="font-size:32px;display:block;margin-bottom:8px;opacity:.4">search_off</span>
            No matching records found
          </td>`;
          noResultRow.style.display = "none";
          tbl.querySelector("tbody").appendChild(noResultRow);
        }
        noResultRow.style.display = visible === 0 && q ? "" : "none";
      });
    });
  }

  /* ══════════════════════════════════════════════════
     3. EDITABLE GRADE CELLS
     Converts <input> elements inside .tbl cells into
     styled number inputs; recalculates average + badge.
     ══════════════════════════════════════════════════ */
  function wireGrades() {
    document.querySelectorAll(".tbl tbody tr").forEach(row => {
      const inputs = row.querySelectorAll("td input");
      if (inputs.length === 0) return;

      inputs.forEach(input => {
        input.classList.add("grade-input");
        input.type = "number";
        input.min  = "0";
        input.max  = "100";
        input.addEventListener("input", () => recalcRow(row));
        input.addEventListener("focus", () => input.select());
      });
    });
  }

  function recalcRow(row) {
    const inputs = Array.from(row.querySelectorAll("td input.grade-input"));
    const vals   = inputs.map(i => parseFloat(i.value)).filter(v => !isNaN(v) && v >= 0);
    if (vals.length === 0) return;

    /* simple average — in a real app weights would apply */
    const avg = vals.reduce((a, b) => a + b, 0) / vals.length;

    /* update average cell — usually 2nd-to-last td */
    const cells = Array.from(row.querySelectorAll("td"));
    const avgCell = cells[cells.length - 2];
    if (avgCell && !avgCell.querySelector("input") && !avgCell.querySelector(".badge")) {
      avgCell.textContent = avg.toFixed(1) + "%";
    }

    /* update grade badge */
    const badge = row.querySelector(".badge");
    if (!badge) return;
    let grade, cls;
    if      (avg >= 93) { grade = "A+";  cls = "green";  }
    else if (avg >= 85) { grade = "A";   cls = "green";  }
    else if (avg >= 77) { grade = "B+";  cls = "blue";   }
    else if (avg >= 70) { grade = "B";   cls = "blue";   }
    else if (avg >= 60) { grade = "C";   cls = "amber";  }
    else                { grade = "D";   cls = "red";    }
    badge.textContent = grade;
    badge.className   = `badge ${cls}`;
  }

  /* ══════════════════════════════════════════════════
     4. FORM FIELD PERSISTENCE
     Saves / restores all named or id'd form fields
     (excluding passwords, checkboxes) to localStorage.
     ══════════════════════════════════════════════════ */
  function wireFormPersist() {
    document.querySelectorAll("input, select, textarea").forEach(field => {
      if (["password","checkbox","radio","search","file"].includes(field.type)) return;
      const id = field.name || field.id;
      if (!id) return;
      const key = `ngis-${pageKey}-${id}`;
      /* restore */
      const saved = store.get(key);
      if (saved !== null) {
        if (field.tagName === "SELECT") {
          const opt = field.querySelector(`option[value="${saved}"]`);
          if (opt) opt.selected = true;
        } else if (field.value === (field.defaultValue || "")) {
          field.value = saved;
        }
      }
      /* save on change */
      field.addEventListener("change", () => store.set(key, field.value));
    });
  }

  /* ══════════════════════════════════════════════════
     5. TABLE ROW SELECTION
     Click a row to highlight it; click again to deselect.
     ══════════════════════════════════════════════════ */
  function wireRowSelect() {
    document.querySelectorAll(".tbl tbody").forEach(tbody => {
      tbody.querySelectorAll("tr").forEach(row => {
        row.addEventListener("click", e => {
          if (e.target.closest("button, a, input, select, label, .badge")) return;
          const was = row.classList.contains("row-sel");
          tbody.querySelectorAll("tr").forEach(r => r.classList.remove("row-sel"));
          if (!was) row.classList.add("row-sel");
        });
      });
    });
  }

  /* ══════════════════════════════════════════════════
     6. SORTABLE TABLE COLUMNS
     Add data-sort to <th> elements to make them
     click-to-sort. Auto-detects header text.
     ══════════════════════════════════════════════════ */
  function wireTableSort() {
    document.querySelectorAll(".tbl thead tr").forEach(headerRow => {
      const ths = Array.from(headerRow.querySelectorAll("th"));
      ths.forEach((th, colIdx) => {
        /* skip action columns (no text / icons only) */
        if (!th.textContent.trim() || th.querySelector("input")) return;
        th.setAttribute("data-sort", "none");
        th.addEventListener("click", () => {
          const tbl   = th.closest("table");
          const tbody = tbl.querySelector("tbody");
          const rows  = Array.from(tbody.querySelectorAll("tr:not([colspan])"));
          if (rows.length === 0) return;

          const dir = th.classList.contains("asc") ? "desc" : "asc";
          ths.forEach(h => h.classList.remove("asc","desc"));
          th.classList.add(dir);

          rows.sort((a, b) => {
            const aText = (a.cells[colIdx]?.textContent || "").trim().toLowerCase();
            const bText = (b.cells[colIdx]?.textContent || "").trim().toLowerCase();
            const aNum  = parseFloat(aText);
            const bNum  = parseFloat(bText);
            let cmp;
            if (!isNaN(aNum) && !isNaN(bNum)) cmp = aNum - bNum;
            else cmp = aText.localeCompare(bText);
            return dir === "asc" ? cmp : -cmp;
          });

          rows.forEach(r => tbody.appendChild(r));
        });
      });
    });
  }

  /* ══════════════════════════════════════════════════
     7. TOPBAR SEARCH — Search across page content
     ══════════════════════════════════════════════════ */
  function wireGlobalSearch() {
    const searchInput = document.querySelector(".search input");
    if (!searchInput) return;

    searchInput.addEventListener("input", () => {
      const q = searchInput.value.toLowerCase().trim();
      if (!q) {
        document.querySelectorAll(".tbl tbody tr").forEach(r => r.style.display = "");
        return;
      }
      /* highlight matching rows across all tables */
      let found = 0;
      document.querySelectorAll(".tbl tbody tr").forEach(row => {
        const match = row.textContent.toLowerCase().includes(q);
        row.style.display = match ? "" : "none";
        if (match) found++;
      });
    });

    /* Clear on Escape */
    searchInput.addEventListener("keydown", e => {
      if (e.key === "Escape") {
        searchInput.value = "";
        document.querySelectorAll(".tbl tbody tr").forEach(r => r.style.display = "");
        searchInput.blur();
      }
    });
  }

  /* ══════════════════════════════════════════════════
     8. FIX HARDCODED INLINE COLORS → CSS CLASSES
     Replaces hardcoded hex backgrounds/borders on
     notification/announcement cards so dark mode works.
     ══════════════════════════════════════════════════ */
  const COLOR_MAP = [
    { test: ["#dbeafe", "#bfdbfe", "#93c5fd"], cls: "notif-blue"   },
    { test: ["#fef3c7", "#fde68a", "#fcd34d"], cls: "notif-amber"  },
    { test: ["#dcfce7", "#bbf7d0", "#86efac"], cls: "notif-green"  },
    { test: ["#fee2e2", "#fecaca", "#fca5a5"], cls: "notif-red"    },
    { test: ["#ede9fe", "#ddd6fe", "#c4b5fd"], cls: "notif-purple" },
  ];

  function fixInlineColors() {
    document.querySelectorAll("[style]").forEach(el => {
      const raw = el.getAttribute("style") || "";
      if (!raw.includes("#")) return;

      for (const { test, cls } of COLOR_MAP) {
        if (test.some(c => raw.toLowerCase().includes(c.toLowerCase()))) {
          /* Preserve padding, border-radius, and other props; strip only background + border colors */
          el.style.background  = "";
          el.style.backgroundColor = "";
          el.style.borderColor = "";
          /* If the inline border was like border:1px solid #xxx, reset it to just width+style */
          if (/border:\s*1px solid #/.test(raw)) {
            el.style.border = "";
          }
          el.classList.add("notif-card", cls);

          /* Replace hardcoded unread dot colors too */
          el.querySelectorAll("[style*='background:#3b82f6'],[style*='background:#d97706'],[style*='background:#22c55e']").forEach(dot => {
            if (dot.style.width === "8px" || dot.style.borderRadius === "50%") {
              dot.style.background = "";
              dot.classList.add("unread-dot");
            }
          });
          break;
        }
      }
    });
  }

  /* ══════════════════════════════════════════════════
     9. TIMETABLE / MULTI-COL GRID → horizontal scroll
     Any card-pad that contains an inline grid with
     5+ columns gets overflow-x:auto so it scrolls
     cleanly on mobile instead of overflowing the page.
     ══════════════════════════════════════════════════ */
  function fixTimetableScroll() {
    document.querySelectorAll(".card-pad, .card > div").forEach(pad => {
      const grid = pad.querySelector("[style*='grid-template-columns']");
      if (!grid) return;
      const colStr = grid.style.gridTemplateColumns || "";
      const frs = (colStr.match(/\bfr\b/g) || []).length;
      const rpt = (colStr.match(/repeat\((\d+)/)?.[1] || 0) * 1;
      if (frs >= 5 || rpt >= 5) {
        pad.style.overflowX = "auto";
        pad.style.webkitOverflowScrolling = "touch";
        grid.style.minWidth = "600px";
      }
    });
  }

  /* ══════════════════════════════════════════════════
     11. SELECT FILTER — dropdowns labelled All/filter
     wire the role/type filter selects on tables.
     ══════════════════════════════════════════════════ */
  function wireSelectFilter() {
    document.querySelectorAll("select.select").forEach(sel => {
      /* Only wire selects whose options look like filters (All + categories) */
      const opts = Array.from(sel.options).map(o => o.text.trim().toLowerCase());
      if (!opts.includes("all") || opts.length < 2) return;

      /* Find a table nearby (within the same card) */
      const card = sel.closest(".card");
      if (!card) return;
      const tbl  = card.querySelector("table");
      if (!tbl) return;

      sel.addEventListener("change", () => {
        const val = sel.value.trim().toLowerCase();
        tbl.querySelectorAll("tbody tr").forEach(row => {
          row.style.display = (val === "all" || row.textContent.toLowerCase().includes(val)) ? "" : "none";
        });
      });
    });
  }

  /* ══════════════════════════════════════════════════
     12. OVERLAYS — Drawer / Modal
     Trigger: [data-open-drawer="id"] / [data-open-modal="id"]
     Target:  .drawer-overlay[data-drawer="id"] / .modal-overlay[data-modal="id"]
     Close:   click backdrop, [data-close-drawer]/[data-close-modal], Escape
     ══════════════════════════════════════════════════ */
  function openOverlay(sel, id) {
    const ov = document.querySelector(`${sel}[data-${sel === ".drawer-overlay" ? "drawer" : "modal"}="${id}"]`);
    if (ov) ov.classList.add("show");
  }

  function wireOverlays() {
    document.querySelectorAll("[data-open-drawer]").forEach(btn => {
      btn.addEventListener("click", e => {
        e.preventDefault();
        openOverlay(".drawer-overlay", btn.getAttribute("data-open-drawer"));
      });
    });
    document.querySelectorAll("[data-open-modal]").forEach(btn => {
      btn.addEventListener("click", e => {
        e.preventDefault();
        openOverlay(".modal-overlay", btn.getAttribute("data-open-modal"));
      });
    });
    document.querySelectorAll(".drawer-overlay, .modal-overlay").forEach(ov => {
      ov.addEventListener("click", e => { if (e.target === ov) ov.classList.remove("show"); });
      ov.querySelectorAll("[data-close-drawer],[data-close-modal]").forEach(btn => {
        btn.addEventListener("click", () => ov.classList.remove("show"));
      });
    });
    document.addEventListener("keydown", e => {
      if (e.key !== "Escape") return;
      document.querySelectorAll(".drawer-overlay.show, .modal-overlay.show").forEach(ov => ov.classList.remove("show"));
    });
  }

  window.closeOverlay = function (el) {
    const ov = el.closest(".drawer-overlay, .modal-overlay");
    if (ov) ov.classList.remove("show");
  };
  window.openDrawer = id => openOverlay(".drawer-overlay", id);
  window.openModal  = id => openOverlay(".modal-overlay", id);

  /* ══════════════════════════════════════════════════
     13. TABS
     .tabs > .tab-btn[data-tab] toggles sibling
     .tab-panel[data-tab-panel] within the same wrapper.
     ══════════════════════════════════════════════════ */
  function wireTabs() {
    document.querySelectorAll(".tabs").forEach(tabs => {
      const btns = tabs.querySelectorAll(".tab-btn");
      const wrap = tabs.parentElement;
      if (!wrap) return;
      btns.forEach(btn => {
        btn.addEventListener("click", () => {
          const key = btn.getAttribute("data-tab");
          btns.forEach(b => b.classList.toggle("active", b === btn));
          wrap.querySelectorAll(":scope > .tab-panel").forEach(p => {
            p.classList.toggle("active", p.getAttribute("data-tab-panel") === key);
          });
        });
      });
    });
  }

  /* ══════════════════════════════════════════════════
     14. DROPZONE — click or drag files onto .dropzone
     ══════════════════════════════════════════════════ */
  function wireDropzone() {
    function handleFiles(dz, files) {
      let list = dz.nextElementSibling;
      if (!list || !list.classList.contains("dz-file-list")) {
        list = document.createElement("div");
        list.className = "dz-file-list";
        dz.after(list);
      }
      Array.from(files).forEach(f => {
        const row = document.createElement("div");
        row.className = "dz-file";
        row.innerHTML = `<span class="material-symbols-outlined">description</span><span>${f.name}</span><button class="icon-btn" type="button" aria-label="Remove"><span class="material-symbols-outlined" style="font-size:16px">close</span></button>`;
        row.querySelector("button").addEventListener("click", () => row.remove());
        list.appendChild(row);
      });
      if (window.toast) window.toast(files.length > 1 ? `${files.length} files added` : `${files[0].name} added`, "success");
    }

    document.querySelectorAll(".dropzone").forEach(dz => {
      const input = dz.querySelector("input[type=file]");
      if (!input) return;
      dz.addEventListener("click", () => input.click());
      dz.addEventListener("dragover", e => { e.preventDefault(); dz.classList.add("drag"); });
      dz.addEventListener("dragleave", () => dz.classList.remove("drag"));
      dz.addEventListener("drop", e => {
        e.preventDefault();
        dz.classList.remove("drag");
        if (e.dataTransfer.files.length) handleFiles(dz, e.dataTransfer.files);
      });
      input.addEventListener("change", () => { if (input.files.length) handleFiles(dz, input.files); });
    });
  }

  /* ══════════════════════════════════════════════════
     15. AVATAR UPLOAD — click edit badge to preview a photo
     ══════════════════════════════════════════════════ */
  function wireAvatarUpload() {
    document.querySelectorAll(".avatar-upload").forEach(au => {
      const input = au.querySelector("input[type=file]");
      const img = au.querySelector("img, .au-fallback");
      const edit = au.querySelector(".au-edit");
      if (!input) return;
      if (edit) edit.addEventListener("click", e => { e.stopPropagation(); input.click(); });
      input.addEventListener("change", () => {
        const file = input.files[0];
        if (!file || !img) return;
        const reader = new FileReader();
        reader.onload = () => {
          if (img.tagName === "IMG") { img.src = reader.result; }
          else {
            const newImg = document.createElement("img");
            newImg.src = reader.result;
            img.replaceWith(newImg);
          }
        };
        reader.readAsDataURL(file);
      });
    });
  }

  /* ══════════════════════════════════════════════════
     INIT
     ══════════════════════════════════════════════════ */
  function init() {
    injectCSS();
    fixInlineColors();      /* must run first to set classes before other wires */
    wireAttendance();
    wireSearch();
    wireGrades();
    wireFormPersist();
    wireRowSelect();
    wireTableSort();
    wireGlobalSearch();
    wireSelectFilter();
    fixTimetableScroll();
    wireOverlays();
    wireTabs();
    wireDropzone();
    wireAvatarUpload();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
