with open('pages/student/student-grades.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')
print('From line 180 to 220:')
for i in range(180, 220):
    print(f'{i+1}: {lines[i]}', end='')
print('\nFrom line 720 to end:')
for i in range(720, len(lines)):
    print(f'{i+1}: {lines[i]}', end='')
