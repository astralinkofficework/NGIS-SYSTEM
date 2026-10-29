import re

# 1. Update pages/admin/admin-users.html
with open(r"pages/admin/admin-users.html", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern for breadcrumb in admin-users.html
breadcrumb_pattern = r'<!-- Clean Breadcrumb -->\s*<div class="flex items-center gap-2 text-xs font-medium text-brand-700 uppercase tracking-wider mb-0\.5">\s*<span>Enterprise User Management</span>\s*<span>[•·\s]+</span>\s*<span class="text-slate-500 font-normal" id="subRoleHeader">.*?</span>\s*</div>\s*'
content, count_b = re.subn(breadcrumb_pattern, '', content)
print(f"admin-users.html: removed breadcrumbs: {count_b}")

# Pattern for rolePillTabs in admin-users.html
tabs_pattern = r'<!-- Clean Role Switcher Tabs[^\n]*-->\s*<div class="flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/80 gap-1 overflow-x-auto text-xs" id="rolePillTabs">[\s\S]*?</div>\s*(?=<!-- Top Right Action Buttons -->)'
content, count_t = re.subn(tabs_pattern, '', content)
print(f"admin-users.html: removed rolePillTabs: {count_t}")

with open(r"pages/admin/admin-users.html", "w", encoding="utf-8") as f:
    f.write(content)

# 2. Update pages/admin/admin-students.html
with open(r"pages/admin/admin-students.html", "r", encoding="utf-8") as f:
    content_s = f.read()

breadcrumb_pattern_s = r'<!-- Clean Breadcrumb -->\s*<div class="flex items-center gap-2 text-xs font-medium text-brand-700 uppercase tracking-wider mb-0\.5">\s*<span>Enterprise User Management</span>\s*<span>[•·\s]+</span>\s*<span class="text-slate-500 font-normal">Student Directory</span>\s*</div>\s*'
content_s, count_bs = re.subn(breadcrumb_pattern_s, '', content_s)
print(f"admin-students.html: removed breadcrumbs: {count_bs}")

with open(r"pages/admin/admin-students.html", "w", encoding="utf-8") as f:
    f.write(content_s)
