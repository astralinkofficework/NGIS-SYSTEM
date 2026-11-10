import sys

with open('assets/js/ngis-profiles.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update renderShell
shell_old_start = '  function renderShell() {'
shell_old_end = '    renderFilterOptions();\n  }'

new_render_shell = '''  function renderShell() {
    var root = $id('profilesRoot');
    var pageTitle = IS_TEACHER ? 'Teacher Profiles' : 'Student Profiles';
    root.innerHTML = [
      '<div class="space-y-6 w-full">',
      // Section 1: Header Page Title & Top Actions
      '  <section class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-2">',
      '    <div>',
      '      <h1 class="text-2xl lg:text-[26px] font-medium text-slate-900 tracking-tight">' + pageTitle + '</h1>',
      '    </div>',
      '    <div class="flex items-center flex-wrap gap-2.5 shrink-0">',
      '      <button type="button" id="btnRefresh" class="' + BTN_SECONDARY + '">',
      '        <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        <span>Sync Registry</span>',
      '      </button>',
      '      <button type="button" id="btnExport" class="' + BTN_SECONDARY + '" title="Export the filtered directory as CSV">',
      '        <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        <span>Export (CSV)</span>',
      '      </button>',
      IS_TEACHER
        ? '      <button type="button" id="btnAddTeacher" class="' + BTN_PRIMARY + '"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2"></path></svg><span>+ Add Teacher</span></button>'
        : '',
      '    </div>',
      '  </section>',
      // Section 2: Executive Telemetry KPI Cards
      '  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-purpose="metrics-telemetry" id="kpiGrid"></section>',
      // Section 3: Standalone Search & Filter Bar (Matching Golden Reference principal-classes.html)
      '  <section class="bg-white rounded-xl border border-[#E1E9E3] p-3 sm:p-4 shadow-2xs" data-purpose="filtering-controls">',
      '    <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">',
      '      <!-- Search Input with padding-left 44px -->',
      '      <div class="relative flex-1 min-w-[260px] max-w-xl">',
      '        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none z-10 flex items-center">',
      '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        </span>',
      '        <input class="w-full pl-11 pr-9 py-2 bg-white border border-[#E1E9E3] rounded-lg text-xs placeholder:text-slate-400 text-slate-800 focus:outline-none focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all min-h-[40px]" id="dirSearch" style="padding-left: 44px !important;" type="text" placeholder="Search ' + (IS_TEACHER ? 'teacher name, ID, subject or email...' : 'student name, ID, class or guardian...') + '">',
      '        <button class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-[#176B45] cursor-pointer" id="clearSearch" type="button" aria-label="Clear search">',
      '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        </button>',
      '      </div>',
      '      <!-- Filter Dropdowns & Status Badge: Clean horizontal row, wraps fluidly on mobile (never awkward vertical tower) -->',
      '      <div class="flex flex-wrap items-center gap-2 sm:gap-2.5 shrink-0">',
      '        <div class="relative flex-1 sm:flex-initial min-w-[130px]">',
      '          <select class="' + SELECT_CLS + '" id="deptFilter"></select>',
      '          <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg></span>',
      '        </div>',
      '        <div class="relative flex-1 sm:flex-initial min-w-[130px]">',
      '          <select class="' + SELECT_CLS + '" id="statusFilter"></select>',
      '          <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg></span>',
      '        </div>',
      '        <div class="relative flex-1 sm:flex-initial min-w-[140px]">',
      '          <select class="' + SELECT_CLS + '" id="sortSelect">',
      IS_TEACHER
        ? '<option value="name-asc">Sort: Name (A-Z)</option><option value="name-desc">Sort: Name (Z-A)</option><option value="yearsAtSchool-desc">Sort: Most Senior</option><option value="classesAssigned-desc">Sort: Most Classes</option><option value="pendingGradeRecords-desc">Sort: Pending Records</option>'
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
      // Section 4: Standalone Clean Data Table
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
      '  </div>',
      '</div>'
    ].join('\\n');

    // Head columns
    $id('dirHead').innerHTML = IS_TEACHER
      ? '<th class="w-10 py-3.5 pl-4 pr-2" scope="col"></th><th class="py-3.5 px-4 font-medium" scope="col">Educator</th><th class="py-3.5 px-4 font-medium" scope="col">Department &amp; Subject</th><th class="py-3.5 px-4 font-medium" scope="col">Classes</th><th class="py-3.5 px-4 font-medium" scope="col">Grade Records</th><th class="py-3.5 px-4 font-medium" scope="col">Status</th><th class="py-3.5 pr-4 pl-4 text-right font-medium" scope="col">Actions</th>'
      : '<th class="w-10 py-3.5 pl-4 pr-2" scope="col"></th><th class="py-3.5 px-4 font-medium" scope="col">Student</th><th class="py-3.5 px-4 font-medium" scope="col">Grade &amp; Class</th><th class="py-3.5 px-4 font-medium" scope="col">Advisor</th><th class="py-3.5 px-4 font-medium" scope="col">GPA</th><th class="py-3.5 px-4 font-medium" scope="col">Attendance</th><th class="py-3.5 px-4 font-medium" scope="col">Requests</th><th class="py-3.5 px-4 font-medium" scope="col">Status</th><th class="py-3.5 pr-4 pl-4 text-right font-medium" scope="col">Actions</th>';

    wireShell();
    renderFilterOptions();
  }'''

idx_start = content.find(shell_old_start)
idx_end = content.find(shell_old_end) + len(shell_old_end)

if idx_start == -1 or idx_end < len(shell_old_end):
    print('Failed to locate renderShell!')
    sys.exit(1)

content = content[:idx_start] + new_render_shell + content[idx_end:]
print('renderShell updated successfully!')

# 2. Update renderKpis
kpi_old_start = '  function renderKpis() {'
kpi_old_end = '    }\n  }\n\n  /* ---------- chips ---------- */'

new_render_kpis = '''  function renderKpis() {
    var grid = $id('kpiGrid');
    if (!grid) return;
    var total = state.all.length;
    if (IS_TEACHER) {
      var active = state.all.filter(function (t) { return String(t.status || '').toLowerCase() === 'active'; }).length;
      var activePct = total ? Math.round(active / total * 100) : 100;
      var depts = uniq('department').length;
      var pendRecords = state.all.reduce(function (n, t) { return n + (t.pendingGradeRecords || 0); }, 0);
      var pubRecords = state.all.reduce(function (n, t) { return n + (t.publishedGradeRecords || 0); }, 0);

      grid.innerHTML = [
        // Card 1: Credentialed Faculty
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Credentialed Faculty</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight text-[#29352E]">' + total + '</span>',
        '        <span class="text-xs font-medium text-emerald-700">' + activePct + '% Active</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">badge</span>',
        '    </div>',
        '  </div>',
        '  <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-600">',
        '    <span class="material-symbols-outlined text-[16px] text-slate-400">domain</span>',
        '    <span class="truncate">' + depts + ' academic departments covered</span>',
        '  </div>',
        '</div>',

        // Card 2: Active Standing & Clearance Rate with Two-Tone Bar
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Clearance Rate</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight text-[#29352E]">' + activePct + '%</span>',
        '        <span class="text-xs font-normal text-slate-400">Target: 100%</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">verified</span>',
        '    </div>',
        '  </div>',
        '  <div class="pt-2 mt-1">',
        '    <div class="flex items-center justify-between text-xs mb-1.5">',
        '      <span class="text-slate-600 font-normal">' + active + ' active</span>',
        '      <span class="text-[#991b1b] font-medium">' + (total - active) + ' on leave/pending</span>',
        '    </div>',
        '    <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">',
        '      <div class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: ' + activePct + '%"></div>',
        '      <div class="bg-[#991b1b] h-full rounded-full transition-all duration-500" style="width: ' + (100 - activePct) + '%"></div>',
        '    </div>',
        '  </div>',
        '</div>',

        // Card 3: Pending Grade Records (Golden Reference corner tint)
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between relative overflow-hidden">',
        (pendRecords > 0 ? '  <div class="absolute right-0 top-0 w-24 h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>' : ''),
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider ' + (pendRecords > 0 ? 'text-[#991b1b]' : 'text-slate-500') + ' block">Pending Clearances</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight ' + (pendRecords > 0 ? 'text-[#991b1b]' : 'text-[#29352E]') + '">' + pendRecords + '</span>',
        (pendRecords > 0
          ? '        <span class="inline-flex items-center gap-1 text-xs font-medium text-[#991b1b] bg-rose-100/90 px-1.5 py-0.5 rounded">High Priority</span>'
          : '        <span class="text-xs font-medium text-emerald-700">All Cleared</span>'),
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg ' + (pendRecords > 0 ? 'bg-rose-100/90 text-[#991b1b]' : 'bg-emerald-50 text-[#176B45]') + ' flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">' + (pendRecords > 0 ? 'pending_actions' : 'check_circle') + '</span>',
        '    </div>',
        '  </div>',
        '  <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-700">',
        '    <span class="material-symbols-outlined text-[16px] ' + (pendRecords > 0 ? 'text-[#991b1b]' : 'text-[#176B45]') + '">flag</span>',
        '    <span class="truncate">' + (pendRecords > 0 ? 'Awaiting principal clearance: Grade records' : 'All faculty records cleared') + '</span>',
        '  </div>',
        '</div>',

        // Card 4: Published Records / Turnaround
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Published Records</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight text-[#29352E]">' + pubRecords + '<span class="text-lg font-normal text-slate-400"> recs</span></span>',
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">publish</span>',
        '    </div>',
        '  </div>',
        '  <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-700">',
        '    <span class="material-symbols-outlined text-[16px] text-[#176B45]">trending_up</span>',
        '    <span class="font-normal truncate">Released to student transcripts</span>',
        '  </div>',
        '</div>'
      ].join('\\n');
    } else {
      // Students
      var gpa = total ? state.all.reduce(function (n, s) { return n + (Number(s.gpaLive) || 0); }, 0) / total : 0;
      var att = total ? state.all.reduce(function (n, s) { return n + (Number(s.attendancePct) || 0); }, 0) / total : 0;
      var open = state.all.reduce(function (n, s) { return n + (s.openRequests || 0); }, 0);
      var classes = uniq('class').length;
      var gpaPct = Math.min(100, Math.round((gpa / 4.0) * 100));

      grid.innerHTML = [
        // Card 1: Enrolled Students
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Enrolled Students</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight text-[#29352E]">' + total + '</span>',
        '        <span class="text-xs font-medium text-emerald-700">100% Active</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">school</span>',
        '    </div>',
        '  </div>',
        '  <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-600">',
        '    <span class="material-symbols-outlined text-[16px] text-slate-400">domain</span>',
        '    <span class="truncate">Enrolled across ' + classes + ' cohort sections</span>',
        '  </div>',
        '</div>',

        // Card 2: Cohort GPA Standing
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Cohort Standing (GPA)</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight text-[#29352E]">' + num(gpa) + '</span>',
        '        <span class="text-xs font-normal text-slate-400">/ 4.00</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">verified</span>',
        '    </div>',
        '  </div>',
        '  <div class="pt-2 mt-1">',
        '    <div class="flex items-center justify-between text-xs mb-1.5">',
        '      <span class="text-slate-600 font-normal">Live term performance</span>',
        '      <span class="text-emerald-700 font-medium">' + gpaPct + '% of max</span>',
        '    </div>',
        '    <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">',
        '      <div class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: ' + gpaPct + '%"></div>',
        '    </div>',
        '  </div>',
        '</div>',

        // Card 3: Open Service Requests (Golden Reference corner tint)
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between relative overflow-hidden">',
        (open > 0 ? '  <div class="absolute right-0 top-0 w-24 h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>' : ''),
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider ' + (open > 0 ? 'text-[#991b1b]' : 'text-slate-500') + ' block">Open Service Requests</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight ' + (open > 0 ? 'text-[#991b1b]' : 'text-[#29352E]') + '">' + open + '</span>',
        (open > 0
          ? '        <span class="inline-flex items-center gap-1 text-xs font-medium text-[#991b1b] bg-rose-100/90 px-1.5 py-0.5 rounded">High Priority</span>'
          : '        <span class="text-xs font-medium text-emerald-700">All Completed</span>'),
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg ' + (open > 0 ? 'bg-rose-100/90 text-[#991b1b]' : 'bg-emerald-50 text-[#176B45]') + ' flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">' + (open > 0 ? 'pending_actions' : 'check_circle') + '</span>',
        '    </div>',
        '  </div>',
        '  <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-700">',
        '    <span class="material-symbols-outlined text-[16px] ' + (open > 0 ? 'text-[#991b1b]' : 'text-[#176B45]') + '">flag</span>',
        '    <span class="truncate">' + (open > 0 ? 'ID cards, transcripts & fees pending' : 'Zero outstanding student requests') + '</span>',
        '  </div>',
        '</div>',

        // Card 4: Attendance Average
        '<div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">',
        '  <div class="flex items-start justify-between">',
        '    <div>',
        '      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Average Attendance</span>',
        '      <div class="flex items-baseline gap-2 mt-1">',
        '        <span class="text-3xl font-medium tracking-tight text-[#29352E]">' + num(att, 1) + '%</span>',
        '      </div>',
        '    </div>',
        '    <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">',
        '      <span class="material-symbols-outlined text-[22px]">fact_check</span>',
        '    </div>',
        '  </div>',
        '  <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-700">',
        '    <span class="material-symbols-outlined text-[16px] text-[#176B45]">event_available</span>',
        '    <span class="font-normal truncate">Mean presence across roster</span>',
        '  </div>',
        '</div>'
      ].join('\\n');
    }
  }

  /* ---------- chips ---------- */'''

idx_start = content.find(kpi_old_start)
idx_end = content.find(kpi_old_end) + len(kpi_old_end)

if idx_start == -1 or idx_end < len(kpi_old_end):
    print('Failed to locate renderKpis!')
    sys.exit(1)

content = content[:idx_start] + new_render_kpis + content[idx_end:]
print('renderKpis updated successfully!')

# 3. Update renderChips to update filterStatusText
chip_old = "$id('dirCount').innerHTML = 'Showing <strong class=\"text-slate-800 font-medium\">' + state.filtered.length + '</strong> of <strong class=\"text-slate-800 font-medium\">' + state.all.length + '</strong> ' + PLURAL_LABEL.toLowerCase();"
chip_new = '''$id('dirCount').innerHTML = 'Showing <strong class="text-slate-800 font-medium">' + state.filtered.length + '</strong> of <strong class="text-slate-800 font-medium">' + state.all.length + '</strong> ' + PLURAL_LABEL.toLowerCase();
    var st = $id('filterStatusText');
    if (st) st.textContent = state.filtered.length + ' ' + PLURAL_LABEL.toLowerCase();'''

content = content.replace(chip_old, chip_new, 1)
print('renderChips updated successfully!')

# 4. Update actions in renderTable
actions_old = '''    body.innerHTML = pageRows.map(function (r) {
      var actions = '<div class="flex items-center justify-end gap-1.5">' +
        actionBtn('edit', r.id, 'edit', 'Edit record') +
        actionBtn('toggle', r.id, String(r.status || '').toLowerCase() === 'active' ? 'power_off' : 'power_settings_new',
          String(r.status || '').toLowerCase() === 'active' ? 'Deactivate' : 'Activate') +
        '<button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">Profile</button>' +
        '</div>';'''

actions_new = '''    body.innerHTML = pageRows.map(function (r) {
      var isActive = String(r.status || '').toLowerCase() === 'active';
      var actions = '<div class="inline-flex items-center gap-1.5">' +
        '<button type="button" data-act="view" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
          'Profile' +
        '</button>' +
        '<button type="button" data-act="edit" data-id="' + esc(r.id) + '" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 border border-slate-200/70 rounded-lg hover:bg-[#176B45] hover:text-white hover:border-[#176B45] transition-colors cursor-pointer min-h-[32px]">' +
          'Edit' +
        '</button>' +
        '<button type="button" data-act="toggle" data-id="' + esc(r.id) + '" title="' + (isActive ? 'Deactivate record' : 'Activate record') + '" class="p-1 text-slate-400 hover:text-slate-700 rounded transition-colors cursor-pointer min-h-[32px] min-w-[32px] flex items-center justify-center" aria-label="Toggle status">' +
          '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="1" fill="currentColor"></circle><circle cx="12" cy="5" r="1" fill="currentColor"></circle><circle cx="12" cy="19" r="1" fill="currentColor"></circle></svg>' +
        '</button>' +
        '</div>';'''

if actions_old not in content:
    print('Failed to locate actions in renderTable!')
    sys.exit(1)

content = content.replace(actions_old, actions_new, 1)
print('renderTable actions updated successfully!')

# 5. Update renderPager
pager_old = "info.innerHTML = 'Showing <strong class=\"text-slate-800 font-medium\">' + start + ' to ' + end + '</strong> of <strong class=\"text-slate-800 font-medium\">' + total + '</strong> ' + PLURAL_LABEL.toLowerCase() +"
pager_new = "info.innerHTML = 'Showing <span class=\"font-medium text-slate-800\">' + start + '</span> to <span class=\"font-medium text-slate-800\">' + end + '</span> of <span class=\"font-medium text-slate-800\">' + total + '</span> active ' + PLURAL_LABEL.toLowerCase() +"

content = content.replace(pager_old, pager_new, 1)
print('renderPager updated successfully!')

with open('assets/js/ngis-profiles.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('All updates successfully written to assets/js/ngis-profiles.js!')

