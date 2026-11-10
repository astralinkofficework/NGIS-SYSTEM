def inspect_snippet(filename, keyword, length=500):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    idx = text.find(keyword)
    if idx != -1:
        start = max(0, idx - 100)
        print(f"=== {filename} ({keyword}) ===")
        print(text[start:start+length])
        print("------------------------------------------")

inspect_snippet('pages/admin/admin-services.html', 'openModal')
inspect_snippet('pages/admin/admin-grade-release.html', 'btn-authorize')
inspect_snippet('pages/admin/admin-attendance.html', 'openOverrideModal')
inspect_snippet('pages/admin/admin-grades.html', 'openOverrideModal')
inspect_snippet('pages/admin/admin-campus.html', 'link-btn')
inspect_snippet('pages/admin/admin-news.html', 'deletePost')
inspect_snippet('pages/teacher/teacher-reports.html', 'publishSingle')
inspect_snippet('pages/teacher/teacher-submissions.html', 'submissionsTableBody')
inspect_snippet('pages/teacher/teacher-lessons.html', 'lessonsTbody')
inspect_snippet('pages-directory.html', 'btn-primary btn-sm')

