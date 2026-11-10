import glob, re

targets = [
    'pages/admin/admin-grade-release.html',
    'pages/admin/admin-services.html',
    'pages/admin/admin-attendance.html',
    'pages/admin/admin-grades.html',
    'pages/admin/admin-campus.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-users.html',
    'pages/admin/admin-exams.html',
    'pages/admin/admin-lessons.html',
    'pages/principal/principal-services.html',
    'pages/principal/principal-lost-found.html',
    'pages/principal/principal-reports.html',
    'pages/principal/principal-timetables.html',
    'pages/student/student-lost-found.html',
    'pages/student/student-assignments.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-submissions.html',
    'pages/teacher/teacher-lessons.html',
    'pages/teacher/teacher-roster.html',
    'pages-directory.html'
]

for p in targets:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    print(f"\n==================== {p} ====================")
    # find table headers with action
    th_match = re.search(r'<th[^>]*>.*?(?:action|manage|operation|opt).*?</th>', text, re.IGNORECASE)
    if th_match:
        print("Action TH:", th_match.group(0))
    # find where tbody is populated or table rows
    rows = re.findall(r'<td[^>]*class=["\'][^"\']*(?:action|table-action|btn)[^"\']*["\'][^>]*>(.*?)</td>', text, re.DOTALL | re.IGNORECASE)
    if rows:
        print(f"Matched TD by class ({len(rows)}):")
        for r in rows[:3]:
            print("  ", ' '.join(r.split())[:140])
    else:
        # search for innerHTML row template
        row_templates = re.findall(r'<tr>(.*?)</tr>', text, re.DOTALL | re.IGNORECASE)
        last_tds = []
        for row in row_templates:
            tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
            if tds:
                last_tds.append(' '.join(tds[-1].split()))
        if last_tds:
            print(f"Last TDs in rows ({len(last_tds)}):")
            for ltd in last_tds[:4]:
                print("  ", ltd[:140])

