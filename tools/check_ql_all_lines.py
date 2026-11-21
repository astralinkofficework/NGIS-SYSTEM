with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(h in l for h in ['student-assignments.html', 'student-timetable.html', 'student-grades.html', '../shared/lessons.html']):
        print(f'{i+1}: {l.strip()[:90]}')
