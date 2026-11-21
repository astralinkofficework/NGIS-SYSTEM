with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(363, 400):
    print(f'{i+1}: {lines[i]}', end='')
