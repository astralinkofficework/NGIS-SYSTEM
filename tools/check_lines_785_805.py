with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(785, 805):
    print(f'{i+1}: {lines[i]}', end='')
