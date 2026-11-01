with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[-35:]
print(''.join(lines).encode('ascii', errors='replace').decode('ascii'))
