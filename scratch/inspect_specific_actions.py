import glob, re

files = [
    'pages/admin/admin-campus.html',
    'pages/admin/admin-campuses.html',
    'pages/admin/admin-grade-release.html',
    'pages/admin/admin-services.html',
    'pages/admin/admin-department-detail.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-users.html',
    'pages/principal/principal-classes.html',
    'pages/principal/principal-departments.html',
    'pages/principal/principal-timetables.html',
    'pages/principal/principal-reports.html',
    'pages/principal/principal-services.html',
    'pages/principal/principal-lost-found.html',
    'pages/principal/principal-teacher-profiles.html',
    'pages/principal/principal-student-profiles.html',
    'pages/student/student-lost-found.html',
    'pages/student/student-assignments.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-submissions.html',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-lessons.html',
    'pages/teacher/teacher-services.html',
    'pages-directory.html'
]

for path in files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n==================== {path} ====================")
        # Search for table headers
        ths = re.findall(r'<th[^>]*>(.*?)</th>', content, re.DOTALL | re.IGNORECASE)
        print("Headers:", [re.sub(r'<[^>]+>', '', t).strip() for t in ths])
        
        # Search for action button snippets in JS or HTML
        action_snippets = re.findall(r'(?:<td[^>]*class=["\'][^"\']*actions?[^"\']*["\'][^>]*>.*?</td>|class=["\']action-group["\'].*?</div>|btn-authorize.*?button|<button[^>]*class=["\'][^"\']*btn[^"\']*["\'][^>]*>.*?</button>)', content, re.DOTALL | re.IGNORECASE)
        print(f"Action snippets found: {len(action_snippets)}")
        for s in action_snippets[:4]:
            print("  ->", ' '.join(s.split())[:130])
    except Exception as e:
        print(f"Error reading {path}: {e}")

