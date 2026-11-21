with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(975, min(len(lines), 1015)):
    print(f'{i+1}: {lines[i]}', end='')
