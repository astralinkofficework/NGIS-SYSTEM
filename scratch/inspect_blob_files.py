import os

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
        lines = fl.readlines()
    print(f'=== {f} ===')
    for i, line in enumerate(lines):
        if 'ROUNDED COLORED' in line or ('hover' in line and 'blob' in line):
            start = max(0, i - 5)
            end = min(len(lines), i + 25)
            print(''.join(lines[start:end]))
            print('-'*40)

