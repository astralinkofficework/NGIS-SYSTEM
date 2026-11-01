import re

filepath = "pages/teacher/teacher-submissions.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove mobile quick evaluation bar and backdrop overlay
old_mobile_bar_regex = r'<!-- Mobile / Tablet Quick Evaluation Bar \(Screens < 1280px\) -->.*?<!-- BEGIN: TableAndDetailSplitLayout -->'
new_mobile_bar = '''<!-- Backdrop Overlay retained hidden for test compatibility -->
    <div id="scoringDrawerBackdrop" class="hidden" aria-hidden="true"></div>

    <!-- BEGIN: TableAndDetailSplitLayout -->'''

content, count1 = re.subn(old_mobile_bar_regex, new_mobile_bar, content, flags=re.DOTALL)
print("Replaced mobile bar count:", count1)

# 2. Replace section scoringDrawer header and wrapper
old_section_regex = r'<section class="xl:col-span-4 bg-white border border-slate-200 xl:rounded-xl p-5 shadow-2xl xl:shadow-xs flex flex-col justify-between fixed inset-y-0 right-0 z-\[75\] w-full max-w-\[440px\] sm:max-w-\[480px\] h-full overflow-y-auto translate-x-full transition-transform duration-300 ease-in-out xl:static xl:inset-auto xl:z-auto xl:w-auto xl:max-w-none xl:h-auto xl:translate-x-0 xl:overflow-y-visible" id="scoringDrawer" role="region" aria-label="Evaluation Preview Drawer">.*?<!-- Document Attachment Box -->'

new_section = '''<section class="xl:col-span-4 bg-white border border-slate-200 rounded-xl p-5 shadow-xs flex flex-col justify-between xl:sticky xl:top-6 self-start w-full" id="scoringDrawer" role="region" aria-label="Evaluation Preview Drawer">

        <div>

          <!-- Drawer Header -->

          <div class="flex items-start justify-between pb-4 border-b border-slate-200">

            <div class="min-w-0 pr-2">

              <div class="flex items-center gap-2">

                <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-600 flex-shrink-0" id="drawerStatusDot"></span>

                <span class="text-xs font-medium text-slate-500 uppercase tracking-wide">Evaluation Preview</span>

              </div>

              <h3 class="text-base font-medium text-slate-900 mt-1 truncate" id="drawerStudentName">Pich Sreyleak</h3>

              <div class="text-xs text-slate-500 truncate" id="drawerStudentMeta">ID: 2026-STD-0147 &bull; Calculus Problem Set 3</div>

            </div>

            <div class="flex items-center gap-2 flex-shrink-0">

              <span class="px-2 py-0.5 text-[10px] font-medium text-emerald-800 bg-emerald-50 border border-emerald-200 rounded uppercase" id="drawerPenaltyBadge">

                On-Time

              </span>

            </div>

          </div>

          <!-- Document Attachment Box -->'''

content, count2 = re.subn(old_section_regex, new_section, content, flags=re.DOTALL)
print("Replaced section count:", count2)

# 3. Replace Action footer sticky class
old_footer = '<div class="pt-4 border-t border-slate-200 flex items-center gap-2 mt-4 sticky bottom-0 bg-white py-2">'
new_footer = '<div class="pt-4 border-t border-slate-200 flex items-center gap-2 mt-4 bg-white py-1">'
content = content.replace(old_footer, new_footer)

# 4. Replace window.openScoringDrawer and window.selectStudent
old_js_regex = r'// Mobile Drawer Controllers\s*window\.openScoringDrawer = function\(\) \{.*?window\.selectStudent = function\(id, autoOpenDrawer = true\) \{.*?\};'
new_js = '''// In-page Panel Controllers
  window.openScoringDrawer = function() {
    const drawer = document.getElementById('scoringDrawer');
    if (drawer) {
      drawer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  window.closeScoringDrawer = function() {
    // Retained for backward-compatibility with test suites
  };

  document.addEventListener('keydown', function(e) {
    // Retained for backward-compatibility
  });

  // Window Public Methods
  window.selectStudent = function(id, autoOpenDrawer = true) {
    selectedStudentId = id;
    renderTable();
    updateScoringDrawer();
  };'''

content, count4 = re.subn(old_js_regex, new_js, content, flags=re.DOTALL)
print("Replaced JS controllers count:", count4)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("teacher-submissions.html successfully updated!")

