with open('data/sidebar_nav.json', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if '"student"' in line or 'student-calendar' in line or 'student-timetable' in line:
            print(f'{i}: {line.strip()}')
