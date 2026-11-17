import re
import json

print("=== 1. Patching assets/js/action-icons.js ===")
with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    ai_content = f.read()

# Add circle to PATHS if not present
if 'circle:' not in ai_content:
    ai_content = ai_content.replace(
        'menu: "<path',
        'circle: "<circle cx=\\"8\\" cy=\\"8\\" r=\\"5.5\\" fill=\\"none\\" stroke=\\"currentColor\\" stroke-width=\\"1.2\\"/>",\n    menu: "<path'
    )

# Add aliases to ALIASES
aliases_block = """    /* Navigation & Sidebar Aliases */
    'co_present': 'teachers',
    'assignment_ind': 'user',
    'verified_user': 'shield',
    'group_add': 'users',
    'support_agent': 'user',
    'account_balance': 'bank',
    'bar_chart': 'report',
    'menu_book': 'book',
    'location_city': 'building',
    'calendar_view_week': 'calendarWeek',
    'calendar_month': 'calendar',
    'date_range': 'calendar',
    'view_week': 'calendarWeek',
    'inventory_2': 'inventory',
    'dashboard_customize': 'dashboardCustom',
    'view_quilt': 'grid',
    'grid_view': 'grid',
    'local_activity': 'activity',
    'business_center': 'building',
    'how_to_reg': 'attendance',
    'circle': 'circle',
"""

if '/* Navigation & Sidebar Aliases */' not in ai_content:
    ai_content = ai_content.replace(
        "var ALIASES = {\n    /* Master action mapping aliases */\n",
        "var ALIASES = {\n" + aliases_block + "    /* Master action mapping aliases */\n"
    )

with open('assets/js/action-icons.js', 'w', encoding='utf-8') as f:
    f.write(ai_content)
print("action-icons.js patched successfully!")

print("\n=== 2. Patching assets/js/layout.js ===")
with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    layout_content = f.read()

# Admin Overview group icon
layout_content = layout_content.replace(
    '{ label:"Overview", links:[\n          { id:"dashboard", label:"Dashboard", icon:"dashboard"',
    '{ id:"overview", label:"Overview", icon:"dashboard", links:[\n          { id:"dashboard", label:"Dashboard", icon:"dashboard"'
)

# Admin Account Directories sublinks
old_users_dir = """            children: [
              { id: "users-students", label: "Student Accounts", href: "pages/admin/admin-users-students.html" },
              { id: "users-teachers", label: "Teacher Accounts", href: "pages/admin/admin-users-teachers.html" },
              { id: "users-staff", label: "Staff Accounts", href: "pages/admin/admin-users-staff.html" },
              { id: "users-principals", label: "Principal Accounts", href: "pages/admin/admin-users-principals.html" },
              { id: "users-admins", label: "Admin Accounts", href: "pages/admin/admin-users-admins.html" },
            ]"""

new_users_dir = """            children: [
              { id: "users-students", label: "Student Accounts", icon: "school", href: "pages/admin/admin-users-students.html" },
              { id: "users-teachers", label: "Teacher Accounts", icon: "teachers", href: "pages/admin/admin-users-teachers.html" },
              { id: "users-staff", label: "Staff Accounts", icon: "user", href: "pages/admin/admin-users-staff.html" },
              { id: "users-principals", label: "Principal Accounts", icon: "bank", href: "pages/admin/admin-users-principals.html" },
              { id: "users-admins", label: "Admin Accounts", icon: "shield", href: "pages/admin/admin-users-admins.html" },
            ]"""
layout_content = layout_content.replace(old_users_dir, new_users_dir)

# Admin Teachers Management sublinks
old_teach_mgmt = """            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/admin/admin-teacher-profiles.html" },
              { id: "teacher-class-assignment", label: "Teacher-Class Assignment", href: "pages/admin/admin-teacher-class-assignment.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", href: "pages/admin/admin-teacher-verify.html" },
            ]"""

new_teach_mgmt = """            children: [
              { id: "teacher-profiles", label: "Teacher Profile", icon: "teachers", href: "pages/admin/admin-teacher-profiles.html" },
              { id: "teacher-class-assignment", label: "Teacher-Class Assignment", icon: "co_present", href: "pages/admin/admin-teacher-class-assignment.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", icon: "checkCircle", href: "pages/admin/admin-teacher-verify.html" },
            ]"""
