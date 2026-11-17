import os

def fix_admin_logs():
    p = 'pages/admin/admin-logs.html'
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    c = c.replace('<title>NGIS \ufffd Audit Logs</title>', '<title>NGIS — Audit Logs</title>')
    c = c.replace('placeholder="Search logs\ufffd"', 'placeholder="Search logs..."')
    c = c.replace('Showing 1\ufffd8 of 12,483 events', 'Showing 1–8 of 12,483 events')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def fix_admin_reports():
    p = 'pages/admin/admin-reports.html'
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    c = c.replace('<title>NGIS \ufffd Reports & Analytics</title>', '<title>NGIS — Reports & Analytics</title>')
    c = c.replace('Monthly average \ufffd Academic Year 2025\ufffd26', 'Monthly average — Academic Year 2025–26')
    c = c.replace('All students \ufffd Current semester', 'All students — Current semester')
    c = c.replace('3.0\ufffd3.9 (Good)', '3.0–3.9 (Good)')
    c = c.replace('2.0\ufffd2.9 (Average)', '2.0–2.9 (Average)')
    c = c.replace("window.toast('Exporting ' + r.name + ' as ' + formats[bi] + '\ufffd', 'info');", "window.toast('Exporting ' + r.name + ' as ' + formats[bi] + '...', 'info');")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def fix_student_calendar():
    p = 'pages/student/student-calendar.html'
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    c = c.replace("text: 'Grade 10 \ufffd Science Stream'", "text: 'Grade 10 — Science Stream'")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def fix_teacher_documents():
    p = 'pages/teacher/teacher-documents.html'
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    c = c.replace('<title>NGIS \ufffd Documents</title>', '<title>NGIS — Documents</title>')
    c = c.replace("window.toast('Opening Lesson Plans\ufffd','info')", "window.toast('Opening Lesson Plans...','info')")
    c = c.replace('48 files \ufffd 4.2 GB used', '48 files • 4.2 GB used')
    c = c.replace('placeholder="Search files\ufffd"', 'placeholder="Search files..."')
    c = c.replace("window.toast('Opening Lesson Plan\ufffd','info')", "window.toast('Opening Lesson Plan...','info')")
    c = c.replace('Lesson Plan \ufffd Integration', 'Lesson Plan — Integration')
    c = c.replace("window.toast('Opening worksheet\ufffd','info')", "window.toast('Opening worksheet...','info')")
    c = c.replace("window.toast('Opening presentation\ufffd','info')", "window.toast('Opening presentation...','info')")
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def fix_teacher_notifications():
    p = 'pages/teacher/teacher-notifications.html'
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    c = c.replace('<title>NGIS \ufffd Notifications</title>', '<title>NGIS — Notifications</title>')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def fix_teacher_profile():
    p = 'pages/teacher/teacher-profile.html'
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    c = c.replace('<title>NGIS \ufffd My Profile</title>', '<title>NGIS — My Profile</title>')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

fix_admin_logs()
fix_admin_reports()
fix_student_calendar()
fix_teacher_documents()
fix_teacher_notifications()
fix_teacher_profile()
print("All files updated.")
