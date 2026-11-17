files = [
    'pages/admin/admin-services.html',
    'pages/admin/admin-timetables.html',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-submissions.html'
]

for f in files:
    with open(f, encoding='utf-8') as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines, 1):
            if '<h1' in line:
                print(f"{f}:{i}: {line.strip()[:80]}")
