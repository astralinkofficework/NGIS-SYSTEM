with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('reload lines:')
for i in range(120, 165):
    print(f'{i+1}: {lines[i]}', end='')

print('\nfilteredExams lines:')
for i in range(330, 365):
    print(f'{i+1}: {lines[i]}', end='')