layout_content = layout_content.replace(old_teach_mgmt, new_teach_mgmt)

# Admin Student Management sublinks
old_stud_mgmt = """            children: [
              { id: "student-profiles", label: "Student Information", href: "pages/admin/admin-student-profiles.html" },
              { id: "verify-student", label: "Verify Student Update", href: "pages/admin/admin-student-verify.html" },
              { id: "student-assign", label: "Student Assign To Class", href: "pages/admin/admin-student-assign.html" },
              { id: "input-attendance", label: "Input Attendance", href: "pages/admin/admin-attendance.html" },
              { id: "absence-stats", label: "Absence Statistics", href: "pages/admin/admin-absence-stats.html" },
            ]"""

new_stud_mgmt = """            children: [
              { id: "student-profiles", label: "Student Information", icon: "school", href: "pages/admin/admin-student-profiles.html" },
              { id: "verify-student", label: "Verify Student Update", icon: "checkCircle", href: "pages/admin/admin-student-verify.html" },
              { id: "student-assign", label: "Student Assign To Class", icon: "group_add", href: "pages/admin/admin-student-assign.html" },
              { id: "input-attendance", label: "Input Attendance", icon: "attendance", href: "pages/admin/admin-attendance.html" },
              { id: "absence-stats", label: "Absence Statistics", icon: "report", href: "pages/admin/admin-absence-stats.html" },
            ]"""
layout_content = layout_content.replace(old_stud_mgmt, new_stud_mgmt)

# Admin System Management dropdown sublinks
old_sys_mgmt = """            children: [
              { id: "dashboard-content-sys", label: "Dashboard Content", href: "pages/admin/admin-dashboard-content.html" },
              { id: "school-information", label: "School Information & Settings", href: "pages/admin/admin-school-information.html" },
              { id: "sys-school-info", label: "School Profile (Legacy)", href: "pages/admin/admin-system-school-info.html" },
              { id: "sys-schedule", label: "Schedule", href: "pages/admin/admin-system-schedule.html" },
              { id: "sys-general-setting", label: "General Setting", href: "pages/admin/admin-system-general-setting.html" },
            ]"""

new_sys_mgmt = """            children: [
              { id: "dashboard-content-sys", label: "Dashboard Content", icon: "grid", href: "pages/admin/admin-dashboard-content.html" },
              { id: "school-information", label: "School Information & Settings", icon: "settings", href: "pages/admin/admin-school-information.html" },
              { id: "sys-school-info", label: "School Profile (Legacy)", icon: "building", href: "pages/admin/admin-system-school-info.html" },
              { id: "sys-schedule", label: "Schedule", icon: "calendar", href: "pages/admin/admin-system-schedule.html" },
              { id: "sys-general-setting", label: "General Setting", icon: "tune", href: "pages/admin/admin-system-general-setting.html" },
            ]"""
layout_content = layout_content.replace(old_sys_mgmt, new_sys_mgmt)

# Admin School Year Configuration dropdown sublinks
old_year_cfg = """            children: [
              { id: "sys-school-year", label: "School Year", href: "pages/admin/admin-system-school-year.html" },
              { id: "sys-school-week", label: "School Week", href: "pages/admin/admin-system-school-week.html" },
              { id: "sys-exam-config", label: "School Exam Configuration", href: "pages/admin/admin-system-exam-config.html" }
            ]"""

new_year_cfg = """            children: [
              { id: "sys-school-year", label: "School Year", icon: "calendar", href: "pages/admin/admin-system-school-year.html" },
              { id: "sys-school-week", label: "School Week", icon: "calendarWeek", href: "pages/admin/admin-system-school-week.html" },
              { id: "sys-exam-config", label: "School Exam Configuration", icon: "exams", href: "pages/admin/admin-system-exam-config.html" }
            ]"""
layout_content = layout_content.replace(old_year_cfg, new_year_cfg)

