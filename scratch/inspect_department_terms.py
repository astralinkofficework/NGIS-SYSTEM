with open(r'pages\shared\department.html', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['Attendance', 'Report Cards', 'Lessons', 'Tasks', 'Exams', 'Timetable']:
    print(term, 'in text:', term in text)

