import re

path = "pages/principal/principal-classes.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace metrics-telemetry and filtering-controls sections
old_pattern = r'<!-- BEGIN: Executive Telemetry Cards.*?<!-- END: Search & Filter Bar -->'

new_block = '''<!-- BEGIN: Executive Telemetry Cards (Golden Reference Image Design) -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" data-purpose="metrics-telemetry">
      <!-- Card 1: Credentialed Faculty & Classes -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E5E5E8] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Credentialed Classes</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#013623]" id="kpiTotalClasses">5</span>
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
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E5E5E8] flex flex-col justify-between">
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
            <span class="text-[#92243D] font-medium" id="kpiPendingCount">1 open seat</span>
          </div>
          <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
            <div id="clearanceProgressBar" class="bg-[#1e4d38] h-full rounded-full transition-all duration-500" style="width: 99.3%"></div>
            <div id="pendingProgressBar" class="bg-[#92243D] h-full rounded-full transition-all duration-500" style="width: 0.7%"></div>
          </div>
        </div>
      </div>

      <!-- Card 3: Pending Clearances with Corner Tint Accent -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E5E5E8] flex flex-col justify-between relative overflow-hidden">
        <div class="absolute right-0 top-0 w-24 h-24 bg-rose-500/10 rounded-bl-full pointer-events-none"></div>
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-[#92243D] block">Pending Clearances</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#92243D]" id="kpiPendingFaculty">2</span>
              <span class="inline-flex items-center gap-1 text-xs font-medium text-[#92243D] bg-rose-100/80 px-1.5 py-0.5 rounded">
                High Priority
              </span>
            </div>
          </div>
          <div class="w-10 h-10 rounded-lg bg-rose-100 text-[#92243D] flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[22px]">pending_actions</span>
          </div>
        </div>
        <div class="telemetry-pill mt-3">
          <span class="material-symbols-outlined text-[16px] text-[#92243D]">flag</span>
          <span class="truncate text-slate-700">Awaiting review: Math &amp; Humanities</span>
        </div>
      </div>

      <!-- Card 4: Registry Turnaround -->
      <div class="telemetry-card bg-white rounded-xl p-5 border border-[#E5E5E8] flex flex-col justify-between">
        <div class="flex items-start justify-between">
          <div>
            <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 block">Registry Turnaround</span>
            <div class="flex items-baseline gap-2 mt-1">
              <span class="text-3xl font-medium tracking-tight text-[#013623]">2.4<span class="text-lg font-normal text-slate-400"> hrs</span></span>
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
          <input id="classSearchInput" class="w-full !pl-11 pr-4 py-2 bg-slate-50 hover:bg-slate-100/70 focus:bg-white border border-slate-200 rounded-lg text-xs placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition-all min-h-[40px] classes-search-input" style="padding-left: 44px !important;" placeholder="Search cohort, homeroom educator, room, or campus..." type="text">
        </div>

        <!-- Filter Dropdowns & Status Badge (Clean horizontal flow, no awkward column stacking) -->
        <div class="flex flex-wrap sm:flex-nowrap items-center gap-2.5 shrink-0">
          <div class="relative flex-1 sm:flex-initial" style="min-width: 125px;">
            <select id="gradeFilter" class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-slate-200/90 bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#1e4d38] focus:border-[#1e4d38] cursor-pointer min-h-[40px] appearance-none" style="width: auto !important; min-width: 125px;">
              <option value="all">All Grades</option>
              <option value="10">Grade 10</option>
              <option value="11">Grade 11</option>
              <option value="12">Grade 12</option>
            </select>
            <span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400 text-[18px]">expand_more</span>
          </div>

          <div class="relative flex-1 sm:flex-initial" style="min-width: 135px;">
            <select id="campusFilter" class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-slate-200/90 bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#1e4d38] focus:border-[#1e4d38] cursor-pointer min-h-[40px] appearance-none" style="width: auto !important; min-width: 135px;">
              <option value="all">All Campuses</option>
              <option value="Sensok">Sensok Campus</option>
              <option value="TK">TK Campus</option>
            </select>
            <span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400 text-[18px]">expand_more</span>
          </div>

          <div class="relative flex-1 sm:flex-initial" style="min-width: 125px;">
            <select id="statusFilter" class="w-full text-xs py-2 pl-3 pr-8 rounded-lg border border-slate-200/90 bg-white text-slate-700 font-medium focus:ring-1 focus:ring-[#1e4d38] focus:border-[#1e4d38] cursor-pointer min-h-[40px] appearance-none" style="width: auto !important; min-width: 125px;">
              <option value="all">Status: All</option>
              <option value="active" selected="">Active Only</option>
              <option value="inactive">Inactive</option>
            </select>
            <span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400 text-[18px]">expand_more</span>
          </div>

          <span class="text-xs text-slate-300 px-0.5 hidden xl:inline">|</span>
          <span class="text-xs font-medium text-slate-500 whitespace-nowrap text-center sm:text-left pt-1 sm:pt-0" id="filterStatusCount">5 active cohorts</span>
        </div>
      </div>
    </section>
    <!-- END: Search & Filter Bar -->'''

match = re.search(old_pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + new_block + content[match.end():]
    print("Replaced telemetry and filter section!")
else:
    print("Pattern not found!")

# Also update updateKpis in script
old_kpis = r'function updateKpis\(\) \{.*?\n\}'
new_kpis = '''function updateKpis() {
  const totalClasses = allClasses.length;
  if (document.getElementById("kpiTotalClasses")) document.getElementById("kpiTotalClasses").textContent = totalClasses;
  if (document.getElementById("metricActiveCohortsSub")) document.getElementById("metricActiveCohortsSub").textContent = `Assigned across ${totalClasses} academic cohorts`;
  if (document.getElementById("filterStatusCount")) document.getElementById("filterStatusCount").textContent = `${totalClasses} active cohorts`;
  if (document.getElementById("mobileActiveBadge")) document.getElementById("mobileActiveBadge").textContent = `${totalClasses} Active Cohorts`;

  const totalStudents = allClasses.reduce((sum, c) => sum + (c.studentCount || 0), 0);
  const targetSeats = totalClasses * 30; // 150
  const rate = targetSeats > 0 ? ((totalStudents / targetSeats) * 100).toFixed(1) : "100";
  if (document.getElementById("kpiClearanceRate")) document.getElementById("kpiClearanceRate").textContent = `${rate}%`;
  if (document.getElementById("kpiClearedCount")) document.getElementById("kpiClearedCount").textContent = `${totalStudents} enrolled`;
  const openSeats = Math.max(0, targetSeats - totalStudents);
  if (document.getElementById("kpiPendingCount")) document.getElementById("kpiPendingCount").textContent = `${openSeats} open seat${openSeats === 1 ? '' : 's'}`;
  if (document.getElementById("clearanceProgressBar")) document.getElementById("clearanceProgressBar").style.width = `${rate}%`;
  if (document.getElementById("pendingProgressBar")) document.getElementById("pendingProgressBar").style.width = `${(100 - parseFloat(rate)).toFixed(1)}%`;

  if (document.getElementById("kpiPendingFaculty")) document.getElementById("kpiPendingFaculty").textContent = "2";
}'''

match_kpis = re.search(old_kpis, content, re.DOTALL)
if match_kpis:
    content = content[:match_kpis.start()] + new_kpis + content[match_kpis.end():]
    print("Replaced updateKpis function!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved principal-classes.html successfully!")

