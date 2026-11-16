/**
 * ============================================================================
 * NGIS — Admin Timetable Monitoring Controller
 * ============================================================================
 * Read-only administrative oversight of timetable preparation, draft progress,
 * and publication tracking across all school classes.
 *
 * Enforces:
 * - Read-only oversight: NO builder, NO drag-and-drop, NO slot editing
 * - Real backend statistics and audit timestamps
 * - Cooldown-protected administrative reminder dispatch
 * - Deep validation breakdown and read-only weekly timetable previews
 * ============================================================================
 */

(function (window, document) {
  "use strict";

  // State management
  const state = {
    filters: {
      campus: "",
      department: "",
      grade: "",
      status: "",
      responsible: "",
      search: "",
      sort: "attention",
      page: 1,
      page_size: 10,
    },
    meta: {
      campuses: [],
      departments: [],
      grades: [],
      statuses: [],
      academic_year: "",
    },
    summary: {
      total_classes: 0,
      published: 0,
      draft_in_progress: 0,
      not_started: 0,
      breakdown: {},
    },
    rows: [],
    pagination: {
      total: 0,
      page: 1,
      page_size: 10,
      total_pages: 1,
    },
    currentDetail: null,
    previewMode: "draft", // 'draft' or 'published'
    activeTab: "overview", // 'overview', 'preview', 'history'
    reminderTarget: null,
    isLoading: false,
  };

  // Auth & API Header Helper
  function getActorHeaders() {
    let user = null;
    try {
      if (window.NGISAuth && typeof window.NGISAuth.getUser === "function") {
        user = window.NGISAuth.getUser();
      }
    } catch (_) {}
    if (!user && window.NGIS_CURRENT_USER) {
      user = window.NGIS_CURRENT_USER;
    }
    if (!user) {
      user = {
        firstName: "Mr. Heng",
        lastName: "Samnang",
        role: "admin",
        id: "ADM-2024-001",
        email: "heng.samnang@ngis.edu.kh",
      };
    }
    const role = (user.role || "admin").toLowerCase();
    const fullName = `${user.firstName || ""} ${user.lastName || ""}`.trim() || user.name || "Mr. Heng Samnang";
    return {
      "Content-Type": "application/json",
      "X-Actor-Role": role,
      "X-User-Role": role,
      "X-Actor": fullName,
      "X-Actor-Id": user.id || "ADM-2024-001",
      "X-Actor-Email": user.email || "admin@ngis.edu.kh",
      "Authorization": `Bearer mock-jwt-token-${role}`,
    };
  }

  // Toast Notification
  function showToast(message, type = "success") {
  /* Shared NGIS operation-feedback engine (ui-states.js) — no page-local
     toast UI; keeps this module's showToast(message, type) signature. */
  if (!(window.NGISUI && window.NGISUI.toast)) {
    if (window.console) console.warn('toast unavailable:', message);
    return null;
  }
  var kind = type === 'error' ? 'error' : (type === 'warning' || type === 'warn') ? 'warning' : (type === 'info') ? 'info' : 'success';
  return window.NGISUI.toast.show(kind, String(message));
}

  // Format Dates
  function formatDate(isoStr) {
    if (!isoStr) return "—";
    try {
      const d = new Date(isoStr);
      if (isNaN(d.getTime())) return isoStr;
      return d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch (_) {
      return isoStr;
    }
  }

  // Status Badge Builder
  function renderStatusBadge(status, label) {
    switch (status) {
      case "published":
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/80">
          <i class="ph-fill ph-check-circle text-xs"></i> ${label || "Published"}
        </span>`;
      case "update_in_draft":
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200/80">
          <i class="ph-fill ph-pencil-simple-line text-xs"></i> ${label || "Update in Draft"}
        </span>`;
      case "ready_to_publish":
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200/80">
          <i class="ph-fill ph-sparkle text-xs"></i> ${label || "Ready to Publish"}
        </span>`;
      case "in_progress":
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-sky-50 text-sky-700 border border-sky-200/80">
          <i class="ph-fill ph-hourglass text-xs"></i> ${label || "In Progress"}
        </span>`;
      case "draft":
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200/80">
          <i class="ph-fill ph-file-text text-xs"></i> ${label || "Draft"}
        </span>`;
      case "needs_attention":
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-rose-50 text-rose-700 border border-rose-200/80">
          <i class="ph-fill ph-warning-diamond text-xs"></i> ${label || "Needs Attention"}
        </span>`;
      case "not_started":
      default:
        return `<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium bg-slate-50 text-slate-500 border border-slate-200/60">
          <i class="ph ph-circle-dashed text-xs"></i> ${label || "Not Started"}
        </span>`;
    }
  }

  // Draft Status Badge
  function renderDraftBadge(label) {
    if (label === "No Draft") {
      return `<span class="text-xs text-slate-400">No Draft</span>`;
    }
    if (label === "Modified Draft") {
      return `<span class="inline-flex items-center gap-1 text-[11px] font-medium text-amber-700 bg-amber-50/80 px-2 py-0.5 rounded border border-amber-200/60">
        <i class="ph ph-pencil-simple text-xs"></i> Modified
      </span>`;
    }
    if (label === "Clean (In Sync)") {
      return `<span class="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50/80 px-2 py-0.5 rounded border border-emerald-200/60">
        <i class="ph ph-check text-xs"></i> Clean
      </span>`;
    }
    return `<span class="inline-flex items-center gap-1 text-[11px] font-medium text-slate-700 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
      <i class="ph ph-floppy-disk text-xs"></i> Saved Draft
    </span>`;
  }

  // Completion Bar
  function renderCompletion(row) {
    if (!row.completion_available) {
      return `<span class="text-xs text-slate-400">Not available</span>`;
    }
    const pct = row.completion_pct != null ? row.completion_pct : 0;
    const placed = row.placed_periods || 0;
    const required = row.required_periods || 0;
    let barColor = "bg-slate-300";
    if (pct === 100) barColor = "bg-emerald-500";
    else if (pct > 0) barColor = "bg-sky-500";

    const conflictNotice =
      row.conflicts_count > 0
        ? `<span class="inline-flex items-center gap-0.5 text-[10px] font-medium text-rose-600 bg-rose-50 px-1.5 py-0.2 rounded border border-rose-200/60" title="${row.conflicts_count} schedule conflict(s)">
            <i class="ph ph-warning"></i> ${row.conflicts_count} conflict
          </span>`
        : "";

    return `
      <div class="space-y-1 min-w-[130px]">
        <div class="flex items-center justify-between text-xs">
          <span class="font-medium text-slate-700">${placed}/${required} <span class="text-slate-400 font-normal">(${pct}%)</span></span>
          ${conflictNotice}
        </div>
        <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
          <div class="${barColor} h-1.5 rounded-full transition-all duration-300" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
  }

  // Fetch Class Monitoring Rows & Metrics
  async function loadMonitoringData() {
    state.isLoading = true;
    renderLoadingState();
    try {
      const q = new URLSearchParams();
      if (state.filters.campus) q.set("campus", state.filters.campus);
      if (state.filters.department) q.set("department", state.filters.department);
      if (state.filters.grade) q.set("grade", state.filters.grade);
      if (state.filters.status) q.set("status", state.filters.status);
      if (state.filters.responsible) q.set("responsible", state.filters.responsible);
      if (state.filters.search) q.set("search", state.filters.search);
      if (state.filters.sort) q.set("sort", state.filters.sort);
      q.set("page", state.filters.page);
      q.set("page_size", state.filters.page_size);

      const res = await fetch(`/api/timetable/monitoring/classes?${q.toString()}`, {
        headers: getActorHeaders(),
      });

      if (!res.ok) {
        throw new Error(`Failed to load data (${res.status})`);
      }

      const json = await res.json();
      if (!json.success) {
        throw new Error(json.error || "Data load failed");
      }

      state.summary = json.summary || state.summary;
      state.meta = json.meta || state.meta;
      state.rows = json.rows || [];
      state.pagination = json.pagination || state.pagination;

      updateSummaryKPIs();
      populateFilterDropdowns();
      renderTableRows();
      renderPaginationControls();
    } catch (err) {
      console.error("[Timetable Monitoring] Load error:", err);
      showToast(`Error loading monitoring records: ${err.message}`, "error");
      renderErrorState(err.message);
    } finally {
      state.isLoading = false;
    }
  }

  // Render Summary Metric Cards (Section 12)
  function updateSummaryKPIs() {
    const s = state.summary;
    const total = s.total_classes || 0;
    const pub = s.published || 0;
    const draft = s.draft_in_progress || 0;
    const notStarted = s.not_started || 0;

    const elTotal = document.getElementById("statTotalClasses");
    const elPub = document.getElementById("statPublished");
    const elDraft = document.getElementById("statDraft");
    const elNotStarted = document.getElementById("statNotStarted");

    if (elTotal) elTotal.textContent = total;
    if (elPub) elPub.textContent = pub;
    if (elDraft) elDraft.textContent = draft;
    if (elNotStarted) elNotStarted.textContent = notStarted;

    const elPubPct = document.getElementById("statPublishedPct");
    const elDraftPct = document.getElementById("statDraftPct");
    const elNotStartedPct = document.getElementById("statNotStartedPct");

    if (elPubPct && total > 0) {
      elPubPct.textContent = `${Math.round((pub / total) * 100)}% of total`;
    }
    if (elDraftPct && total > 0) {
      elDraftPct.textContent = `${Math.round((draft / total) * 100)}% active prep`;
    }
    if (elNotStartedPct && total > 0) {
      elNotStartedPct.textContent = `${Math.round((notStarted / total) * 100)}% uninitiated`;
    }
  }

  // Populate Filter Dropdowns dynamically
  function populateFilterDropdowns() {
    const campusSel = document.getElementById("filterCampus");
    if (campusSel && campusSel.options.length <= 1) {
      (state.meta.campuses || []).forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        if (state.filters.campus === c) opt.selected = true;
        campusSel.appendChild(opt);
      });
    }

    const deptSel = document.getElementById("filterDepartment");
    if (deptSel && deptSel.options.length <= 1) {
      (state.meta.departments || []).forEach((d) => {
        const opt = document.createElement("option");
        opt.value = d;
        opt.textContent = d;
        if (state.filters.department === d) opt.selected = true;
        deptSel.appendChild(opt);
      });
    }

    const gradeSel = document.getElementById("filterGrade");
    if (gradeSel && gradeSel.options.length <= 1) {
      (state.meta.grades || []).forEach((g) => {
        const opt = document.createElement("option");
        opt.value = g;
        opt.textContent = `Grade ${g}`;
        if (state.filters.grade === g) opt.selected = true;
        gradeSel.appendChild(opt);
      });
    }

    const ayEl = document.getElementById("metaAcademicYear");
    if (ayEl && state.meta.academic_year) {
      ayEl.textContent = state.meta.academic_year;
    }
  }

  // Render Table Rows
  function renderTableRows() {
    const tbody = document.getElementById("monitoringTableBody");
    if (!tbody) return;

    if (!state.rows || state.rows.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="12" class="px-6 py-12 text-center">
            <div class="max-w-sm mx-auto text-center space-y-3">
              <div class="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center mx-auto text-slate-400">
                <i class="ph ph-magnifying-glass text-2xl"></i>
              </div>
              <p class="text-sm font-medium text-slate-700">No matching classes found</p>
              <p class="text-xs text-slate-500">There are no classes that match your selected filters. Try clearing your search or status filters.</p>
              <button type="button" class="btn-clear-filters px-3 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 shadow-xs">
                Reset Filters
              </button>
            </div>
          </td>
        </tr>
      `;
      tbody.querySelector(".btn-clear-filters")?.addEventListener("click", clearAllFilters);
      return;
    }

    tbody.innerHTML = state.rows
      .map((row) => {
        const canRemind = row.status !== "published" || row.update_in_draft;
        const responsibleDisplay = row.responsible_display || "Unassigned";
        const responsibleRole = row.responsible_role || "—";
        const isAssigned = row.responsible_recorded;

        const editorBadge = isAssigned
          ? `<div class="flex items-center gap-1.5">
               <span class="w-5 h-5 rounded-full bg-slate-100 flex items-center justify-center text-[10px] text-slate-600 font-medium shrink-0">
                 ${responsibleDisplay.charAt(0)}
               </span>
               <div class="leading-tight truncate">
                 <div class="font-medium text-slate-800 text-xs truncate max-w-[140px]">${responsibleDisplay}</div>
                 <div class="text-[10px] text-slate-400">${responsibleRole}</div>
               </div>
             </div>`
          : `<span class="text-xs text-slate-400 font-normal">Unassigned</span>`;

        return `
          <tr class="hover:bg-slate-50/70 border-b border-slate-100 transition-colors" data-class-id="${row.class_id}">
            <!-- Class -->
            <td class="px-4 py-3 whitespace-nowrap">
              <div class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-lg bg-brand-50 border border-brand-100 text-brand-700 flex items-center justify-center text-xs font-medium shrink-0">
                  ${row.class_display}
                </span>
                <div>
                  <div class="text-xs font-medium text-slate-900">${row.class_display}</div>
                  <div class="text-[10px] text-slate-400">Grade ${row.grade} · ${row.room || "Room —"}</div>
                </div>
              </div>
            </td>

            <!-- Campus -->
            <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-700">
              <div class="flex items-center gap-1.5">
                <i class="ph ph-buildings text-slate-400 text-sm"></i>
                <span>${row.campus || "Main"}</span>
              </div>
            </td>

            <!-- Department -->
            <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-700">
              <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-normal bg-slate-100 text-slate-600 border border-slate-200/60">
                ${row.department || "General"}
              </span>
            </td>

            <!-- Responsible Person -->
            <td class="px-4 py-3 whitespace-nowrap">
              ${editorBadge}
            </td>

            <!-- Completion -->
            <td class="px-4 py-3 whitespace-nowrap">
              ${renderCompletion(row)}
            </td>

            <!-- Draft Status -->
            <td class="px-4 py-3 whitespace-nowrap">
              ${renderDraftBadge(row.draft_status_label)}
            </td>

            <!-- Publication Status -->
            <td class="px-4 py-3 whitespace-nowrap">
              ${renderStatusBadge(row.status, row.status_label)}
            </td>

            <!-- Last Edited By -->
            <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-600">
              ${row.last_edited_by || "—"}
            </td>

            <!-- Last Edited -->
            <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-500 font-mono">
              ${formatDate(row.last_edited_at)}
            </td>

            <!-- Published By -->
            <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-600">
              ${row.published_by || "—"}
            </td>

            <!-- Published At -->
            <td class="px-4 py-3 whitespace-nowrap text-xs text-slate-500 font-mono">
              ${formatDate(row.published_at)}
            </td>

            <!-- Actions -->
            <td class="px-4 py-3 whitespace-nowrap text-right text-xs">
              <div class="flex items-center justify-end gap-1.5">
                <button type="button"
                  class="btn-view-details inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 shadow-xs transition cursor-pointer"
                  data-class-id="${row.class_id}"
                  title="View complete timetable status and read-only schedule">
                  <i class="ph ph-eye text-sm text-slate-500"></i>
                  <span>View</span>
                </button>
                ${
                  canRemind
                    ? `<button type="button"
                        class="btn-send-reminder inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 shadow-xs transition cursor-pointer"
                        data-class-id="${row.class_id}"
                        title="Send timetable follow-up reminder">
                        <i class="ph ph-bell text-sm text-amber-600"></i>
                        <span>Remind</span>
                      </button>`
                    : ""
                }
              </div>
            </td>
          </tr>
        `;
      })
      .join("");

    // Attach listeners
    tbody.querySelectorAll(".btn-view-details").forEach((btn) => {
      btn.addEventListener("click", () => openClassDetail(btn.dataset.classId));
    });
    tbody.querySelectorAll(".btn-send-reminder").forEach((btn) => {
      btn.addEventListener("click", () => openReminderModal(btn.dataset.classId));
    });
  }

  // Render Pagination Controls
  function renderPaginationControls() {
    const p = state.pagination;
    const start = (p.page - 1) * p.page_size + 1;
    const end = Math.min(p.page * p.page_size, p.total);

    const infoEl = document.getElementById("paginationInfo");
    if (infoEl) {
      if (p.total === 0) {
        infoEl.textContent = "No classes";
      } else {
        infoEl.textContent = `Showing ${start}–${end} of ${p.total} classes`;
      }
    }

    const prevBtn = document.getElementById("btnPrevPage");
    const nextBtn = document.getElementById("btnNextPage");

    if (prevBtn) {
      prevBtn.disabled = p.page <= 1;
    }
    if (nextBtn) {
      nextBtn.disabled = p.page >= p.total_pages;
    }

    const pageSelect = document.getElementById("pageSizeSelect");
    if (pageSelect) {
      pageSelect.value = state.filters.page_size;
    }
  }

  // Loading and Error States
  function renderLoadingState() {
    const tbody = document.getElementById("monitoringTableBody");
    if (!tbody) return;
    tbody.innerHTML = `
      <tr>
        <td colspan="12" class="px-6 py-12 text-center text-slate-500">
          <div class="inline-flex items-center gap-2 text-xs">
            <svg class="animate-spin h-4 w-4 text-brand-600" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Loading class timetable statuses...</span>
          </div>
        </td>
      </tr>
    `;
  }

  function renderErrorState(msg) {
    const tbody = document.getElementById("monitoringTableBody");
    if (!tbody) return;
    tbody.innerHTML = `
      <tr>
        <td colspan="12" class="px-6 py-8 text-center text-rose-600 text-xs">
          <p class="font-medium">Failed to load monitoring data</p>
          <p class="text-slate-500 mt-1">${msg}</p>
          <button type="button" class="btn-retry mt-3 px-3 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50">
            Retry Connection
          </button>
        </td>
      </tr>
    `;
    tbody.querySelector(".btn-retry")?.addEventListener("click", loadMonitoringData);
  }

  // Clear Filters
  function clearAllFilters() {
    state.filters.campus = "";
    state.filters.department = "";
    state.filters.grade = "";
    state.filters.status = "";
    state.filters.responsible = "";
    state.filters.search = "";
    state.filters.sort = "attention";
    state.filters.page = 1;

    const fc = document.getElementById("filterCampus");
    if (fc) fc.value = "";
    const fd = document.getElementById("filterDepartment");
    if (fd) fd.value = "";
    const fg = document.getElementById("filterGrade");
    if (fg) fg.value = "";
    const fs = document.getElementById("filterStatus");
    if (fs) fs.value = "";
    const fr = document.getElementById("filterResponsible");
    if (fr) fr.value = "";
    const fq = document.getElementById("filterSearch");
    if (fq) fq.value = "";
    const fst = document.getElementById("filterSort");
    if (fst) fst.value = "attention";

    loadMonitoringData();
  }

  // ==========================================================================
  // Class Timetable Detail View (Section 8)
  // ==========================================================================
  async function openClassDetail(classId) {
    const modal = document.getElementById("modalClassDetail");
    if (!modal) return;
    modal.classList.remove("hidden");

    const contentEl = document.getElementById("modalClassDetailContent");
    if (contentEl) {
      contentEl.innerHTML = `
        <div class="p-12 text-center text-slate-500">
          <svg class="animate-spin h-5 w-5 text-brand-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-xs">Fetching class details and read-only schedule...</span>
        </div>
      `;
    }

    try {
      const res = await fetch(`/api/timetable/monitoring/classes/${encodeURIComponent(classId)}`, {
        headers: getActorHeaders(),
      });
      if (!res.ok) throw new Error(`Detail load failed (${res.status})`);
      const data = await res.json();
      if (!data.success) throw new Error(data.error || "Failed to load class");

      state.currentDetail = data;
      state.activeTab = "overview";
      state.previewMode = data.publication?.has_publication && !data.preparation?.draft_exists ? "published" : "draft";

      renderDetailModal();
    } catch (err) {
      showToast(`Error: ${err.message}`, "error");
      if (contentEl) {
        contentEl.innerHTML = `
          <div class="p-8 text-center text-rose-600 text-xs">
            <p class="font-medium">Failed to retrieve class timetable detail</p>
            <p class="text-slate-500 mt-1">${err.message}</p>
          </div>
        `;
      }
    }
  }

  function closeClassDetail() {
    const modal = document.getElementById("modalClassDetail");
    if (modal) modal.classList.add("hidden");
    state.currentDetail = null;
  }

  function renderDetailModal() {
    const contentEl = document.getElementById("modalClassDetailContent");
    if (!contentEl || !state.currentDetail) return;
    const d = state.currentDetail;
    const info = d.class_info || {};
    const prep = d.preparation || {};
    const pub = d.publication || {};
    const row = d.row || {};

    // Header info
    contentEl.innerHTML = `
      <!-- Modal Header -->
      <div class="px-6 py-5 border-b border-slate-200/80 flex items-start justify-between bg-slate-50/50">
        <div class="space-y-1">
          <div class="flex items-center gap-2.5">
            <span class="px-2.5 py-1 rounded-lg bg-brand-50 border border-brand-200 text-brand-700 text-sm font-medium">
              ${info.class}
            </span>
            <h3 class="text-lg font-medium text-slate-900 tracking-tight">Class ${info.class} Timetable Monitoring</h3>
            ${renderStatusBadge(prep.status, prep.status_label)}
          </div>
          <p class="text-xs text-slate-500">
            ${info.campus || "Main Campus"} • ${info.department || "General"} • Grade ${info.grade} • ${info.room || "Room —"} • ${info.student_count || 0} students
          </p>
        </div>
        <button type="button" class="btn-close-modal p-1.5 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition cursor-pointer">
          <i class="ph ph-x text-lg"></i>
        </button>
      </div>

      <!-- Detail Tabs -->
      <div class="border-b border-slate-200 px-6 flex items-center gap-2 bg-white text-xs">
        <button type="button" class="tab-btn px-3 py-2.5 font-medium border-b-2 transition cursor-pointer ${
          state.activeTab === "overview"
            ? "border-brand-600 text-brand-700"
            : "border-transparent text-slate-500 hover:text-slate-800"
        }" data-tab="overview">
          <i class="ph ph-gauge mr-1"></i> Status &amp; Validation
        </button>
        <button type="button" class="tab-btn px-3 py-2.5 font-medium border-b-2 transition cursor-pointer ${
          state.activeTab === "preview"
            ? "border-brand-600 text-brand-700"
            : "border-transparent text-slate-500 hover:text-slate-800"
        }" data-tab="preview">
          <i class="ph ph-calendar mr-1"></i> Weekly Grid Preview (Read-Only)
        </button>
        <button type="button" class="tab-btn px-3 py-2.5 font-medium border-b-2 transition cursor-pointer ${
          state.activeTab === "history"
            ? "border-brand-600 text-brand-700"
            : "border-transparent text-slate-500 hover:text-slate-800"
        }" data-tab="history">
          <i class="ph ph-clock-counter-clockwise mr-1"></i> Activity &amp; Audit Log
        </button>
      </div>

      <!-- Tab Content Area -->
      <div class="p-6 max-h-[70vh] overflow-y-auto" id="detailTabContent">
        <!-- Rendered by tab -->
      </div>
    `;

    contentEl.querySelector(".btn-close-modal")?.addEventListener("click", closeClassDetail);
    contentEl.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.activeTab = btn.dataset.tab;
        renderDetailModal();
      });
    });

    renderActiveTabContent();
  }

  function renderActiveTabContent() {
    const tabEl = document.getElementById("detailTabContent");
    if (!tabEl || !state.currentDetail) return;
    const d = state.currentDetail;
    const info = d.class_info || {};
    const prep = d.preparation || {};
    const pub = d.publication || {};
    const row = d.row || {};

    if (state.activeTab === "overview") {
      // OVERVIEW & VALIDATION TAB
      const conflictsHtml =
        prep.conflicts && prep.conflicts.length > 0
          ? `
            <div class="rounded-xl border border-rose-200 bg-rose-50/60 p-4 space-y-2">
              <div class="flex items-center gap-2 text-rose-800 font-medium text-xs">
                <i class="ph-fill ph-warning-diamond text-base text-rose-600"></i>
                <span>Schedule Conflicts Detected (${prep.conflicts.length})</span>
              </div>
              <ul class="text-xs text-rose-700 space-y-1 list-disc list-inside">
                ${prep.conflicts
                  .map(
                    (c) =>
                      `<li><span class="font-medium font-mono">${c.key}</span>: ${c.message_en || c.type}</li>`
                  )
                  .join("")}
              </ul>
            </div>
          `
          : `
            <div class="rounded-xl border border-emerald-200 bg-emerald-50/50 p-3.5 flex items-center gap-2.5 text-xs text-emerald-800">
              <i class="ph-fill ph-check-circle text-base text-emerald-600 shrink-0"></i>
              <span>Zero schedule conflicts detected. Teacher assignments and room allocations are valid.</span>
            </div>
          `;

      const subjectsHtml = (prep.subjects || [])
        .map((s) => {
          const statusBadge = s.complete
            ? `<span class="text-emerald-700 text-[11px] font-medium"><i class="ph ph-check"></i> Complete</span>`
            : `<span class="text-amber-700 text-[11px] font-medium">${s.missing} missing</span>`;
          return `
            <tr class="border-b border-slate-100 text-xs">
              <td class="py-2 px-3 font-medium text-slate-800 flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full shrink-0" style="background-color: ${s.color}"></span>
                <span>${s.subject_name}</span>
                <span class="text-slate-400 font-normal">(${s.subject_code})</span>
              </td>
              <td class="py-2 px-3 text-slate-600 text-center font-mono">${s.required}</td>
              <td class="py-2 px-3 text-slate-800 text-center font-mono font-medium">${s.placed}</td>
              <td class="py-2 px-3 text-slate-500 text-center font-mono">${s.missing}</td>
              <td class="py-2 px-3 text-right">${statusBadge}</td>
            </tr>
          `;
        })
        .join("");

      tabEl.innerHTML = `
        <div class="space-y-6">
          <!-- 4 Cards Summary -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <div class="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <div class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Responsible Person</div>
              <div class="text-xs font-medium text-slate-900 truncate">${info.responsible_display || "Unassigned"}</div>
              <div class="text-[11px] text-slate-500">${info.responsible_role || "—"}</div>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <div class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Completion Status</div>
              <div class="text-xs font-medium text-slate-900">${prep.placed_periods || 0} / ${prep.required_periods || 0} periods</div>
              <div class="text-[11px] text-slate-500">${prep.completion_pct != null ? prep.completion_pct + "% complete" : "Not available"}</div>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <div class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Publication Status</div>
              <div class="text-xs font-medium text-slate-900">${pub.has_publication ? `v${pub.version} Published` : "Not Published"}</div>
              <div class="text-[11px] text-slate-500">${pub.published_at ? formatDate(pub.published_at) : "No published version"}</div>
            </div>

            <div class="p-3.5 rounded-xl border border-slate-200/80 bg-white space-y-1">
              <div class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Last Modification</div>
              <div class="text-xs font-medium text-slate-900">${row.last_edited_by || "—"}</div>
              <div class="text-[11px] text-slate-500 font-mono">${formatDate(row.last_edited_at)}</div>
            </div>
          </div>

          <!-- Conflicts Alert -->
          ${conflictsHtml}

          <!-- Subject Quota Table -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <h4 class="text-xs font-medium text-slate-900 uppercase tracking-wider">Curriculum Subject Allocation</h4>
              <span class="text-xs text-slate-400">${prep.subjects?.length || 0} subjects prescribed</span>
            </div>
            <div class="border border-slate-200/80 rounded-xl overflow-x-auto bg-white">
              <table class="w-full min-w-[480px] text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50 text-[11px] text-slate-500 font-medium border-b border-slate-200">
                    <th class="py-2 px-3">Subject</th>
                    <th class="py-2 px-3 text-center">Required</th>
                    <th class="py-2 px-3 text-center">Placed</th>
                    <th class="py-2 px-3 text-center">Remaining</th>
                    <th class="py-2 px-3 text-right">Progress</th>
                  </tr>
                </thead>
                <tbody>
                  ${subjectsHtml || '<tr><td colspan="5" class="py-4 text-center text-xs text-slate-400">No subject quotas configured</td></tr>'}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      `;
    } else if (state.activeTab === "preview") {
      // WEEKLY GRID PREVIEW TAB (READ-ONLY)
      const preview = d.preview || {};
      const hasDraft = preview.draft && preview.draft.length > 0;
      const hasPub = preview.published && preview.published.length > 0;

      const matrix = state.previewMode === "published" ? preview.published_matrix : preview.draft_matrix;
      const days = ["ច័ន្ទ", "អង្គារ", "ពុធ", "ព្រហស្បតិ៍", "សុក្រ", "សៅរ៍"];
      const daysEn = {
        ច័ន្ទ: "Mon",
        អង្គារ: "Tue",
        ពុធ: "Wed",
        ព្រហស្បតិ៍: "Thu",
        សុក្រ: "Fri",
        សៅរ៍: "Sat",
      };

      const periods = [
        { shift: "ព្រឹក", pNum: 1, label: "P1 (07:00–07:50)", key: "ព្រឹក|1" },
        { shift: "ព្រឹក", pNum: 2, label: "P2 (07:50–08:40)", key: "ព្រឹក|2" },
        { shift: "ព្រឹក", pNum: 3, label: "P3 (08:40–09:30)", key: "ព្រឹក|3" },
        { shift: "ព្រឹក", pNum: 4, label: "P4 (09:30–10:20)", key: "ព្រឹក|4" },
        { shift: "ព្រឹក", pNum: 5, label: "P5 (10:20–11:10)", key: "ព្រឹក|5" },
        { shift: "រសៀល", pNum: 1, label: "P6 (13:00–13:50)", key: "រសៀល|1" },
        { shift: "រសៀល", pNum: 2, label: "P7 (13:50–14:40)", key: "រសៀល|2" },
        { shift: "រសៀល", pNum: 3, label: "P8 (14:40–15:30)", key: "រសៀល|3" },
        { shift: "រសៀល", pNum: 4, label: "P9 (15:30–16:20)", key: "រសៀល|4" },
        { shift: "រសៀល", pNum: 5, label: "P10 (16:20–17:10)", key: "រសៀល|5" },
      ];

      tabEl.innerHTML = `
        <div class="space-y-4">
          <!-- Banner: Read-Only Oversight Notice -->
          <div class="rounded-xl border border-slate-200 bg-slate-50 p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-center gap-2.5 text-xs text-slate-700">
              <i class="ph ph-lock-key text-base text-slate-400"></i>
              <span><span class="font-medium">Read-Only Preview Mode:</span> Administrative oversight view. Drag-and-drop and schedule editing are disabled.</span>
            </div>
            <!-- Switch Draft / Published -->
            <div class="flex items-center gap-1.5 bg-white p-1 rounded-lg border border-slate-200 shrink-0 text-xs font-medium">
              <button type="button" class="btn-toggle-preview px-2.5 py-1 rounded transition ${
                state.previewMode === "draft"
                  ? "bg-slate-900 text-white"
                  : "text-slate-600 hover:text-slate-900"
              }" data-mode="draft">
                Draft (${preview.draft?.length || 0} periods)
              </button>
              <button type="button" class="btn-toggle-preview px-2.5 py-1 rounded transition ${
                state.previewMode === "published"
                  ? "bg-slate-900 text-white"
                  : "text-slate-600 hover:text-slate-900"
              }" data-mode="published" ${!hasPub ? "disabled title='No published version yet'" : ""}>
                Published (${preview.published?.length || 0} periods)
              </button>
            </div>
          </div>

          <!-- Weekly Schedule Table -->
          <div class="border border-slate-200/80 rounded-xl overflow-x-auto bg-white shadow-xs">
            <table class="w-full border-collapse min-w-[700px] text-xs">
              <thead>
                <tr class="bg-slate-50 border-b border-slate-200 text-slate-600 text-[11px] font-medium">
                  <th class="py-2.5 px-3 text-left w-36 border-r border-slate-200">Period</th>
                  ${days
                    .map(
                      (d) =>
                        `<th class="py-2.5 px-2 text-center border-r border-slate-200 last:border-r-0">${d} <span class="text-slate-400 font-normal">(${daysEn[d]})</span></th>`
                    )
                    .join("")}
                </tr>
              </thead>
              <tbody>
                ${periods
                  .map((p, idx) => {
                    const isMorningBreak = idx === 4;
                    return `
                      <tr class="border-b border-slate-100 hover:bg-slate-50/50 ${
                        isMorningBreak ? "border-b-2 border-slate-300" : ""
                      }">
                        <td class="py-2 px-3 font-medium text-slate-700 bg-slate-50/60 border-r border-slate-200 whitespace-nowrap">
                          ${p.label}
                        </td>
                        ${days
                          .map((d) => {
                            const cell = matrix && matrix[d] ? matrix[d][p.key] : null;
                            if (cell) {
                              return `
                                <td class="p-1 border-r border-slate-100 last:border-r-0 align-top">
                                  <div class="p-1.5 rounded-md border text-[11px] space-y-0.5 leading-tight" style="background-color: ${cell.color}15; border-color: ${cell.color}40;">
                                    <div class="font-medium text-slate-900 truncate" style="color: ${cell.color}">${cell.subject_code} · ${cell.subject_name}</div>
                                    <div class="text-slate-600 truncate text-[10px]">${cell.teacher_name || cell.teacher_id}</div>
                                  </div>
                                </td>
                              `;
                            }
                            return `
                              <td class="p-1 border-r border-slate-100 last:border-r-0 text-center text-slate-300">
                                <span class="text-slate-200">—</span>
                              </td>
                            `;
                          })
                          .join("")}
                      </tr>
                    `;
                  })
                  .join("")}
              </tbody>
            </table>
          </div>
        </div>
      `;

      tabEl.querySelectorAll(".btn-toggle-preview").forEach((btn) => {
        btn.addEventListener("click", () => {
          if (btn.disabled) return;
          state.previewMode = btn.dataset.mode;
          renderActiveTabContent();
        });
      });
    } else if (state.activeTab === "history") {
      // ACTIVITY & AUDIT HISTORY TAB
      const history = d.activity_history || [];
      if (history.length === 0) {
        tabEl.innerHTML = `
          <div class="p-12 text-center text-slate-400 text-xs">
            <i class="ph ph-clock-counter-clockwise text-3xl mb-2 block mx-auto text-slate-300"></i>
            <p>No activity logs recorded for this class yet.</p>
          </div>
        `;
        return;
      }

      tabEl.innerHTML = `
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-xs font-medium text-slate-900 uppercase tracking-wider">Chronological Audit Log</h4>
            <span class="text-xs text-slate-400">${history.length} events</span>
          </div>
          <div class="border border-slate-200/80 rounded-xl bg-white p-4">
            <div class="relative pl-6 space-y-4 before:content-[''] before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
              ${history
                .map((ev) => {
                  let iconColor = "bg-slate-400";
                  if (ev.type === "publication") iconColor = "bg-emerald-500";
                  else if (ev.type === "reminder") iconColor = "bg-amber-500";

                  return `
                    <div class="relative text-xs">
                      <span class="absolute -left-[29px] top-1 w-2.5 h-2.5 rounded-full ${iconColor} ring-4 ring-white"></span>
                      <div class="flex items-center justify-between">
                        <span class="font-medium text-slate-900">${ev.action}</span>
                        <span class="text-slate-400 font-mono text-[11px]">${formatDate(ev.at)}</span>
                      </div>
                      <div class="text-slate-500 text-[11px] mt-0.5">
                        By <span class="font-medium text-slate-700">${ev.actor || "Unrecorded"}</span>
                        ${ev.detail ? `· <span class="font-mono text-slate-400">${ev.detail}</span>` : ""}
                      </div>
                    </div>
                  `;
                })
                .join("")}
            </div>
          </div>
        </div>
      `;
    }
  }

  // ==========================================================================
  // Administrative Follow-up / Reminders (Section 10)
  // ==========================================================================
  function openReminderModal(classId) {
    const row = state.rows.find((r) => r.class_id === classId);
    if (!row) return;

    state.reminderTarget = row;
    const modal = document.getElementById("modalSendReminder");
    if (!modal) return;

    const resp = row.responsible || {
      id: "PRIN-2024-001",
      name: "Dr. Ly Bunheng",
      role: "Principal",
      email: "principal@ngis.edu.kh",
    };

    document.getElementById("remindRecipientName").textContent = resp.name || "Dr. Ly Bunheng";
    document.getElementById("remindRecipientRole").textContent = `${resp.role || "Principal"} • ${resp.email || "principal@ngis.edu.kh"}`;
    document.getElementById("remindClassName").textContent = `${row.class_display} (${row.campus || "Main Campus"})`;
    document.getElementById("remindClassStatus").innerHTML = renderStatusBadge(row.status, row.status_label);

    const defaultMsg =
      row.status === "not_started"
        ? `Your timetable for Grade ${row.class_display} has not been started. Please initiate the schedule preparation process immediately.`
        : `Your timetable for Grade ${row.class_display} is incomplete (${row.missing_periods || 0} periods remaining). Please review and complete the timetable preparation process.`;

    const txtMsg = document.getElementById("remindMessageInput");
    if (txtMsg) txtMsg.value = defaultMsg;

    const dtInput = document.getElementById("remindDeadlineInput");
    if (dtInput) {
      const d = new Date();
      d.setDate(d.getDate() + 3);
      dtInput.value = d.toISOString().split("T")[0];
    }

    const warningEl = document.getElementById("remindCooldownWarning");
    if (warningEl) warningEl.classList.add("hidden");

    const modalEl = document.getElementById("modalSendReminder");
    if (window.NGISKit && modalEl) window.NGISKit.clearContainerErrors(modalEl);
    const forceChk = document.getElementById("remindForceDuplicate");
    if (forceChk) forceChk.checked = false;

    modal.classList.remove("hidden");
  }

  function closeReminderModal() {
    const modal = document.getElementById("modalSendReminder");
    if (modal) modal.classList.add("hidden");
    state.reminderTarget = null;
  }

  async function submitReminder() {
    if (!state.reminderTarget) return;
    const row = state.reminderTarget;
    const modalEl = document.getElementById("modalSendReminder");
    const txtMsg = document.getElementById("remindMessageInput");
    const dtInput = document.getElementById("remindDeadlineInput");
    const forceChk = document.getElementById("remindForceDuplicate");
    const btnSend = document.getElementById("btnConfirmSendReminder");

    if (window.NGISKit && modalEl) window.NGISKit.clearContainerErrors(modalEl);

    const msgVal = (txtMsg?.value || "").trim();
    const dtVal = (dtInput?.value || "").trim();
    let hasErr = false;
    if (!msgVal) {
      hasErr = true;
      if (window.NGISKit && txtMsg) window.NGISKit.setFieldError(txtMsg, "Please write a short reminder message for the staff member.");
      else showToast("Please write a short reminder message first.", "warning");
    }
    if (!dtVal) {
      hasErr = true;
      if (window.NGISKit && dtInput) window.NGISKit.setFieldError(dtInput, "Please choose a target completion date.");
    }
    if (hasErr) return;

    const payload = {
      message: msgVal,
      deadline: dtVal,
      force_duplicate: forceChk?.checked || false,
    };

    if (btnSend) {
      btnSend.disabled = true;
      btnSend.innerHTML = `<i class="ph ph-circle-notch animate-spin text-sm"></i> Sending...`;
    }

    try {
      const res = await fetch(`/api/timetable/monitoring/classes/${encodeURIComponent(row.class_id)}/remind`, {
        method: "POST",
        headers: getActorHeaders(),
        body: JSON.stringify(payload),
      });

      const json = await res.json();

      if (res.status === 409 && json.cooldown_warning) {
        // Cooldown alert: prompt user to confirm force duplicate
        const warningEl = document.getElementById("remindCooldownWarning");
        const warningMsg = document.getElementById("remindCooldownText");
        if (warningEl && warningMsg) {
          warningMsg.textContent = json.message || "A reminder was recently sent for this class.";
          warningEl.classList.remove("hidden");
        }
        showToast("Notice: A reminder was recently dispatched. Check the duplicate override to proceed.", "warning");
        return;
      }

      if (!res.ok || !json.success) {
        throw new Error(json.error || json.message || "Failed to dispatch reminder");
      }

      showToast(`Reminder sent to ${json.reminder?.recipient_name || "editor"}.`, "success");
      closeReminderModal();
      loadMonitoringData();
    } catch (err) {
      showToast(`Error: ${err.message}`, "error");
    } finally {
      if (btnSend) {
        btnSend.disabled = false;
        btnSend.innerHTML = `<span>Send Reminder</span>`;
      }
    }
  }

  // Export CSV directly (Section 15)
  function exportCsv() {
    const q = new URLSearchParams();
    if (state.filters.campus) q.set("campus", state.filters.campus);
    if (state.filters.department) q.set("department", state.filters.department);
    if (state.filters.grade) q.set("grade", state.filters.grade);
    if (state.filters.status) q.set("status", state.filters.status);
    if (state.filters.responsible) q.set("responsible", state.filters.responsible);
    if (state.filters.search) q.set("search", state.filters.search);
    if (state.filters.sort) q.set("sort", state.filters.sort);

    showToast("Generating timetable monitoring CSV export...", "info");
    // Trigger download via link with auth headers or direct location
    window.location.href = `/api/timetable/monitoring/export?${q.toString()}`;
  }

  // Initialize UI event handlers
  function init() {
    // Top actions
    document.getElementById("btnRefreshData")?.addEventListener("click", () => {
      showToast("Refreshing monitoring records...", "info");
      loadMonitoringData();
    });
    document.getElementById("btnExportCsv")?.addEventListener("click", exportCsv);

    // Filters
    document.getElementById("filterCampus")?.addEventListener("change", (e) => {
      state.filters.campus = e.target.value;
      state.filters.page = 1;
      loadMonitoringData();
    });
    document.getElementById("filterDepartment")?.addEventListener("change", (e) => {
      state.filters.department = e.target.value;
      state.filters.page = 1;
      loadMonitoringData();
    });
    document.getElementById("filterGrade")?.addEventListener("change", (e) => {
      state.filters.grade = e.target.value;
      state.filters.page = 1;
      loadMonitoringData();
    });
    document.getElementById("filterStatus")?.addEventListener("change", (e) => {
      state.filters.status = e.target.value;
      state.filters.page = 1;
      loadMonitoringData();
    });
    document.getElementById("filterResponsible")?.addEventListener("change", (e) => {
      state.filters.responsible = e.target.value;
      state.filters.page = 1;
      loadMonitoringData();
    });
    document.getElementById("filterSort")?.addEventListener("change", (e) => {
      state.filters.sort = e.target.value;
      state.filters.page = 1;
      loadMonitoringData();
    });

    let searchTimeout = null;
    document.getElementById("filterSearch")?.addEventListener("input", (e) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        state.filters.search = e.target.value.trim();
        state.filters.page = 1;
        loadMonitoringData();
      }, 300);
    });

    document.getElementById("btnClearFilters")?.addEventListener("click", clearAllFilters);

    document.getElementById("btnOpenMobileFilters")?.addEventListener("click", () => {
      if (!window.NGISKit || !window.NGISKit.FilterSheet) return;
      const draft = {
        campus: state.filters.campus || "",
        department: state.filters.department || "",
        grade: state.filters.grade || "",
        status: state.filters.status || "",
        responsible: state.filters.responsible || "",
        sort: state.filters.sort || "attention",
      };
      const collectOptions = (id) => {
        const el = document.getElementById(id);
        return el ? Array.from(el.options).map((o) => ({ value: o.value, label: o.textContent })) : [];
      };
      const refreshPreviewCount = () => {
        const q = new URLSearchParams();
        if (draft.campus) q.set("campus", draft.campus);
        if (draft.department) q.set("department", draft.department);
        if (draft.grade) q.set("grade", draft.grade);
        if (draft.status) q.set("status", draft.status);
        if (draft.responsible) q.set("responsible", draft.responsible);
        if (state.filters.search) q.set("search", state.filters.search);
        q.set("page", "1");
        q.set("page_size", "1");
        fetch(`/api/timetable/monitoring/classes?${q.toString()}`, { headers: getActorHeaders() })
          .then((r) => r.json())
          .then((j) => {
            const total = j?.pagination?.total_items ?? j?.total ?? state.pagination?.total_items ?? 0;
            window.NGISKit.FilterSheet.updateCount(total);
          })
          .catch(() => {});
      };
      window.NGISKit.FilterSheet.open({
        title: "Filter Timetables",
        count: state.pagination?.total_items || state.rows?.length || 0,
        sections: [
          { key: "campus", label: "Campus", value: draft.campus, options: collectOptions("filterCampus") },
          { key: "department", label: "Department", value: draft.department, options: collectOptions("filterDepartment") },
          { key: "grade", label: "Grade", value: draft.grade, options: collectOptions("filterGrade") },
          { key: "status", label: "Timetable Status", value: draft.status, options: collectOptions("filterStatus") },
          { key: "responsible", label: "Responsible Person", value: draft.responsible, options: collectOptions("filterResponsible") },
          { key: "sort", label: "Sort Priority", value: draft.sort, options: collectOptions("filterSort") },
        ],
        onChange: (key, val) => {
          draft[key] = val;
          refreshPreviewCount();
        },
        onReset: () => {
          draft.campus = "";
          draft.department = "";
          draft.grade = "";
          draft.status = "";
          draft.responsible = "";
          draft.sort = "attention";
          refreshPreviewCount();
        },
        onApply: () => {
          Object.assign(state.filters, draft);
          state.filters.page = 1;
          ["filterCampus", "filterDepartment", "filterGrade", "filterStatus", "filterResponsible", "filterSort"].forEach((id) => {
            const k = id.replace("filter", "").toLowerCase();
            const sel = document.getElementById(id);
            if (sel) sel.value = draft[k] || "";
          });
          loadMonitoringData();
        },
      });
    });

    // Pagination
    document.getElementById("btnPrevPage")?.addEventListener("click", () => {
      if (state.filters.page > 1) {
        state.filters.page--;
        loadMonitoringData();
      }
    });
    document.getElementById("btnNextPage")?.addEventListener("click", () => {
      if (state.filters.page < state.pagination.total_pages) {
        state.filters.page++;
        loadMonitoringData();
      }
    });
    document.getElementById("pageSizeSelect")?.addEventListener("change", (e) => {
      state.filters.page_size = parseInt(e.target.value, 10) || 10;
      state.filters.page = 1;
      loadMonitoringData();
    });

    // Modals
    document.getElementById("btnCloseDetailModal")?.addEventListener("click", closeClassDetail);
    document.getElementById("btnCancelReminder")?.addEventListener("click", closeReminderModal);
    document.getElementById("btnCloseReminderX")?.addEventListener("click", closeReminderModal);
    document.getElementById("btnConfirmSendReminder")?.addEventListener("click", submitReminder);

    // Initial load
    loadMonitoringData();
  }

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Export to window for external integration
  window.NGISTimetableMonitoring = {
    loadMonitoringData,
    openClassDetail,
    openReminderModal,
    exportCsv,
    state,
  };
})(window, document);

