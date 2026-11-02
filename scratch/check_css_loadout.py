import re

files = [
    'pages/student/student.html',
    'pages/teacher/teacher.html',
    'pages/admin/admin.html',
    'pages/principal/principal.html',
    'pages/staff/staff.html',
    'pages/shared/announcements.html',
    'pages/shared/department.html',
    'index.html',
]
for f in files:
    src = open(f, encoding='utf-8', errors='ignore').read(8000)
    css = re.findall(r'href="([^"]*\.css[^"]*)"', src)
    js = re.findall(r'src="([^"]*(?:layout|interactions|app)[^"]*\.js[^"]*)"', src)
    print(f, '->', css)
    print('   JS:', js)
