with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_admin_block = """            id: "teachers-mgmt-drop",
            label: "Teachers Management",
            icon: "co_present",
            collapsible: true,
            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/admin/admin-teacher-profiles.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", href: "pages/admin/admin-teacher-profiles.html?view=verify" },
              { id: "teaching-assignment", label: "Teaching Assignment", href: "pages/admin/admin-assignments.html" },
              { id: "homeroom-assign", label: "Homeroom Teacher Assign", href: "pages/admin/admin-classes.html?tab=homeroom" },
              { id: "teacher-attendance", label: "Teacher Attendance", href: "pages/admin/admin-attendance.html?filter=teachers" },
              { id: "teacher-commendation", label: "Commendation", href: "pages/admin/admin-services.html?category=commendation" },
              { id: "teacher-discipline", label: "Discipline", href: "pages/admin/admin-services.html?category=discipline" },
              { id: "teacher-efforts", label: "Input Teacher Efforts", href: "pages/admin/admin-reports.html?tab=efforts" },
            ]"""

new_admin_block = """            id: "teachers-mgmt-drop",
            label: "Teachers Management",
            icon: "co_present",
            collapsible: true,
            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/admin/admin-teacher-profiles.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", href: "pages/admin/admin-teacher-verify.html" },
              { id: "teaching-assignment", label: "Teaching Assignment", href: "pages/admin/admin-teacher-assignments.html" },
              { id: "homeroom-assign", label: "Homeroom Teacher Assign", href: "pages/admin/admin-teacher-homeroom.html" },
              { id: "teacher-attendance", label: "Teacher Attendance", href: "pages/admin/admin-teacher-attendance.html" },
              { id: "teacher-commendation", label: "Commendation", href: "pages/admin/admin-teacher-commendation.html" },
              { id: "teacher-discipline", label: "Discipline", href: "pages/admin/admin-teacher-discipline.html" },
              { id: "teacher-efforts", label: "Input Teacher Efforts", href: "pages/admin/admin-teacher-efforts.html" },
            ]"""

old_prl_block = """            id: "teachers-mgmt-drop",
            label: "Teachers Management",
            icon: "co_present",
            collapsible: true,
            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/principal/principal-teacher-profiles.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", href: "pages/principal/principal-teacher-profiles.html?view=verify" },
              { id: "teaching-assignment", label: "Teaching Assignment", href: "pages/principal/principal-timetables.html?tab=assignments" },
              { id: "homeroom-assign", label: "Homeroom Teacher Assign", href: "pages/principal/principal-classes.html?tab=homeroom" },
              { id: "teacher-attendance", label: "Teacher Attendance", href: "pages/principal/principal-attendance.html?filter=teachers" },
              { id: "teacher-commendation", label: "Commendation", href: "pages/principal/principal-services.html?category=commendation" },
              { id: "teacher-discipline", label: "Discipline", href: "pages/principal/principal-services.html?category=discipline" },
              { id: "teacher-efforts", label: "Input Teacher Efforts", href: "pages/principal/principal-reports.html?tab=efforts" },
            ]"""

new_prl_block = """            id: "teachers-mgmt-drop",
            label: "Teachers Management",
            icon: "co_present",
            collapsible: true,
            children: [
              { id: "teacher-profiles", label: "Teacher Profile", href: "pages/principal/principal-teacher-profiles.html" },
              { id: "verify-teacher", label: "Verify Teacher Update", href: "pages/principal/principal-teacher-verify.html" },
              { id: "teaching-assignment", label: "Teaching Assignment", href: "pages/principal/principal-teacher-assignments.html" },
              { id: "homeroom-assign", label: "Homeroom Teacher Assign", href: "pages/principal/principal-teacher-homeroom.html" },
              { id: "teacher-attendance", label: "Teacher Attendance", href: "pages/principal/principal-teacher-attendance.html" },
              { id: "teacher-commendation", label: "Commendation", href: "pages/principal/principal-teacher-commendation.html" },
              { id: "teacher-discipline", label: "Discipline", href: "pages/principal/principal-teacher-discipline.html" },
              { id: "teacher-efforts", label: "Input Teacher Efforts", href: "pages/principal/principal-teacher-efforts.html" },
            ]"""

assert old_admin_block in text, "old_admin_block not found in text!"
assert old_prl_block in text, "old_prl_block not found in text!"

text = text.replace(old_admin_block, new_admin_block)
text = text.replace(old_prl_block, new_prl_block)

with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(text)

with open('layout.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated layout.js and assets/js/layout.js successfully!")

