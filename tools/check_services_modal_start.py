with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(845, 875):
    print(f'{i+1}: {lines[i]}', end='')
