import os

file_path = r"pages/principal/principal-classes.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update style block with custom select chevron and input styles
style_target = """  #classSearchInput {
    padding-left: 44px !important;
  }"""

style_replacement = """  #classSearchInput {
    padding-left: 44px !important;
  }
  .custom-select-icon {
    pointer-events: none;
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
  }"""

if style_target in content:
    content = content.replace(style_target, style_replacement, 1)

# 2. Update Telemetry Cards and Filter Bar
cards_filter_target = """        <!-- BEGIN: Executive Telemetry Cards (Golden Reference Image Design) -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-purpose="metrics-telemetry">
      <!-- Card 1: Credentialed Faculty & Classes -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Credentialed Classes</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#29352E]" id="kpiTotalClasses">5</span>
              <span class="text-xs font-medium text-emerald-700">100% Active</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">school</span>
          </div>
        </div>
        <div class="telemetry-pill mt-3">
          <span class="material-symbols-outlined text-[16px] text-slate-400">domain</span>
          <span class="truncate" id="metricActiveCohortsSub">Assigned across 5 academic cohorts</span>
        </div>
      </div>

      <!-- Card 2: Clearance & Enrollment with Two-Tone Bar -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Clearance Rate</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-slate-900" id="kpiClearanceRate">99.3%</span>
              <span class="text-xs font-normal text-slate-400">Target: 100%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-emerald-100/70 text-emerald-800 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">verified</span>
          </div>
        </div>
        <div class="pt-2 mt-1">
          <div class="flex items-center justify-between text-xs mb-1.5">
            <span class="text-slate-600 font-normal" id="kpiClearedCount">149 enrolled</span>
            <span class="text-[#176B45] font-medium" id="kpiPendingCount">1 open seat</span>
          </div>
          <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
            <div id="clearanceProgressBar" class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: 99.3%"></div>
            <div id="pendingProgressBar" class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: 0.7%"></div>
          </div>
        </div>
      </div>

      <!-- Card 3: Pending Clearances with Corner Tint Accent -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between relative overflow-hidden">
        <div class="absolute right-0 top-0 w-24 h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-[#176B45] block">Pending Clearances</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#176B45]" id="kpiPendingFaculty">2</span>
              <span class="inline-flex items-center gap-1 text-xs font-medium text-[#176B45] bg-rose-100/80 px-1.5 py-0.5 rounded">
                High Priority
              </span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-rose-100 text-[#176B45] flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">pending_actions</span>
          </div>
        </div>
        <div class="telemetry-pill mt-3">
          <span class="material-symbols-outlined text-[16px] text-[#176B45]">flag</span>
          <span class="truncate text-slate-700">Awaiting review: Math &amp; Humanities</span>
        </div>
      </div>

      <!-- Card 4: Registry Turnaround -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Registry Turnaround</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#29352E]">2.4<span class="text-lg font-normal text-slate-400"> hrs</span></span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">speed</span>
          </div>
        </div>
        <div class="telemetry-pill mt-3">
          <span class="material-symbols-outlined text-[16px] text-emerald-700">trending_down</span>
          <span class="font-normal text-slate-700 truncate">35 mins faster than Q1 AY 2024-25</span>
        </div>
      </div>
    </section>
    <!-- END: Executive Telemetry Cards -->

    <!-- BEGIN: Search & Filter Bar -->
    <section class="bg-white rounded-xl border border-slate-200/90 p-3.5 sm:p-4 shadow-2xs" data-purpose="filtering-controls">
      <div class="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3">
        <!-- Search Input with ample left padding preventing icon collision -->
        <div class="relative flex-1 min-w-[240px] max-w-lg">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none flex items-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
            </svg>
          </span>
          <input id="classSearchInput" class="w-full !pl-11 pr-4 py-2 bg-slate-50 hover:bg-slate-100/70 focus:bg-white border border-slate-200 rounded-lg text-xs placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all min-h-[40px] classes-search-input" style="padding-left: 44px !important;" placeholder="Search cohort, homeroom educator, room, or campus..." type="text">
        </div>

        <!-- Filter Dropdowns & Status Badge (Clean horizontal flow, no awkward column stacking) -->
        <div class="flex flex-wrap sm:flex-nowrap items-center gap-2.5 shrink-0">
          <div class="relative flex-1 sm:flex-initial" style="min-width: 125px;">
            <select id="gradeFilter" class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-slate-200/90 bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none" style="width: auto !important; min-width: 125px;">
              <option value="all">All Grades</option>
              <option value="10">Grade 10</option>
              <option value="11">Grade 11</option>
              <option value="12">Grade 12</option>
            </select>
          </div>

          <div class="relative flex-1 sm:flex-initial" style="min-width: 135px;">
            <select id="campusFilter" class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-slate-200/90 bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none" style="width: auto !important; min-width: 135px;">
              <option value="all">All Campuses</option>
              <option value="Sensok">Sensok Campus</option>
              <option value="TK">TK Campus</option>
            </select>
          </div>

          <div class="relative flex-1 sm:flex-initial" style="min-width: 125px;">
            <select id="statusFilter" class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-slate-200/90 bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none" style="width: auto !important; min-width: 125px;">
              <option value="all">Status: All</option>
              <option value="active" selected="">Active Only</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          <span class="text-xs text-slate-300 px-0.5 hidden xl:inline">|</span>
          <span class="text-xs font-medium text-slate-500 whitespace-nowrap text-center sm:text-left pt-1 sm:pt-0" id="filterStatusCount">5 active cohorts</span>
        </div>
      </div>
    </section>
    <!-- END: Search & Filter Bar -->"""

