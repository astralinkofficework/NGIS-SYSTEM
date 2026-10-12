import re

replacement_mobile_markup = '''<div class="student-mobile-view" id="studentMobileView">
  <div class="mobile-app-shell w-full min-h-screen flex flex-col bg-[#f4f7fa] text-[#182329] font-['Plus_Jakarta_Sans',sans-serif]">
    
    <!-- Top Floating Hero Card (Matching Reference Screen 1) -->
    <div class="pt-safe px-3.5 pt-3 pb-2 shrink-0">
      <div class="bg-gradient-to-br from-[#13829b] via-[#0e7490] to-[#155e75] text-white rounded-[28px] p-5 shadow-[0_12px_30px_-8px_rgba(19,130,155,0.4)] relative overflow-hidden">
        
        <!-- Top Row: Avatar + Greeting + Bell Notification -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-3">
            <div class="relative cursor-pointer shrink-0" onclick="window.location.href='student-profile.html'" title="View profile">
              <img src="../../assets/images/dashboard-student-portrait.jpg" alt="Nrinphouneta Hok" class="w-11 h-11 rounded-full object-cover border-2 border-white/80 shadow-md">
              <div class="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full bg-amber-400 border border-white flex items-center justify-center text-slate-900 shadow-sm" title="Active">
                <i class="ph-fill ph-star text-[8px]"></i>
              </div>
            </div>
            <div class="min-w-0">
              <p class="text-[11px] text-teal-100/90 font-medium tracking-wide">Good Day!</p>
              <h2 class="text-base font-bold text-white leading-tight truncate">Nrinphouneta Hok</h2>
            </div>
          </div>

          <!-- Notification Bell Button -->
          <button type="button" aria-label="Notifications" onclick="window.location.href='student-notifications.html'" class="w-10 h-10 rounded-full bg-white/15 hover:bg-white/25 active:scale-95 border border-white/25 flex items-center justify-center text-white relative transition-all shrink-0">
            <i class="ph-bold ph-bell text-lg"></i>
            <span class="absolute top-2 right-2 w-2 h-2 rounded-full bg-rose-500 ring-2 ring-[#0e7490]"></span>
          </button>
        </div>

        <!-- Academic Standing Eye Metric Row -->
        <div class="flex items-center justify-between text-teal-100 text-xs font-medium mb-1">
          <div class="flex items-center gap-1.5">
            <span class="tracking-wide">Academic Standing</span>
            <i class="ph-bold ph-eye text-sm text-teal-200"></i>
          </div>
          <span class="text-[11px] px-2 py-0.5 rounded-full bg-white/15 text-white font-semibold border border-white/20">Grade 10 · Term 2</span>
        </div>

        <!-- Large Hero Numbers -->
        <div class="flex items-baseline gap-2 mb-4">
          <span class="text-3xl font-extrabold tracking-tight text-white">3.85</span>
          <span class="text-sm font-semibold text-teal-100">GPA</span>
          <span class="text-xs text-emerald-300 font-bold bg-emerald-500/25 px-2.5 py-0.5 rounded-full border border-emerald-400/30 ml-1">92% Attendance</span>
        </div>

        <!-- Two Glassmorphic Pill Buttons Side by Side -->
        <div class="grid grid-cols-2 gap-2.5">
          <button type="button" onclick="window.openDigitalIdModal()" class="w-full py-2.5 px-3 rounded-2xl bg-white/15 hover:bg-white/25 active:scale-[0.98] border border-white/25 text-white font-bold text-xs flex items-center justify-center gap-2 backdrop-blur-md transition-all shadow-sm">
            <i class="ph-bold ph-arrow-down-left text-base text-teal-200"></i>
            <span>Digital ID</span>
          </button>
          <button type="button" onclick="window.location.href='student-grades.html'" class="w-full py-2.5 px-3 rounded-2xl bg-white/15 hover:bg-white/25 active:scale-[0.98] border border-white/25 text-white font-bold text-xs flex items-center justify-center gap-2 backdrop-blur-md transition-all shadow-sm">
            <i class="ph-bold ph-arrow-up-right text-base text-teal-200"></i>
            <span>Report Card</span>
          </button>
        </div>

      </div>
    </div>

    <!-- Main Content Container with Natural Document Scroll -->
    <main class="w-full max-w-3xl mx-auto px-3.5 space-y-3.5 pb-28 flex-1">

      <!-- Notice Banner (Matching Upgrade Banner in Reference) -->
      <div onclick="window.location.href='student-announcements.html'" class="bg-white border border-slate-200/90 rounded-2xl p-3 flex items-center justify-between shadow-sm hover:border-teal-500/30 active:scale-[0.99] transition-all cursor-pointer">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-9 h-9 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center shrink-0 border border-amber-200/60 shadow-xs">
            <i class="ph-bold ph-trophy text-lg"></i>
          </div>
          <div class="min-w-0">
            <h4 class="text-xs font-bold text-slate-800 truncate leading-tight">Annual Sports Carnival 2026</h4>
            <p class="text-[11px] text-slate-500 truncate mt-0.5">Registration closes this Friday · Hall A</p>
          </div>
        </div>
        <i class="ph-bold ph-caret-right text-slate-400 text-sm shrink-0 ml-2"></i>
      </div>

      <!-- Quick Actions: 4 Soft Pastel Rounded Square Tiles (Matching Reference) -->
      <section data-purpose="quick-actions">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-600 mb-2 px-0.5">Quick Actions</h3>
        <div class="grid grid-cols-4 gap-2.5">
          <!-- Grades -->
          <div onclick="window.location.href='student-grades.html'" class="flex flex-col items-center justify-center p-3 rounded-2xl bg-[#e8f5f6] hover:bg-[#d8eef0] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-white/90 text-[#13829b] flex items-center justify-center mb-1.5 shadow-xs">
              <i class="ph-bold ph-chart-line-up text-lg"></i>
            </div>
            <span class="text-[11px] font-bold text-[#13829b] text-center leading-tight">Grades</span>
          </div>
          <!-- Tasks -->
          <div onclick="window.location.href='student-assignments.html'" class="flex flex-col items-center justify-center p-3 rounded-2xl bg-[#fef3c7] hover:bg-[#fde68a] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-white/90 text-[#d97706] flex items-center justify-center mb-1.5 shadow-xs">
              <i class="ph-bold ph-notebook text-lg"></i>
            </div>
            <span class="text-[11px] font-bold text-[#b45309] text-center leading-tight">Tasks</span>
          </div>
          <!-- Classes -->
          <div onclick="window.location.href='student-timetable.html'" class="flex flex-col items-center justify-center p-3 rounded-2xl bg-[#ecfdf5] hover:bg-[#d1fae5] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-white/90 text-[#059669] flex items-center justify-center mb-1.5 shadow-xs">
              <i class="ph-bold ph-calendar-check text-lg"></i>
            </div>
            <span class="text-[11px] font-bold text-[#047857] text-center leading-tight">Classes</span>
          </div>
          <!-- Reports -->
          <div onclick="window.location.href='student-profile.html'" class="flex flex-col items-center justify-center p-3 rounded-2xl bg-[#f1f5f9] hover:bg-[#e2e8f0] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-white/90 text-[#475569] flex items-center justify-center mb-1.5 shadow-xs">
              <i class="ph-bold ph-file-text text-lg"></i>
            </div>
            <span class="text-[11px] font-bold text-[#334155] text-center leading-tight">Reports</span>
          </div>
        </div>
      </section>

      <!-- Attendance & Statistics (Matching Reference Screen 2) -->
      <section class="bg-white border border-slate-200/90 rounded-2xl p-4 shadow-sm space-y-3" data-purpose="attendance-statistics">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-[#13829b]"></span>
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700">Attendance &amp; Statistics</h3>
          </div>
          <span class="text-xs font-bold text-[#13829b] bg-teal-50 px-2 py-0.5 rounded-full">Term 2</span>
        </div>

        <!-- Gauge Summary -->
        <div class="flex items-center gap-4 py-1">
          <div class="relative w-16 h-16 shrink-0 flex items-center justify-center">
            <svg class="w-16 h-16 transform -rotate-90" viewBox="0 0 36 36">
              <path class="text-slate-100" stroke-width="3.5" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path class="text-[#13829b]" stroke-dasharray="92, 100" stroke-width="3.5" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <span class="absolute text-xs font-extrabold text-slate-800">92%</span>
          </div>
          <div class="flex-1 space-y-1 text-xs">
            <div class="flex items-center justify-between">
              <span class="flex items-center gap-1.5 text-slate-600"><span class="w-2 h-2 rounded-full bg-[#13829b]"></span>Present</span>
              <span class="font-bold text-slate-800">22 days</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="flex items-center gap-1.5 text-slate-600"><span class="w-2 h-2 rounded-full bg-rose-500"></span>Absent</span>
              <span class="font-bold text-slate-800">2 days</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="flex items-center gap-1.5 text-slate-600"><span class="w-2 h-2 rounded-full bg-amber-500"></span>Late</span>
              <span class="font-bold text-slate-800">1 day</span>
            </div>
          </div>
        </div>

        <!-- Breakdown List Items with Chevrons -->
        <div class="space-y-1 pt-1 border-t border-slate-100">
          <div onclick="window.location.href='student-attendance.html'" class="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-teal-50 text-[#13829b] flex items-center justify-center">
                <i class="ph-bold ph-check-circle text-base"></i>
              </div>
              <div>
                <p class="text-xs font-bold text-slate-800 leading-tight">Classes Attended</p>
                <p class="text-[10px] text-slate-500">44 of 48 sessions on time</p>
              </div>
            </div>
            <i class="ph-bold ph-caret-right text-slate-400 text-xs"></i>
          </div>

          <div onclick="window.location.href='student-timetable.html'" class="flex items-center justify-between p-2 rounded-xl hover:bg-slate-50 transition-colors cursor-pointer">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
                <i class="ph-bold ph-calendar-check text-base"></i>
              </div>
              <div>
                <p class="text-xs font-bold text-slate-800 leading-tight">Next Class: Physics Lab</p>
                <p class="text-[10px] text-slate-500">Tomorrow · 09:00 AM · Hall A</p>
              </div>
            </div>
            <i class="ph-bold ph-caret-right text-slate-400 text-xs"></i>
          </div>
        </div>
      </section>

      <!-- Recent Deadlines & Tasks (Matching "Recent Transactions" in Reference Screen 1) -->
      <section data-purpose="recent-tasks">
        <div class="flex items-center justify-between mb-2 px-0.5">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-600">Recent Deadlines &amp; Tasks</h3>
          <div class="flex items-center gap-2">
            <button type="button" aria-label="Filter" class="w-7 h-7 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-xs transition-colors">
              <i class="ph-bold ph-funnel text-xs"></i>
            </button>
            <a href="student-assignments.html" class="text-xs font-bold text-[#13829b] hover:underline">View All</a>
          </div>
        </div>

        <div class="space-y-2">
          <!-- Task 1: History Essay (Urgent) -->
          <div class="bg-white border border-slate-200/90 rounded-2xl p-3 shadow-sm flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center shrink-0 border border-rose-100">
                <i class="ph-bold ph-hourglass-high text-lg"></i>
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-2">
                  <h4 class="text-xs font-bold text-slate-800 truncate">History Essay Draft</h4>
                  <span class="text-[9px] font-bold text-rose-700 bg-rose-100 px-1.5 py-0.2 rounded">Urgent</span>
                </div>
                <p class="text-[11px] text-slate-500 truncate mt-0.5">Due Jun 27, 11:59 PM · Mr. Sophea</p>
              </div>
            </div>
            <button type="button" onclick="window.location.href='student-assignments.html'" class="px-3 py-1.5 bg-[#006c49] hover:bg-[#005237] text-white text-xs font-bold rounded-xl shrink-0 transition-colors">
              Submit
            </button>
          </div>

          <!-- Task 2: Math Problem Set (Soon) -->
          <div class="bg-white border border-slate-200/90 rounded-2xl p-3 shadow-sm flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center shrink-0 border border-amber-100">
                <i class="ph-bold ph-math-operations text-lg"></i>
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-2">
                  <h4 class="text-xs font-bold text-slate-800 truncate">Math Problem Set 4</h4>
                  <span class="text-[9px] font-bold text-amber-700 bg-amber-100 px-1.5 py-0.2 rounded">Soon</span>
                </div>
                <p class="text-[11px] text-slate-500 truncate mt-0.5">Due Jun 29, 11:59 PM</p>
              </div>
            </div>
            <button type="button" onclick="window.location.href='student-assignments.html'" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl shrink-0 transition-colors">
              View
            </button>
          </div>

          <!-- Task 3: Chemistry Lab Report (Graded) -->
          <div class="bg-white border border-slate-200/90 rounded-2xl p-3 shadow-sm flex items-center justify-between gap-3">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0 border border-emerald-100">
                <i class="ph-bold ph-flask text-lg"></i>
              </div>
              <div class="min-w-0">
                <div class="flex items-center gap-2">
                  <h4 class="text-xs font-bold text-slate-800 truncate">Chemistry Lab Report</h4>
                  <span class="text-[9px] font-bold text-emerald-700 bg-emerald-100 px-1.5 py-0.2 rounded">Graded</span>
                </div>
                <p class="text-[11px] text-slate-500 truncate mt-0.5">Submitted · Ms. Kiry Sokha</p>
              </div>
            </div>
            <span class="text-xs font-extrabold text-emerald-600 bg-emerald-50 border border-emerald-200/60 px-2.5 py-1 rounded-xl shrink-0">
              88%
            </span>
          </div>
        </div>
      </section>

    </main>

    <!-- Professional Fixed Bottom Navigation Dock (5 Destinations) -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-md border-t border-slate-200/90 shadow-[0_-4px_16px_rgba(23,33,47,0.06)] z-40" data-purpose="bottom-navigation-bar">
      <div class="max-w-md mx-auto px-4 py-1.5 flex items-center justify-between pb-safe">
        <!-- Home (Active) -->
        <a href="student.html" class="flex flex-col items-center justify-center py-1 px-2.5 rounded-xl bg-teal-50 text-[#13829b] transition-all min-w-[48px] min-h-[44px]">
          <i class="ph-fill ph-house-simple text-xl"></i>
          <span class="text-[10px] font-bold mt-0.5">Home</span>
        </a>
        <!-- Classes / Timetable -->
        <a href="student-timetable.html" class="flex flex-col items-center justify-center py-1 px-2.5 text-slate-500 hover:text-slate-800 transition-all min-w-[48px] min-h-[44px]">
          <i class="ph-bold ph-squares-four text-xl"></i>
          <span class="text-[10px] font-medium mt-0.5">Classes</span>
        </a>
        <!-- Central Chat Action -->
        <div class="flex items-center justify-center">
          <a href="student-chat.html" aria-label="Quick Chat" class="w-10 h-10 rounded-full bg-[#0e6d82] text-white flex items-center justify-center shadow-[0_4px_12px_rgba(14,116,144,0.28)] active:scale-95 transition-transform" title="Student Chat">
            <i class="ph-fill ph-chat-circle-dots text-xl"></i>
          </a>
        </div>
        <!-- Alerts / Notifications -->
        <a href="student-notifications.html" class="flex flex-col items-center justify-center py-1 px-2.5 text-slate-500 hover:text-slate-800 relative transition-all min-w-[48px] min-h-[44px]">
          <div class="relative">
            <i class="ph-bold ph-bell text-xl"></i>
            <span class="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-rose-500"></span>
          </div>
          <span class="text-[10px] font-medium mt-0.5">Alerts</span>
        </a>
        <!-- Profile -->
        <a href="student-profile.html" class="flex flex-col items-center justify-center py-1 px-2.5 text-slate-500 hover:text-slate-800 transition-all min-w-[48px] min-h-[44px]">
          <i class="ph-bold ph-user text-xl"></i>
          <span class="text-[10px] font-medium mt-0.5">Profile</span>
        </a>
      </div>
    </nav>

  </div>
</div>'''

filepath = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace from `<div class="student-mobile-view"` to `</div>\n</div>\n\n</div><!-- /.main -->`
pattern = r'<div class="student-mobile-view" id="studentMobileView">.*?</div>\s*</div>\s*(?=\n</div><!-- /.main -->)'
new_content, count = re.subn(pattern, replacement_mobile_markup, content, flags=re.DOTALL)

if count == 1:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Mobile view replaced accurately!")
else:
    print(f"FAILED: Pattern match count was {count}")
