# Script to cleanly inject School Operations & System Control into pages/admin/admin.html

control_section_html = '''
        <!-- ═══════════════════════════════════════════════════════════════
             SECTION A–H: SCHOOL OPERATIONS & IT CONTROL CENTER (MASTER MVP)
             ═══════════════════════════════════════════════════════════════ -->
        <section class="ops-control-section anim-up space-y-6 mb-8" id="secOpsControl">
          
          <!-- SECTION A — HEADER -->
          <div class="bg-white border border-[#E1E9E3] rounded-2xl p-4 sm:p-5 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-11 h-11 rounded-2xl bg-emerald-50 text-emerald-800 border border-emerald-200/80 flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-2xl">tune</span>
              </div>
              <div>
                <div class="flex items-center gap-2 flex-wrap">
                  <h2 class="text-base font-medium text-slate-900">School Operations &amp; System Control</h2>
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-200">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse"></span>Live Monitoring Active
                  </span>
                </div>
                <p class="text-xs text-slate-500 font-normal mt-0.5">
                  Monitor academic workflows, system health, missing records, and operational issues across the school.
                </p>
              </div>
            </div>

            <!-- Filters & Actions -->
            <div class="flex items-center gap-2.5 flex-wrap shrink-0">
              <div class="flex items-center gap-1.5 text-xs text-slate-600">
                <label for="opsCampusFilter" class="font-normal text-slate-400">Campus:</label>
                <select id="opsCampusFilter" class="px-2.5 py-1.5 rounded-xl border border-[#E1E9E3] bg-white text-xs font-normal text-slate-700 focus:outline-none">
                  <option value="CMP-01">Tuol Kork Main Campus</option>
                  <option value="CMP-02">Chamkarmon High School Branch</option>
                  <option value="CMP-03">STEM &amp; Robotics Hub</option>
                </select>
              </div>

              <button type="button" id="btnOpsRefresh" onclick="OPS_CONTROL.refresh()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#E1E9E3] bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium transition shadow-xs">
                <span class="material-symbols-outlined text-[16px]">refresh</span>
                <span>Refresh</span>
              </button>
            </div>
          </div>

          <!-- SECTION B — OPERATIONAL SUMMARY (5 KPI CARDS) -->
          <div class="ops-kpi-grid">
            <div class="ops-kpi-card">
              <div class="flex items-center justify-between text-slate-500">
                <span class="text-xs font-medium text-slate-600">Modules Operational</span>
                <span class="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
                  <span class="material-symbols-outlined text-[16px]">check_circle</span>
                </span>
              </div>
              <div class="mt-2">
                <span id="kpiOpsModules" class="ops-kpi-val text-emerald-700">2</span>
                <span class="text-[11px] text-slate-400 font-normal ml-1">of 6 core suites</span>
              </div>
              <p class="ops-kpi-label">Lessons &amp; Core Engine verified</p>
            </div>

            <div class="ops-kpi-card">
              <div class="flex items-center justify-between text-slate-500">
                <span class="text-xs font-medium text-slate-600">Workflows Incomplete</span>
                <span class="w-7 h-7 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center">
                  <span class="material-symbols-outlined text-[16px]">pending_actions</span>
                </span>
              </div>
              <div class="mt-2">
                <span id="kpiOpsIncomplete" class="ops-kpi-val text-amber-700">4</span>
                <span class="text-[11px] text-slate-400 font-normal ml-1">in progress</span>
              </div>
              <p class="ops-kpi-label">Schedules, grades &amp; exam setup</p>
            </div>

            <div class="ops-kpi-card">
              <div class="flex items-center justify-between text-slate-500">
                <span class="text-xs font-medium text-slate-600">Records Missing</span>
                <span class="w-7 h-7 rounded-lg bg-red-50 text-red-700 flex items-center justify-center">
                  <span class="material-symbols-outlined text-[16px]">content_paste_off</span>
                </span>
              </div>
              <div class="mt-2">
                <span id="kpiOpsMissing" class="ops-kpi-val text-slate-900">438</span>
                <span class="text-[11px] text-slate-400 font-normal ml-1">entries</span>
              </div>
              <p class="ops-kpi-label">Unplaced periods &amp; attendance</p>
            </div>

            <div class="ops-kpi-card">
              <div class="flex items-center justify-between text-slate-500">
                <span class="text-xs font-medium text-slate-600">Errors Detected</span>
                <span class="w-7 h-7 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center">
                  <span class="material-symbols-outlined text-[16px]">bug_report</span>
                </span>
              </div>
              <div class="mt-2">
                <span id="kpiOpsErrors" class="ops-kpi-val text-slate-700">2</span>
                <span class="text-[11px] text-slate-400 font-normal ml-1">warnings</span>
              </div>
              <p class="ops-kpi-label">0 critical · 2 validation warnings</p>
            </div>

            <div class="ops-kpi-card">
              <div class="flex items-center justify-between text-slate-500">
                <span class="text-xs font-medium text-slate-600">Pending Reviews</span>
                <span class="w-7 h-7 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center">
                  <span class="material-symbols-outlined text-[16px]">rate_review</span>
                </span>
              </div>
              <div class="mt-2">
                <span id="kpiOpsReviews" class="ops-kpi-val text-purple-700">5</span>
                <span class="text-[11px] text-slate-400 font-normal ml-1">submissions</span>
              </div>
              <p class="ops-kpi-label">Awaiting Principal &amp; Director approval</p>
            </div>
          </div>

          <!-- SECTION C — SIX MONITORING CARDS (3x2 GRID) -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-slate-900 flex items-center gap-2">
                  <span>Primary Operational Monitoring Cards</span>
                  <span class="text-xs text-slate-400 font-normal">(Restored 6-Module Suite)</span>
                </h3>
                <p class="text-xs text-slate-500 font-normal mt-0.5">Click any card to inspect live audit entries, responsible educators, and follow-up tools.</p>
              </div>
              <span class="text-xs text-slate-400 font-normal hidden sm:inline-block">3 Columns × 2 Rows</span>
            </div>

            <div id="opsMonitoringCardsContainer" class="ops-cards-grid">
              <div class="p-8 text-center text-slate-400 text-xs font-normal col-span-3 bg-white rounded-2xl border border-[#E1E9E3]">
                <span class="material-symbols-outlined text-2xl animate-spin mb-1">sync</span>
                <p>Auditing school operations across all modules...</p>
              </div>
            </div>
          </div>

          <!-- SECTION D — WORKFLOW STATUS PIPELINE -->
          <div class="bg-white border border-[#E1E9E3] rounded-2xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-[#E1E9E3]">
              <div>
                <h3 class="text-base font-medium text-slate-900 flex items-center gap-2">
                  <span>System-Wide Workflow &amp; Dependency Architecture</span>
                </h3>
                <p class="text-xs text-slate-500 font-normal mt-0.5">
                  Real-time multi-stage process dependencies. Upstream blockers automatically flag dependent downstream workflows.
                </p>
              </div>
              <span class="text-xs text-emerald-700 font-medium hidden sm:inline-block">Root-Cause Tracing Active</span>
            </div>

            <div id="opsWorkflowPipelineContainer" class="flex flex-col xl:flex-row gap-3 items-stretch overflow-x-auto pb-1"></div>
          </div>

          <!-- SECTION E — ISSUES REQUIRING ATTENTION -->
          <div class="bg-white border border-[#E1E9E3] rounded-2xl p-5 shadow-xs space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-[#E1E9E3]">
              <div>
                <h3 class="text-base font-medium text-slate-900 flex items-center gap-2">
                  <span>System-Wide Issues &amp; Missing Work Registry</span>
                </h3>
                <p class="text-xs text-slate-500 font-normal mt-0.5">
                  Consolidated operational registry of missing data, workflow blockers, and validation notices across the institution.
                </p>
              </div>

              <div class="flex items-center gap-2 flex-wrap">
                <select onchange="OPS_CONTROL.setIssueCategory(this.value)" class="px-2.5 py-1.5 text-xs rounded-xl border border-[#E1E9E3] bg-white text-slate-700 focus:outline-none">
                  <option value="all">All Categories</option>
                  <option value="Missing Data">Missing Data</option>
                  <option value="Incomplete Workflow">Incomplete Workflow</option>
                  <option value="Validation Warning">Validation Warning</option>
                </select>
                <select onchange="OPS_CONTROL.setIssueSeverity(this.value)" class="px-2.5 py-1.5 text-xs rounded-xl border border-[#E1E9E3] bg-white text-slate-700 focus:outline-none">
                  <option value="all">All Severities</option>
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>
            </div>

            <div id="opsIssuesTableBody"></div>
          </div>

          <!-- SECTION F & G — STAFF FOLLOW-UP & SYSTEM HEALTH -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white border border-[#E1E9E3] rounded-2xl p-5 shadow-xs space-y-3">
              <div class="flex items-center justify-between pb-2 border-b border-[#E1E9E3]">
                <h3 class="text-sm font-medium text-slate-900 flex items-center gap-1.5">
                  <span class="material-symbols-outlined text-emerald-700 text-[18px]">co_present</span>
                  <span>Staff Follow-up &amp; Ownership</span>
                </h3>
                <span class="text-[11px] text-slate-400 font-normal">Active Responsibilities</span>
              </div>
              <p class="text-xs text-slate-500 font-normal">Follow up with key academic and administrative staff responsible for pending operational workflows.</p>
              <div id="opsStaffFollowupContainer" class="pt-2"></div>
            </div>

            <div class="bg-white border border-[#E1E9E3] rounded-2xl p-5 shadow-xs space-y-3">
              <div class="flex items-center justify-between pb-2 border-b border-[#E1E9E3]">
                <h3 class="text-sm font-medium text-slate-900 flex items-center gap-1.5">
                  <span class="material-symbols-outlined text-slate-700 text-[18px]">dns</span>
                  <span>Technical System Health Probes</span>
                </h3>
                <span class="text-[11px] text-emerald-700 font-medium">All Probes Passing</span>
              </div>
              <p class="text-xs text-slate-500 font-normal">Live health checks for backend services, database stores, file storage, and notification dispatchers.</p>
              <div id="opsSystemHealthContainer" class="pt-2"></div>
            </div>
          </div>

          <!-- SECTION H — AUDIT ACTIVITY LOG -->
          <div class="bg-white border border-[#E1E9E3] rounded-2xl p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-[#E1E9E3]">
              <h3 class="text-sm font-medium text-slate-900 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-slate-700 text-[18px]">history</span>
                <span>Cross-Module Audit Activity Log</span>
              </h3>
              <span class="text-[11px] text-slate-400 font-normal">Chronological Records</span>
            </div>
            <p class="text-xs text-slate-500 font-normal">Real event journal tracking administrative configurations, schedule updates, grade approvals, and reminder dispatches.</p>
            <div id="opsAuditTimelineContainer" class="pt-2"></div>
          </div>

        </section>
'''

