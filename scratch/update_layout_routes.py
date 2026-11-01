import re

def update_layout(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update NAV.student departments href to include ?portal=student
    old_dept = 'href:"pages/shared/departments.html"'
    new_dept = 'href:"pages/shared/departments.html?portal=student"'
    
    # 2. Update NAV.admin announcements href to include ?portal=admin
    old_admin_ann = 'href:"pages/shared/announcements.html"'
    new_admin_ann = 'href:"pages/shared/announcements.html?portal=admin"'

    # 3. Update Priority 3 in resolvePortalRole
    old_p3 = """    // Priority 3: Explicit pageRole configured on window.PAGE
    if (pageRole) {
      const normalizedPageRole = normalizeRole(pageRole);
      if (["admin", "teacher", "student", "staff", "principal"].includes(normalizedPageRole)) {
        return normalizedPageRole;
      }
    }"""
    
    new_p3 = """    // Priority 3: Explicit pageRole configured on window.PAGE
    if (pageRole) {
      const normalizedPageRole = normalizeRole(pageRole);
      if (["admin", "teacher", "student", "staff", "principal"].includes(normalizedPageRole)) {
        try { localStorage.setItem("ngis_active_portal", normalizedPageRole); } catch (e) {}
        return normalizedPageRole;
      }
    }"""

    # Perform updates
    c = content.replace('\r\n', '\n')
    
    # In student block only for departments
    # Let's target student block specifically
    student_pattern = r'(student:\s*\{[\s\S]*?id:\s*"departments"[^\n]*href:\s*")[^"]*(")'
    c, count1 = re.subn(student_pattern, r'\g<1>pages/shared/departments.html?portal=student\g<2>', c)
    print(f"[{file_path}] updated student departments: {count1}")

    # In admin announcements
    admin_pattern = r'(admin:\s*\{[\s\S]*?id:\s*"announcements"[^\n]*href:\s*")[^"]*(")'
    c, count2 = re.subn(admin_pattern, r'\g<1>pages/shared/announcements.html?portal=admin\g<2>', c)
    print(f"[{file_path}] updated admin announcements: {count2}")

    # In principal announcements
    principal_pattern = r'(principal:\s*\{[\s\S]*?id:\s*"announcements"[^\n]*href:\s*")[^"]*(")'
    c, count3 = re.subn(principal_pattern, r'\g<1>pages/shared/announcements.html?portal=principal\g<2>', c)
    print(f"[{file_path}] updated principal announcements: {count3}")

    # In staff announcements
    staff_pattern = r'(staff:\s*\{[\s\S]*?id:\s*"announcements"[^\n]*href:\s*")[^"]*(")'
    c, count4 = re.subn(staff_pattern, r'\g<1>pages/shared/announcements.html?portal=staff\g<2>', c)
    print(f"[{file_path}] updated staff announcements: {count4}")

    # Priority 3
    if old_p3.replace('\r\n', '\n') in c:
        c = c.replace(old_p3.replace('\r\n', '\n'), new_p3.replace('\r\n', '\n'))
        print(f"[{file_path}] updated priority 3 in resolvePortalRole")
    else:
        print(f"[{file_path}] old_p3 not matched")

    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(c)

update_layout('assets/js/layout.js')
update_layout('layout.js')