# Superadmin Overview group icon
layout_content = layout_content.replace(
    'superadmin: {\n      brand: "Super Admin", meta: "Root System Suite · 2025–26",\n      groups: [\n        { label: "Overview", links: [',
    'superadmin: {\n      brand: "Super Admin", meta: "Root System Suite · 2025–26",\n      groups: [\n        { id: "sa-overview-grp", label: "Overview", icon: "dashboard", links: ['
)

# Superadmin User Directories sublinks
old_sa_dir = """          { id: "sa-directories-drop", label: "User Directories", icon: "group", collapsible: true, children: [
            { id: "sa-students", label: "Student Accounts", href: "pages/admin/admin-users-students.html" },
            { id: "sa-teachers", label: "Teacher Accounts", href: "pages/admin/admin-users-teachers.html" },
            { id: "sa-staff", label: "Staff Accounts", href: "pages/admin/admin-users-staff.html" },
            { id: "sa-principals", label: "Principal Accounts", href: "pages/admin/admin-users-principals.html" },
            { id: "sa-admins", label: "Admin Accounts", href: "pages/admin/admin-users-admins.html" }
          ]}"""

new_sa_dir = """          { id: "sa-directories-drop", label: "User Directories", icon: "group", collapsible: true, children: [
            { id: "sa-students", label: "Student Accounts", icon: "school", href: "pages/admin/admin-users-students.html" },
            { id: "sa-teachers", label: "Teacher Accounts", icon: "teachers", href: "pages/admin/admin-users-teachers.html" },
            { id: "sa-staff", label: "Staff Accounts", icon: "user", href: "pages/admin/admin-users-staff.html" },
            { id: "sa-principals", label: "Principal Accounts", icon: "bank", href: "pages/admin/admin-users-principals.html" },
            { id: "sa-admins", label: "Admin Accounts", icon: "shield", href: "pages/admin/admin-users-admins.html" }
          ]}"""
layout_content = layout_content.replace(old_sa_dir, new_sa_dir)

# Teacher Overview group icon
layout_content = layout_content.replace(
    'teacher: {\n\n      brand: "Teacher", meta: "Faculty Portal · 2025–26",\n\n      groups: [\n\n        { label:"Overview", links:[',
    'teacher: {\n\n      brand: "Teacher", meta: "Faculty Portal · 2025–26",\n\n      groups: [\n\n        { id:"overview", label:"Overview", icon:"dashboard", links:['
)

# Student Main group icon
layout_content = layout_content.replace(
    'student: {\n\n      brand: "Student", meta: "Student Portal · 2025–26",\n\n      groups: [\n\n        { label:"Main", links:[',
    'student: {\n\n      brand: "Student", meta: "Student Portal · 2025–26",\n\n      groups: [\n\n        { id:"main", label:"Main", icon:"dashboard", links:['
)

# Principal Overview group icon
layout_content = layout_content.replace(
    'principal: {\n      brand: "Principal", meta: "School Operations · 2025–26",\n      groups: [\n        { label: "Overview", links: [',
    'principal: {\n      brand: "Principal", meta: "School Operations · 2025–26",\n      groups: [\n        { id: "overview", label: "Overview", icon: "dashboard", links: ['
)

# Staff Overview group icon
layout_content = layout_content.replace(
    'staff: {\n      brand: "Staff", meta: "Campus Operations Hub · 2025–26",\n      groups: [\n        { label: "Overview", links: [',
    'staff: {\n      brand: "Staff", meta: "Campus Operations Hub · 2025–26",\n      groups: [\n        { id: "staff-overview-grp", label: "Overview", icon: "dashboard", links: ['
)

# Update renderNavIcon to guarantee fallback icon
old_render_nav_icon = """    function renderNavIcon(icon, className) {
      if (!icon) return "";
      const trimmed = String(icon).trim();
      if (trimmed.startsWith("<svg")) {
        return `<span class="nav-icon ${className} nav-icon-svg" aria-hidden="true">${trimmed}</span>`;
      }
      if (trimmed.startsWith("ph ") || trimmed.startsWith("ph-")) {
        /* Phosphor glyph: upgrade to the shared Bootstrap-icon engine while
           keeping the Phosphor ligature as a no-engine fallback. */
        const phName = trimmed.replace(/^ph[\\s-]+/, "").replace(/^ph-/, "");
        return `<i class="${trimmed} ${className} nav-icon" data-ngis-icon="${esc(phName)}" aria-hidden="true">${esc(phName)}</i>`;
      }
      /* Material Symbols glyph with a data-ngis-icon slot: the shared icon
         engine (action-icons.js) replaces it with the official Bootstrap
         Icons SVG when present; the ligature text remains a graceful
         fallback so the sidebar never loses its icons. */
      return `<span class="material-symbols-outlined ${className} nav-icon" data-ngis-icon="${esc(trimmed)}" aria-hidden="true">${esc(trimmed)}</span>`;
    }"""

