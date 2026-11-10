import glob, re

files = [
    'pages/admin/admin-assignments.html',
    'pages/admin/admin-attendance.html',
    'pages/admin/admin-campus.html',
    'pages/admin/admin-classes.html',
    'pages/admin/admin-department-detail.html',
    'pages/admin/admin-exams.html',
    'pages/admin/admin-grades.html',
    'pages/admin/admin-lessons.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-reports.html',
    'pages/admin/admin-services.html',
    'pages/admin/admin-timetables.html',
    'pages/teacher/teacher-gradebook.html',
    'pages/teacher/teacher-lessons.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-submissions.html',
    'pages/student/student-assignments.html'
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # find table actions column
    print(f"\n==================== {fpath} ====================")
    matches = re.findall(r'<td[^>]*class="[^"]*(?:table-actions|text-right)[^"]*"[^>]*>(.*?)</td>', content, re.DOTALL)
    if matches:
        for m in matches[:3]:
            # clean up
            lines = [l.strip() for l in m.strip().split('\n') if l.strip()]
            print("  STATIC/TEMPLATE TD:")
            print("   ", ' '.join(lines)[:150])
    
    # Also find in JS scripts where render... produces td
    js_tds = re.findall(r'<td[^>]*class=[^>]*table-actions[^>]*>(.*?)</td>', content, re.DOTALL)
    # also check if any buttons have text
    pills = re.findall(r'action-btn-pill', content)
    if pills:
        print(f"  --> HAS {len(pills)} action-btn-pill")

