principal_nav_code = """    principal: {
      brand: "Principal", meta: "School Operations · 2025–26",
      groups: [
        { label: "Overview", links: [
          { id: "dashboard", label: "Home", icon: "home", href: "pages/principal/principal.html" },
        ]},
        { id: "teachers-mgmt", label: "TEACHER MANAGEMENT", icon: "school", links: [
          { id: "classes", label: "My Class", icon: "school", href: "pages/principal/principal-classes.html" },
          { id: "departments", label: "Department", icon: "apartment", href: "pages/principal/principal-departments.html" },
          { id: "teachers", label: "Teachers & Staff", icon: "co_present", href: "pages/principal/principal-teachers.html" },
          { id: "timetables", label: "Timetable Management", icon: "calendar_month", href: "pages/principal/principal-timetables.html" },
        ]},
        { id: "academic-oversight", label: "ACADEMIC OVERSIGHT", icon: "assignment", links: [
          { id: "attendance", label: "Attendance", icon: "how_to_reg", href: "pages/principal/principal-attendance.html" },
          { id: "assignments", label: "Assignment & Students", icon: "description", href: "pages/principal/principal-assignments.html" },
          { id: "reports", label: "Student Results & Reports", icon: "assessment", href: "pages/principal/principal-reports.html" },
          { id: "documents", label: "Official Documents", icon: "verified", href: "pages/principal/principal-documents.html" },
        ]},
        { id: "students-mgmt", label: "STUDENT MANAGEMENT", icon: "group", links: [
          { id: "students", label: "Student Records", icon: "person_search", href: "pages/principal/principal-students.html" },
          { id: "services", label: "Student Service Hub", icon: "grid_view", href: "pages/principal/principal-services.html" },
          { id: "lost-found", label: "Lost and Found", icon: "inventory_2", href: "pages/principal/principal-lost-found.html" },
        ]},
        { id: "approvals-grp", label: "DECISIONS & NOTICES", icon: "verified", links: [
          { id: "approvals", label: "Waiting for Approval", icon: "task_alt", href: "pages/principal/principal-approvals.html", badge: "3" },
          { id: "announcements", label: "School Announcements", icon: "campaign", href: "pages/shared/announcements.html?portal=principal" },
          { id: "activity", label: "Change History", icon: "history", href: "pages/principal/principal-activity.html" },
        ]},
        { id: "account-grp", label: "ACCOUNT", icon: "person", links: [
          { id: "profile", label: "Settings & Profile", icon: "settings", href: "pages/principal/principal-profile.html" },
          { id: "logout", label: "Log out", icon: "logout", href: "index.html" },
        ]},
      ],
    },"""

principal_bottom_code = """    principal: [
      { id:"dashboard",  label:"Home",       icon:"home",           href:"pages/principal/principal.html" },
      { id:"classes",    label:"Classes",    icon:"school",         href:"pages/principal/principal-classes.html" },
      { id:"approvals",  label:"Approvals",  icon:"verified",       href:"pages/principal/principal-approvals.html" },
      { id:"services",   label:"Services",   icon:"grid_view",      href:"pages/principal/principal-services.html" },
      { id:"profile",    label:"Profile",    icon:"person",         href:"pages/principal/principal-profile.html" },
    ],"""

for fname in ['assets/js/layout.js', 'layout.js']:
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read().replace('\r\n', '\n')
    
    # 1. Replace principal NAV
    start_p = text.find('principal: {')
    if start_p != -1:
        # Find closing of principal: { ... }
        # Look for '  };' after start_p
        end_p = text.find('  };', start_p)
        if end_p != -1:
            old_nav = text[start_p:end_p].strip()
            # Let's replace from start_p to end_p
            text = text[:start_p] + principal_nav_code + "\n" + text[end_p:]
            print(f"Replaced principal NAV in {fname}")
        else:
            print(f"Could not find end of principal NAV in {fname}")
            
    # 2. Replace principal BOTTOM
    b_start = text.find('principal: [\n      { id:"dashboard"')
    if b_start != -1:
        b_end = text.find('],', b_start)
        if b_end != -1:
            text = text[:b_start] + principal_bottom_code + "\n" + text[b_end+2:]
            print(f"Replaced principal BOTTOM in {fname}")

    with open(fname, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)

print("Finished updating layout.js")

