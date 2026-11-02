import os, re

files = [
    'pages/admin/admin-attendance.html',
    'pages/admin/css/dashboard.css',
    'pages/student/css/base.css',
    'pages/teacher/teacher-classes.html',
    'pages/teacher/teacher-gradebook.html',
    'pages/teacher/teacher-grades.html',
    'pages/teacher/teacher-lessons.html',
]

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fl:
        content = fl.read()
    print(f'=== {f} ===')
    for m in re.finditer(r'.{0,100}(?:blob|circular|ripple|hover:bg-|group-hover).{0,100}', content, re.IGNORECASE):
        print('  MATCH:', m.group(0).strip())

