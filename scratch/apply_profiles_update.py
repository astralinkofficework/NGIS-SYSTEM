import os

profiles_path = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js'

with open(profiles_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Let's inspect the sections to replace
shell_start = code.find("  function renderShell() {")
shell_end = code.find("  function renderFilterOptions() {")

assert shell_start != -1 and shell_end != -1, "shell bounds not found"

new_shell_and_wire = '''  function renderShell() {
    var root = $id('profilesRoot');
    var pageTitle = IS_TEACHER ? 'Teacher Profiles' : 'Student Profiles';
    root.innerHTML = [
      '<div class="space-y-6 w-full">',
      // Section 1: Header Page Title & Top Actions
      '  <section class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-2">',
      '    <div>',
      '      <h1 class="text-2xl lg:text-[26px] font-medium text-slate-900 tracking-tight">' + pageTitle + '</h1>',
      '      <p class="text-xs text-slate-500 mt-1 font-normal">' + (IS_TEACHER ? 'Modern row-based faculty registry & academic configuration' : 'Student directory and academic standing') + '</p>',
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
        ? '      <button type="button" id="btnPasteExcel" class="' + BTN_SECONDARY + '" title="Paste from Excel or Google Sheets"><span class="material-symbols-outlined text-[16px] text-slate-500">content_paste</span><span>Paste from Excel</span></button>' +
          '      <button type="button" id="btnAddTeacher" class="' + BTN_PRIMARY + '"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2"></path></svg><span>+ Add Teacher</span></button>'
        : '',
      '    </div>',
      '  </section>',
      // Section 2: Executive Telemetry KPI Cards
      '  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-purpose="metrics-telemetry" id="kpiGrid"></section>',
      // Section 3: Standalone Search & Filter Bar
      '  <section class="bg-white rounded-xl border border-[#E1E9E3] p-3 sm:p-4 shadow-2xs" data-purpose="filtering-controls">',
      '    <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">',
      '      <!-- Search Input with padding-left 44px -->',
      '      <div class="relative flex-1 min-w-[260px] max-w-xl">',
      '        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none z-10 flex items-center">',
      '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        </span>',
      '        <input class="w-full pl-11 pr-9 py-2 bg-white border border-[#E1E9E3] rounded-lg text-xs placeholder:text-slate-400 text-slate-800 focus:outline-none focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all min-h-[40px]" id="dirSearch" style="padding-left: 44px !important;" type="text" placeholder="Search ' + (IS_TEACHER ? 'teacher name, ID, code, subject or department...' : 'student name, ID, class or guardian...') + '">',
      '        <button class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-[#176B45] cursor-pointer" id="clearSearch" type="button" aria-label="Clear search">',
      '          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>',
      '        </button>',
      '      </div>',
      '      <!-- Filter Dropdowns & Status Badge -->',
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
          ].join('\\n')
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
          ].join('\\n'),
      '</div>'
    ].join('\\n');

    if (!IS_TEACHER) {
      $id('dirHead').innerHTML = '<th class="w-10 py-3.5 pl-4 pr-2" scope="col"></th><th class="py-3.5 px-4 font-medium" scope="col">Student</th><th class="py-3.5 px-4 font-medium" scope="col">Grade &amp; Class</th><th class="py-3.5 px-4 font-medium" scope="col">Advisor</th><th class="py-3.5 px-4 font-medium" scope="col">GPA</th><th class="py-3.5 px-4 font-medium" scope="col">Attendance</th><th class="py-3.5 px-4 font-medium" scope="col">Requests</th><th class="py-3.5 px-4 font-medium" scope="col">Status</th><th class="py-3.5 pr-4 pl-4 text-right font-medium" scope="col">Actions</th>';
    }

    wireShell();
    renderFilterOptions();
  }

  function resetAllFilters() {
    state.search = ''; state.dept = 'ALL'; state.status = 'ALL'; state.sort = 'name-asc'; state.page = 1;
    $id('dirSearch').value = ''; $('#clearSearch').classList.add('hidden');
    $id('deptFilter').value = 'ALL'; $id('statusFilter').value = 'ALL'; $id('sortSelect').value = 'name-asc';
    applyFilters();
  }

  function wireShell() {
    $id('dirSearch').addEventListener('input', function (e) {
      state.search = e.target.value; state.page = 1;
      $('#clearSearch').classList.toggle('hidden', !state.search);
      applyFilters();
    });
    $('#clearSearch').addEventListener('click', function () {
      state.search = ''; $id('dirSearch').value = ''; $('#clearSearch').classList.add('hidden'); applyFilters();
    });
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
      else if (which === 'search') { state.search = ''; $id('dirSearch').value = ''; $('#clearSearch').classList.add('hidden'); }
      applyFilters();
    });
  }
'''

code = code[:shell_start] + new_shell_and_wire + code[shell_end:]
print("Replaced renderShell and wireShell")

with open(profiles_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Saved ngis-profiles.js checkpoint 1")

