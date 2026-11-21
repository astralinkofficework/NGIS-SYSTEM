with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(540, min(len(lines), 750)):
    print(f'{i+1}: {lines[i]}', end='')