cards_filter_replacement = """    <!-- BEGIN: Executive Telemetry Cards (Golden Reference Image Design) -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-purpose="metrics-telemetry">
      <!-- Card 1: Credentialed Faculty & Classes -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Credentialed Classes</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#29352E]" id="kpiTotalClasses">5</span>
              <span class="text-xs font-medium text-emerald-700">100% Active</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">badge</span>
          </div>
        </div>
        <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-600">
          <span class="material-symbols-outlined text-[16px] text-slate-400">domain</span>
          <span class="truncate" id="metricActiveCohortsSub">Assigned across 5 academic cohorts</span>
        </div>
      </div>

      <!-- Card 2: Clearance & Enrollment with Two-Tone Bar -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Clearance Rate</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#29352E]" id="kpiClearanceRate">99.3%</span>
              <span class="text-xs font-normal text-slate-400">Target: 100%</span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">verified</span>
          </div>
        </div>
        <div class="pt-2 mt-1">
          <div class="flex items-center justify-between text-xs mb-1.5">
            <span class="text-slate-600 font-normal" id="kpiClearedCount">149 enrolled</span>
            <span class="text-[#991b1b] font-medium" id="kpiPendingCount">1 open seat</span>
          </div>
          <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
            <div id="clearanceProgressBar" class="bg-[#176B45] h-full rounded-full transition-all duration-500" style="width: 99.3%"></div>
            <div id="pendingProgressBar" class="bg-[#991b1b] h-full rounded-full transition-all duration-500" style="width: 0.7%"></div>
          </div>
        </div>
      </div>

      <!-- Card 3: Pending Clearances with Corner Tint Accent -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between relative overflow-hidden">
        <div class="absolute right-0 top-0 w-24 h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-[#991b1b] block">Pending Clearances</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#991b1b]" id="kpiPendingFaculty">2</span>
              <span class="inline-flex items-center gap-1 text-xs font-medium text-[#991b1b] bg-rose-100/90 px-1.5 py-0.5 rounded">
                High Priority
              </span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-rose-100/90 text-[#991b1b] flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">pending_actions</span>
          </div>
        </div>
        <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-700">
          <span class="material-symbols-outlined text-[16px] text-[#991b1b]">flag</span>
          <span class="truncate">Awaiting review: Math &amp; Humanities</span>
        </div>
      </div>

      <!-- Card 4: Registry Turnaround -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E1E9E3] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Registry Turnaround</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#29352E]">2.4<span class="text-lg font-normal text-slate-400"> hrs</span></span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">speed</span>
          </div>
        </div>
        <div class="mt-3.5 bg-slate-50/80 rounded-lg p-2 flex items-center gap-2 border border-slate-100 text-xs text-slate-700">
          <span class="material-symbols-outlined text-[16px] text-[#176B45]">trending_down</span>
          <span class="font-normal truncate">35 mins faster than Q1 AY 2024-25</span>
        </div>
      </div>
    </section>
    <!-- END: Executive Telemetry Cards -->

    <!-- BEGIN: Search & Filter Bar (Fully Responsive & Modern) -->
    <section class="bg-white rounded-xl border border-[#E1E9E3] p-3 sm:p-4 shadow-2xs" data-purpose="filtering-controls">
      <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
        <!-- Search Input with robust icon spacing (guarantees zero icon-text overlap) -->
        <div class="relative flex-1 min-w-[260px] max-w-xl">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none flex items-center z-10">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
            </svg>
          </span>
          <input id="classSearchInput" class="w-full !pl-11 pr-4 py-2.5 bg-slate-50 hover:bg-slate-100/60 focus:bg-white border border-[#E1E9E3] rounded-lg text-xs placeholder:text-slate-400 text-slate-800 focus:outline-none focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all min-h-[40px] classes-search-input" style="padding-left: 44px !important;" placeholder="Search cohort, homeroom educator, room, or campus..." type="text">
        </div>

        <!-- Filter Dropdowns & Status Badge: Clean horizontal row, wraps fluidly on mobile (never awkward vertical tower) -->
        <div class="flex flex-wrap items-center gap-2 sm:gap-2.5 shrink-0">
          <div class="relative flex-1 sm:flex-initial min-w-[130px]">
            <select id="gradeFilter" class="w-full text-xs py-2.5 pl-3 pr-8 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none transition-colors">
              <option value="all">All Grades</option>
              <option value="10">Grade 10</option>
              <option value="11">Grade 11</option>
              <option value="12">Grade 12</option>
            </select>
            <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </span>
          </div>

          <div class="relative flex-1 sm:flex-initial min-w-[140px]">
            <select id="campusFilter" class="w-full text-xs py-2.5 pl-3 pr-8 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none transition-colors">
              <option value="all">All Campuses</option>
              <option value="Sensok">Sensok Campus</option>
              <option value="TK">TK Campus</option>
            </select>
            <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </span>
          </div>

          <div class="relative flex-1 sm:flex-initial min-w-[130px]">
            <select id="statusFilter" class="w-full text-xs py-2.5 pl-3 pr-8 rounded-lg border border-[#E1E9E3] bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] cursor-pointer min-h-[40px] appearance-none transition-colors">
              <option value="all">Status: All</option>
              <option value="active" selected="">Active Only</option>
              <option value="inactive">Inactive</option>
            </select>
            <span class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
            </span>
          </div>

          <div class="flex items-center gap-1.5 pl-1 sm:pl-2 shrink-0">
            <span class="text-xs text-slate-300 hidden md:inline">|</span>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-50 border border-slate-200/80 text-xs font-medium text-slate-600 whitespace-nowrap" id="filterStatusCount">
              <span class="w-1.5 h-1.5 rounded-full bg-[#176B45]"></span>
              5 active cohorts
            </span>
          </div>
        </div>
      </div>
    </section>
    <!-- END: Search & Filter Bar -->"""

