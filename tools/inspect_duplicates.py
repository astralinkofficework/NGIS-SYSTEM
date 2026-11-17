import re

files_to_check = [
    'pages/admin/admin-department-detail.html',
    'pages/admin/admin-departments.html',
    'pages/admin/admin-grade-release.html',
    'pages/principal/principal-reports.html',
    'pages/student/student-assignments.html',
    'pages/student/student-calendar.html',
    'pages/student/student-grades.html',
    'pages/student/student-lost-found.html',
    'pages/student/student-notifications.html',
    'pages/student/student-profile.html',
    'pages/student/student-services.html',
    'pages/teacher/teacher-submissions.html'
]

for filepath in files_to_check:
    print(f"=== {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    seen = {}
    for idx, line in enumerate(lines):
        line_s = line.strip()
        m_link = re.search(r'<link[^>]+href=["\']([^"\']+)["\']', line_s)
        m_script = re.search(r'<script[^>]+src=["\']([^"\']+)["\']', line_s)
        key = None
        if m_link:
            key = ('link', m_link.group(1))
        elif m_script:
            key = ('script', m_script.group(1))
        if key:
            if key in seen:
                print(f"  Duplicate: {key[0]} {key[1]} at line {idx+1} (first seen at line {seen[key]})")
            else:
                seen[key] = idx + 1
