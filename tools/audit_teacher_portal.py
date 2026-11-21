import os, re

pages = [
    'pages/teacher/teacher.html',
    'pages/teacher/teacher-submissions.html',
    'pages/teacher/teacher-attendance.html',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-lessons.html',
    'pages/teacher/teacher-exams.html',
    'pages/teacher/teacher-services.html',
    'pages/teacher/teacher-lost-found.html',
    'pages/teacher/teacher-calendar.html',
    'pages/teacher/teacher-departments.html',
    'pages/teacher/teacher-documents.html',
    'pages/teacher/teacher-gradebook.html'
]

for p in pages:
    if not os.path.exists(p):
        print('MISSING:', p)
        continue
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    bolds = len(re.findall(r'font-bold|font-extrabold|font-black', content))
    modals = len(re.findall(r'id=["\'][^"\']*modal[^"\']*["\']', content, re.IGNORECASE))
    scripts = len(re.findall(r'<script', content, re.IGNORECASE))
    print(f'{p}: size={len(content)}, bolds={bolds}, modals={modals}, scripts={scripts}')
