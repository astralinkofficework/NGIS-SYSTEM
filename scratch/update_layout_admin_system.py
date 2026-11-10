import shutil

with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        { id:"system", label:"SYSTEM & SECURITY", icon:"admin_panel_settings", links:[

          { id:"logs",     label:"Audit Logs",      icon:"history",  href:"pages/admin/admin-logs.html" },'''

replacement = '''        { id:"system", label:"SYSTEM & SECURITY", icon:"admin_panel_settings", links:[

          {
            id: "system-mgmt-drop",
            label: "System",
            icon: "settings",
            collapsible: true,
            children: [
              { id: "sys-school-info", label: "School Information", href: "pages/admin/admin-system-school-info.html" },
              {
                id: "sys-year-config-drop",
                label: "School Year Configuration",
                collapsible: true,
                children: [
                  { id: "sys-school-year", label: "School Year", href: "pages/admin/admin-system-school-year.html" },
                  { id: "sys-school-week", label: "School Week", href: "pages/admin/admin-system-school-week.html" },
                  { id: "sys-exam-config", label: "School Exam Configuration", href: "pages/admin/admin-system-exam-config.html" },
                  { id: "sys-score-lock", label: "Score Lock Configuration", href: "pages/admin/admin-system-score-lock.html" },
                  { id: "sys-define-curriculum", label: "Define Curriculum", href: "pages/admin/admin-system-define-curriculum.html" },
                  { id: "sys-design-curriculum", label: "Design Curriculum", href: "pages/admin/admin-system-design-curriculum.html" },
                  { id: "sys-declare-class", label: "Declare Class", href: "pages/admin/admin-system-declare-class.html" },
                  { id: "sys-student-transition", label: "Student Transition", href: "pages/admin/admin-system-student-transition.html" },
                  { id: "sys-technician-assign", label: "Technician & Monitor Assign", href: "pages/admin/admin-system-technician-assign.html" },
                ]
              },
              {
                id: "sys-account-mgmt-drop",
                label: "Account Management",
                collapsible: true,
                children: [
                  { id: "sys-employee-group", label: "Employee Group", href: "pages/admin/admin-system-employee-group.html" },
                  { id: "sys-employee-accounts", label: "Employee Accounts", href: "pages/admin/admin-system-employee-accounts.html" },
                  { id: "sys-student-accounts", label: "Student Accounts", href: "pages/admin/admin-system-student-accounts.html" },
                  { id: "sys-parent-accounts", label: "Parent Accounts", href: "pages/admin/admin-system-parent-accounts.html" },
                ]
              },
              { id: "sys-schedule", label: "Schedule", href: "pages/admin/admin-system-schedule.html" },
              { id: "sys-general-setting", label: "General Setting", href: "pages/admin/admin-system-general-setting.html" },
            ]
          },

          { id:"logs",     label:"Audit Logs",      icon:"history",  href:"pages/admin/admin-logs.html" },'''

if target in content:
    content = content.replace(target, replacement, 1)
    with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
        f.write(content)
    # Synchronize layout.js
    shutil.copyfile('assets/js/layout.js', 'layout.js')
    print('Successfully updated assets/js/layout.js and synced to layout.js')
else:
    print('Error: Target string not found in assets/js/layout.js')

