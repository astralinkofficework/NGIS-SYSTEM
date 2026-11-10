pages = [
    'pages/admin/admin-services.html',
    'pages/admin/admin-grade-release.html',
    'pages/admin/admin-attendance.html',
    'pages/admin/admin-grades.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-users.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-submissions.html',
    'pages/teacher/teacher-lessons.html',
    'pages-directory.html',
    'pages/admin/admin-campus.html',
    'pages/admin/admin-exams.html',
    'pages/admin/admin-lessons.html'
]

for p in pages:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"\n==================== {p} ====================")
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if any(k in l.lower() for k in ['actions', 'action-group', 'btn-authorize', 'openmodal', 'btn-edit', 'deletepost', 'openclassdetail', 'link-btn', 'class="action']):
            # print surrounding lines
            start = max(0, i-2)
            end = min(len(lines), i+6)
            for j in range(start, end):
                print(f"  {j+1}: {lines[j].strip()}")
            print("  ---")
            break

