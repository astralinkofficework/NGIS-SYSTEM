with open('pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix container padding
content = content.replace('w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6',
                          'w-full max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-4 sm:pt-6 pb-28 sm:pb-32 lg:pb-16')

# Replace the KPI strip with responsive-friendly layout
old_kpi = '''<!-- 4-KPI Metric Strip -->
<div class="grid grid-cols-2 md:grid-cols-4 gap-space-md">
<div class="flex items-center gap-space-md p-space-sm rounded-lg bg-surface-container-low/70 border border-outline-variant/60">
<div class="w-11 h-11 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[24px]">functions</span>
</div>
<div class="flex flex-col min-w-0">
<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider truncate">Discipline Group</span>
<span class="font-headline-sm text-headline-sm text-on-surface truncate">Mathematics</span>
</div>
</div>
<div class="flex items-center gap-space-md p-space-sm rounded-lg bg-surface-container-low/70 border border-outline-variant/60">
<div class="w-11 h-11 rounded-lg bg-secondary/10 text-secondary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[24px]">class</span>
</div>
<div class="flex flex-col min-w-0">
<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider truncate">Assigned Classes</span>
<span class="font-headline-sm text-headline-sm text-on-surface truncate">3 Active Cohorts</span>
</div>
</div>
<div class="flex items-center gap-space-md p-space-sm rounded-lg bg-surface-container-low/70 border border-outline-variant/60">
<div class="w-11 h-11 rounded-lg bg-primary-container/15 text-primary-container flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[24px]">group</span>
</div>
<div class="flex flex-col min-w-0">
<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider truncate">Taught Learners</span>
<span class="font-headline-sm text-headline-sm text-on-surface truncate">84 Total Students</span>
</div>
</div>
<div class="flex items-center gap-space-md p-space-sm rounded-lg bg-surface-container-low/70 border border-outline-variant/60">
<div class="w-11 h-11 rounded-lg bg-surface-container-highest text-on-surface-variant flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[24px]">badge</span>
</div>
<div class="flex flex-col min-w-0">
<span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider truncate">Department Roster</span>
<span class="font-headline-sm text-headline-sm text-on-surface truncate">8 Faculty Members</span>
</div>
</div>
</div>'''

new_kpi = '''<!-- 4-KPI Metric Strip (Responsive, No Truncation) -->
<div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 sm:gap-space-md">
<div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
<div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px] sm:text-[24px]">functions</span>
</div>
<div class="flex flex-col min-w-0 w-full">
<span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Discipline Group</span>
<span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">Mathematics</span>
</div>
</div>
<div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
<div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-secondary/10 text-secondary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px] sm:text-[24px]">class</span>
</div>
<div class="flex flex-col min-w-0 w-full">
<span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Assigned Classes</span>
<span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">3 Cohorts</span>
</div>
</div>
<div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
<div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-primary-container/15 text-primary-container flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px] sm:text-[24px]">group</span>
</div>
<div class="flex flex-col min-w-0 w-full">
<span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Taught Learners</span>
<span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">84 Students</span>
</div>
</div>
<div class="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-space-md p-3 sm:p-space-sm rounded-xl bg-surface-container-low/70 border border-outline-variant/60 transition-all hover:bg-surface-container-low">
<div class="w-8 h-8 sm:w-11 sm:h-11 rounded-lg bg-surface-container-highest text-on-surface-variant flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px] sm:text-[24px]">badge</span>
</div>
<div class="flex flex-col min-w-0 w-full">
<span class="text-[10px] sm:text-label-sm font-medium text-on-surface-variant uppercase tracking-wider truncate">Department</span>
<span class="text-xs sm:text-headline-sm font-medium text-on-surface truncate">8 Faculty</span>
</div>
</div>
</div>'''

content = content.replace(old_kpi, new_kpi)

with open('pages/teacher/teacher-departments.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated teacher-departments.html!')

