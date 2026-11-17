/* ============================================================
   NGIS Profile Hubs — shared directory + profile engine.
   Drives Teacher Profiles and Student Profiles in the
   Principal and Admin portals from real backend data only.
   Configured by window.NGIS_PROFILES = { kind, portal }.
   ============================================================ */
(function () {
  'use strict';

  var CFG = Object.assign({ kind: 'teacher', portal: 'principal' }, window.NGIS_PROFILES || {});
  var IS_TEACHER = CFG.kind === 'teacher';
  var API_BASE = '/api/principal/roster/' + (IS_TEACHER ? 'teachers' : 'students');
  var DOCS_API = '/api/principal/profile-docs';
  var PER_PAGE = 10;
  var KIND_LABEL = IS_TEACHER ? 'Teacher' : 'Student';
  var PLURAL_LABEL = IS_TEACHER ? 'Teachers' : 'Students';

  var state = {
    all: [], filtered: [], page: 1,
    search: '', dept: 'ALL', status: 'ALL', sort: 'name-asc',
    loading: true, error: '',
    profile: null, profileId: null, tab: 0, profileLoading: false,
    docsBusy: false
  };

  var TEACHER_TABS = ['Personal Information', 'Employment', 'Academic & Teaching',
    'Education & Qualifications', 'Documents', 'Activity & History'];
  var STUDENT_TABS = ['Personal Information', 'Academic Record', 'Attendance',
    'Student Services', 'Documents', 'Guardian & Contact', 'Activity & History'];
  var TABS = IS_TEACHER ? TEACHER_TABS : STUDENT_TABS;
  var DOCS_TAB_INDEX = TABS.indexOf('Documents');
  var DOC_CATEGORIES = IS_TEACHER
    ? ['General', 'Employment Contract', 'Certification', 'Compliance', 'Other']
    : ['General', 'Transcript', 'Medical', 'ID Document', 'Consent Form', 'Other'];

  /* ---------- tiny helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $id(x) { return document.getElementById(x); }
  function dash(v) { return (v == null || v === '') ? '—' : esc(v); }
  function initials(name) {
    var parts = String(name || '').trim().split(/\s+/);
    return ((parts[0] || 'N')[0] + (parts.length > 1 ? parts[parts.length - 1][0] : '')).toUpperCase();
  }
  function getSubjectColor(subj) {
    var s = String(subj || '').toLowerCase();
    if (s.indexOf('khmer') !== -1) return '#d97706';
    if (s.indexOf('math') !== -1) return '#2563eb';
    if (s.indexOf('phys') !== -1) return '#7c3aed';
    if (s.indexOf('chem') !== -1) return '#db2777';
    if (s.indexOf('bio') !== -1) return '#059669';
    if (s.indexOf('hist') !== -1 || s.indexOf('geo') !== -1) return '#b45309';
    if (s.indexOf('eng') !== -1) return '#0284c7';
    if (s.indexOf('sport') !== -1 || s.indexOf('pe') !== -1) return '#dc2626';
    return '#176B45';
  }
  function fmtDT(iso) {
    if (!iso) return '—';
    try {
      var d = new Date(String(iso).replace(' ', 'T'));
      if (isNaN(d)) return esc(iso);
      return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) +
        ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch (e) { return esc(iso); }
  }
  function num(v, dp) {
    var n = Number(v);
    return isNaN(n) ? '—' : n.toFixed(dp == null ? 2 : dp);
  }
  function api(path, opts) { return NGISAuth.api(path, opts || {}); }
  function apiError(err, fallback) {
    var e = (err && (err.error || err)) || {};
    return (e.message || e.detail || fallback || 'Request failed');
  }

  var toastTimer = null;
  function toast(__a, __b) {
  /* Shared NGIS operation-feedback engine (ui-states.js) — single
     implementation across all portals; no page-local toast UI anymore. */
  if (!(window.NGISUI && window.NGISUI.toast)) {
    if (window.console) console.warn('toast unavailable:', __a);
    return null;
  }
  var __k = __b;
  if (__b === true || __b === 'error' || __b === 'danger' || __b === 'fail' || __b === 'isError') __k = 'error';
  else if (__b === 'warning' || __b === 'warn') __k = 'warning';
  else if (__b === 'info') __k = 'info';
  else if (__b === 'loading') __k = 'loading';
  else if (__b === false || __b === undefined || __b === null || __b === 'success' || __b === 'ok' || __b === 'done') __k = 'success';
  else __k = 'info';
  return window.NGISUI.toast.show(__k, String(__a));
}

  /* ---------- confirm / reason dialog ---------- */
  var confirmResolve = null;
  function confirmDlg(opts) {
    return new Promise(function (resolve) {
      confirmResolve = resolve;
      var m = $id('confirmModal');
      $('h3', m).textContent = opts.title;
      $('#cfMessage', m).textContent = opts.message || '';
      $('#cfReasonWrap', m).style.display = opts.requireReason ? '' : 'none';
      $('#cfReason', m).value = '';
      $('#cfReasonError', m).style.display = 'none';
      $('#cfOk', m).textContent = opts.confirmLabel || 'Confirm';
      $('#cfOk').className = 'px-4 py-2 rounded-lg font-medium text-sm shadow-sm transition cursor-pointer ' +
        (opts.danger ? 'bg-[#B3261E] text-white hover:bg-[#8c1d17]' : 'bg-[#176B45] text-white hover:bg-[#125638]');
      m.classList.remove('hidden');
      if (opts.requireReason) setTimeout(function () { $('#cfReason').focus(); }, 60);
    });
  }
  function closeConfirm(value) {
    $id('confirmModal').classList.add('hidden');
    var r = confirmResolve; confirmResolve = null;
    if (r) r(value);
  }

  /* ---------- data loading ---------- */
  function loadDirectory() {
    state.loading = true; state.error = '';
    var st = $id('filterStatusText');
    if (st) st.textContent = 'Loading...';
    var badge = $id('filterStatusBadge');
    if (badge) badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-50 border border-slate-200/80 text-xs font-medium text-slate-600 whitespace-nowrap';
    renderTable(); renderKpis();
    api(API_BASE).then(function (res) {
      state.all = (res && res.data) || [];
      state.loading = false;
      applyFilters();
      deepLink();
    }).catch(function (err) {
      state.loading = false;
      state.error = apiError(err, 'Could not load the directory');
      var stEl = $id('filterStatusText');
      if (stEl) stEl.textContent = 'Error loading records';
      var badgeEl = $id('filterStatusBadge');
      if (badgeEl) badgeEl.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-50 border border-rose-200 text-xs font-medium text-rose-700 whitespace-nowrap';
      var countEl = $id('dirCount');
      if (countEl) countEl.textContent = 'Failed to load records';
      renderTable(); renderKpis();
    });
  }

  function uniq(key) {
    var seen = {}, out = [];
    state.all.forEach(function (r) {
      var v = (r[key] || '').toString().trim();
      if (v && !seen[v]) { seen[v] = 1; out.push(v); }
    });
    return out.sort();
  }

  function applyFilters() {
    var q = state.search.toLowerCase().trim();
    var rows = state.all.filter(function (r) {
      var hay = IS_TEACHER
        ? [r.name, r.id, r.email, r.subject, r.department, r.role, r.code, r.employee_id, r.specialization, r.notes]
        : [r.name, r.id, r.grade, r.class, r.parentName, r.parentEmail, r.advisor];
      if (q && !hay.some(function (v) { return String(v || '').toLowerCase().indexOf(q) !== -1; })) return false;
      if (state.dept !== 'ALL') {
        var field = IS_TEACHER ? r.department : r.grade;
        if (String(field || '').indexOf(state.dept) === -1) return false;
      }
      if (state.status !== 'ALL' && String(r.status || '').toLowerCase() !== state.status.toLowerCase()) return false;
      return true;
    });
    var desc = state.sort.indexOf('-desc') !== -1 || state.sort === 'name-desc';
    var key = state.sort.replace(/-(asc|desc)$/, '');
    rows.sort(function (a, b) {
      if (key === 'name') return String(a.name || '').localeCompare(String(b.name || '')) * (desc ? -1 : 1);
      if (key === 'target') {
        var at = Number(a.target || (a.classesAssigned ? a.classesAssigned * 3 : 17));
        var bt = Number(b.target || (b.classesAssigned ? b.classesAssigned * 3 : 17));
        return (bt - at) * (desc ? -1 : 1);
      }
      var av = Number(a[key] || 0), bv = Number(b[key] || 0);
      return (bv - av) * (desc ? -1 : 1);
    });
    state.filtered = rows;
    var maxPage = Math.max(1, Math.ceil(rows.length / PER_PAGE));
    if (state.page > maxPage) state.page = maxPage;
    renderKpis(); renderChips(); renderTable();
    var mb = $id('mobileBadge');
    if (mb) {
      var pend = IS_TEACHER
        ? state.all.filter(function (t) { return (t.pendingGradeRecords || 0) > 0; }).length
        : state.all.reduce(function (n, s) { return n + (s.openRequests || 0); }, 0);
      mb.textContent = IS_TEACHER ? pend + ' Pending' : pend + ' Open Requests';
    }
  }

  function exportCSV() {
    var cols = IS_TEACHER
      ? ['id', 'name', 'subject', 'department', 'email', 'role', 'status', 'classesAssigned', 'yearsAtSchool', 'pendingGradeRecords', 'publishedGradeRecords']
      : ['id', 'name', 'gender', 'grade', 'class', 'status', 'advisor', 'parentName', 'parentEmail', 'gpaLive', 'attendancePct', 'openRequests'];
    var header = cols.join(',');
    var lines = state.filtered.map(function (r) {
      return cols.map(function (c) {
        var v = String(r[c] == null ? '' : r[c]).replace(/"/g, '""');
        return '"' + v + '"';
      }).join(',');
    });
    var blob = new Blob([header + '\n' + lines.join('\n')], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'ngis-' + CFG.kind + '-directory.csv';
    document.body.appendChild(a); a.click(); a.remove();
    toast('Exported ' + state.filtered.length + ' ' + PLURAL_LABEL.toLowerCase() + ' records to CSV.');
  }

  /* ---------- shell ---------- */
  var BTN_SECONDARY = 'inline-flex items-center gap-2 px-3.5 py-2 rounded-lg border border-slate-200/90 bg-white text-slate-700 text-xs font-medium hover:bg-slate-50 hover:border-slate-300 transition-all shadow-xs cursor-pointer min-h-[40px]';
  var BTN_PRIMARY = 'inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#125638] transition-all shadow-xs active:scale-[0.98] cursor-pointer min-h-[40px]';
  var SELECT_CLS = 'w-full text-xs py-2.5 pl-3 pr-8 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none transition-colors !bg-none';

  function renderShell() {
    var root = $id('profilesRoot');
    var pageTitle = IS_TEACHER ? 'Teacher Profiles' : 'Student Profiles';
    root.innerHTML = [
      '<div class="space-y-6 w-full">',
      // Section 1: Header Page Title & Top Actions (Title hidden on mobile to eliminate duplication with appbar)
      '  <section class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-1">',
      '    <div class="min-w-0">',
      '      <h1 class="text-2xl lg:text-[26px] font-medium text-slate-900 tracking-tight leading-tight hidden lg:block">' + pageTitle + '</h1>',
      '    </div>',
      '    <div class="flex items-center flex-wrap gap-2.5 shrink-0 w-full sm:w-auto justify-between sm:justify-end">',
      '      <button type="button" id="btnRefresh" class="' + BTN_SECONDARY + '">',
      '        <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        <span>Sync Registry</span>',
      '      </button>',
      '      <button type="button" id="btnExport" class="' + BTN_SECONDARY + '" title="Export the filtered directory as CSV">',
      '        <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        <span>Export (CSV)</span>',
      '      </button>',
      IS_TEACHER
        ? '      <button type="button" id="btnPasteExcel" class="' + BTN_SECONDARY + '" title="Paste from Excel or Google Sheets"><span class="material-symbols-outlined text-[16px] text-slate-500">content_paste</span><span>Paste from Excel</span></button>' +
          '      <button type="button" id="btnAddTeacher" class="' + BTN_PRIMARY + '"><svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2"></path></svg><span>Add Teacher</span></button>'
        : '',
      '    </div>',
      '  </section>',
      // Section 2: Executive Telemetry KPI Cards (Compact 2-column grid on mobile)
      '  <section class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4" data-purpose="metrics-telemetry" id="kpiGrid"></section>',
      // Section 3: Standalone Search & Filter Bar
      '  <section class="bg-white rounded-xl border border-[#E1E9E3] p-3 sm:p-4 shadow-2xs" data-purpose="filtering-controls">',
      '    <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">',
      '      <!-- Search Input Container -->',
      '      <div class="ngis-search relative flex-1 min-w-[240px] max-w-xl">',
      '        <span class="ngis-search-icon text-slate-400 pointer-events-none flex items-center">',
      '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        </span>',
      '        <input class="w-full text-xs placeholder:text-slate-400 text-slate-800" id="dirSearch" type="search" placeholder="Search ' + (IS_TEACHER ? 'teacher name, ID, code, subject or department...' : 'student name, ID, class or guardian...') + '">',
      '        <button class="ngis-search-clear" id="clearSearch" type="button" aria-label="Clear search">',
      '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        </button>',
      '      </div>',
      '      <!-- Filter Dropdowns & Status Badge -->',
      '      <div class="flex flex-wrap items-center gap-2 sm:gap-2.5 shrink-0">',
      '        <div class="relative flex-1 sm:flex-initial min-w-[130px]">',
      '          <select class="' + SELECT_CLS + '" id="deptFilter" style="background-image: none !important; -webkit-appearance: none !important; appearance: none !important;"></select>',
      '          <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg></span>',
      '        </div>',
      '        <div class="relative flex-1 sm:flex-initial min-w-[130px]">',
      '          <select class="' + SELECT_CLS + '" id="statusFilter" style="background-image: none !important; -webkit-appearance: none !important; appearance: none !important;"></select>',
      '          <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg></span>',
      '        </div>',
      '        <div class="relative flex-1 sm:flex-initial min-w-[140px]">',
      '          <select class="' + SELECT_CLS + '" id="sortSelect" style="background-image: none !important; -webkit-appearance: none !important; appearance: none !important;">',
      IS_TEACHER
        ? '<option value="name-asc">Sort: Name (A-Z)</option><option value="name-desc">Sort: Name (Z-A)</option><option value="target-desc">Sort: Workload Target</option><option value="classesAssigned-desc">Sort: Most Classes</option><option value="yearsAtSchool-desc">Sort: Most Senior</option>'
        : '<option value="name-asc">Sort: Name (A-Z)</option><option value="name-desc">Sort: Name (Z-A)</option><option value="gpaLive-desc">Sort: GPA (High to Low)</option><option value="gpaLive-asc">Sort: GPA (Low to High)</option><option value="attendancePct-desc">Sort: Attendance (High to Low)</option><option value="attendancePct-asc">Sort: Attendance (Low to High)</option>',
      '          </select>',
      '          <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg></span>',
      '        </div>',
      '        <button type="button" id="btnResetFilters" class="px-3.5 py-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 text-xs font-medium hover:bg-slate-50 hover:border-slate-300 transition-all shadow-xs cursor-pointer min-h-[40px] flex items-center justify-center gap-1.5">',
      '          <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '          <span>Reset</span>',
      '        </button>',
      '        <div class="flex items-center gap-1.5 pl-1 sm:pl-2 shrink-0">',
      '          <span class="text-xs text-slate-300 hidden md:inline">|</span>',
      '          <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-50 border border-slate-200/80 text-xs font-medium text-slate-600 whitespace-nowrap" id="filterStatusBadge">',
      '            <span class="w-1.5 h-1.5 rounded-full bg-[#176B45]"></span>',
      '            <span id="filterStatusText">Loading...</span>',
      '          </span>',
      '        </div>',
      '      </div>',
      '    </div>',
      '    <!-- Active Filter Feedback & Count -->',
      '    <div class="mt-3 pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-2 text-slate-600 text-xs font-medium">',
      '      <div class="flex flex-wrap items-center gap-2" id="filterChips"></div>',
      '      <span id="dirCount" class="text-xs text-slate-500"></span>',
      '    </div>',
      '  </section>',
      // Section 4: Data Container (Modern Rows for Teachers, Table for Students)
      IS_TEACHER
        ? [
            '  <div class="space-y-3 w-full" data-purpose="teacher-roster-list" id="rosterListContainer">',
            '    <!-- Desktop Header Guide (Hidden on mobile & tablet) -->',
            '    <div class="hidden lg:grid grid-cols-12 gap-4 px-5 py-3 text-[11px] font-medium uppercase tracking-wider text-slate-500 bg-white rounded-xl border border-[#E1E9E3] items-center shadow-2xs">',
            '      <div class="col-span-4">Faculty Member &amp; ID</div>',
            '      <div class="col-span-3">Department &amp; Subject</div>',
            '      <div class="col-span-2">Workload Target</div>',
            '      <div class="col-span-1">Status</div>',
            '      <div class="col-span-2 text-right">Actions</div>',
            '    </div>',
            '    <!-- Inline New Teacher Registration Card -->',
            '    <div id="newTeacherRowWrap" class="hidden"></div>',
            '    <!-- Row List -->',
            '    <div id="dirRows" class="space-y-2.5"></div>',
            '    <!-- Pagination & Bottom Statistics Bar -->',
            '    <div class="py-3 px-4 rounded-xl border border-[#E1E9E3] bg-white flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500 shadow-2xs">',
            '      <div class="flex items-center gap-2">',
            '        <span id="pagerInfo"></span>',
            '      </div>',
            '      <div class="flex items-center gap-1" id="pagerControls"></div>',
            '    </div>',
            '  </div>'
          ].join('\n')
        : [
            '  <div class="bg-white rounded-xl border border-slate-200/80 overflow-hidden shadow-xs" data-purpose="roster-table">',
            '    <div class="w-full overflow-x-auto">',
            '      <table class="w-full text-left text-xs whitespace-nowrap min-w-[960px] classes-table">',
            '        <thead><tr class="border-b border-slate-200/80 bg-slate-50/60 text-slate-500 font-medium tracking-wider text-[11px] uppercase" id="dirHead"></tr></thead>',
            '        <tbody class="divide-y divide-slate-100 font-normal text-slate-700 bg-white" id="dirBody"></tbody>',
            '      </table>',
            '    </div>',
            '    <!-- Pagination & Bottom Statistics Bar -->',
            '    <div class="py-3 px-4 border-t border-slate-200/80 bg-white flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">',
            '      <div class="flex items-center gap-2">',
            '        <span id="pagerInfo"></span>',
            '      </div>',
            '      <div class="flex items-center gap-1" id="pagerControls"></div>',
            '    </div>',
            '  </div>'
          ].join('\n'),
      '</div>'
    ].join('\n');

    if (!IS_TEACHER) {
      $id('dirHead').innerHTML = '<th class="w-10 py-3.5 pl-4 pr-2" scope="col"></th><th class="py-3.5 px-4 font-medium" scope="col">Student</th><th class="py-3.5 px-4 font-medium" scope="col">Grade &amp; Class</th><th class="py-3.5 px-4 font-medium" scope="col">Advisor</th><th class="py-3.5 px-4 font-medium" scope="col">GPA</th><th class="py-3.5 px-4 font-medium" scope="col">Attendance</th><th class="py-3.5 px-4 font-medium" scope="col">Requests</th><th class="py-3.5 px-4 font-medium" scope="col">Status</th><th class="py-3.5 pr-4 pl-4 text-right font-medium" scope="col">Actions</th>';
    }

    wireShell();
    renderFilterOptions();
  }

  function resetAllFilters() {
    state.search = ''; state.dept = 'ALL'; state.status = 'ALL'; state.sort = 'name-asc'; state.page = 1;
    var sInput = $id('dirSearch');
    if (sInput) sInput.value = '';
    var clr = $id('clearSearch') || $('.ngis-search-clear');
    if (clr) clr.classList.add('hidden');
    if ($id('deptFilter')) $id('deptFilter').value = 'ALL';
    if ($id('statusFilter')) $id('statusFilter').value = 'ALL';
    if ($id('sortSelect')) $id('sortSelect').value = 'name-asc';
    applyFilters();
  }

  function wireShell() {
    var sInput = $id('dirSearch');
    if (sInput) {
      sInput.addEventListener('input', function (e) {
        state.search = e.target.value; state.page = 1;
        var clr = $id('clearSearch') || $('.ngis-search-clear');
        if (clr) clr.classList.toggle('hidden', !state.search);
        applyFilters();
      });
    }
    var clrBtn = $id('clearSearch') || $('.ngis-search-clear');
    if (clrBtn) {
      clrBtn.addEventListener('click', function () {
        state.search = '';
        if (sInput) sInput.value = '';
        clrBtn.classList.add('hidden');
        applyFilters();
      });
    }
    $id('deptFilter').addEventListener('change', function (e) { state.dept = e.target.value; state.page = 1; applyFilters(); });
    $id('statusFilter').addEventListener('change', function (e) { state.status = e.target.value; state.page = 1; applyFilters(); });
    $id('sortSelect').addEventListener('change', function (e) { state.sort = e.target.value; state.page = 1; applyFilters(); });
    $id('btnExport').addEventListener('click', exportCSV);
    $id('btnRefresh').addEventListener('click', function () { loadDirectory(); toast('Directory refreshed from live data.'); });
    $id('btnResetFilters').addEventListener('click', resetAllFilters);

    var addBtn = $id('btnAddTeacher');
    if (addBtn) addBtn.addEventListener('click', toggleNewTeacherRow);

    var pasteBtn = $id('btnPasteExcel');
    if (pasteBtn) pasteBtn.addEventListener('click', openExcelImportModal);

    var dirRows = $id('dirRows');
    if (dirRows) {
      dirRows.addEventListener('click', function (e) {
        var actBtn = e.target.closest('[data-act]');
        if (!actBtn) return;
        var act = actBtn.getAttribute('data-act');
        var id = actBtn.getAttribute('data-id');

        if (act === 'toggle-expand') {
          toggleRowAccordion(id);
        } else if (act === 'edit-row') {
          openRowEditor(id);
        } else if (act === 'cancel-editor') {
          closeRowEditor(id);
        } else if (act === 'reset-editor') {
          resetRowEditor(id);
        } else if (act === 'save-editor') {
          saveRowEditor(id);
        } else if (act === 'view') {
          openProfile(id);
        } else if (act === 'toggle') {
          toggleStatus(id);
        }
      });
    }

    var dirBody = $id('dirBody');
    if (dirBody) {
      dirBody.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-act]');
        if (!btn) return;
        var id = btn.getAttribute('data-id');
        var act = btn.getAttribute('data-act');
        if (act === 'view') openProfile(id);
        else if (act === 'edit') openForm(id);
        else if (act === 'toggle') toggleStatus(id);
      });
    }

    $id('pagerControls').addEventListener('click', function (e) {
      var b = e.target.closest('[data-page]');
      if (!b) return;
      state.page = parseInt(b.getAttribute('data-page'), 10) || 1;
      renderTable();
      var c = $id('rosterListContainer') || $id('dirBody');
      if (c && c.scrollIntoView) c.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    $id('filterChips').addEventListener('click', function (e) {
      var b = e.target.closest('[data-chip-reset]');
      if (!b) return;
      var which = b.getAttribute('data-chip-reset');
      if (which === 'all') { resetAllFilters(); return; }
      if (which === 'dept') { state.dept = 'ALL'; $id('deptFilter').value = 'ALL'; }
      else if (which === 'status') { state.status = 'ALL'; $id('statusFilter').value = 'ALL'; }
      else if (which === 'search') { state.search = ''; if ($id('dirSearch')) $id('dirSearch').value = ''; var clr = $id('clearSearch') || $('.ngis-search-clear'); if (clr) clr.classList.add('hidden'); }
      applyFilters();
    });
  }
  function renderFilterOptions() {
    var deptSel = $id('deptFilter');
    var values = uniq(IS_TEACHER ? 'department' : 'grade');
    deptSel.innerHTML = '<option value="ALL">' + (IS_TEACHER ? 'Dept: All Faculty' : 'Grade: All Cohorts') + '</option>' +
      values.map(function (v) { return '<option value="' + esc(v) + '">' + (IS_TEACHER ? 'Dept: ' : 'Grade: ') + esc(v) + '</option>'; }).join('');
    var stSel = $id('statusFilter');
    var statuses = uniq('status');
    stSel.innerHTML = '<option value="ALL">Status: All</option>' +
      statuses.map(function (v) { return '<option value="' + esc(v) + '">Status: ' + esc(v) + '</option>'; }).join('');
  }

  /* ---------- KPI cards (computed from live directory) ---------- */
  function kpiCard(label, valueHtml, unit, icon) {
    return '<div class="bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">' +
      '<div class="flex items-start justify-between">' +
      '<div>' +
      '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">' + esc(label) + '</span>' +
      '<div class="flex items-baseline gap-2 mt-1">' +
      '<span class="text-3xl font-medium tracking-tight text-[#29352E] leading-none">' + valueHtml + '</span>' +
      (unit ? '<span class="text-xs font-medium text-slate-600">' + unit + '</span>' : '') +
      '</div>' +
      '</div>' +
      '<div class="w-10 h-10 rounded-lg bg-[#E8F3ED] text-[#176B45] flex items-center justify-center shrink-0">' +
      '<span class="material-symbols-outlined text-[22px]">' + icon + '</span>' +
      '</div>' +
      '</div>' +
      '</div>';
  }

  function renderKpis() {
    var grid = $id('kpiGrid');
    if (!grid) return;
    var total = state.all.length;
    if (IS_TEACHER) {
      var active = state.all.filter(function (t) { return String(t.status || '').toLowerCase() === 'active'; }).length;
      var activePct = total > 0 ? Math.round(active / total * 100) : 0;
      var depts = uniq('department').length;
      var pendRecords = state.all.reduce(function (n, t) { return n + (t.pendingGradeRecords || 0); }, 0);
      var pubRecords = state.all.reduce(function (n, t) { return n + (t.publishedGradeRecords || 0); }, 0);

      grid.innerHTML = [
        // Card 1: Credentialed Faculty
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider text-slate-500 block truncate">Credentialed Faculty</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight text-[#29352E]">' + total + '</span>',
        '        <span class="text-[11px] sm:text-xs font-medium ' + (total > 0 ? 'text-emerald-700' : 'text-slate-400') + '">' + (total > 0 ? (activePct + '% Active') : '0 Active') + '</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">badge</span>',
        '    </div>',
        '  </div>',
        '</div>',

        // Card 2: Active Standing & Clearance Rate with Two-Tone Bar
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider text-slate-500 block truncate">Clearance Rate</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight text-[#29352E]">' + (total > 0 ? (activePct + '%') : '—') + '</span>',
        '        <span class="text-[11px] sm:text-xs font-normal text-slate-400">' + (total > 0 ? 'Target: 100%' : 'No records') + '</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">verified</span>',
        '    </div>',
        '  </div>',
        '  <div class="pt-2 mt-1">',
        '    <div class="flex items-center justify-between text-[11px] sm:text-xs mb-1.5">',
        '      <span class="text-slate-600 font-normal truncate">' + active + ' active</span>',
        '      <span class="text-[#991b1b] font-medium truncate">' + (total - active) + ' on leave</span>',
        '    </div>',
        '    <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">',
        (total > 0
          ? '      <div class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: ' + activePct + '%"></div>' +
            '      <div class="bg-[#991b1b] h-full rounded-full transition-all duration-500" style="width: ' + (100 - activePct) + '%"></div>'
          : '      <div class="bg-slate-200 h-full rounded-full w-full"></div>'),
        '    </div>',
        '  </div>',
        '</div>',

        // Card 3: Pending Grade Records
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between relative overflow-hidden">',
        (pendRecords > 0 ? '  <div class="absolute right-0 top-0 w-16 sm:w-24 h-16 sm:h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>' : ''),
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider ' + (pendRecords > 0 ? 'text-[#991b1b]' : 'text-slate-500') + ' block truncate">Pending Clearances</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight ' + (pendRecords > 0 ? 'text-[#991b1b]' : 'text-[#29352E]') + '">' + pendRecords + '</span>',
        (pendRecords > 0
          ? '        <span class="inline-flex items-center gap-1 text-[11px] sm:text-xs font-medium text-[#991b1b] bg-rose-100/90 px-1.5 py-0.5 rounded">High Priority</span>'
          : '        <span class="text-[11px] sm:text-xs font-medium text-emerald-700">All Cleared</span>'),
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg ' + (pendRecords > 0 ? 'bg-rose-100/90 text-[#991b1b]' : 'bg-emerald-50 text-[#176B45]') + ' flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">' + (pendRecords > 0 ? 'pending_actions' : 'check_circle') + '</span>',
        '    </div>',
        '  </div>',
        '</div>',

        // Card 4: Published Records / Turnaround
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider text-slate-500 block truncate">Published Records</span>',
        '      <div class="flex items-baseline gap-1 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight text-[#29352E]">' + pubRecords + '<span class="text-sm font-normal text-slate-400"> recs</span></span>',
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">publish</span>',
        '    </div>',
        '  </div>',
        '</div>'
      ].join('\n');
    } else {
      // Students
      var gpa = total ? state.all.reduce(function (n, s) { return n + (Number(s.gpaLive) || 0); }, 0) / total : 0;
      var att = total ? state.all.reduce(function (n, s) { return n + (Number(s.attendancePct) || 0); }, 0) / total : 0;
      var open = state.all.reduce(function (n, s) { return n + (s.openRequests || 0); }, 0);
      var classes = uniq('class').length;
      var gpaPct = total > 0 ? Math.min(100, Math.round((gpa / 4.0) * 100)) : 0;

      grid.innerHTML = [
        // Card 1: Enrolled Students
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider text-slate-500 block truncate">Enrolled Students</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight text-[#29352E]">' + total + '</span>',
        '        <span class="text-[11px] sm:text-xs font-medium ' + (total > 0 ? 'text-emerald-700' : 'text-slate-400') + '">' + (total > 0 ? '100% Active' : '0 Enrolled') + '</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">school</span>',
        '    </div>',
        '  </div>',
        '</div>',

        // Card 2: Cohort GPA Standing
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider text-slate-500 block truncate">Cohort Standing (GPA)</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight text-[#29352E]">' + (total > 0 ? num(gpa) : '—') + '</span>',
        '        <span class="text-[11px] sm:text-xs font-normal text-slate-400">' + (total > 0 ? '/ 4.00' : 'No records') + '</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">verified</span>',
        '    </div>',
        '  </div>',
        '  <div class="pt-2 mt-1">',
        '    <div class="flex items-center justify-between text-[11px] sm:text-xs mb-1.5">',
        '      <span class="text-slate-600 font-normal truncate">Live term performance</span>',
        '      <span class="text-emerald-700 font-medium truncate">' + (total > 0 ? (gpaPct + '% of max') : '—') + '</span>',
        '    </div>',
        '    <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">',
        (total > 0
          ? '      <div class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: ' + gpaPct + '%"></div>'
          : '      <div class="bg-slate-200 h-full rounded-full w-full"></div>'),
        '    </div>',
        '  </div>',
        '</div>',

        // Card 3: Open Service Requests
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between relative overflow-hidden">',
        (open > 0 ? '  <div class="absolute right-0 top-0 w-16 sm:w-24 h-16 sm:h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>' : ''),
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider ' + (open > 0 ? 'text-[#991b1b]' : 'text-slate-500') + ' block truncate">Open Service Requests</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight ' + (open > 0 ? 'text-[#991b1b]' : 'text-[#29352E]') + '">' + open + '</span>',
        (open > 0
          ? '        <span class="inline-flex items-center gap-1 text-[11px] sm:text-xs font-medium text-[#991b1b] bg-rose-100/90 px-1.5 py-0.5 rounded">High Priority</span>'
          : '        <span class="text-[11px] sm:text-xs font-medium text-emerald-700">All Completed</span>'),
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg ' + (open > 0 ? 'bg-rose-100/90 text-[#991b1b]' : 'bg-emerald-50 text-[#176B45]') + ' flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">' + (open > 0 ? 'pending_actions' : 'check_circle') + '</span>',
        '    </div>',
        '  </div>',
        '</div>',

        // Card 4: Attendance Average
        '<div class="telemetry-card bg-white rounded-xl p-3.5 sm:p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[10px] sm:text-[11px] font-medium uppercase tracking-wider text-slate-500 block truncate">Average Attendance</span>',
        '      <div class="flex items-baseline gap-1.5 sm:gap-2 mt-1">',
        '        <span class="text-2xl sm:text-3xl font-medium tracking-tight text-[#29352E]">' + (total > 0 ? (num(att, 1) + '%') : '—') + '</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[18px] sm:text-[22px]">fact_check</span>',
        '    </div>',
        '  </div>',
        '</div>'
      ].join('\n');
    }
  }

  /* ---------- chips ---------- */
  function chip(label, resetKey, tone) {
    return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full ' + tone + ' text-xs font-medium">' +
      '<span class="w-1.5 h-1.5 rounded-full bg-current opacity-70"></span>' + esc(label) +
      '<button class="hover:opacity-70 leading-none cursor-pointer" type="button" data-chip-reset="' + resetKey + '"><span class="material-symbols-outlined text-[11px]">close</span></button></span>';
  }
  function renderChips() {
    var box = $id('filterChips');
    if (!box) return;
    var html = '<span class="w-2 h-2 rounded-full bg-[#94a3b8] inline-block"></span>' +
      '<span class="uppercase tracking-wider text-xs font-medium text-slate-600">Filters:</span>';
    if (state.search) html += chip('Search: "' + state.search + '"', 'search', 'bg-slate-50 text-slate-600 border border-slate-200');
    if (state.dept !== 'ALL') html += chip((IS_TEACHER ? 'Dept: ' : 'Grade: ') + state.dept, 'dept', 'bg-[#E8F3ED] text-[#204F3A] border border-[#c4dece]');
    if (state.status !== 'ALL') html += chip('Status: ' + state.status, 'status', 'bg-slate-50 text-slate-600 border border-slate-200');
    if (state.search || state.dept !== 'ALL' || state.status !== 'ALL') {
      html += '<button class="text-xs text-slate-600 hover:underline ml-1 cursor-pointer font-medium" type="button" data-chip-reset="all">Reset all filters</button>';
    } else {
      html += '<span class="text-[#94a3b8] ml-1 text-xs font-medium">None applied</span>';
    }
    box.innerHTML = html;
    $id('dirCount').innerHTML = 'Showing <span class="text-slate-800 font-medium">' + state.filtered.length + '</span> of <span class="text-slate-800 font-medium">' + state.all.length + '</span> ' + PLURAL_LABEL.toLowerCase();
    var st = $id('filterStatusText');
    if (st) st.textContent = state.filtered.length + ' ' + PLURAL_LABEL.toLowerCase();
  }

  /* ---------- table ---------- */
  function statusBadge(status) {
    var s = String(status || '—');
    var l = s.toLowerCase();
    var tone = 'bg-slate-100 text-slate-600', dot = 'bg-slate-300';
    if (l === 'active' || l === 'cleared' || l === 'enrolled') { tone = 'bg-[#E8F3ED] text-[#204F3A]'; dot = 'bg-[#176B45]'; }
    else if (l === 'pending' || l === 'probation' || l === 'transfer' || l === 'on-leave') { tone = 'bg-[#ffeadb] text-[#822714]'; dot = 'bg-[#b8541f]'; }
    else if (l === 'inactive' || l === 'suspended' || l === 'graduated') { tone = 'bg-slate-100 text-slate-600'; dot = 'bg-slate-300'; }
    return '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ' + tone + '">' +
      '<span class="w-1.5 h-1.5 rounded-full ' + dot + '"></span>' + esc(s) + '</span>';
  }

  function actionBtn(act, id, icon, label) {
    return '<button type="button" data-act="' + act + '" data-id="' + esc(id) + '" title="' + esc(label) + '" aria-label="' + esc(label) + '" class="w-8 h-8 rounded-lg bg-slate-100 hover:bg-[#E8F3ED] text-slate-600 flex items-center justify-center transition-colors cursor-pointer"><span class="material-symbols-outlined text-[16px] text-slate-700">' + icon + '</span></button>';
  }

  function nameCell(r) {
    return '<div class="flex items-center gap-2.5">' +
      '<div class="w-7 h-7 rounded-full bg-[#E8F3ED] text-[#176B45] flex items-center justify-center font-medium text-xs shrink-0">' + esc(initials(r.name)) + '</div>' +
      '<div class="flex flex-col min-w-0">' +
      '<span data-act="view" data-id="' + esc(r.id) + '" class="font-medium text-sm text-slate-900 hover:text-[#176B45] cursor-pointer truncate leading-tight">' + esc(r.name) + '</span>' +
      '<span class="text-[11px] text-slate-500">' + esc(r.id) + (IS_TEACHER ? ' · ' + esc(r.role || 'Faculty') : ' · ' + esc(r.class || r.grade || 'Student')) + '</span>' +
      '</div></div>';
  }

  /* ---------- Teacher Row Card & Inline Accordion Editor ---------- */
  function teacherRowHtml(r) {
    var teacherCode = r.code || r.id || 'TCH';
    var subjectColor = getSubjectColor(r.subject);
    var classesAssigned = (r.assignments && r.assignments.length) ? r.assignments.length : (r.classesAssigned != null ? r.classesAssigned : (r.classes ? r.classes.length : 0));
    var targetHours = r.target || (classesAssigned ? classesAssigned * 3 : 17);
    var maxDaily = r.max_daily || 5;
    var isActive = String(r.status || '').toLowerCase() === 'active';
    var isLeave = String(r.status || '').toLowerCase().indexOf('leave') !== -1;
    var statusTone = isActive ? 'bg-[#E8F3ED] text-[#176B45]' : (isLeave ? 'bg-[#ffeadb] text-[#822714]' : 'bg-slate-100 text-slate-600');
    var statusDot = isActive ? 'bg-[#176B45]' : (isLeave ? 'bg-[#b8541f]' : 'bg-slate-400');
    var gender = r.gender || 'Male';

    var deptSummary = esc(r.department || 'MoEYS Faculty');
    var subjectLabel = esc(r.subject || 'General');
    if (r.assignments && r.assignments.length > 0) {
      var dMap = {};
      r.assignments.forEach(function (a) {
        var d = (a.department || '').replace(' Studies', '').replace(' Language', '').replace(' Department', '');
        dMap[d] = dMap[d] || [];
        var c = (a.class || '').replace('Grade ', '');
        if (c && dMap[d].indexOf(c) === -1) dMap[d].push(c);
      });
      var dKeys = Object.keys(dMap);
      if (dKeys.length > 1) {
        deptSummary = dKeys.map(function (k) { return k + ': ' + dMap[k].join(', '); }).join(' · ');
      } else if (dKeys.length === 1 && dMap[dKeys[0]].length > 0) {
        deptSummary = dKeys[0] + ': ' + dMap[dKeys[0]].join(', ');
      }
      var distinctSubjs = [];
      r.assignments.forEach(function (a) {
        if (a.subject && distinctSubjs.indexOf(a.subject) === -1) distinctSubjs.push(a.subject);
      });
      if (distinctSubjs.length > 1) {
        subjectLabel = esc(distinctSubjs.slice(0, 2).join(', ')) + (distinctSubjs.length > 2 ? ' +' + (distinctSubjs.length - 2) : '');
      }
    }

    return [
      '<div class="teacher-row-card bg-white rounded-xl border border-[#E1E9E3] hover:border-slate-300 transition-all shadow-2xs overflow-hidden" data-id="' + esc(r.id) + '" id="teacherCard_' + esc(r.id) + '">',
      // Row Bar (Clickable to toggle expand)
      '  <div class="p-3 sm:p-4 flex flex-col lg:grid lg:grid-cols-12 gap-3 lg:gap-4 items-start lg:items-center cursor-pointer select-none transition-colors hover:bg-slate-50/50" data-act="toggle-expand" data-id="' + esc(r.id) + '">',
      '    <!-- Col 1: Avatar, Name, Code, ID -->',
      '    <div class="lg:col-span-4 flex items-center gap-3 min-w-0 w-full">',
      '      <div class="w-10 h-10 rounded-full bg-[#E8F3ED] text-[#176B45] flex items-center justify-center font-medium text-xs shrink-0 shadow-2xs border border-[#176B45]/15">',
      '        ' + esc(initials(r.name)),
      '      </div>',
      '      <div class="min-w-0 flex-1">',
      '        <div class="flex items-center gap-2 flex-wrap">',
      '          <span class="font-medium text-sm text-slate-900 hover:text-[#176B45] transition-colors truncate" data-act="view" data-id="' + esc(r.id) + '">' + esc(r.name) + '</span>',
      '          <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-100 text-slate-700 border border-slate-200/80">' + esc(teacherCode) + '</span>',
      '        </div>',
      '        <div class="text-[11px] text-slate-500 flex items-center gap-1.5 truncate mt-0.5">',
      '          <span>' + esc(r.id) + '</span>',
      '          <span class="text-slate-300">•</span>',
      '          <span>' + esc(r.role || 'Faculty') + '</span>',
      '        </div>',
      '      </div>',
      '    </div>',

      '    <!-- Col 2: Department & Subject -->',
      '    <div class="lg:col-span-3 min-w-0 w-full flex flex-col justify-center">',
      '      <div class="flex items-center gap-1.5">',
      '        <span class="w-2 h-2 rounded-full shrink-0" style="background-color: ' + subjectColor + ';"></span>',
      '        <span class="font-medium text-xs text-slate-800 truncate">' + subjectLabel + '</span>',
      '      </div>',
      '      <span class="text-[11px] text-slate-500 truncate ml-3.5">' + deptSummary + '</span>',
      '    </div>',

      '    <!-- Col 3: Workload & Classes -->',
      '    <div class="lg:col-span-2 min-w-0 w-full flex items-center gap-2">',
      '      <div class="flex flex-col">',
      '        <span class="text-xs font-medium text-slate-700">' + targetHours + ' hrs/wk</span>',
      '        <span class="text-[11px] text-slate-400">' + classesAssigned + ' classes assigned</span>',
      '      </div>',
      '    </div>',

      '    <!-- Col 4: Status -->',
      '    <div class="lg:col-span-1 min-w-0 flex items-center">',
      '      <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ' + statusTone + '">',
      '        <span class="w-1.5 h-1.5 rounded-full ' + statusDot + '"></span>' + esc(r.status || 'Active') + '',
      '      </span>',
      '    </div>',

      '    <!-- Col 5: Actions -->',
      '    <div class="lg:col-span-2 flex items-center justify-end gap-1.5 w-full shrink-0" >',
      '      <button type="button" data-act="edit-row" data-id="' + esc(r.id) + '" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-[#E8F3ED] hover:text-[#176B45] hover:border-[#176B45]/40 transition-colors cursor-pointer flex items-center gap-1 min-h-[32px]">',
      '        <span class="material-symbols-outlined text-[15px]">edit</span>',
      '        <span>Edit</span>',
      '      </button>',
      '      <button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors cursor-pointer flex items-center gap-1 min-h-[32px]" title="View Full Profile">',
      '        <span>Profile</span>',
      '      </button>',
      '      <button type="button" data-act="toggle" data-id="' + esc(r.id) + '" title="' + (isActive ? 'Deactivate record' : 'Activate record') + '" class="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" aria-label="Toggle status">',
      '        <span class="material-symbols-outlined text-[18px]">more_vert</span>',
      '      </button>',
      '      <button type="button" data-act="toggle-expand" data-id="' + esc(r.id) + '" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-all cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" title="Expand Details" aria-label="Expand Details">',
      '        <span class="material-symbols-outlined text-[20px] transition-transform duration-200 chevron-icon" id="chevron_' + esc(r.id) + '">expand_more</span>',
      '      </button>',
      '    </div>',
      '  </div>',

      // Inline Expandable Details Editor
      '  <div class="teacher-inline-editor border-t border-[#E1E9E3] bg-[#F7F9F7]/90 p-4 sm:p-5 rounded-b-xl hidden" id="editor_' + esc(r.id) + '" >',
      '    <div class="flex items-center justify-between pb-3.5 mb-5 border-b border-slate-200/90">',
      '      <div class="flex items-center gap-2.5">',
      '        <div class="w-2.5 h-2.5 rounded-full bg-[#176B45]"></div>',
      '        <h3 class="text-xs font-medium uppercase tracking-wider text-[#29352E]">',
      '          Faculty Member Record Editor — ' + esc(r.name) + ' <span class="text-slate-400 font-normal">(' + esc(r.id) + ')</span>',
      '        </h3>',
      '      </div>',
      '      <span class="text-[11px] text-slate-500 hidden sm:inline">Inline editor · Instant synchronization to Live Timetable</span>',
      '    </div>',

      '    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-left">',
      '      <!-- SECTION A — Basic Information -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">person</span>',
      '          <span>Section A — Basic Information</span>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edName_' + r.id + '">Full Name <span class="text-rose-500">*</span></label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edName_' + r.id + '" type="text" value="' + esc(r.name || '') + '">',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edGender_' + r.id + '">Gender</label>',
      '            <select class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edGender_' + r.id + '">',
      '              <option value="Male"' + (gender === 'Male' ? ' selected' : '') + '>Male</option>',
      '              <option value="Female"' + (gender === 'Female' ? ' selected' : '') + '>Female</option>',
      '            </select>',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edPhone_' + r.id + '">Phone</label>',
      '            <input class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edPhone_' + r.id + '" type="text" value="' + esc(r.phone || '') + '">',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edEmail_' + r.id + '">Email Address <span class="text-rose-500">*</span></label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edEmail_' + r.id + '" type="email" value="' + esc(r.email || '') + '">',
      '        </div>',
      '      </div>',

      '      <!-- SECTION B — Employment -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">work</span>',
      '          <span>Section B — Employment</span>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edRole_' + r.id + '">Position / Role</label>',
      '          <select class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edRole_' + r.id + '">',
      '            <option value="Faculty"' + (r.role === 'Faculty' ? ' selected' : '') + '>Faculty</option>',
      '            <option value="Senior Faculty"' + (r.role === 'Senior Faculty' ? ' selected' : '') + '>Senior Faculty</option>',
      '            <option value="Head of Department"' + (r.role === 'Head of Department' ? ' selected' : '') + '>Head of Department</option>',
      '            <option value="Coordinator"' + (r.role === 'Coordinator' ? ' selected' : '') + '>Coordinator</option>',
      '          </select>',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edEmploy_' + r.id + '">Category</label>',
      '            <select class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edEmploy_' + r.id + '">',
      '              <option value="Full-time"' + (r.employmentType === 'Full-time' ? ' selected' : '') + '>Full-time</option>',
      '              <option value="Part-time"' + (r.employmentType === 'Part-time' ? ' selected' : '') + '>Part-time</option>',
      '              <option value="Contract"' + (r.employmentType === 'Contract' ? ' selected' : '') + '>Contract</option>',
      '            </select>',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edYears_' + r.id + '">Years at School</label>',
      '            <input class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edYears_' + r.id + '" type="number" min="0" value="' + (r.yearsAtSchool || 0) + '">',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edRank_' + r.id + '">Rank / Classification</label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edRank_' + r.id + '" type="text" value="' + esc(r.rank || 'Senior Faculty') + '">',
      '        </div>',
      '      </div>',

      '      <!-- SECTION C — Academic Information -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">menu_book</span>',
      '          <span>Section C — Academic Information</span>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edDept_' + r.id + '">Department <span class="text-rose-500">*</span></label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edDept_' + r.id + '" type="text" value="' + esc(r.department || '') + '">',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edSubject_' + r.id + '">Primary Subject <span class="text-rose-500">*</span></label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edSubject_' + r.id + '" type="text" value="' + esc(r.subject || r.department || 'General') + '">',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edCode_' + r.id + '">Teacher Code</label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] font-mono font-medium" id="edCode_' + r.id + '" type="text" value="' + esc(r.code || teacherCode) + '">',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edQualified_' + r.id + '">Qualified Subjects</label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edQualified_' + r.id + '" type="text" placeholder="e.g. Khmer, Literature, History" value="' + esc(r.qualifiedSubjects || r.subject || '') + '">',
      '        </div>',
      '      </div>',

      '      <!-- SECTION D & E — Scheduling & Status -->',
      '      <div class="bg-white p-3.5 rounded-xl border border-[#E1E9E3] space-y-3 shadow-2xs">',
      '        <div class="flex items-center gap-1.5 pb-1 border-b border-slate-100 text-xs font-medium text-slate-700">',
      '          <span class="material-symbols-outlined text-[16px] text-[#176B45]">tune</span>',
      '          <span>Section D &amp; E — Scheduling &amp; Status</span>',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edTarget_' + r.id + '">Target (hrs/wk)</label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edTarget_' + r.id + '" type="number" min="1" max="40" value="' + (r.target || 17) + '">',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edMaxDaily_' + r.id + '">Max / Day</label>',
      '            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edMaxDaily_' + r.id + '" type="number" min="1" max="10" value="' + (r.max_daily || 5) + '">',
      '          </div>',
      '        </div>',
      '        <div class="grid grid-cols-2 gap-2">',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edClasses_' + r.id + '">Classes</label>',
      '            <input class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edClasses_' + r.id + '" type="number" min="0" value="' + (r.classesAssigned != null ? r.classesAssigned : 0) + '">',
      '          </div>',
      '          <div>',
      '            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edStatus_' + r.id + '">Status</label>',
      '            <select class="w-full text-xs py-2 px-2 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edStatus_' + r.id + '">',
      '              <option value="Active"' + (String(r.status || '').toLowerCase() === 'active' ? ' selected' : '') + '>Active</option>',
      '              <option value="On Leave"' + (String(r.status || '').toLowerCase().indexOf('leave') !== -1 ? ' selected' : '') + '>On Leave</option>',
      '              <option value="Inactive"' + (String(r.status || '').toLowerCase() === 'inactive' ? ' selected' : '') + '>Inactive</option>',
      '            </select>',
      '          </div>',
      '        </div>',
      '        <div>',
      '          <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edNotes_' + r.id + '">Scheduling Notes</label>',
      '          <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edNotes_' + r.id + '" type="text" placeholder="Special availability or notes..." value="' + esc(r.notes || '') + '">',
      '        </div>',
      '      </div>',
      '    </div>',

      '    <!-- Bottom Action Bar -->',
      '    <div class="mt-5 pt-4 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3">',
      '      <div class="flex items-center gap-2 text-xs text-slate-500">',
      '        <span class="material-symbols-outlined text-[16px] text-[#176B45]">check_circle</span>',
      '        <span>Click Save Changes to commit directly to the faculty database.</span>',
      '      </div>',
      '      <div class="flex items-center gap-2 w-full sm:w-auto justify-end">',
      '        <button type="button" data-act="reset-editor" data-id="' + esc(r.id) + '" class="px-3 py-2 text-xs font-medium text-slate-500 hover:text-slate-800 transition cursor-pointer">',
      '          Reset',
      '        </button>',
      '        <button type="button" data-act="cancel-editor" data-id="' + esc(r.id) + '" class="px-4 py-2 rounded-lg border border-[#E1E9E3] bg-white text-xs font-medium text-slate-700 hover:bg-slate-50 transition cursor-pointer">',
      '          Cancel',
      '        </button>',
      '        <button type="button" data-act="save-editor" data-id="' + esc(r.id) + '" class="px-5 py-2 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium shadow-xs flex items-center gap-1.5 transition active:scale-[0.98] cursor-pointer" id="btnSaveEd_' + esc(r.id) + '">',
      '          <span class="material-symbols-outlined text-[16px]">save</span>',
      '          <span>Save Changes</span>',
      '        </button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('\n');
  }

  function toggleRowAccordion(id) {
    var editor = $id('editor_' + id);
    var chevron = $id('chevron_' + id);
    if (!editor) return;
    var isHidden = editor.classList.contains('hidden');
    if (isHidden) {
      editor.classList.remove('hidden');
      if (chevron) chevron.classList.add('is-open');
    } else {
      editor.classList.add('hidden');
      if (chevron) chevron.classList.remove('is-open');
    }
  }

  function openRowEditor(id) {
    var editor = $id('editor_' + id);
    var chevron = $id('chevron_' + id);
    if (!editor) return;
    editor.classList.remove('hidden');
    if (chevron) chevron.classList.add('is-open');
    var firstInput = $id('edName_' + id);
    if (firstInput) setTimeout(function () { firstInput.focus(); }, 50);
  }

  function closeRowEditor(id) {
    var editor = $id('editor_' + id);
    var chevron = $id('chevron_' + id);
    if (editor) editor.classList.add('hidden');
    if (chevron) chevron.classList.remove('is-open');
  }

  function resetRowEditor(id) {
    var r = state.all.filter(function (x) { return String(x.id) === String(id); })[0];
    if (!r) return;
    var nameEl = $id('edName_' + id); if (nameEl) nameEl.value = r.name || '';
    var genderEl = $id('edGender_' + id); if (genderEl) genderEl.value = r.gender || 'Male';
    var phoneEl = $id('edPhone_' + id); if (phoneEl) phoneEl.value = r.phone || '';
    var emailEl = $id('edEmail_' + id); if (emailEl) emailEl.value = r.email || '';
    var roleEl = $id('edRole_' + id); if (roleEl) roleEl.value = r.role || 'Faculty';
    var empEl = $id('edEmploy_' + id); if (empEl) empEl.value = r.employmentType || 'Full-time';
    var yearsEl = $id('edYears_' + id); if (yearsEl) yearsEl.value = r.yearsAtSchool || 0;
    var rankEl = $id('edRank_' + id); if (rankEl) rankEl.value = r.rank || 'Senior Faculty';
    var deptEl = $id('edDept_' + id); if (deptEl) deptEl.value = r.department || '';
    var subjEl = $id('edSubject_' + id); if (subjEl) subjEl.value = r.subject || '';
    var codeEl = $id('edCode_' + id); if (codeEl) codeEl.value = r.code || id;
    var qualEl = $id('edQualified_' + id); if (qualEl) qualEl.value = r.qualifiedSubjects || r.subject || '';
    var targetEl = $id('edTarget_' + id); if (targetEl) targetEl.value = r.target || 17;
    var maxDailyEl = $id('edMaxDaily_' + id); if (maxDailyEl) maxDailyEl.value = r.max_daily || 5;
    var clsEl = $id('edClasses_' + id); if (clsEl) clsEl.value = r.classesAssigned != null ? r.classesAssigned : 0;
    var stEl = $id('edStatus_' + id); if (stEl) stEl.value = r.status || 'Active';
    var notesEl = $id('edNotes_' + id); if (notesEl) notesEl.value = r.notes || '';
    toast('Fields reset to saved values.');
  }

  function saveRowEditor(id) {
    var name = fv('edName_' + id);
    var email = fv('edEmail_' + id);
    var department = fv('edDept_' + id) || 'General';
    var subject = fv('edSubject_' + id) || department || 'General';

    if (!name || !email) {
      toast('Name and Email are required.', true);
      return;
    }

    var payload = {
      name: name,
      email: email,
      department: department,
      subject: subject,
      gender: fv('edGender_' + id),
      phone: fv('edPhone_' + id),
      role: fv('edRole_' + id),
      employmentType: fv('edEmploy_' + id),
      yearsAtSchool: parseInt(fv('edYears_' + id), 10) || 0,
      rank: fv('edRank_' + id),
      code: fv('edCode_' + id) || id,
      qualifiedSubjects: fv('edQualified_' + id),
      target: parseInt(fv('edTarget_' + id), 10) || 17,
      max_daily: parseInt(fv('edMaxDaily_' + id), 10) || 5,
      classesAssigned: parseInt(fv('edClasses_' + id), 10) || 0,
      status: fv('edStatus_' + id),
      notes: fv('edNotes_' + id)
    };

    var btn = $id('btnSaveEd_' + id);
    if (btn) btn.disabled = true;

    api(API_BASE + '/' + encodeURIComponent(id), { method: 'PUT', body: JSON.stringify(payload) })
      .then(function (res) {
        if (btn) btn.disabled = false;
        // Update in memory
        state.all.forEach(function (t) {
          if (String(t.id) === String(id)) Object.assign(t, payload);
        });
        state.filtered.forEach(function (t) {
          if (String(t.id) === String(id)) Object.assign(t, payload);
        });
        // Close editor & re-render table to reflect updated indicators
        closeRowEditor(id);
        renderTable();
        renderKpis();
        toast('Record for ' + payload.name + ' saved.');
      })
      .catch(function (err) {
        if (btn) btn.disabled = false;
        toast(apiError(err, 'Failed to save teacher updates'), true);
      });
  }

  /* ---------- Inline New Teacher Form ---------- */
  function toggleNewTeacherRow() {
    var wrap = $id('newTeacherRowWrap');
    if (!wrap) return;
    var isHidden = wrap.classList.contains('hidden');
    if (!isHidden) {
      wrap.classList.add('hidden');
      return;
    }
    wrap.innerHTML = [
      '<div class="bg-white rounded-xl border-2 border-[#176B45]/40 p-5 shadow-sm space-y-4 mb-3 animate-fade-in">',
      '  <div class="flex items-center justify-between pb-3 border-b border-slate-200">',
      '    <div class="flex items-center gap-2">',
      '      <span class="w-2.5 h-2.5 rounded-full bg-[#176B45]"></span>',
      '      <h3 class="text-sm font-medium text-slate-900">Register New Faculty Member</h3>',
      '    </div>',
      '    <button type="button" id="btnCancelNewTeacher" class="text-slate-400 hover:text-slate-600 cursor-pointer p-1 rounded-lg hover:bg-slate-100">',
      '      <span class="material-symbols-outlined text-[18px]">close</span>',
      '    </button>',
      '  </div>',
      '  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3.5 text-left text-xs">',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_name">Full Name <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_name" type="text" placeholder="e.g. Sok Dara">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_email">Email <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_email" type="email" placeholder="e.g. sok.dara@ngis.edu.kh">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_dept">Department <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_dept" type="text" placeholder="e.g. Khmer Literature">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_subject">Primary Subject <span class="text-rose-500">*</span></label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45]" id="new_subject" type="text" placeholder="e.g. Khmer Literature">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_code">Teacher Code</label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 font-mono" id="new_code" type="text" placeholder="e.g. K2">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_role">Position / Role</label>',
      '      <select class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800" id="new_role">',
      '        <option value="Faculty">Faculty</option>',
      '        <option value="Senior Faculty">Senior Faculty</option>',
      '        <option value="Head of Department">Head of Department</option>',
      '        <option value="Coordinator">Coordinator</option>',
      '      </select>',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_target">Target Workload (hrs/wk)</label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800" id="new_target" type="number" value="17" min="1" max="40">',
      '    </div>',
      '    <div>',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="new_phone">Phone</label>',
      '      <input class="w-full text-xs py-2 px-3 rounded-lg border border-[#E1E9E3] bg-white text-slate-800" id="new_phone" type="text" placeholder="+855 ...">',
      '    </div>',
      '  </div>',
      '  <div class="flex items-center justify-between pt-3 border-t border-slate-200">',
      '    <span class="text-xs text-rose-600 font-medium" id="newTeacherError"></span>',
      '    <div class="flex items-center gap-2">',
      '      <button type="button" id="btnDiscardNewTeacher" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-slate-50 cursor-pointer">Cancel</button>',
      '      <button type="button" id="btnSubmitNewTeacher" class="px-5 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs cursor-pointer flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px]">person_add</span><span>Register Teacher</span></button>',
      '    </div>',
      '  </div>',
      '</div>'
    ].join('\n');

    wrap.classList.remove('hidden');

    $id('btnCancelNewTeacher').addEventListener('click', function () { wrap.classList.add('hidden'); });
    $id('btnDiscardNewTeacher').addEventListener('click', function () { wrap.classList.add('hidden'); });
    $id('btnSubmitNewTeacher').addEventListener('click', submitNewTeacher);
  }

  function submitNewTeacher() {
    var name = fv('new_name');
    var email = fv('new_email');
    var dept = fv('new_dept');
    var subject = fv('new_subject');
    var errEl = $id('newTeacherError');

    if (!name || !email || !dept || !subject) {
      if (errEl) errEl.textContent = 'Name, email, department, and subject are required.';
      return;
    }

    var body = {
      name: name,
      email: email,
      department: dept,
      subject: subject,
      role: fv('new_role') || 'Faculty',
      code: fv('new_code') || '',
      target: parseInt(fv('new_target'), 10) || 17,
      phone: fv('new_phone') || '',
      status: 'active'
    };

    var btn = $id('btnSubmitNewTeacher');
    if (btn) btn.disabled = true;

    api(API_BASE, { method: 'POST', body: JSON.stringify(body) })
      .then(function (res) {
        if (btn) btn.disabled = false;
        var newRec = (res && res.data) || body;
        state.all.unshift(newRec);
        $id('newTeacherRowWrap').classList.add('hidden');
        applyFilters();
        toast('Teacher ' + name + ' registered.');
      })
      .catch(function (err) {
        if (btn) btn.disabled = false;
        if (errEl) errEl.textContent = apiError(err, 'Failed to create teacher record');
      });
  }

  /* ---------- Excel Bulk Import Workflow ---------- */
  var parsedExcelTeachers = [];
  function openExcelImportModal() {
    var m = $id('excelImportModal');
    if (!m) return;
    $id('excelPasteInput').value = '';
    $id('excelPreviewSection').classList.add('hidden');
    $id('excelImportError').textContent = '';
    $id('btnExecuteExcelImport').disabled = true;
    parsedExcelTeachers = [];
    m.classList.remove('hidden');
  }

  function closeExcelImportModal() {
    var m = $id('excelImportModal');
    if (m) m.classList.add('hidden');
  }
  window.__ngisCloseExcelModal = closeExcelImportModal;

  function renderTable() {
    if (IS_TEACHER) {
      var rowsContainer = $id('dirRows');
      if (!rowsContainer) return;
      if (state.loading) {
        rowsContainer.innerHTML = window.NGIS_SKELETON
          ? window.NGIS_SKELETON.table({ rows: 5 })
          : '<div class="ngis-sk-table-container p-6"></div>';
        renderPager(); return;
      }
      if (state.error) {
        rowsContainer.innerHTML = '<div class="py-12 text-center text-rose-600 bg-white rounded-xl border border-[#E1E9E3]"><div class="flex flex-col items-center justify-center gap-2.5"><span class="material-symbols-outlined text-4xl text-[#B3261E] opacity-70">cloud_off</span><p class="font-medium text-sm text-[#B3261E]">' + esc(state.error) + '</p><button type="button" class="mt-2 px-3.5 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition cursor-pointer" id="btnRetryLoad">Retry</button></div></div>';
        var rb = $id('btnRetryLoad');
        if (rb) rb.addEventListener('click', loadDirectory);
        renderPager(); return;
      }
      if (!state.filtered.length) {
        rowsContainer.innerHTML = '<div class="py-12 text-center text-slate-500 bg-white rounded-xl border border-[#E1E9E3]"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] opacity-40">person_search</span><p class="font-medium text-sm">No teachers match your active filters</p><button type="button" class="text-xs text-[#176B45] hover:underline mt-1 font-medium cursor-pointer" id="emptyReset">Reset Filters</button></div></div>';
        var er = $id('emptyReset');
        if (er) er.addEventListener('click', resetAllFilters);
        renderPager(); return;
      }
      var start = (state.page - 1) * PER_PAGE;
      var pageRows = state.filtered.slice(start, start + PER_PAGE);
      rowsContainer.innerHTML = pageRows.map(teacherRowHtml).join('\n');
      renderPager();
      return;
    }

    var body = $id('dirBody');
    if (!body) return;
    if (state.loading) {
      body.innerHTML = (function() {
        if (window.NGIS_SKELETON) {
          var out = '';
          for (var k = 0; k < 6; k++) {
            out += '<tr><td colspan="9" class="p-3">' +
              '<div class="flex items-center gap-3">' +
                window.NGIS_SKELETON.avatar({ size: "sm" }) +
                '<div class="flex-1 flex flex-col gap-1">' +
                  window.NGIS_SKELETON.text({ width: (40 + (k % 3) * 20) + "%", size: "sm" }) +
                  window.NGIS_SKELETON.text({ width: "25%", size: "xs" }) +
                '</div>' +
                window.NGIS_SKELETON.badge({ width: "70px" }) +
              '</div>' +
            '</td></tr>';
          }
          return out;
        }
        return '<tr><td colspan="9" class="p-4"></td></tr>';
      })();
      renderPager(); return;
    }
    if (state.error) {
      body.innerHTML = '<tr><td colspan="9" class="py-12 text-center text-rose-600"><div class="flex flex-col items-center justify-center gap-2.5"><span class="material-symbols-outlined text-4xl text-[#B3261E] opacity-70">cloud_off</span><p class="font-medium text-sm text-[#B3261E]">' + esc(state.error) + '</p><button type="button" class="mt-2 px-3.5 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition cursor-pointer" id="btnRetryLoadStudents">Retry</button></div></td></tr>';
      var rb2 = $id('btnRetryLoadStudents');
      if (rb2) rb2.addEventListener('click', loadDirectory);
      renderPager(); return;
    }
    if (!state.filtered.length) {
      body.innerHTML = '<tr><td colspan="9" class="py-12 text-center text-slate-500"><div class="flex flex-col items-center justify-center gap-2"><span class="material-symbols-outlined text-4xl text-[#94a3b8] opacity-40">person_search</span><p class="font-medium text-sm">No ' + PLURAL_LABEL.toLowerCase() + ' match your active filters</p><button type="button" class="text-xs text-slate-600 hover:underline mt-1 font-medium cursor-pointer" id="emptyReset">Reset Filters</button></div></td></tr>';
      var er2 = $id('emptyReset');
      if (er2) er2.addEventListener('click', resetAllFilters);
      renderPager(); return;
    }
    var start2 = (state.page - 1) * PER_PAGE;
    var pageRows2 = state.filtered.slice(start2, start2 + PER_PAGE);
    body.innerHTML = pageRows2.map(function (r) {
      var isActive2 = String(r.status || '').toLowerCase() === 'active';
      var actions2 = '<div class="inline-flex items-center gap-1.5">' +
        '<button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
          'Profile' +
        '</button>' +
        '<button type="button" data-act="edit" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
          'Edit' +
        '</button>' +
        '<button type="button" data-act="toggle" data-id="' + esc(r.id) + '" title="' + (isActive2 ? 'Deactivate record' : 'Activate record') + '" class="p-1 text-slate-400 hover:text-slate-700 rounded transition-colors cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" aria-label="Toggle status">' +
          '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"></circle><circle cx="12" cy="5" r="1" fill="currentColor"></circle><circle cx="12" cy="19" r="1" fill="currentColor"></circle></svg>' +
        '</button>' +
        '</div>';
      return '<tr class="transition-colors group" data-id="' + esc(r.id) + '"><td class="py-3.5 pl-4 pr-2 align-middle"><input class="row-checkbox rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]/20 focus:ring-offset-0 cursor-pointer accent-[#176B45]" type="checkbox" data-id="' + esc(r.id) + '"></td>' +
        '<td class="py-3.5 px-4 align-middle">' + nameCell(r) + '</td>' +
        '<td class="py-3.5 px-4 align-middle"><div class="font-medium text-sm text-slate-900">' + esc(r.grade || '—') + '</div><div class="text-[11px] text-slate-500">' + esc(r.class || '—') + '</div></td>' +
        '<td class="py-3.5 px-4 align-middle font-medium text-sm text-slate-800">' + esc(r.advisor || '—') + '</td>' +
        '<td class="py-3.5 px-4 align-middle font-headline-sm text-sm font-medium text-[#176B45]">' + (r.gpaLive == null ? '—' : num(r.gpaLive)) + '</td>' +
        '<td class="py-3.5 px-4 align-middle"><span class="inline-flex items-center px-2 py-0.5 rounded-full font-medium text-xs bg-slate-50 font-medium ' + (Number(r.attendancePct) < 85 ? 'text-[#B3261E]' : 'text-slate-600') + '">' + (r.attendancePct == null ? '—' : num(r.attendancePct, 1) + '%') + '</span></td>' +
        '<td class="py-3.5 px-4 align-middle font-medium text-sm text-slate-800">' + (r.openRequests || 0) + '</td>' +
        '<td class="py-3.5 px-4 align-middle">' + statusBadge(r.status) + '</td>' +
        '<td class="py-3.5 pr-4 pl-4 text-right align-middle">' + actions2 + '</td></tr>';
    }).join('');
    renderPager();
  }
  function renderPager() {
    var info = $id('pagerInfo'), ctr = $id('pagerControls');
    if (!info || !ctr) return;
    var total = state.filtered.length, pages = Math.max(1, Math.ceil(total / PER_PAGE));
    var start = total ? (state.page - 1) * PER_PAGE + 1 : 0;
    var end = Math.min(state.page * PER_PAGE, total);
    info.innerHTML = 'Showing <span class="font-medium text-slate-800">' + start + '</span> to <span class="font-medium text-slate-800">' + end + '</span> of <span class="font-medium text-slate-800">' + total + '</span> active ' + PLURAL_LABEL.toLowerCase() +
      ' <span class="mx-1">•</span> <span class="text-slate-600">Page ' + state.page + ' of ' + pages + '</span>';
    var nums = [];
    for (var p = 1; p <= pages; p++) {
      if (p === 1 || p === pages || Math.abs(p - state.page) <= 1) nums.push(p);
      else if (nums[nums.length - 1] !== '…') nums.push('…');
    }
    ctr.innerHTML =
      '<button type="button" class="px-3 py-1.5 rounded border border-[#E1E9E3] text-slate-700 text-xs font-medium hover:bg-[#F7F9F7] hover:border-slate-300 transition-all disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer" data-page="' + (state.page - 1) + '"' + (state.page <= 1 ? ' disabled' : '') + '><span class="material-symbols-outlined text-[16px] text-slate-400">chevron_left</span><span class="hidden sm:inline">Previous</span></button>' +
      nums.map(function (n) {
        if (n === '…') return '<span class="px-1 text-slate-600 text-xs font-medium">…</span>';
        var on = n === state.page;
        return '<button type="button" class="w-8 h-8 rounded-lg font-medium text-sm flex items-center justify-center transition-all cursor-pointer ' + (on ? 'bg-[#176B45] text-white' : 'bg-white border border-[#E1E9E3] text-slate-700 hover:bg-[#F7F9F7]') + '" data-page="' + n + '">' + n + '</button>';
      }).join('') +
      '<button type="button" class="px-3 py-1.5 rounded border border-[#E1E9E3] text-slate-700 text-xs font-medium hover:bg-[#F7F9F7] hover:border-slate-300 transition-all disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer" data-page="' + (state.page + 1) + '"' + (state.page >= pages ? ' disabled' : '') + '><span class="hidden sm:inline">Next</span><span class="material-symbols-outlined text-[16px] text-slate-400">chevron_right</span></button>';
  }

  function deepLink() {
    var params = new URLSearchParams(window.location.search);
    var target = params.get(IS_TEACHER ? 'teacher' : 'student') || params.get('profile');
    if (target) openProfile(target);
  }

  /* ---------- profile modal ---------- */
  function openProfile(id) {
    state.profileId = id; state.tab = 0; state.profile = null; state.profileLoading = true;
    var m = $id('profileModal');
    if (m) {
      m.classList.remove('hidden');
      m.classList.add('open', 'is-open');
    }
    renderProfileShell(null);
    api(API_BASE + '/' + encodeURIComponent(id)).then(function (res) {
      state.profile = (res && res.data) || null;
      state.profileLoading = false;
      renderProfileShell(state.profile);
    }).catch(function (err) {
      state.profileLoading = false;
      renderProfileShell({ __error: apiError(err, 'Profile could not be loaded') });
    });
  }
  function closeProfile() {
    var m = $id('profileModal');
    if (m) {
      m.classList.add('hidden');
      m.classList.remove('open', 'is-open');
    }
    state.profile = null;
  }

  function renderProfileShell(p) {
    var box = $id('profileModalInner');
    var err = p && p.__error;

    var khmerName = (p && (p.khmerName || p.khmer_name)) || '';
    var gradeText = (p && p.grade) || '';
    var classText = (p && p.class ? 'Section ' + p.class : '');
    var idText = (p && p.id) || '';

    var head = '<div class="h-1 bg-[#176B45] shrink-0"></div>' +
      '<header class="px-5 sm:px-8 pt-5 sm:pt-6 pb-4 border-b border-slate-100 bg-white sticky top-0 z-20 shrink-0">' +
        '<div class="flex items-start justify-between gap-3 sm:gap-4">' +
          '<div class="flex items-center gap-3 sm:gap-4 min-w-0">' +
            '<div class="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-emerald-50 border-2 border-emerald-100/80 text-emerald-800 flex items-center justify-center font-medium text-base sm:text-lg shrink-0 tracking-tight shadow-sm" data-purpose="student-avatar">' +
              (p && !err ? esc(initials(p.name)) : '—') +
            '</div>' +
            '<div class="min-w-0">' +
              '<div class="flex flex-wrap items-baseline gap-2">' +
                '<h2 id="profileModalTitle" class="text-lg sm:text-2xl font-medium text-slate-900 tracking-tight truncate">' +
                  (p && !err ? esc(p.name) : KIND_LABEL + ' Profile') +
                '</h2>' +
                (khmerName ? '<span class="text-sm sm:text-base text-slate-400 font-khmer font-normal">' + esc(khmerName) + '</span>' : '') +
              '</div>' +
              '<div class="flex flex-wrap items-center text-xs text-slate-500 font-normal gap-x-2 mt-0.5">' +
                (p && !err ? (
                  IS_TEACHER
                    ? '<span>' + esc(p.department || '') + '</span><span class="text-slate-300">•</span><span>' + esc(p.subject || '') + '</span><span class="text-slate-300">•</span><span class="font-mono text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded text-[11px]">' + esc(p.id) + '</span>'
                    : '<span>' + esc(gradeText) + '</span><span class="text-slate-300">•</span><span>' + esc(classText) + '</span><span class="text-slate-300">•</span><span class="font-mono text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded text-[11px]">' + esc(idText) + '</span>'
                ) : 'Loading from live records…') +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center gap-2 shrink-0">' +
            (p && !err ? '<button type="button" id="pfEditBtn" class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-colors shadow-2xs active:scale-95 cursor-pointer" title="Edit Student Record"><span class="material-symbols-outlined text-[16px] text-slate-500">edit</span><span class="hidden sm:inline">Edit Record</span></button>' : '') +
            '<button type="button" onclick="window.__ngisCloseProfile()" class="p-1.5 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors cursor-pointer active:scale-95" aria-label="Close dialog"><span class="material-symbols-outlined text-[20px]">close</span></button>' +
          '</div>' +
        '</div>' +
        (p && !err ? (
          '<nav aria-label="Student details tabs" class="flex items-center gap-1 sm:gap-2.5 lg:gap-3.5 mt-4 sm:mt-5 overflow-x-auto border-b border-slate-200 pf-scroll" id="pfTabBar">' +
          TABS.map(function (t, i) {
            var isActive = i === state.tab;
            return '<button type="button" class="tab-button text-xs sm:text-[13px] px-1 sm:px-1.5 pb-2.5 sm:pb-3 border-b-2 whitespace-nowrap transition-colors focus:outline-none cursor-pointer ' +
              (isActive ? 'border-[#176B45] text-[#176B45] font-medium' : 'border-transparent text-slate-500 font-normal hover:text-slate-700 hover:border-slate-300') +
              '" data-tab="' + i + '">' + esc(t) +
              (i === DOCS_TAB_INDEX ? ' <span class="text-[11px] text-slate-400 font-normal ml-0.5" id="docsCountChip">' + ((p.documents || []).length) + '</span>' : '') +
              '</button>';
          }).join('') +
          '</nav>'
        ) : '') +
      '</header>';

    var body;
    if (!p || err) {
      body = err
        ? '<div class="p-10 text-center font-normal text-sm text-slate-500"><span class="material-symbols-outlined text-[24px] block mx-auto mb-2 text-[#B3261E]">error</span>' + esc(err) + '</div>'
        : '<div class="p-6">' + (window.NGIS_SKELETON ? window.NGIS_SKELETON.form({ fields: 4 }) : '<div class="py-12 text-center text-xs text-slate-400">Loading profile…</div>') + '</div>';
    } else {
      body = '<main class="px-5 sm:px-8 py-5 sm:py-6 overflow-y-auto pf-scroll flex-1 bg-white" style="max-height: 65vh" id="pfTabBody">' +
        tabBody(p, state.tab) +
        '</main>';
    }

    box.innerHTML = head + (body || '') +
      '<footer class="px-5 sm:px-8 py-3.5 sm:py-4 bg-slate-50 border-t border-[#E1E9E3] flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shrink-0">' +
        '<div class="flex items-center gap-2 text-slate-500 font-normal text-[11px]">' +
          '<span class="material-symbols-outlined text-[15px] text-[#176B45]">verified</span>' +
          '<span>All records are read live from the NGIS academic store.</span>' +
        '</div>' +
        '<div class="flex items-center gap-2.5 self-end sm:self-auto">' +
          '<button type="button" onclick="window.print()" class="px-3.5 py-2 font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-xl hover:bg-slate-50 hover:text-slate-900 transition-colors shadow-2xs active:scale-95 cursor-pointer">' +
            'Print Summary' +
          '</button>' +
          '<button type="button" onclick="window.__ngisCloseProfile()" class="px-5 py-2 font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-xl transition-colors shadow-xs active:scale-95 cursor-pointer">' +
            'Close' +
          '</button>' +
        '</div>' +
      '</footer>';

    var editBtn = $id('pfEditBtn');
    if (editBtn) editBtn.addEventListener('click', function () { openForm(state.profileId); });
    var bar = $id('pfTabBar');
    if (bar) bar.addEventListener('click', function (e) {
      var b = e.target.closest('[data-tab]');
      if (!b || !state.profile) return;
      state.tab = parseInt(b.getAttribute('data-tab'), 10);
      renderProfileShell(state.profile);
      wireTabEvents();
    });
    wireTabEvents();
  }

  function cell(label, valueHtml) {
    return '<div><span class="text-[11px] font-medium uppercase tracking-wider text-slate-400 block">' + esc(label) + '</span><span class="text-sm font-medium text-slate-900 mt-1 block truncate">' + valueHtml + '</span></div>';
  }
  function chips(list) {
    if (!list || !list.length) return '<span class="text-slate-400">—</span>';
    return list.map(function (c) { return '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-lg bg-slate-100 border border-slate-200 text-xs font-medium text-slate-700">' + esc(c) + '</span>'; }).join('');
  }
  function miniTable(headRow, rows, emptyMsg) {
    if (!rows || !rows.length) return '<div class="p-6 text-center text-xs text-slate-500 border border-[#E1E9E3] rounded-xl bg-[#F7F9F7]/60">' + esc(emptyMsg) + '</div>';
    return '<div class="border border-slate-200 rounded-2xl overflow-hidden overflow-x-auto pf-scroll"><table class="w-full text-left text-xs min-w-[520px]"><thead class="bg-slate-50 text-[11px] font-medium text-slate-500 uppercase tracking-wider border-b border-slate-200"><tr>' +
      headRow + '</tr></thead><tbody class="divide-y divide-slate-100 bg-white">' + rows + '</tbody></table></div>';
  }
  function td(txt, cls) { return '<td class="py-3 px-4 font-medium text-xs text-slate-800 ' + (cls || '') + '">' + txt + '</td>'; }

  function tabBody(p, i) {
    if (IS_TEACHER) {
      if (i === 0) return '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-6 bg-slate-50/60 p-4 sm:p-5 rounded-2xl border border-slate-100">' +
        cell('Full name', esc(p.name)) + cell('Educator ID', esc(p.id)) + cell('Role', esc(p.role || 'Faculty')) +
        cell('Email', '<a class="text-[#176B45] hover:underline break-all" href="mailto:' + esc(p.email) + '">' + dash(p.email) + '</a>') +
        cell('Phone', dash(p.phone)) + cell('Languages', chips(p.languages)) + '</div>';
      if (i === 1) return '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-6 bg-slate-50/60 p-4 sm:p-5 rounded-2xl border border-slate-100">' +
        cell('Department', dash(p.department)) + cell('Primary subject', dash(p.subject)) +
        cell('Employment type', dash(p.employmentType)) + cell('Contract end date', dash(p.contractEnd)) +
        cell('Years at school', dash(p.yearsAtSchool)) + cell('Registry status', statusBadge(p.status)) + '</div>';
      if (i === 2) {
        var asgns = p.assignments || [];
        var asgnRows = asgns.map(function (as) {
          var dName = as.department || p.department || '—';
          var gName = as.grade || '—';
          var cName = as.class || '—';
          var sName = as.subject || p.subject || '—';
          return '<tr>' +
            td('<span class="font-medium text-slate-800">' + esc(dName) + '</span>') +
            td(esc(gName)) +
            td('<span class="font-medium text-[#176B45]">' + esc(cName) + '</span>') +
            td(esc(sName), 'text-slate-600') +
            td('<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium bg-[#E8F3ED] text-[#176B45]">Active</span>') +
            '</tr>';
        });

        var asgnSection = '<div class="mb-5">' +
          '<div class="flex items-center justify-between mb-2">' +
            '<h4 class="text-[11px] font-medium uppercase tracking-wider text-slate-600">Assigned Classes &amp; Subjects (' + asgns.length + ')</h4>' +
          '</div>' +
          miniTable('<th class="py-2.5 px-3 font-medium text-left">Department</th><th class="py-2.5 px-3 font-medium text-left">Grade</th><th class="py-2.5 px-3 font-medium text-left">Class</th><th class="py-2.5 px-3 font-medium text-left">Subject</th><th class="py-2.5 px-3 font-medium text-left">Status</th>', asgnRows, 'No dynamic class assignments found.') +
        '</div>';

        var classesTaughtList = p.classesTaught || p.classes || (asgns.length ? asgns.map(function (a) { return (a.class || '').replace('Grade ', ''); }) : []);

        return '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-4">' +
          cell('Subjects taught', chips(p.subjects && p.subjects.length ? p.subjects : [p.subject])) +
          cell('Homeroom', dash(p.homeroom)) + cell('Advisee count', dash(p.adviseeCount)) +
          cell('Classes assigned', dash(p.classesAssigned != null ? p.classesAssigned : asgns.length)) +
          cell('Pending grade records', '<span class="' + ((p.pendingGradeRecords || 0) > 0 ? 'text-[#B3261E]' : 'text-[#204F3A]') + '">' + (p.pendingGradeRecords || 0) + '</span>') +
          cell('Published records', dash(p.publishedGradeRecords)) + '</div>' +
          asgnSection +
          '<h4 class="text-[11px] font-medium uppercase tracking-wider text-slate-600 mb-2">Classes Taught</h4>' +
          '<div class="flex flex-wrap gap-2">' + chips(classesTaughtList) + '</div>';
      }
      if (i === 3) return '<h4 class="text-[11px] font-medium uppercase tracking-wider text-slate-600 mb-2">Certifications &amp; Licences</h4>' +
        '<div class="flex flex-wrap gap-2 mb-4">' + chips(p.certifications) + '</div>' +
        '<h4 class="text-[11px] font-medium uppercase tracking-wider text-slate-600 mb-2">Spoken Languages</h4>' +
        '<div class="flex flex-wrap gap-2 mb-4">' + chips(p.languages) + '</div>' +
        '<p class="text-[11px] text-slate-500">Upload certified copies of degrees, licences and safeguarding training from the Documents tab — every upload is timestamped and audited.</p>';
    } else {
      // ═══ STUDENT PROFILE TABS ═══
      if (i === 0) {
        var genderRaw = String(p.gender || '').trim();
        var genderLetter = genderRaw.toUpperCase().charAt(0);
        var genderVal = genderRaw
          ? (genderLetter === 'F' ? 'Female (F)' : genderLetter === 'M' ? 'Male (M)' : genderRaw)
          : '';
        var gpaVal = p.gpaLive != null ? num(p.gpaLive, 2)
          : (p.gpa != null ? num(p.gpa, 2) : '');
        var dobVal = p.dob || p.dateOfBirth || p.dobIso || '';
        var campusVal = p.campus || p.campusName || '';
        var residencyVal = p.residencyType || p.residency || '';
        var advisorVal = p.advisorName || '';
        var enr0 = (p.enrollments && p.enrollments[0]) || {};
        var placementVal = enr0.class_id || (p.class ? 'cls-' + String(p.class).toLowerCase() : '');

        return '<section class="space-y-6">' +
          '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-400 mb-4">Official Student Credentials</h3>' +
            '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-5 gap-x-6 bg-slate-50/60 p-5 rounded-2xl border border-slate-100">' +
              cell('Full Name', esc(p.name)) +
              cell('Student ID', '<span class="font-mono text-slate-800">' + esc(p.id) + '</span>') +
              cell('Gender', esc(genderVal || 'Not recorded')) +
              cell('Primary Grade', esc(p.grade || 'Not recorded')) +
              cell('Primary Class', p.class ? 'Class ' + esc(p.class) : 'Not recorded') +
              cell('Advisor', '<span class="truncate" title="' + esc(advisorVal) + '">' + dash(advisorVal) + '</span>') +
              '<div><p class="text-[11px] font-medium uppercase tracking-wider text-slate-400">Enrolment Status</p>' +
              '<div class="inline-flex items-center gap-1.5 mt-1">' +
              '<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>' +
              '<span class="text-sm font-medium text-emerald-800 capitalize">' + esc(p.status || 'active') + '</span></div></div>' +
              '<div><p class="text-[11px] font-medium uppercase tracking-wider text-slate-400">Live GPA</p>' +
              (gpaVal
                ? '<p class="text-sm font-medium text-slate-900 mt-1"><span class="text-base text-[#176B45] font-medium">' + esc(gpaVal) + '</span> <span class="text-slate-400 font-normal text-xs">/ 4.00</span></p>'
                : '<p class="text-sm font-normal text-slate-400 mt-1">Not yet graded</p>') + '</div>' +
              cell('Active Placement', p.enrollments && p.enrollments.length ? esc(placementVal) : 'Not recorded') +
              cell('Date of Birth', esc(dobVal || 'Not recorded')) +
              cell('Primary Campus', esc(campusVal || 'Not recorded')) +
              cell('Residency Type', esc(residencyVal || 'Not recorded')) +
            '</div>' +
          '</div>' +
        '</section>';
      }
      if (i === 1) {
        var enrs = p.enrollments || [];
        var enrRows = enrs.map(function (en) {
          var dName = en.department || '—';
          var gName = en.grade || p.grade || '—';
          var cName = en.class || en.class_id || '—';
          var yName = en.academic_year || '—';
          var st = en.status || 'active';
          return '<tr class="hover:bg-slate-50/50 transition-colors">' +
            '<td class="py-3 px-4 font-medium text-slate-900">' + esc(dName) + '</td>' +
            '<td class="py-3 px-4 text-slate-600">' + esc(gName) + '</td>' +
            '<td class="py-3 px-4 font-mono font-medium text-[#176B45]">' + esc(cName) + '</td>' +
            '<td class="py-3 px-4 text-slate-600">' + esc(yName) + '</td>' +
            '<td class="py-3 px-4"><span class="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700"><span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>' + esc(st) + '</span></td>' +
            '</tr>';
        }).join('');

        var enrSection = enrs.length
          ? '<div>' +
              '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Academic Department Enrollments (' + enrs.length + ')</h3>' +
              '<div class="overflow-x-auto border border-slate-200 rounded-2xl">' +
                '<table class="w-full text-left text-xs text-slate-700 divide-y divide-slate-200">' +
                  '<thead class="bg-slate-50 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                    '<tr><th class="py-3 px-4">Department</th><th class="py-3 px-4">Grade</th><th class="py-3 px-4">Class</th><th class="py-3 px-4">Academic Year</th><th class="py-3 px-4">Status</th></tr>' +
                  '</thead>' +
                  '<tbody class="divide-y divide-slate-100 bg-white">' + enrRows + '</tbody>' +
                '</table>' +
              '</div>' +
            '</div>'
          : '<div class="border border-dashed border-slate-200 rounded-2xl p-6 text-center">' +
              '<p class="text-sm font-medium text-slate-700">No department enrollments recorded</p>' +
              '<p class="text-xs text-slate-400 mt-1 font-normal">Enrollments appear here once the student is placed in a class.</p>' +
            '</div>';

        // Subject averages computed from the student's real graded assessments.
        var subjAgg = {};
        (p.grades || []).forEach(function (g) {
          var score = Number(g.score);
          if (isNaN(score)) return;
          var maxRaw = g.assessmentMaxScore != null ? Number(g.assessmentMaxScore)
            : (g.maxScore != null ? Number(g.maxScore) : 100);
          var max = (!isNaN(maxRaw) && maxRaw > 0) ? maxRaw : 100;
          var pct = score / max * 100;
          var name = g.subjectName || g.subject_name || g.subject ||
            (g.assessmentTitle ? String(g.assessmentTitle).replace(/\s*[-·]\s*.*$/, '') : '') || 'General Assessments';
          var agg = subjAgg[name] = subjAgg[name] || { n: 0, sum: 0, best: null };
          agg.n += 1; agg.sum += pct;
          if (agg.best == null || pct > agg.best) agg.best = pct;
        });
        var subjNames = Object.keys(subjAgg).sort();
        var bandCls = function (pct) {
          return pct >= 85 ? 'text-emerald-700' : pct >= 70 ? 'text-sky-700' : pct >= 50 ? 'text-amber-700' : 'text-rose-700';
        };
        var subjSection;
        if (subjNames.length) {
          var subRows = subjNames.map(function (name) {
            var agg = subjAgg[name];
            var avg = agg.sum / agg.n;
            return '<tr class="hover:bg-slate-50/50 transition-colors">' +
              '<td class="py-3 px-4 font-medium text-slate-900">' + esc(name) + '</td>' +
              '<td class="py-3 px-4 text-slate-500">' + agg.n + (agg.n === 1 ? ' assessment' : ' assessments') + '</td>' +
              '<td class="py-3 px-4 text-slate-500">' + num(agg.best, 1) + '%</td>' +
              '<td class="py-3 px-4 text-right font-medium ' + bandCls(avg) + '">' + num(avg, 1) + '%</td>' +
              '</tr>';
          }).join('');
          subjSection = '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Subject Averages (From Graded Assessments)</h3>' +
            '<div class="overflow-x-auto border border-slate-200 rounded-2xl">' +
              '<table class="w-full text-left text-xs text-slate-700 divide-y divide-slate-200">' +
                '<thead class="bg-slate-50 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                  '<tr><th class="py-3 px-4">Subject</th><th class="py-3 px-4">Assessments Logged</th><th class="py-3 px-4">Best Score</th><th class="py-3 px-4 text-right">Student Average</th></tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-slate-100 bg-white">' + subRows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
        } else {
          subjSection = '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Subject Averages (From Graded Assessments)</h3>' +
            '<div class="border border-dashed border-slate-200 rounded-2xl p-6 text-center">' +
              '<p class="text-sm font-medium text-slate-700">No graded assessments recorded yet</p>' +
              '<p class="text-xs text-slate-400 mt-1 font-normal">Published assessment scores will build this subject breakdown.</p>' +
            '</div>' +
          '</div>';
        }

        var transcripts = p.transcripts || [];
        var transcriptSection;
        if (transcripts.length) {
          var trRows = transcripts.map(function (t) {
            return '<div class="border border-dashed border-slate-200 rounded-2xl p-4 bg-slate-50/50 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">' +
              '<div class="flex items-center gap-3">' +
                '<span class="w-9 h-9 rounded-xl bg-slate-100 text-slate-500 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-[20px]">description</span></span>' +
                '<div><p class="font-medium text-slate-800">' + esc(t.term || t.title || 'Official Transcript') + '</p>' +
                '<p class="text-slate-400 text-[11px] font-normal">' + esc(t.fileName || 'Transcript record') + (t.generatedAt || t.createdAt ? ' • ' + esc(fmtDT(t.generatedAt || t.createdAt)) : '') + '</p></div>' +
              '</div>' +
              (t.fileUrl ? '<a class="font-medium text-[#176B45] hover:text-[#125638] inline-flex items-center gap-1.5 hover:underline" href="' + esc(t.fileUrl) + '" target="_blank" rel="noopener">Download Official Copy <span class="material-symbols-outlined text-[15px]">download</span></a>' : '<span class="text-slate-400">No file attached</span>') +
            '</div>';
          }).join('');
          transcriptSection = '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Issued Transcripts &amp; Formal Records (' + transcripts.length + ')</h3>' +
            '<div class="space-y-2">' + trRows + '</div>' +
          '</div>';
        } else {
          transcriptSection = '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Issued Transcripts &amp; Formal Records</h3>' +
            '<div class="border border-dashed border-slate-200 rounded-2xl p-6 text-center">' +
              '<p class="text-sm font-medium text-slate-700">No transcripts issued yet</p>' +
              '<p class="text-xs text-slate-400 mt-1 font-normal">Official transcripts generated by the registrar will be listed here.</p>' +
            '</div>' +
          '</div>';
        }

        return '<section class="space-y-6">' + enrSection + subjSection + transcriptSection + '</section>';
      }
      if (i === 2) {
        var att = (p.attendance && typeof p.attendance === 'object') ? p.attendance : {};
        var attRecords = att.records || [];
        var sum = att.summary || {};
        var attRaw = sum.percentage != null ? sum.percentage :
          (p.attendancePct != null ? p.attendancePct :
          (p.attendanceRate != null ? p.attendanceRate :
          (typeof p.attendance === 'number' ? p.attendance :
          (p.stats && p.stats.attendance != null ? p.stats.attendance : null))));
        var hasAtt = attRaw != null && (sum.total == null || sum.total > 0);
        var attVal = hasAtt ? parseFloat(num(attRaw, 1)) || 0 : 0;
        var attColor = attVal >= 85 ? 'bg-emerald-500' : 'bg-amber-500';
        var attLabel = !hasAtt ? '<span class="text-xs text-slate-400 font-normal">No data</span>'
          : attVal >= 85 ? '<span class="text-xs text-emerald-700 font-medium">Good Standing (&ge;85%)</span>'
          : '<span class="text-xs text-amber-700 font-medium">Needs Attention (&lt;85%)</span>';

        var STATUS_STYLES = {
          present: { chip: 'bg-emerald-50 text-emerald-800 border-emerald-200', dot: 'bg-emerald-600' },
          tardy: { chip: 'bg-amber-50 text-amber-800 border-amber-200', dot: 'bg-amber-500' },
          absent: { chip: 'bg-rose-50 text-rose-700 border-rose-200', dot: 'bg-rose-600' },
          excused: { chip: 'bg-sky-50 text-sky-700 border-sky-200', dot: 'bg-sky-600' }
        };

        var logSection;
        if (attRecords.length) {
          var logRows = attRecords.map(function (lg) {
            var st = String(lg.status || '').toLowerCase();
            var sty = STATUS_STYLES[st] || STATUS_STYLES.present;
            return '<tr class="hover:bg-slate-50/50 transition-colors">' +
              '<td class="py-3 px-4 font-mono font-medium text-slate-900">' + esc(lg.attendance_date || lg.date || '—') + '</td>' +
              '<td class="py-3 px-4 text-slate-600">' + esc((lg.session === 'daily' ? 'Daily Session' : (lg.session || '—'))) + '</td>' +
              '<td class="py-3 px-4 text-slate-400">' + esc(lg.recorded_by || lg.source || '—') + '</td>' +
              '<td class="py-3 px-4"><span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium border ' + sty.chip + '"><span class="w-1.5 h-1.5 rounded-full ' + sty.dot + '"></span>' + esc(st || '—') + '</span></td>' +
              '<td class="py-3 px-4 text-slate-500 max-w-[180px] truncate" title="' + esc(lg.note || '') + '">' + esc(lg.note || '—') + '</td>' +
              '</tr>';
          }).join('');
          logSection = '<div>' +
            '<div class="flex items-center justify-between mb-3">' +
              '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500">Recent Attendance Log</h3>' +
              '<span class="text-xs text-slate-400 font-normal">Latest ' + attRecords.length + ' records</span>' +
            '</div>' +
            '<div class="overflow-x-auto border border-slate-200 rounded-2xl">' +
              '<table class="w-full text-left text-xs text-slate-700 divide-y divide-slate-200">' +
                '<thead class="bg-slate-50 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                  '<tr><th class="py-3 px-4">Date</th><th class="py-3 px-4">Session</th><th class="py-3 px-4">Recorded By</th><th class="py-3 px-4">Status</th><th class="py-3 px-4">Note</th></tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-slate-100 bg-white">' + logRows + '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
        } else {
          logSection = '<div>' +
            '<div class="flex items-center justify-between mb-3">' +
              '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500">Recent Attendance Log</h3>' +
            '</div>' +
            '<div class="border border-dashed border-slate-200 rounded-2xl p-8 text-center">' +
              '<div class="w-10 h-10 rounded-full bg-slate-100 text-slate-400 mx-auto flex items-center justify-center mb-2"><span class="material-symbols-outlined text-xl">fact_check</span></div>' +
              '<p class="text-sm font-medium text-slate-700">No attendance records yet</p>' +
              '<p class="text-xs text-slate-400 mt-1 font-normal">Daily rollcall and gate check-ins will appear here once recorded.</p>' +
            '</div>' +
          '</div>';
        }

        return '<section class="space-y-6">' +
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">' +
            '<div class="border border-slate-200 bg-slate-50/60 rounded-2xl p-4">' +
              '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-400 block mb-1">Overall Attendance</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span class="text-2xl font-medium text-slate-900">' + (hasAtt ? esc(num(attVal, 1)) + '%' : '—') + '</span>' +
                attLabel +
              '</div>' +
              '<div class="w-full bg-slate-200 rounded-full h-1.5 mt-2 overflow-hidden">' +
                '<div class="' + attColor + ' h-1.5 rounded-full" style="width: ' + (hasAtt ? Math.min(attVal, 100) : 0) + '%"></div>' +
              '</div>' +
            '</div>' +
            '<div class="border border-slate-200 bg-slate-50/60 rounded-2xl p-4">' +
              '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-400 block mb-1">Present Days</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span class="text-2xl font-medium text-slate-900">' + (sum.present != null ? esc(String(sum.present)) : '—') + '</span>' +
                '<span class="text-xs text-slate-500 font-normal">Sessions</span>' +
              '</div>' +
              '<p class="text-xs text-slate-500 font-normal mt-2">' + (sum.tardy != null ? esc(String(sum.tardy)) + ' tardy arrivals' : 'No tardy data') + '</p>' +
            '</div>' +
            '<div class="border border-slate-200 bg-slate-50/60 rounded-2xl p-4">' +
              '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-400 block mb-1">Total Absences</span>' +
              '<div class="flex items-baseline gap-2">' +
                '<span class="text-2xl font-medium text-slate-900">' + (sum.absent != null ? esc(String(sum.absent)) : '—') + '</span>' +
                '<span class="text-xs text-slate-500 font-normal">Sessions</span>' +
              '</div>' +
              '<p class="text-xs text-slate-500 font-normal mt-2">' + (sum.excused != null ? esc(String(sum.excused)) + ' excused' : 'No excused data') + '</p>' +
            '</div>' +
          '</div>' +
          logSection +
        '</section>';
      }
      if (i === 3) {
        var reqs = p.serviceRequests || [];
        var openN = p.openRequests != null ? p.openRequests
          : reqs.filter(function (r) { return ['open', 'pending', 'in_progress'].indexOf(String(r.status || '').toLowerCase()) >= 0; }).length;
        var reqRows = reqs.map(function (r) {
          var st = String(r.status || '').toLowerCase();
          var stCls = (st === 'completed' || st === 'approved') ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
            : (st === 'rejected') ? 'bg-rose-50 text-rose-700 border-rose-200'
            : 'bg-amber-50 text-amber-800 border-amber-200';
          return '<tr class="hover:bg-slate-50/50 transition-colors">' +
            '<td class="py-3 px-4 font-medium text-slate-900 max-w-[220px] truncate" title="' + esc(r.title || r.type || '') + '">' + esc(r.title || r.type || '—') + '</td>' +
            '<td class="py-3 px-4 text-slate-600 capitalize">' + esc(String(r.category || '').replace(/_/g, ' ') || '—') + '</td>' +
            '<td class="py-3 px-4 text-slate-500">' + esc(fmtDT(r.date || r.createdAt)) + '</td>' +
            '<td class="py-3 px-4"><span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-medium border capitalize ' + stCls + '">' + esc(st || '—') + '</span></td>' +
            '</tr>';
        }).join('');
        var reqSection = reqs.length
          ? '<div class="overflow-x-auto border border-slate-200 rounded-2xl">' +
              '<table class="w-full text-left text-xs text-slate-700 divide-y divide-slate-200">' +
                '<thead class="bg-slate-50 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                  '<tr><th class="py-3 px-4">Request</th><th class="py-3 px-4">Category</th><th class="py-3 px-4">Submitted</th><th class="py-3 px-4">Status</th></tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-slate-100 bg-white">' + reqRows + '</tbody>' +
              '</table>' +
            '</div>'
          : '<div class="border border-slate-200/80 rounded-2xl bg-slate-50/40 p-8 sm:p-12 text-center my-4 flex flex-col items-center justify-center">' +
              '<div class="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mb-3"><span class="material-symbols-outlined text-2xl">support_agent</span></div>' +
              '<p class="text-sm text-slate-600 font-medium">This student has no service requests on file.</p>' +
              '<p class="text-xs text-slate-400 mt-1 max-w-sm font-normal">Counseling, academic support accommodations, IT requests, and transportation inquiries logged will appear here.</p>' +
            '</div>';

        return '<section class="space-y-6">' +
          '<div class="flex items-center justify-between gap-6 py-2 px-1 border-b border-slate-100">' +
            '<div class="flex items-center gap-6 sm:gap-8">' +
              '<div class="flex items-center gap-2.5 sm:gap-3"><span class="text-[11px] font-medium uppercase tracking-wider text-slate-500">OPEN REQUESTS</span><span class="text-lg font-medium text-slate-900">' + Number(openN || 0) + '</span></div>' +
              '<div class="flex items-center gap-2.5 sm:gap-3"><span class="text-[11px] font-medium uppercase tracking-wider text-slate-500">TOTAL REQUESTS</span><span class="text-lg font-medium text-slate-900">' + reqs.length + '</span></div>' +
            '</div>' +
          '</div>' +
          reqSection +
          '<div class="mt-6">' +
            '<div class="flex items-center justify-between mb-3">' +
              '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500">Available Support Services</h3>' +
            '</div>' +
            '<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">' +
              '<div class="p-3.5 border border-slate-200 rounded-xl bg-white hover:border-slate-300 transition-colors flex items-start gap-3">' +
                '<div class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-lg">psychology</span></div>' +
                '<div><p class="text-xs font-medium text-slate-900">Academic Guidance</p><p class="text-[11px] text-slate-400 mt-0.5 font-normal">Tutoring &amp; course advisement</p></div>' +
              '</div>' +
              '<div class="p-3.5 border border-slate-200 rounded-xl bg-white hover:border-slate-300 transition-colors flex items-start gap-3">' +
                '<div class="w-8 h-8 rounded-lg bg-sky-50 text-sky-700 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-lg">medical_services</span></div>' +
                '<div><p class="text-xs font-medium text-slate-900">Health &amp; Wellness</p><p class="text-[11px] text-slate-400 mt-0.5 font-normal">Nurse pass &amp; care plans</p></div>' +
              '</div>' +
              '<div class="p-3.5 border border-slate-200 rounded-xl bg-white hover:border-slate-300 transition-colors flex items-start gap-3">' +
                '<div class="w-8 h-8 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center shrink-0"><span class="material-symbols-outlined text-lg">directions_bus</span></div>' +
                '<div><p class="text-xs font-medium text-slate-900">Transportation &amp; Boarding</p><p class="text-[11px] text-slate-400 mt-0.5 font-normal">Bus route &amp; campus shuttle</p></div>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</section>';
      }
      if (i === 5) {
        var g = p.guardian || {};
        var gName = g.name || p.parentName || '';
        var gRel = g.relation || '';
        var gEmail = g.email || p.parentEmail || '';
        var gPhone = g.phone || p.parentPhone || '';
        var gOcc = g.occupation || '';
        var gDist = g.district || '';
        var gLang = g.preferredLanguage || '';
        var gLast = g.lastContact || '';
        var notRec = '<span class="text-sm font-normal text-slate-400">Not recorded</span>';
        var valOrNot = function (v) { return v ? esc(v) : notRec; };

        var linked = (g.linkedStudents && g.linkedStudents.length ? g.linkedStudents : [{ id: p.id, name: p.name, class: p.class, grade: p.grade }])
          .map(function (ls) {
            var isCurrent = String(ls.id) === String(p.id);
            var lsName = ls.name || ls.studentName || '—';
            var lsMeta = 'ID: ' + esc(ls.id || '—') + (ls.class ? ' • Section ' + esc(ls.class) : '') + (ls.grade ? ' • ' + esc(ls.grade) : '');
            return '<div class="p-3.5 flex items-center justify-between hover:bg-slate-50/50 transition-colors">' +
              '<div class="flex items-center gap-3">' +
                '<div class="w-8 h-8 rounded-full bg-slate-100 text-slate-600 font-medium text-xs flex items-center justify-center shrink-0">' + esc(initials(lsName)) + '</div>' +
                '<div><p class="text-xs font-medium text-slate-900">' + esc(lsName) + (isCurrent ? ' (Current Student)' : '') + '</p><p class="text-[11px] text-slate-500 font-normal">' + lsMeta + '</p></div>' +
              '</div>' +
              '<span class="text-xs font-medium text-[#176B45] bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded">Enrolled</span>' +
            '</div>';
          }).join('');

        return '<section class="space-y-6">' +
          '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Primary Legal Guardian</h3>' +
            '<div class="bg-white border border-slate-200 rounded-2xl p-4 sm:p-5 shadow-xs">' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-y-4 sm:gap-y-5 gap-x-6">' +
                cell('Guardian Name', valOrNot(gName)) +
                cell('Relationship', valOrNot(gRel)) +
                '<div><p class="text-[11px] font-medium uppercase tracking-wider text-slate-400">Email Address</p>' +
                (gEmail
                  ? '<a class="text-sm font-medium text-[#176B45] hover:underline block truncate mt-1" href="mailto:' + esc(gEmail) + '" title="' + esc(gEmail) + '">' + esc(gEmail) + '</a>'
                  : notRec) + '</div>' +
                '<div><p class="text-[11px] font-medium uppercase tracking-wider text-slate-400">Phone (Primary)</p>' +
                '<div class="mt-1">' + (gPhone ? '<span class="text-sm font-medium text-slate-900">' + esc(gPhone) + '</span>' : notRec) + '</div></div>' +
                cell('Occupation', valOrNot(gOcc)) +
                cell('Residential District', valOrNot(gDist)) +
                cell('Preferred Language', valOrNot(gLang)) +
                cell('Consent On File', g.consentOnFile != null
                  ? (g.consentOnFile ? '<span class="text-sm font-medium text-emerald-800 flex items-center gap-1 mt-1"><span class="material-symbols-outlined text-[16px] text-emerald-600">check</span> Signed Digital Consent</span>' : '<span class="text-sm font-normal text-slate-400">No consent on file</span>')
                  : notRec) +
                cell('Last School Contact', valOrNot(gLast)) +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div>' +
            '<h3 class="text-xs font-medium uppercase tracking-wider text-slate-500 mb-3">Linked Household Students</h3>' +
            '<div class="border border-slate-200 rounded-2xl divide-y divide-slate-100 bg-white overflow-hidden">' + linked + '</div>' +
          '</div>' +
        '</section>';
      }
    }
    if (i === DOCS_TAB_INDEX) return docsTabMarkup(p);
    if (i === TABS.length - 1) {
      var acts = (p.activity || []).map(function (a) {
        var actor = '';
        try { actor = (JSON.parse(a.metadata_json || '{}').actorName) || a.actor_id || ''; } catch (e) { actor = a.actor_id || ''; }
        return '<tr class="hover:bg-slate-50/50 transition-colors">' +
          '<td class="py-3 px-4"><span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-[#F7F9F7] border border-[#E1E9E3] text-xs font-medium text-slate-700">' + esc(String(a.action || '').replace(/_/g, ' ')) + '</span></td>' +
          '<td class="py-3 px-4 text-slate-700">' + esc(a.reason || '—') + '</td>' +
          '<td class="py-3 px-4 text-slate-600">' + esc(actor) + '</td>' +
          '<td class="py-3 px-4 text-slate-500">' + esc(fmtDT(a.created_at || a.timestamp)) + '</td>' +
          '</tr>';
      });

      if (!acts || !acts.length) {
        return '<div class="border border-dashed border-slate-200 rounded-2xl p-8 text-center">' +
          '<div class="w-10 h-10 rounded-full bg-slate-100 text-slate-400 mx-auto flex items-center justify-center mb-2"><span class="material-symbols-outlined text-xl">history</span></div>' +
          '<p class="text-sm font-medium text-slate-700">No recent activity</p>' +
          '<p class="text-xs text-slate-400 mt-1 font-normal">Audit trails and enrollment status changes are archived here.</p>' +
          '</div>';
      }

      return '<div class="overflow-x-auto border border-slate-200 rounded-2xl">' +
        '<table class="w-full text-left text-xs text-slate-700 divide-y divide-slate-200">' +
          '<thead class="bg-slate-50 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
            '<tr><th class="py-3 px-4">Action</th><th class="py-3 px-4">Reason</th><th class="py-3 px-4">Actor</th><th class="py-3 px-4">When</th></tr>' +
          '</thead>' +
          '<tbody class="divide-y divide-slate-100 bg-white">' + acts.join('') + '</tbody>' +
        '</table>' +
      '</div>';
    }
    return '';
  }
  /* ---------- documents tab ---------- */
  function docsTabMarkup(p) {
    var rows = (p.documents || []).map(function (d) {
      return '<tr>' + td('<div class="flex flex-col min-w-0"><span class="font-medium text-sm text-slate-800">' + esc(d.fileName) + '</span><span class="block text-[11px] text-slate-500 mt-0.5">' + esc(d.category) + ' · ' + esc(d.sizeKB) + ' KB · by ' + esc(d.uploadedByName || d.uploadedBy) + '</span>' + (d.note ? '<span class="block text-[11px] text-slate-500 mt-0.5">' + esc(d.note) + '</span>' : '')) + '</td>' +
        td(esc(fmtDT(d.uploadedAt)), 'text-slate-600') +
        td('<div class="flex items-center gap-1 justify-end"><a href="' + esc(d.fileUrl) + '" target="_blank" rel="noopener" class="w-8 h-8 rounded-lg bg-[#F7F9F7] hover:bg-[#E8F3ED] text-slate-600 flex items-center justify-center transition-colors" title="Open document"><span class="material-symbols-outlined text-[16px]">open_in_new</span></a>' +
          '<a href="' + esc(d.fileUrl) + '" download="' + esc(d.fileName) + '" class="w-8 h-8 rounded-lg bg-[#F7F9F7] hover:bg-[#E8F3ED] text-slate-600 flex items-center justify-center transition-colors" title="Download document"><span class="material-symbols-outlined text-[16px]">download</span></a>' +
          '<button type="button" data-doc-del="' + esc(d.id) + '" class="w-8 h-8 rounded-lg bg-[#F7F9F7] hover:bg-[#ffdad6] hover:text-[#93000a] text-slate-600 flex items-center justify-center transition-colors cursor-pointer" title="Delete document"><span class="material-symbols-outlined text-[16px]">delete</span></button></div></tr>');
    });
    return '<div class="flex items-center justify-between mb-3"><h4 class="text-[11px] font-medium uppercase tracking-wider text-slate-600">Official Documents</h4>' +
      '<span class="text-xs text-slate-500 font-medium">PDF, PNG, JPG or WEBP · max 5 MB</span></div>' +
      miniTable('<th class="py-2.5 px-3 font-medium text-left">Document</th><th class="py-2.5 px-3 font-medium text-left">Uploaded</th><th class="py-2.5 px-3 text-right font-medium">File Actions</th>', rows, 'No documents uploaded yet — add the first one below.') +
      '<div class="border border-[#E1E9E3] rounded-xl p-4 mt-4 bg-[#F7F9F7]/40">' +
      '<h4 class="text-[11px] font-medium uppercase tracking-wider text-slate-600 mb-3">Upload New Document</h4>' +
      '<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">' +
      '<div><label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="docCat">Category</label><select class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none" id="docCat">' + DOC_CATEGORIES.map(function (c) { return '<option>' + esc(c) + '</option>'; }).join('') + '</select></div>' +
      '<div><label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="docFile">File</label><input type="file" id="docFile" accept=".pdf,.png,.jpg,.jpeg,.webp" class="w-full text-xs text-slate-700 file:mr-3 file:px-3 file:py-1.5 file:rounded-lg file:border-0 file:bg-[#E8F3ED] file:text-[#176B45] file:font-medium file:cursor-pointer cursor-pointer"></div>' +
      '</div>' +
      '<div class="mb-3"><label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="docNote">Note (optional)</label><input type="text" id="docNote" maxlength="240" placeholder="e.g. Signed contract for AY 2026-27" class="w-full text-xs py-2 pl-3 pr-4 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]"></div>' +
      '<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">' +
      '<span class="text-xs text-slate-500 font-medium">Uploads are stored on the school server and recorded in the audit trail.</span>' +
      '<button type="button" id="docUploadBtn" class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-[#176B45] text-white text-xs font-medium shadow-sm hover:bg-[#125638] transition-all cursor-pointer disabled:opacity-50 disabled:cursor-wait min-h-[40px]"><span class="material-symbols-outlined text-[16px]">upload_file</span><span>Upload Document</span></button>' +
      '</div></div>';
  }

  function wireTabEvents() {
    var btn = $id('docUploadBtn');
    if (btn) btn.addEventListener('click', uploadDoc);
    var box = $id('pfTabBody');
    if (box) box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-doc-del]');
      if (!b) return;
      deleteDoc(b.getAttribute('data-doc-del'));
    });
  }

  function authHeader() { return { 'Authorization': 'Bearer ' + NGISAuth.getToken() }; }

  function refreshProfileDocs() {
    api(API_BASE + '/' + encodeURIComponent(state.profileId)).then(function (res) {
      state.profile = (res && res.data) || state.profile;
      renderProfileShell(state.profile);
      wireTabEvents();
    }).catch(function () { /* keep current render */ });
  }

  function uploadDoc() {
    var fileEl = $id('docFile');
    if (!fileEl || !fileEl.files || !fileEl.files.length) { toast('Choose a file to upload first.', true); return; }
    var f = fileEl.files[0];
    if (f.size > 5 * 1024 * 1024) { toast('Documents must not exceed 5 MB.', true); return; }
    var btn = $id('docUploadBtn');
    btn.disabled = true;
    var fd = new FormData();
    fd.append('ownerType', CFG.kind);
    fd.append('ownerId', state.profileId);
    fd.append('category', $id('docCat').value);
    fd.append('note', $id('docNote').value);
    fd.append('file', f);
    fetch(DOCS_API, { method: 'POST', headers: authHeader(), body: fd })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (out) {
        btn.disabled = false;
        if (!out.ok) { toast(apiError(out.j, 'Upload rejected'), true); return; }
        toast('Document "' + out.j.data.fileName + '" uploaded and audited.');
        refreshProfileDocs();
        loadDirectory();
      })
      .catch(function () { btn.disabled = false; toast('Upload failed — server unreachable.', true); });
  }

  function deleteDoc(docId) {
    var doc = ((state.profile || {}).documents || []).filter(function (d) { return d.id === docId; })[0] || {};
    confirmDlg({
      title: 'Delete document',
      message: 'Permanently remove "' + (doc.fileName || docId) + '" from this profile? The deletion is written to the audit trail.',
      confirmLabel: 'Delete', danger: true
    }).then(function (yes) {
      if (!yes) return;
      fetch(DOCS_API + '/' + encodeURIComponent(docId), { method: 'DELETE', headers: authHeader() })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (out) {
          if (!out.ok) { toast(apiError(out.j, 'Delete failed'), true); return; }
          toast('Document deleted.');
          refreshProfileDocs();
        })
        .catch(function () { toast('Delete failed — server unreachable.', true); });
    });
  }

  /* ---------- add / edit forms ---------- */
  function fieldRow(label, id, value, type, options) {
    var input;
    if (options) {
      input = '<select class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none" id="' + id + '">' + options.map(function (o) {
        return '<option value="' + esc(o) + '"' + (String(o) === String(value == null ? '' : value) ? ' selected' : '') + '>' + esc(o) + '</option>';
      }).join('') + '</select>';
    } else {
      input = '<input class="w-full text-xs py-2 pl-3 pr-4 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] min-h-[40px]" id="' + id + '" type="' + (type || 'text') + '" value="' + esc(value == null ? '' : value) + '">';
    }
    return '<div><label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="' + id + '">' + esc(label) + '</label>' + input + '</div>';
  }

  var formEditId = null;
  function openForm(id) {
    var rec = id ? state.all.filter(function (r) { return String(r.id) === String(id); })[0] : null;
    if (id && !rec) { toast('Record not found in directory.', true); return; }
    if (id && IS_TEACHER) {
      api(API_BASE + '/' + encodeURIComponent(id)).then(function (res) {
        if (res && res.data) rec = Object.assign({}, rec, res.data);
        fillForm(id, rec);
      }).catch(function () { fillForm(id, rec); });
      return;
    }
    fillForm(id, rec);
  }

  function fillForm(id, rec) {
    formEditId = id;
    var m = $id('formModal');
    var depts = IS_TEACHER ? uniq('department') : [];
    var grades = IS_TEACHER ? [] : uniq('grade');
    var known = uniq('status');
    var extra = IS_TEACHER ? ['Active', 'Inactive', 'Pending'] : ['Enrolled', 'Inactive', 'Transfer', 'Graduated'];
    var statuses = known.concat(extra.filter(function (x) {
      return !known.some(function (k) { return k.toLowerCase() === x.toLowerCase(); });
    }));
    $('#formTitle').textContent = (id ? 'Edit ' : 'Register new ') + KIND_LABEL;
    var fields;
    if (IS_TEACHER) {
      fields = [
        fieldRow('Full name', 'fxName', rec && rec.name),
        fieldRow('Email', 'fxEmail', rec && rec.email, 'email'),
        fieldRow('Subject', 'fxSubject', rec && rec.subject),
        depts.length ? fieldRow('Department', 'fxDept', rec && rec.department, null, depts) : fieldRow('Department', 'fxDept', rec && rec.department),
        fieldRow('Role', 'fxRole', (rec && rec.role) || 'Faculty', null, ['Faculty', 'Senior Faculty', 'Head of Department', 'Coordinator']),
        fieldRow('Phone', 'fxPhone', rec && rec.phone),
        fieldRow('Employment type', 'fxEmploy', (rec && rec.employmentType) || 'Full-time', null, ['Full-time', 'Part-time', 'Contract']),
        fieldRow('Contract end', 'fxContract', rec && rec.contractEnd, 'date'),
        fieldRow('Classes assigned', 'fxClasses', rec && rec.classesAssigned, 'number'),
        fieldRow('Years at school', 'fxYears', rec && rec.yearsAtSchool, 'number'),
        fieldRow('Status', 'fxStatus', (rec && rec.status) || 'Active', null, statuses)
      ].join('');
    } else {
      fields = [
        fieldRow('Full name', 'fxName', rec && rec.name),
        fieldRow('Gender', 'fxGender', (rec && rec.gender) || 'Male', null, ['Male', 'Female']),
        grades.length ? fieldRow('Grade level', 'fxGrade', rec && rec.grade, null, grades) : fieldRow('Grade level', 'fxGrade', rec && rec.grade),
        fieldRow('Class', 'fxClass', rec && rec.class),
        fieldRow('Advisor (teacher name or ID)', 'fxAdvisor', rec && rec.advisor),
        fieldRow('Guardian name', 'fxParent', rec && rec.parentName),
        fieldRow('Guardian email', 'fxParentEmail', rec && rec.parentEmail, 'email'),
        fieldRow('Status', 'fxStatus', (rec && rec.status) || 'Enrolled', null, statuses),
        '<div class="lg:col-span-2"><label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="fxReason">Reason for correction <span class="text-[#B3261E]">*</span> <span class="text-xs text-slate-400 normal-case">(mandatory — written to the audit trail)</span></label><textarea class="w-full text-xs py-2 pl-3 pr-4 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="fxReason" rows="2" placeholder="e.g. Class reassignment approved by academic council on 12 Oct"></textarea><span class="text-[11px] text-[#B3261E] hidden" id="fxReasonErr">A reason is required before saving student record changes.</span></div>'
      ].join('');
    }
    $('#formFields').innerHTML = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">' + fields + '</div>';
    $('#formSaveBtn span:last-child').textContent = id ? 'Save Changes' : 'Create ' + KIND_LABEL;
    m.classList.remove('hidden');
    $('#formError').textContent = '';
  }
  function closeForm() { $id('formModal').classList.add('hidden'); }

  function fv(id) { var el = $id(id); return el ? el.value.trim() : ''; }

  function saveForm() {
    var body, url, method;
    if (IS_TEACHER) {
      body = {
        name: fv('fxName'), email: fv('fxEmail'), subject: fv('fxSubject'),
        department: fv('fxDept'), role: fv('fxRole'), phone: fv('fxPhone'),
        employmentType: fv('fxEmploy'), contractEnd: fv('fxContract'),
        classesAssigned: fv('fxClasses') || 0, yearsAtSchool: fv('fxYears') || 0,
        status: fv('fxStatus')
      };
      if (!formEditId) {
        if (!body.name || !body.department || !body.subject || !body.email) {
          $('#formError').textContent = 'Name, department, subject and email are required.'; return;
        }
        url = API_BASE; method = 'POST';
      } else {
        Object.keys(body).forEach(function (k) {
          if (typeof body[k] === 'string' && body[k] === '' && ['classesAssigned', 'yearsAtSchool'].indexOf(k) === -1) delete body[k];
        });
        url = API_BASE + '/' + encodeURIComponent(formEditId); method = 'PUT';
      }
    } else {
      var currentRec = state.all.filter(function (r) { return String(r.id) === String(formEditId); })[0] || {};
      var enrs = currentRec.enrollments ? JSON.parse(JSON.stringify(currentRec.enrollments)) : [];
      if (enrs.length > 0) {
        if (fv('fxGrade')) enrs[0].grade = fv('fxGrade');
        if (fv('fxClass')) {
          enrs[0].class = fv('fxClass').replace('Grade ', '').split(' (')[0].trim();
          enrs[0].class_id = 'cls-' + enrs[0].class.toLowerCase();
        }
        if (fv('fxStatus')) enrs[0].status = fv('fxStatus');
      }
      body = {
        name: fv('fxName'), gender: fv('fxGender'), grade: fv('fxGrade'), class: fv('fxClass'),
        advisor: fv('fxAdvisor'), parentName: fv('fxParent'), parentEmail: fv('fxParentEmail'),
        status: fv('fxStatus'), enrollments: enrs, reason: fv('fxReason')
      };
      if (!body.reason) { $('#fxReasonErr').classList.remove('hidden'); $('#formError').textContent = ''; return; }
      url = API_BASE + '/' + encodeURIComponent(formEditId); method = 'PUT';
    }
    $('#formSaveBtn').disabled = true;
    api(url, { method: method, body: JSON.stringify(body) })
      .then(function (res) {
        $('#formSaveBtn').disabled = false;
        closeForm();
        toast((method === 'POST' ? (res.data && res.data.id ? res.data.id + ' added' : 'Record created') : 'Record updated') + ' and written to the audit trail.');
        loadDirectory();
        if (state.profile && !$('#profileModal').classList.contains('hidden')) refreshProfileDocs();
      })
      .catch(function (err) {
        $('#formSaveBtn').disabled = false;
        $('#formError').textContent = apiError(err, 'The server rejected this change');
      });
  }

  /* ---------- activate / deactivate ---------- */
  function toggleStatus(id) {
    var rec = state.all.filter(function (r) { return String(r.id) === String(id); })[0] || {};
    var isActive = String(rec.status || '').toLowerCase() === 'active';
    var next = isActive ? 'Inactive' : 'Active';
    var opts = {
      title: (isActive ? 'Deactivate' : 'Activate') + ' ' + KIND_LABEL,
      message: 'Set ' + (rec.name || id) + ' to "' + next + '"? The change is applied to the live registry and audited.',
      confirmLabel: 'Set ' + next,
      danger: isActive,
      requireReason: !IS_TEACHER
    };
    confirmDlg(opts).then(function (reason) {
      if (reason === null || reason === false) return;
      var payload = { status: next };
      if (!IS_TEACHER) payload.reason = reason;
      api(API_BASE + '/' + encodeURIComponent(id), { method: 'PUT', body: JSON.stringify(payload) })
        .then(function () {
          toast((rec.name || id) + ' is now ' + next.toLowerCase() + '.');
          loadDirectory();
          if (state.profile && !$('#profileModal').classList.contains('hidden')) refreshProfileDocs();
        })
        .catch(function (err) { toast(apiError(err, 'Status change rejected'), true); });
    });
  }

  /* ---------- global wiring ---------- */
  window.__ngisCloseProfile = closeProfile;

  function mountModals() {
    var wrap = document.createElement('div');
    wrap.innerHTML = [
      // Profile modal
      '<div id="profileModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 md:p-6 bg-slate-900/50 backdrop-blur-xs transition-opacity" role="dialog" aria-modal="true" aria-labelledby="profileModalTitle" onclick="if(event.target===this)__ngisCloseProfile()">',
      '  <div id="profileModalInner" class="w-full max-w-4xl bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[92vh] flex flex-col relative animate-fade-in"></div>',
      '</div>',
      // Add/edit form modal
      '<div id="formModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" onclick="if(event.target===this)window.__ngisCloseForm()">',
      '  <div class="w-full max-w-lg bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[90vh] flex flex-col relative animate-fade-in">',
      '    <div class="px-6 sm:px-7 pt-6 pb-5 border-b border-[#E1E9E3] flex items-center justify-between">',
      '      <div class="flex items-center gap-2"><span class="material-symbols-outlined text-slate-400 text-[18px]">edit_note</span><h3 class="text-base font-medium text-slate-900" id="formTitle">Edit Record</h3></div>',
      '      <button type="button" onclick="window.__ngisCloseForm()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1.5 hover:bg-slate-100 transition-colors cursor-pointer min-h-[36px] min-w-[36px] flex items-center justify-center" aria-label="Close modal">',
      '        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '      </button>',
      '    </div>',
      '    <div class="p-4 sm:p-6 overflow-y-auto pf-scroll" id="formFields"></div>',
      '    <div class="px-6 sm:px-7 py-4 border-t border-[#E1E9E3] bg-[#F7F9F7]/50 flex items-center justify-between gap-2">',
      '      <span class="text-xs text-[#B3261E] font-medium" id="formError"></span>',
      '      <div class="flex items-center gap-2 ml-auto">',
      '        <button type="button" onclick="window.__ngisCloseForm()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-[#F7F9F7] transition-all cursor-pointer min-h-[40px]">Cancel</button>',
      '        <button type="button" id="formSaveBtn" class="px-4 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs active:scale-95 transition-all cursor-pointer min-h-[40px] flex items-center justify-center gap-2"><span class="material-symbols-outlined text-[16px]">save</span><span>Save</span></button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>',
      // Bulk Excel Import Modal
      '<div id="excelImportModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" onclick="if(event.target===this)window.__ngisCloseExcelModal()">',
      '  <div class="w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[90vh] flex flex-col relative animate-fade-in">',
      '    <div class="px-6 sm:px-7 pt-6 pb-4 border-b border-[#E1E9E3] flex items-center justify-between">',
      '      <div class="flex items-center gap-2.5">',
      '        <span class="material-symbols-outlined text-[#176B45] text-[24px]">content_paste</span>',
      '        <div>',
      '          <h3 class="text-base font-medium text-slate-900 leading-tight">Paste &amp; Import from Excel</h3>',
      '          <p class="text-[11px] text-slate-500 mt-0.5">Copy columns from Excel or Google Sheets (Name, Subject, Department, Email, Code, Workload) and paste below</p>',
      '        </div>',
      '      </div>',
      '      <button type="button" onclick="window.__ngisCloseExcelModal()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1.5 hover:bg-slate-100 transition-colors cursor-pointer" aria-label="Close modal">',
      '        <span class="material-symbols-outlined text-[20px]">close</span>',
      '      </button>',
      '    </div>',
      '    <div class="p-6 space-y-4 overflow-y-auto pf-scroll">',
      '      <div>',
      '        <label class="block text-xs font-medium text-slate-700 mb-1.5" for="excelPasteInput">Paste Tabular Data (Ctrl+V)</label>',
      '        <textarea id="excelPasteInput" rows="6" class="w-full text-xs font-mono p-3 rounded-xl border border-[#E1E9E3] bg-[#F7F9F7] text-slate-800 placeholder:text-slate-400 focus:bg-white focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all" placeholder="Sok Dara\tKhmer Literature\tMoEYS Faculty\tsok.dara@ngis.edu.kh\tK1\t17\nChou Meng\tMathematics\tScience & Math\tchou.meng@ngis.edu.kh\tM1\t18"></textarea>',
      '      </div>',
      '      <div id="excelPreviewSection" class="hidden space-y-2">',
      '        <div class="flex items-center justify-between text-xs font-medium text-slate-700">',
      '          <span>Parsed Records Preview (<span id="excelParsedCount">0</span> teachers detected)</span>',
      '          <span class="text-[11px] text-emerald-700 font-medium" id="excelValidCount"></span>',
      '        </div>',
      '        <div class="border border-[#E1E9E3] rounded-xl overflow-hidden max-h-48 overflow-y-auto">',
      '          <table class="w-full text-left text-xs whitespace-nowrap min-w-full">',
      '            <thead class="bg-slate-50 border-b border-slate-200 text-slate-500 font-medium text-[11px]">',
      '              <tr><th class="py-2 px-3">Name</th><th class="py-2 px-3">Subject</th><th class="py-2 px-3">Department</th><th class="py-2 px-3">Email</th><th class="py-2 px-3">Code</th><th class="py-2 px-3">Workload</th></tr>',
      '            </thead>',
      '            <tbody id="excelPreviewBody" class="divide-y divide-slate-100 bg-white"></tbody>',
      '          </table>',
      '        </div>',
      '      </div>',
      '    </div>',
      '    <div class="px-6 py-4 border-t border-[#E1E9E3] bg-[#F7F9F7]/50 flex items-center justify-between gap-2">',
      '      <span class="text-xs text-rose-600 font-medium" id="excelImportError"></span>',
      '      <div class="flex items-center gap-2 ml-auto">',
      '        <button type="button" onclick="window.__ngisCloseExcelModal()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-[#F7F9F7] transition-all cursor-pointer">Cancel</button>',
      '        <button type="button" id="btnExecuteExcelImport" disabled class="px-5 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] disabled:opacity-40 disabled:cursor-not-allowed rounded-lg shadow-xs transition-all cursor-pointer flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px]">file_download</span><span>Import Records</span></button>',
      '      </div>',
      '    </div>',
      '  </div>',
      '</div>',
      // Confirm / reason dialog
      '<div id="confirmModal" class="hidden fixed inset-0 z-[70] flex items-center justify-center p-4 sm:p-6 bg-black/40 backdrop-blur-xs">',
      '  <div class="bg-white rounded-2xl shadow-sm border border-[#E1E9E3] max-w-md w-full p-6">',
      '    <h3 class="text-base font-medium text-[#29352E] mb-1.5"></h3>',
      '    <p class="text-sm text-slate-600 mb-4" id="cfMessage"></p>',
      '    <div id="cfReasonWrap" class="mb-4">',
      '      <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="cfReason">Written reason <span class="text-[#B3261E]">*</span> <span class="text-xs text-slate-400 normal-case">(required by audit policy)</span></label>',
      '      <textarea class="w-full text-xs py-2 pl-3 pr-4 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="cfReason" rows="2" placeholder="e.g. Contract ended per HR letter dated 2026-09-30"></textarea>',
      '      <span class="text-[11px] text-[#B3261E] hidden" id="cfReasonError">A reason is required before this action can be confirmed.</span>',
      '    </div>',
      '    <div class="flex items-center justify-end gap-2">',
      '      <button type="button" id="cfCancel" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-[#E1E9E3] rounded-lg hover:bg-[#F7F9F7] transition-all cursor-pointer min-h-[40px]">Cancel</button>',
      '      <button type="button" id="cfOk" class="px-4 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs transition-all cursor-pointer min-h-[40px]">Confirm</button>',
      '    </div>',
      '  </div>',
      '</div>',
      // Toast
      '<div id="ngisToast" role="status" aria-live="polite" class="fixed bottom-24 right-24 bg-[#29352E] text-white px-4 py-3 rounded-lg font-medium text-xs shadow-lg z-1200 hidden">Toast</div>'
    ].join('\n');
    while (wrap.firstChild) document.body.appendChild(wrap.firstChild);

    window.__ngisCloseForm = closeForm;
    $id('formSaveBtn').addEventListener('click', saveForm);
    $id('cfCancel').addEventListener('click', function () { closeConfirm(null); });
    $id('cfOk').addEventListener('click', function () {
      var requireReason = $id('cfReasonWrap').style.display !== 'none';
      var reason = $id('cfReason').value.trim();
      if (requireReason && !reason) { $id('cfReasonError').classList.remove('hidden'); return; }
      closeConfirm(requireReason ? reason : true);
    });
    $id('confirmModal').addEventListener('click', function (e) {
      if (e.target === this) closeConfirm(null);
    });

    // Excel import textarea parsing
    var pasteArea = $id('excelPasteInput');
    if (pasteArea) {
      pasteArea.addEventListener('input', function () {
        var raw = pasteArea.value.trim();
        if (!raw) {
          $id('excelPreviewSection').classList.add('hidden');
          $id('btnExecuteExcelImport').disabled = true;
          return;
        }
        var lines = raw.split(/\r?\n/).filter(function (l) { return l.trim().length > 0; });
        parsedExcelTeachers = [];
        lines.forEach(function (line) {
          var parts = line.split(/[\t,]/).map(function (p) { return p.trim(); });
          if (parts.length >= 2) {
            // Ignore header row if detected
            if (parts[0].toLowerCase() === 'name' || parts[0].toLowerCase() === 'full name') return;
            var rec = {
              name: parts[0] || '',
              subject: parts[1] || 'General',
              department: parts[2] || 'Faculty',
              email: parts[3] || (parts[0].toLowerCase().replace(/\s+/g, '.') + '@ngis.edu.kh'),
              code: parts[4] || '',
              target: parseInt(parts[5], 10) || 17,
              role: 'Faculty',
              status: 'active'
            };
            if (rec.name) parsedExcelTeachers.push(rec);
          }
        });

        $id('excelParsedCount').textContent = parsedExcelTeachers.length;
        $id('excelValidCount').textContent = parsedExcelTeachers.length + ' ready to import';
        var pBody = $id('excelPreviewBody');
        if (pBody) {
          pBody.innerHTML = parsedExcelTeachers.slice(0, 15).map(function (t) {
            return '<tr class="border-b border-slate-100"><td class="py-2 px-3 font-medium text-slate-800">' + esc(t.name) + '</td><td class="py-2 px-3">' + esc(t.subject) + '</td><td class="py-2 px-3">' + esc(t.department) + '</td><td class="py-2 px-3 font-mono text-[11px]">' + esc(t.email) + '</td><td class="py-2 px-3 font-mono">' + esc(t.code || '—') + '</td><td class="py-2 px-3">' + t.target + ' hrs</td></tr>';
          }).join('') + (parsedExcelTeachers.length > 15 ? '<tr><td colspan="6" class="py-1 px-3 text-center text-slate-400 text-[11px]">... and ' + (parsedExcelTeachers.length - 15) + ' more records</td></tr>' : '');
        }
        $id('excelPreviewSection').classList.remove('hidden');
        $id('btnExecuteExcelImport').disabled = parsedExcelTeachers.length === 0;
      });
    }

    var btnExecExcel = $id('btnExecuteExcelImport');
    if (btnExecExcel) {
      btnExecExcel.addEventListener('click', function () {
        if (!parsedExcelTeachers.length) return;
        btnExecExcel.disabled = true;
        var importedCount = 0;
        var promises = parsedExcelTeachers.map(function (t) {
          return api(API_BASE, { method: 'POST', body: JSON.stringify(t) })
            .then(function (res) {
              importedCount++;
              if (res && res.data) state.all.unshift(res.data);
            })
            .catch(function () {});
        });

        Promise.all(promises).then(function () {
          btnExecExcel.disabled = false;
          closeExcelImportModal();
          applyFilters();
          toast('Imported ' + importedCount + ' teachers from Excel.');
        });
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (!$id('confirmModal').classList.contains('hidden')) closeConfirm(null);
        else if (!$id('formModal').classList.contains('hidden')) closeForm();
        else if (!$id('profileModal').classList.contains('hidden')) closeProfile();
        else if (!$id('excelImportModal').classList.contains('hidden')) closeExcelImportModal();
      }
    });
  }
  function boot() {
    renderShell();
    mountModals();
    loadDirectory();
    // Deep link: admin-users-students/teachers open profiles here with
    // ?open-profile=<institutional id>. Clean the URL, then auto-open the
    // actual record's profile modal once the shell is mounted.
    var deepId = '';
    try {
      var sp = new URLSearchParams(window.location.search);
      deepId = (sp.get('open-profile') || '').trim();
      if (deepId) {
        sp.delete('open-profile');
        var qs = sp.toString();
        history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : ''));
      }
    } catch (e) { /* older browsers: deep link simply not applied */ }
    if (deepId) {
      var tries = 0;
      (function tryOpen() {
        tries += 1;
        var m = $id('profileModal');
        if (m) { openProfile(deepId); return; }
        if (tries < 20) window.setTimeout(tryOpen, 200);
      })();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
