with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function openNewRequestModal' in l:
        for j in range(max(0, i-5), min(len(lines), i+60)):
            print(f'{j+1}: {lines[j]}', end='')
        break
