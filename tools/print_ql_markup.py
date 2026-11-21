with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Quick Links' in l:
        for j in range(max(0, i-5), min(len(lines), i+65)):
            print(f'{j+1}: {lines[j]}', end='')
        break