if cards_filter_target in content:
    content = content.replace(cards_filter_target, cards_filter_replacement, 1)
    print("Cards & Filter Bar replaced successfully!")
else:
    print("Error: cards_filter_target not matched!")

# 3. Update Modals (Edit Class Modal and Students Modal)
modals_target = """<!-- Edit / Add Class Modal -->
<div id="editClassModal" class="hidden fixed inset-0 z-50 bg-black/45 backdrop-blur-xs flex items-center justify-center p-4">
  <div class="bg-white border border-[#E1E9E3] rounded-2xl max-w-lg w-full p-6 shadow-2xl relative animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="editClassModalTitle">
    <div class="flex justify-between items-center pb-4 mb-4 border-b border-[#E1E9E3]">
      <h3 id="editClassModalTitle" class="text-base font-medium text-[#000000]">Edit Class Information</h3>
      <button type="button" onclick="closeEditModal()" class="text-slate-400 hover:text-black min-h-[36px] min-w-[36px] flex items-center justify-center cursor-pointer">
        <i class="ph ph-x text-lg"></i>
      </button>
    </div>
    <form id="editClassForm" onsubmit="saveClassChanges(event)" class="space-y-4">
      <input type="hidden" id="editClassId">
      <div>
        <label class="block text-xs font-medium text-[#64746A] mb-1">Class Title</label>
        <input type="text" id="editClassName" required class="w-full text-xs px-3 py-2 border border-[#E1E9E3] rounded-lg outline-none focus:border-[#176B45] min-h-[44px]">
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-medium text-[#64746A] mb-1">Grade Level</label>
          <input type="text" id="editClassGrade" required class="w-full text-xs px-3 py-2 border border-[#E1E9E3] rounded-lg outline-none focus:border-[#176B45] min-h-[44px]">
        </div>
        <div>
          <label class="block text-xs font-medium text-[#64746A] mb-1">Section</label>
          <input type="text" id="editClassSection" required class="w-full text-xs px-3 py-2 border border-[#E1E9E3] rounded-lg outline-none focus:border-[#176B45] min-h-[44px]">
        </div>
      </div>
      <div>
        <label class="block text-xs font-medium text-[#64746A] mb-1">Homeroom Teacher</label>
        <select id="editClassTeacher" class="w-full text-xs px-3 py-2 border border-[#E1E9E3] rounded-lg outline-none focus:border-[#176B45] min-h-[44px] bg-white cursor-pointer">
          <option value="Dr. Sarah Jenkins">Dr. Sarah Jenkins (Mathematics)</option>
          <option value="Dr. Pov Sophea">Dr. Pov Sophea (Science)</option>
          <option value="Ms. Rin Lina">Ms. Rin Lina (English)</option>
          <option value="Mr. Heng Samnang">Mr. Heng Samnang (Humanities)</option>
          <option value="Dr. Alan Vance">Dr. Alan Vance (Mathematics)</option>
          <option value="Muthukumaran Pakkirisamy">Muthukumaran Pakkirisamy (Senior Faculty)</option>
        </select>
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-medium text-[#64746A] mb-1">Assigned Room</label>
          <input type="text" id="editClassRoom" required class="w-full text-xs px-3 py-2 border border-[#E1E9E3] rounded-lg outline-none focus:border-[#176B45] min-h-[44px]">
        </div>
        <div>
          <label class="block text-xs font-medium text-[#64746A] mb-1">Student Capacity</label>
          <input type="number" id="editClassCount" min="1" max="50" required class="w-full text-xs px-3 py-2 border border-[#E1E9E3] rounded-lg outline-none focus:border-[#176B45] min-h-[44px]">
        </div>
      </div>
      <div class="flex justify-end gap-2 pt-4 border-t border-[#E1E9E3]">
        <button type="button" onclick="closeEditModal()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 cursor-pointer min-h-[40px]">Cancel</button>
        <button type="submit" id="saveClassBtn" class="px-4 py-2 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs cursor-pointer min-h-[40px]">Save Changes</button>
      </div>
    </form>
  </div>
</div>

<!-- View Class Students Drawer / Modal -->
<div id="classStudentsModal" class="hidden fixed inset-0 z-50 bg-black/45 backdrop-blur-xs flex items-center justify-center p-4">
  <div class="bg-white border border-[#E1E9E3] rounded-2xl max-w-2xl w-full p-6 shadow-2xl max-h-[85vh] flex flex-col relative animate-fade-in" role="dialog" aria-modal="true">
    <div class="flex justify-between items-center pb-4 mb-4 border-b border-[#E1E9E3]">
      <div>
        <h3 id="classStudentsTitle" class="text-base font-medium text-[#000000]">Assigned Students</h3>
        <p id="classStudentsSubtitle" class="text-xs text-[#64746A] mt-0.5">Enrolled students and academic standing</p>
      </div>
      <button type="button" onclick="closeStudentsModal()" class="text-slate-400 hover:text-black min-h-[36px] min-w-[36px] flex items-center justify-center cursor-pointer">
        <i class="ph ph-x text-lg"></i>
      </button>
    </div>
    <div id="classStudentsList" class="flex-1 overflow-y-auto space-y-2 pr-1">
      <div class="text-xs text-slate-400 py-6 text-center">Loading student records...</div>
    </div>
    <div class="pt-4 mt-4 border-t border-[#E1E9E3] flex justify-end">
      <button type="button" onclick="closeStudentsModal()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 cursor-pointer min-h-[40px]">Close</button>
    </div>
  </div>
</div>"""

