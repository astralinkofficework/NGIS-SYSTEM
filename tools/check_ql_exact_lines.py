with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(805, 855):
    print(f'{i+1}: {lines[i]}', end='')
