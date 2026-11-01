import glob, os, re

files = [
    'student-assignments.html',
    'student-exams.html',
    'student-timetable.html',
    'student-calendar.html',
    'student-announcements.html',
    'student-services.html',
    'student-notifications.html',
    'student-profile.html',
    'student-id.html',
    'student-clubs.html',
    'student-lost-found.html'
]

for fname in files:
    path = os.path.join('pages/student', fname)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    body_match = re.search(r'<body[^>]*>', c)
    body_tag = body_match.group(0) if body_match else 'None'
    has_page_div = '<div class="page' in c or '<div class="page ' in c or '<main class="page' in c
    has_dup_mobile = 'mobile-hamburger-btn' in c and '<div id="heroBanner">' in c
    has_stat_strip = 'stat-grid' in c or 'class="stat' in c
    print(f"=== {fname} ===")
    print(f"  Body: {body_tag}")
    print(f"  Has page div: {has_page_div}")
    print(f"  Has duplicate mobile bar: {has_dup_mobile}")
    print(f"  Has stats: {has_stat_strip}")

