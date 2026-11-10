# D1 fix round 2: admin-campus rewires + pre-existing dead chat/messaging links.
import re, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

FIXES = [
    ('pages/admin/admin-campus.html', 'admin-teachers.html', 'admin-users.html?role=teachers'),
    ('pages/admin/admin-campus.html', 'admin-admins.html', 'admin-users.html?role=admins'),
    ('pages/principal/principal.html', '../messaging/campus-announcements.html', '../shared/announcements.html?portal=principal'),
    ('pages/student/student-services.html', "function chatWithOfficer() { window.location.href = '../shared/chat.html'; }",
     "function chatWithOfficer() { window.location.href = 'student-notifications.html'; }"),
    ('pages/student/student-services.html', "function contactHelpdesk() { window.location.href = '../shared/chat.html'; }",
     "function contactHelpdesk() { window.location.href = 'student-notifications.html'; }"),
    ('pages/student/student-services.html', " chatLink: '../shared/chat.html',", ''),  # hero.js falls back to notifications
    ('pages/teacher/teacher-classes.html', "linkChat.href = '../messaging/class-chats.html?class='",
     "linkChat.href = 'teacher-announcements.html?class='"),
    ('pages/teacher/teacher-roster.html', "location.href='../shared/chat.html?portal=teacher&recipient=${encodeURIComponent(s.name)}'",
     "location.href='teacher-notifications.html?recipient=${encodeURIComponent(s.name)}'"),
    ('pages/teacher/teacher-roster.html', "btnMsg.onclick = () => location.href = `../shared/chat.html?portal=teacher&recipient=${encodeURIComponent(student.name)}`",
     "btnMsg.onclick = () => location.href = `teacher-notifications.html?recipient=${encodeURIComponent(student.name)}`"),
    ('tests/verify_removal.py', '"pages/admin/admin-users.html", "pages/admin/admin-students.html"', '"pages/admin/admin-users.html"'),
]

for path, old, new in FIXES:
    t = open(path, encoding='utf-8').read()
    n = t.count(old)
    if n == 0:
        print(f'MISS {path}: {old[:60]}')
    else:
        open(path, 'w', encoding='utf-8').write(t.replace(old, new))
        print(f'OK   {path}: {n}x -> {new[:60] if new else "(removed)"}')

# any remaining chat.html / messaging refs in live surfaces?
live = glob.glob('pages/**/*.html', recursive=True) + glob.glob('assets/js/*.js') + ['index.html']
for f in live:
    t = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'(?:chat|messaging)[\w/.-]*\.html', t):
        print('LEFTOVER', f, '->', m.group(0))
print('scan done')
