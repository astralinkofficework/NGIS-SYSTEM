with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Last 40 lines of student.html:')
for i in range(max(0, len(lines)-40), len(lines)):
    print(f'{i+1}: {lines[i]}', end='')