modals_replacement = """<!-- Edit / Add Class Modal (Modern Clean Responsive Dialog) -->
<div id="editClassModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" aria-labelledby="editClassModalTitle">
  <div class="w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[90vh] flex flex-col relative animate-fade-in">
    <!-- Header -->
    <div class="px-6 sm:px-7 pt-6 pb-5 border-b border-slate-100 flex items-start justify-between bg-slate-50/50">
      <div class="flex items-center gap-3">
        <span class="relative flex h-2.5 w-2.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#176B45]/40 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#176B45]"></span>
        </span>
        <div>
          <h3 id="editClassModalTitle" class="text-base font-semibold text-slate-900" style="font-family: 'Manrope', sans-serif;">Edit Class Information</h3>
          <p class="text-xs text-slate-500 mt-0.5">Update cohort metadata, educator assignment, and capacity limits</p>
        </div>
      </div>
      <button type="button" onclick="closeEditModal()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1.5 hover:bg-slate-100 transition-colors cursor-pointer min-h-[36px] min-w-[36px] flex items-center justify-center" aria-label="Close modal">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
      </button>
    </div>

    <!-- Modal Form Body -->
    <div class="flex-1 overflow-y-auto px-6 sm:px-7 py-5">
      <form id="editClassForm" onsubmit="saveClassChanges(event)">
        <input type="hidden" id="editClassId">

        <div class="space-y-4">
          <!-- Class Title -->
          <div>
            <label for="editClassName" class="block text-xs font-medium text-slate-700 mb-1.5">Class / Cohort Title <span class="text-rose-500">*</span></label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
              </span>
              <input id="editClassName" required type="text" class="w-full !pl-10 pr-4 py-2.5 text-xs bg-slate-50/50 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#176B45]/20 focus:border-[#176B45] transition-all min-h-[42px]" style="padding-left: 40px !important;" placeholder="e.g. Grade 10 - Advanced Biology">
            </div>
            <p class="text-[11px] text-slate-400 mt-1">Official registry name as displayed on student transcripts and report cards.</p>
          </div>

          <!-- Grade Level & Section Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="editClassGrade" class="block text-xs font-medium text-slate-700 mb-1.5">Grade Level <span class="text-rose-500">*</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                </span>
                <input id="editClassGrade" required type="text" class="w-full !pl-10 pr-4 py-2.5 text-xs bg-slate-50/50 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#176B45]/20 focus:border-[#176B45] transition-all min-h-[42px]" style="padding-left: 40px !important;" placeholder="e.g. Grade 10">
              </div>
            </div>

            <div>
              <label for="editClassSection" class="block text-xs font-medium text-slate-700 mb-1.5">Section / Track <span class="text-rose-500">*</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                </span>
                <input id="editClassSection" required type="text" class="w-full !pl-10 pr-4 py-2.5 text-xs bg-slate-50/50 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#176B45]/20 focus:border-[#176B45] transition-all min-h-[42px]" style="padding-left: 40px !important;" placeholder="e.g. Section A">
              </div>
            </div>
          </div>

          <!-- Homeroom Teacher Assignment -->
          <div>
            <label for="editClassTeacher" class="block text-xs font-medium text-slate-700 mb-1.5">Homeroom Educator <span class="text-rose-500">*</span></label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none z-10">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
              </span>
              <select id="editClassTeacher" class="w-full !pl-10 pr-10 py-2.5 text-xs bg-slate-50/50 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#176B45]/20 focus:border-[#176B45] transition-all appearance-none cursor-pointer min-h-[42px]" style="padding-left: 40px !important;">
                <option value="Dr. Sarah Jenkins">Dr. Sarah Jenkins (Mathematics)</option>
                <option value="Dr. Pov Sophea">Dr. Pov Sophea (Science)</option>
                <option value="Ms. Rin Lina">Ms. Rin Lina (English)</option>
                <option value="Mr. Heng Samnang">Mr. Heng Samnang (Humanities)</option>
                <option value="Dr. Alan Vance">Dr. Alan Vance (Mathematics)</option>
                <option value="Muthukumaran Pakkirisamy">Muthukumaran Pakkirisamy (Senior Faculty)</option>
              </select>
              <span class="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
              </span>
            </div>
          </div>

          <!-- Room Assignment & Student Capacity Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="editClassRoom" class="block text-xs font-medium text-slate-700 mb-1.5">Assigned Room <span class="text-rose-500">*</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                </span>
                <input id="editClassRoom" required type="text" class="w-full !pl-10 pr-4 py-2.5 text-xs bg-slate-50/50 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#176B45]/20 focus:border-[#176B45] transition-all min-h-[42px]" style="padding-left: 40px !important;" placeholder="e.g. Lab 402 / Building B">
              </div>
            </div>

            <div>
              <label for="editClassCount" class="block text-xs font-medium text-slate-700 mb-1.5">Student Capacity <span class="text-rose-500">*</span></label>
              <div class="relative">
                <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
                </span>
                <input id="editClassCount" min="1" max="60" required type="number" class="w-full !pl-10 pr-4 py-2.5 text-xs bg-slate-50/50 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#176B45]/20 focus:border-[#176B45] transition-all min-h-[42px]" style="padding-left: 40px !important;" placeholder="Max seat limit (e.g. 30)">
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Actions (Sticky inside card) -->
        <div class="flex flex-col-reverse sm:flex-row items-center justify-between gap-3 pt-5 mt-5 border-t border-slate-100">
          <div class="text-[11px] text-slate-400 hidden sm:block">
            Changes will take effect immediately across all student rosters.
          </div>
          <div class="flex items-center gap-2.5 w-full sm:w-auto">
            <button type="button" onclick="closeEditModal()" class="w-full sm:w-auto px-4 py-2.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 active:scale-95 transition-all cursor-pointer min-h-[40px]">
              Cancel
            </button>
            <button type="submit" id="saveClassBtn" class="w-full sm:w-auto px-5 py-2.5 text-xs font-medium text-white bg-[#176B45] hover:bg-[#125638] rounded-lg shadow-xs active:scale-95 transition-all cursor-pointer min-h-[40px] flex items-center justify-center gap-2">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
              <span>Save Changes</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- View Class Students Drawer / Modal (Modern Clean Responsive Dialog) -->
<div id="classStudentsModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-8 bg-slate-900/40 backdrop-blur-sm transition-opacity" role="dialog" aria-modal="true" aria-labelledby="classStudentsTitle">
  <div class="w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200/90 overflow-hidden max-h-[88vh] flex flex-col relative animate-fade-in">
    <!-- Header -->
    <div class="px-6 sm:px-7 pt-6 pb-5 border-b border-slate-100 flex items-start justify-between bg-slate-50/50">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-emerald-50 text-[#176B45] flex items-center justify-center shrink-0">
          <span class="material-symbols-outlined text-[20px]">groups</span>
        </div>
        <div>
          <h3 id="classStudentsTitle" class="text-base font-semibold text-slate-900" style="font-family: 'Manrope', sans-serif;">Assigned Students</h3>
          <p id="classStudentsSubtitle" class="text-xs text-slate-500 mt-0.5">Enrolled students and academic standing</p>
        </div>
      </div>
      <button type="button" onclick="closeStudentsModal()" class="text-slate-400 hover:text-slate-600 rounded-lg p-1.5 hover:bg-slate-100 transition-colors cursor-pointer min-h-[36px] min-w-[36px] flex items-center justify-center" aria-label="Close modal">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
      </button>
    </div>

    <!-- Student List -->
    <div id="classStudentsList" class="flex-1 overflow-y-auto px-6 sm:px-7 py-5 space-y-2.5">
      <div class="text-xs text-slate-400 py-8 text-center">Loading student records...</div>
    </div>

    <!-- Footer -->
    <div class="px-6 sm:px-7 py-4 border-t border-slate-100 bg-slate-50/40 flex items-center justify-between">
      <span class="text-xs text-slate-500" id="classStudentsCountText">Cohort student roster</span>
      <button type="button" onclick="closeStudentsModal()" class="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-all cursor-pointer min-h-[38px]">
        Done
      </button>
    </div>
  </div>
</div>"""

if modals_target in content:
    content = content.replace(modals_target, modals_replacement, 1)
    print("Modals replaced successfully!")
else:
    print("Error: modals_target not matched!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Finished patching principal-classes.html")