new_render_nav_icon = """    function renderNavIcon(icon, className) {
      const isGroup = className && className.includes("group");
      const effectiveIcon = (icon && String(icon).trim() !== "") ? icon : (isGroup ? "dashboard" : "circle");
      const trimmed = String(effectiveIcon).trim();
      if (trimmed.startsWith("<svg")) {
        return `<span class="nav-icon ${className} nav-icon-svg" aria-hidden="true">${trimmed}</span>`;
      }
      if (trimmed.startsWith("ph ") || trimmed.startsWith("ph-")) {
        /* Phosphor glyph without bold weight */
        const cleanPh = trimmed.replace(/\\bph-bold\\b/g, "ph").replace(/\\bph-fill\\b/g, "ph");
        const phName = cleanPh.replace(/^ph[\\s-]+/, "").replace(/^ph-/, "");
        return `<i class="${cleanPh} ${className} nav-icon" data-ngis-icon="${esc(phName)}" aria-hidden="true">${esc(phName)}</i>`;
      }
      /* Material Symbols glyph with a data-ngis-icon slot */
      return `<span class="material-symbols-outlined ${className} nav-icon" data-ngis-icon="${esc(trimmed)}" aria-hidden="true">${esc(trimmed)}</span>`;
    }"""

layout_content = layout_content.replace(old_render_nav_icon, new_render_nav_icon)

# Ensure sublinks always render an icon
layout_content = layout_content.replace(
    '${sub.icon ? renderNavIcon(sub.icon, "nav-link-icon") : ""}',
    '${renderNavIcon(sub.icon, "nav-link-icon")}'
)

layout_content = layout_content.replace(
    '${n.icon ? renderNavIcon(n.icon, "nav-link-icon") : ""}',
    '${renderNavIcon(n.icon, "nav-link-icon")}'
)

with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(layout_content)

print("layout.js patched successfully!")

print("\n=== 3. Patching data/sidebar_nav.json ===")
with open('data/sidebar_nav.json', 'r', encoding='utf-8') as f:
    sb_data = json.load(f)

icon_map = {
    'users-students': 'school',
    'users-teachers': 'teachers',
    'users-staff': 'user',
    'users-principals': 'bank',
    'users-admins': 'shield',
    'teacher-profiles': 'teachers',
    'teacher-class-assignment': 'co_present',
    'verify-teacher': 'checkCircle',
    'student-profiles': 'school',
    'verify-student': 'checkCircle',
    'student-assign': 'group_add',
    'input-attendance': 'attendance',
    'absence-stats': 'report',
    'dashboard-content-sys': 'grid',
    'school-information': 'settings',
    'sys-school-info': 'building',
    'sys-schedule': 'calendar',
    'sys-general-setting': 'tune',
    'sys-school-year': 'calendar',
    'sys-school-week': 'calendarWeek',
    'sys-exam-config': 'exams',
    'sa-students': 'school',
    'sa-teachers': 'teachers',
    'sa-staff': 'user',
    'sa-principals': 'bank',
    'sa-admins': 'shield',
}

for p, pdata in sb_data['portals'].items():
    for g in pdata.get('groups', []):
        if not g.get('icon'):
            g['icon'] = 'dashboard'
        for l in g.get('links', []):
            if l.get('id') in icon_map and not l.get('icon'):
                l['icon'] = icon_map[l['id']]
            if l.get('children'):
                for c in l['children']:
                    if c.get('id') in icon_map:
                        c['icon'] = icon_map[c['id']]

with open('data/sidebar_nav.json', 'w', encoding='utf-8') as f:
    json.dump(sb_data, f, indent=2, ensure_ascii=False)

print("sidebar_nav.json patched successfully!")
