import re

pages = [
    'pages/admin/admin-grade-release.html',
    'pages/admin/admin-services.html',
    'pages/admin/admin-attendance.html',
    'pages/admin/admin-grades.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-users.html',
    'pages/principal/principal-services.html',
    'pages/principal/principal-lost-found.html',
    'pages/student/student-lost-found.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-submissions.html',
    'pages/teacher/teacher-lessons.html',
    'pages-directory.html'
]

for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    print(f"\n==================== {p} ====================")
    # Search for renderTable, renderRows, tbody.innerHTML, etc.
    matches = re.findall(r'(function\s+\w*render\w*\(.*?\)\s*\{.*?return.*?\n\})', text, re.DOTALL)
    if not matches:
        matches = re.findall(r'(tbody\w*\.innerHTML\s*=\s*.*?;)', text, re.DOTALL)
    if not matches:
        matches = re.findall(r'(\.map\([^{]*?=>\s*`.*?<\/tr>.*?`\))', text, re.DOTALL)
    for m in matches[:2]:
        print(' '.join(m.split())[:200])

