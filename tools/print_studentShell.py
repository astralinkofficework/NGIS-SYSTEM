with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function studentShell' in l or 'function renderStudent' in l:
        for j in range(i, min(len(lines), i+35)):
            print(f'{j+1}: {lines[j]}', end='')
