with open('pages/shared/exams.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(70, len(lines)):
    print(f'{i+1}: {lines[i]}', end='')
