import os, re

def fix_admin_services():
    p = 'pages/admin/admin-services.html'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r'src=["\']LOGO NGIS \(2\)\.png["\']', 'src="../../assets/images/logo.png"', text)
    text = re.sub(
        r'<button class="htb-hamburger"[^>]*>.*?<\/button>',
        '<button class="htb-hamburger hamburger-btn mobile-hamburger-btn" id="htbHamburger" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation"><i class="ph ph-list text-xl"></i><span class="mi" style="display:none">menu</span></button>',
        text,
        flags=re.DOTALL
    )
    if 'layout.js' not in text:
        text = text.replace(
            '<script>window.PAGE={"role":"admin","active":"services"};</script>',
            '<script>window.PAGE={"role":"admin","active":"services"};</script>\n<script src="../../assets/js/layout.js"></script>'
        )

    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("Fixed pages/admin/admin-services.html")

def fix_admin_campus():
    p = 'pages/admin/admin-campus.html'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    # Replace broken admin-parents.html with admin-users.html?role=parents
    text = text.replace('href="admin-parents.html"', 'href="admin-users.html?role=parents"')
    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("Fixed pages/admin/admin-campus.html")

def fix_teacher_reports():
    p = 'pages/teacher/teacher-reports.html'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    # If there is static unescaped ${tr.fileUrl} in href, replace with javascript:void(0) or data attribute
    text = text.replace('href="${tr.fileUrl}"', 'href="javascript:void(0)" data-href="${tr.fileUrl}"')
    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("Fixed pages/teacher/teacher-reports.html")

def fix_teacher_departments():
    p = 'pages/teacher/teacher-departments.html'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('href="../messaging/department-channels.html"', 'href="teacher-announcements.html"')
    text = text.replace('href="teacher-assignments.html"', 'href="teacher-submissions.html"')
    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("Fixed pages/teacher/teacher-departments.html")

def fix_teacher_classes():
    p = 'pages/teacher/teacher-classes.html'
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('href="../messaging/class-chats.html"', 'href="teacher-announcements.html"')
    with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("Fixed pages/teacher/teacher-classes.html")

def fix_shared_chat_links():
    targets = [
        'pages/admin/admin-department-detail.html',
        'pages/shared/departments.html',
        'pages/student/student-services.html',
        'pages/student/student.html'
    ]
    for p in targets:
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8') as f:
                text = f.read()
            text = text.replace('href="../shared/chat.html"', 'href="javascript:void(0)" onclick="if(window.NGISUI)NGISUI.toast(\'Messaging is currently in maintenance\',\'info\');else alert(\'Messaging is currently in maintenance\');"')
            text = text.replace('href="chat.html"', 'href="javascript:void(0)" onclick="if(window.NGISUI)NGISUI.toast(\'Messaging is currently in maintenance\',\'info\');else alert(\'Messaging is currently in maintenance\');"')
            text = text.replace('href="student-chat.html"', 'href="javascript:void(0)" onclick="if(window.NGISUI)NGISUI.toast(\'Messaging is currently in maintenance\',\'info\');else alert(\'Messaging is currently in maintenance\');"')
            with open(p, 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(text)
            print(f"Fixed chat links in {p}")

if __name__ == '__main__':
    fix_admin_services()
    fix_admin_campus()
    fix_teacher_reports()
    fix_teacher_departments()
    fix_teacher_classes()
    fix_shared_chat_links()

with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()
text = re.sub(r'href=[\'"]\$\{tr\.fileUrl\}[\'"]', 'href="javascript:void(0)"', text)
with open('pages/teacher/teacher-reports.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)
print("Cleaned up teacher-reports.html hrefs")
