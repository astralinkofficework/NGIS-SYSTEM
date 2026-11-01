import os, re

PAGES_CONFIG = {
    'student-exams.html': {
        'title': 'Examinations & Assessments',
        'greeting': 'Official exam schedule, hall allocations, seat assignments, and results',
        'active': 'exams'
    },
    'student-timetable.html': {
        'title': 'Weekly Class Timetable',
        'greeting': 'Academic schedule, course periods, classroom locations, and instructors',
        'active': 'timetable'
    },
    'student-calendar.html': {
        'title': 'Academic & Campus Calendar',
        'greeting': 'Scheduled school events, examination windows, campus activities, and holidays',
        'active': 'calendar'
    },
    'student-announcements.html': {
        'title': 'Official Announcements & Circulars',
        'greeting': 'School notifications, campus news, academic bulletins, and alerts',
        'active': 'announcements'
    },
    'student-services.html': {
        'title': 'Student Services & Support Hub',
        'greeting': 'Official document requests, student support, counseling, and campus facilities',
        'active': 'services'
    },
    'student-notifications.html': {
        'title': 'Notifications & Communications',
        'greeting': 'Campus alerts, instructor communications, and activity notifications',
        'active': 'notifications'
    },
    'student-profile.html': {
        'title': 'Student Profile & Credentials',
        'greeting': 'Personal credentials, academic standing, enrollment history, and contact info',
        'active': 'profile'
    },
    'student-id.html': {
        'title': 'Digital Student ID Card',
        'greeting': 'Official student credential, library card barcode, and campus access pass',
        'active': 'id'
    },
    'student-clubs.html': {
        'title': 'Student Clubs & Co-Curricular',
        'greeting': 'Campus clubs, student leadership, extracurricular activities, and events',
        'active': 'clubs'
    },
    'student-lost-found.html': {
        'title': 'Campus Lost & Found Hub',
        'greeting': 'Report lost personal items, browse discovered campus articles, and claim belongings',
        'active': 'lost-found'
    }
}

css_block = '''<link rel="stylesheet" href="../../assets/css/app.css?v=3.0">
<link rel="stylesheet" href="../../assets/css/mvp-redesign.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="css/overlap.css">
<link rel="stylesheet" href="css/responsive.css">
<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/ui-states.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">'''

for fname, cfg in PAGES_CONFIG.items():
    path = os.path.join('pages/student', fname)
    if not os.path.exists(path):
        print(f"Skipping {fname}: file not found")
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    # 1. Update css links in head
    if '../../assets/css/app.css?v=3.0' not in c:
        if '<link rel="stylesheet" href="../../assets/css/app.css">' in c:
            c = c.replace('<link rel="stylesheet" href="../../assets/css/app.css">', css_block)
        elif '</head>' in c:
            c = c.replace('</head>', css_block + '\n</head>')

    # 2. Update body tag to student-dashboard
    c = re.sub(r'<body([^>]*)>', r'<body data-page="student" data-role="student" class="student-dashboard\1">', c, count=1)
    # clean duplicate class or data-role if already present
    c = re.sub(r'class="student-dashboard([^"]*)\s+class="([^"]*)"', r'class="student-dashboard \1 \2"', c)
    c = re.sub(r'data-role="[^"]*"\s+data-role="student"', 'data-role="student"', c)
    c = re.sub(r'data-page="[^"]*"\s+data-page="student"', 'data-page="student"', c)

    # 3. Replace assets/js/hero.js with js/hero.js
    c = c.replace('<script src="../../assets/js/hero.js"></script>', '<script src="js/hero.js"></script>')

    # 4. Remove duplicate mobile topbars
    c = re.sub(r'<div class="lg:hidden bg-white border-b.*?</div>\s*</div>', '', c, flags=re.DOTALL)

    # 5. Replace page container with subpage-container
    c = c.replace('class="page space-y-7"', 'class="subpage-container space-y-7"')
    c = c.replace('class="page space-y-8"', 'class="subpage-container space-y-8"')
    c = c.replace('class="page space-y-9"', 'class="subpage-container space-y-9"')
    c = c.replace('class="page"', 'class="subpage-container"')
    c = c.replace('class="sh-unified-view', 'class="sh-unified-view subpage-container')
    c = c.replace('id="student-lostfound-main"', 'id="student-lostfound-main" class="subpage-container"')

    # 6. Ensure HERO_CONFIG has the title and greeting
    hero_cfg_snippet = f'''window.PAGE = {{"role":"student","active":"{cfg['active']}"}};
window.HERO_CONFIG = {{
  title: '{cfg['title']}',
  greeting: '{cfg['greeting']}',
'''
    if 'window.HERO_CONFIG = {' in c:
        c = c.replace('window.HERO_CONFIG = {', hero_cfg_snippet, 1)
    elif '<script src="js/hero.js"></script>' in c:
        c = c.replace('<script src="js/hero.js"></script>', f'<script>\n{hero_cfg_snippet}}};\n</script>\n<script src="js/hero.js"></script>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Transformed {fname} -> {cfg['title']}")

print("All student subpages processed.")

