import glob, os, re

files = [
    'pages/principal/principal-classes.html',
    'pages/principal/principal-departments.html',
    'pages/principal/principal-attendance.html',
    'pages/principal/principal-teacher-profiles.html',
    'pages/principal/principal-student-profiles.html',
    'pages/principal/principal-services.html',
    'pages/principal/principal-reports.html',
    'pages/principal/principal-activity.html',
    'pages/principal/principal-school-information.html',
    'pages/principal/principal-timetables.html',
    'pages/principal/principal-timetable-builder.html'
]

for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    print('==============================')
    print('FILE:', f)
    # find where title is rendered
    h1 = re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', c)
    if h1:
        print('H1:', re.sub(r'\s+', ' ', h1[0]).strip()[:150])
    # check for .page or mobile header
    has_page = 'class="page"' in c or 'class="page ' in c
    has_mobile_hdr = 'data-action="toggle-sidebar"' in c
    print(f'has .page: {has_page}, has mobile header: {has_mobile_hdr}')
    # check how main content is wrapped
    m = re.search(r'<main[^>]*>([\s\S]*?)(?:<div class="card|<div class="grid|<div id=|<table)', c)
    if m:
        preview = re.sub(r'\s+', ' ', m.group(1)).strip()[:300]
        print('Header area:', preview)

