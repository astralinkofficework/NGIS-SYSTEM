with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="reportModal"' in l:
        print(f'reportModal starts at line {i+1}:')
        for j in range(i, min(len(lines), i+80)):
            print(f'{j+1}: {lines[j]}', end='')
        break
