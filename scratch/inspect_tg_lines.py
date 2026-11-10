with open('pages/teacher/teacher-gradebook.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(255, 275):
    print(f'{i+1}: {repr(lines[i])}'.encode('ascii', 'replace').decode('ascii'))
