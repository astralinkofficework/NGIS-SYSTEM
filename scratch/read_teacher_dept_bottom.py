with open('pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[-60:]
for i, l in enumerate(lines):
    print(f'{i+1}: {l.strip()[:90]}'.encode('ascii', errors='replace').decode('ascii'))

