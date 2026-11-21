with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(745, min(len(lines), 810)):
    print(f'{i+1}: {lines[i]}', end='')
