import glob, os, re

paths = [
    'pages/principal/principal-school-information.html',
    'pages/principal/principal-timetables.html',
    'pages/principal/principal-timetable-builder.html',
    'pages/principal/principal-subjects.html',
    'pages/principal/principal-classes.html',
    'pages/principal/principal-teacher-class-assignment.html'
]

for p in paths:
    print('==============================')
    print('FILE:', p)
    if not os.path.exists(p):
        print('NOT FOUND')
        continue
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()
    main_match = re.search(r'<body[^>]*>([\s\S]*?)<script', html)
    if main_match:
        print(main_match.group(1).strip()[:600])

