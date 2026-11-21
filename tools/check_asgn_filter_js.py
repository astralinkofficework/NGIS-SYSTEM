with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1400, min(len(lines), 1560)):
    print(f'{i+1}: {lines[i]}', end='')
