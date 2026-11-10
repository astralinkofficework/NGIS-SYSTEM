with open('pages/teacher/teacher-gradebook.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<h1' in l or 'page-title' in l:
        start = max(0, i-2)
        end = min(len(lines), i+3)
        for j in range(start, end):
            print(f'{j+1}: {lines[j].strip()}'.encode('ascii', 'replace').decode('ascii'))

