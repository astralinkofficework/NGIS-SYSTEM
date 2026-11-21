with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1220, min(len(lines), 1360)):
    print(f'{i+1}: {lines[i]}', end='')