modals_html = '''
<!-- ── MODULE AUDIT MODAL (OPENED BY CARDS) ── -->
<div id="opsAuditModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-50 hidden flex items-center justify-center p-4">
  <div class="bg-white rounded-2xl shadow-xl border border-[#E1E9E3] w-full max-w-2xl overflow-hidden animate-in fade-in zoom-in duration-200 flex flex-col max-h-[85vh]">
    <div class="flex items-center justify-between px-6 py-4 border-b border-[#E1E9E3] bg-slate-50/70 shrink-0">
      <div>
        <h3 id="opsAuditModalTitle" class="text-sm font-medium text-slate-900">Module Audit</h3>
        <p id="opsAuditModalSubtitle" class="text-[11px] text-slate-500 font-normal mt-0.5">Authoritative records audit breakdown</p>
      </div>
      <button type="button" onclick="OPS_CONTROL.closeAuditModal()" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200/50 transition">
        <span class="material-symbols-outlined text-[18px]">close</span>
      </button>
    </div>
    <div id="opsAuditModalBody" class="p-6 overflow-y-auto space-y-4 text-xs"></div>
    <div class="px-6 py-3.5 bg-slate-50/70 border-t border-[#E1E9E3] flex items-center justify-end shrink-0">
      <button type="button" onclick="OPS_CONTROL.closeAuditModal()" class="px-4 py-2 rounded-xl border border-[#E1E9E3] bg-white hover:bg-slate-100 text-slate-700 text-xs font-medium transition">
        Close Audit
      </button>
    </div>
  </div>
</div>

<!-- ── SEND REMINDER MODAL ── -->
<div id="opsReminderModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-50 hidden flex items-center justify-center p-4">
  <div class="bg-white rounded-2xl shadow-xl border border-[#E1E9E3] w-full max-w-lg overflow-hidden animate-in fade-in zoom-in duration-200">
    <div class="flex items-center justify-between px-6 py-4 border-b border-[#E1E9E3] bg-slate-50/70">
      <div class="flex items-center gap-2">
        <span class="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-800 flex items-center justify-center">
          <span class="material-symbols-outlined text-[18px]">send</span>
        </span>
        <div>
          <h3 class="text-sm font-medium text-slate-900">Send Operational Reminder</h3>
          <p class="text-[11px] text-slate-500 font-normal">Dispatches an official in-app notice to responsible staff</p>
        </div>
      </div>
      <button type="button" onclick="OPS_CONTROL.closeReminderModal()" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200/50 transition">
        <span class="material-symbols-outlined text-[18px]">close</span>
      </button>
    </div>
    <input type="hidden" id="opsRemindRecipientName" value="">
    <input type="hidden" id="opsRemindRecipientRole" value="">
    <input type="hidden" id="opsRemindRecipientEmail" value="">
    <div class="p-6 space-y-4 text-xs">
      <div class="p-3.5 rounded-xl border border-[#E1E9E3] bg-slate-50/80 space-y-1.5">
        <div class="flex items-center justify-between">
          <span class="text-[11px] text-slate-400 font-normal">Workflow Task</span>
          <span class="text-[11px] text-slate-500 font-normal">Tuol Kork Campus · 2026–2027</span>
        </div>
        <h4 id="opsModalTaskDisplay" class="text-xs font-medium text-slate-800">Operational Task</h4>
        <div class="flex items-center justify-between text-[11px] pt-1 border-t border-slate-200/70">
          <span class="text-slate-500 font-normal">Recipient:</span>
          <span id="opsModalRecipientDisplay" class="text-emerald-800 font-medium">Staff Member</span>
        </div>
      </div>
      <div class="space-y-1">
        <label for="opsRemindDeadlineInput" class="block font-medium text-slate-700 text-xs">Target Completion Date</label>
        <input type="date" id="opsRemindDeadlineInput" class="w-full px-3 py-2 rounded-xl border border-[#E1E9E3] text-xs text-slate-800 focus:outline-none focus:border-emerald-600 focus:ring-1 focus:ring-emerald-600 font-normal">
      </div>
      <div class="space-y-1">
        <label for="opsRemindMessageText" class="block font-medium text-slate-700 text-xs">Official In-App Message</label>
        <textarea id="opsRemindMessageText" rows="4" class="w-full p-3 rounded-xl border border-[#E1E9E3] text-xs text-slate-800 focus:outline-none focus:border-emerald-600 focus:ring-1 focus:ring-emerald-600 font-normal leading-relaxed"></textarea>
      </div>
    </div>
    <div class="px-6 py-4 bg-slate-50/70 border-t border-[#E1E9E3] flex items-center justify-end gap-2.5">
      <button type="button" onclick="OPS_CONTROL.closeReminderModal()" class="px-4 py-2 rounded-xl border border-[#E1E9E3] bg-white hover:bg-slate-100 text-slate-700 text-xs font-medium transition">
        Cancel
      </button>
      <button type="button" id="btnOpsSubmitReminder" onclick="OPS_CONTROL.submitReminder()" class="px-4 py-2 rounded-xl bg-[#176B45] hover:bg-[#145939] text-white text-xs font-medium transition shadow-sm flex items-center gap-1.5">
        <span class="material-symbols-outlined text-[15px]">send</span>
        <span>Send In-App Reminder</span>
      </button>
    </div>
  </div>
</div>
<script src="../../assets/js/admin-operations-control.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {
    if (window.OPS_CONTROL) {
      window.OPS_CONTROL.init();
    }
  });
</script>
'''

with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add css in head
if 'admin-operations-control.css' not in content:
    content = content.replace(
        '<link rel="stylesheet" href="../../assets/css/interactions.css?v=3.2">',
        '<link rel="stylesheet" href="../../assets/css/interactions.css?v=3.2">\n<link rel="stylesheet" href="../../assets/css/admin-operations-control.css?v=1.0">'
    )

# 2. Add section into paneDashboard
target_pane = '<div class="sk-tab-pane" id="paneDashboard">\n'
if 'secOpsControl' not in content and target_pane in content:
    content = content.replace(target_pane, target_pane + control_section_html + '\n')
elif 'secOpsControl' not in content:
    # try with different whitespace
    idx = content.find('id="paneDashboard"')
    if idx != -1:
        end_tag = content.find('>', idx) + 1
        content = content[:end_tag] + '\n' + control_section_html + content[end_tag:]

# 3. Add modals and scripts before </body>
if 'opsAuditModal' not in content:
    content = content.replace('</body>', modals_html + '\n</body>')

with open('pages/admin/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected School Operations & IT Control Center into pages/admin/admin.html successfully!")

