with open('pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update main container padding for bottom dock clearance
text = text.replace('w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6',
                    'w-full max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-4 sm:pt-6 pb-28 sm:pb-32 lg:pb-16')

# 2. Replace 4-KPI Metric Strip
start_marker = '<!-- 4-KPI Metric Strip -->'
next_marker = '<!-- Main Content Layout (70% Left Primary / 30% Right Rail) -->'

idx_start = text.find(start_marker)
idx_end = text.find(next_marker)

print(f'Start: {idx_start}, End: {idx_end}')

new_kpi = '''<!-- 4-KPI Metric Strip (Clean Responsive Hierarchy) -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 sm:gap-space-md">
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
          <div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[18px] sm:text-[24px]">functions</span>
          </div>
          <div class="flex flex-col min-w-0 w-full">
            <span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Discipline</span>
            <span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">Mathematics</span>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
          <div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-secondary/10 text-secondary flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[18px] sm:text-[24px]">class</span>
          </div>
          <div class="flex flex-col min-w-0 w-full">
            <span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Classes</span>
            <span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">3 Cohorts</span>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
          <div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-primary-container/15 text-primary-container flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[18px] sm:text-[24px]">group</span>
          </div>
          <div class="flex flex-col min-w-0 w-full">
            <span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Learners</span>
            <span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">84 Students</span>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
          <div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-surface-container-highest text-on-surface-variant flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[18px] sm:text-[24px]">badge</span>
          </div>
          <div class="flex flex-col min-w-0 w-full">
            <span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Roster</span>
            <span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">8 Faculty</span>
          </div>
        </div>
      </div>
    </div>
  </div>\n\n    '''

text = text[:idx_start] + new_kpi + text[idx_end:]

with open('pages/teacher/teacher-departments.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-departments.html successfully!')

