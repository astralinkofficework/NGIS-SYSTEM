import re

files = [
    'pages/principal/principal-school-information.html',
    'pages/principal/principal-timetables.html',
    'pages/principal/principal-timetable-builder.html',
    'pages/principal/principal-subjects.html',
    'pages/principal/principal-classes.html',
    'pages/admin/admin-teacher-class-assignment.html'
]

for f in files:
    print('==============================')
    print('FILE:', f)
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # check heroBanner or title section
    h1_match = re.findall(r'<h1[\s\S]*?</h1>', c)
    if h1_match:
        print('H1:', h1_match[0][:200])
    # check title section div
    div_match = re.findall(r'(?:<div class="[^"]*page-header[^"]*"|<div class="[^"]*title[^"]*"|<div class="[^"]*flex items-center justify-between[^"]*")[\s\S]*?</div>', c)
    if div_match:
        print('Header DIV:', div_match[0][:200])
    
    # check main tag and immediate children
    m = re.search(r'<main[^>]*>([\s\S]*?)</main>', c)
    if m:
        main_content = m.group(1).strip()
        lines = [line.strip() for line in main_content.split('\n') if line.strip()][:15]
        print('Main head:\n  ' + '\n  '.join(lines))

