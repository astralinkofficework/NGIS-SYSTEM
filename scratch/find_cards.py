import re

paths = [
    'pages/student/student.html',
    'pages/principal/principal.html',
    'pages/teacher/teacher.html',
    'pages/admin/admin.html',
    'pages/teacher/teacher-classes.html',
    'pages/shared/lessons.html'
]

for path in paths:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    cards = re.findall(r'<[a-zA-Z0-9\-]+[^>]+class=["\'][^"\']*(?:card|stat|panel|module|hub|box)[^"\']*["\'][^>]*>', c)
    print(f'{path}: {len(cards)} card elements')
    for card in cards[:5]:
        print('  ', card[:120])

