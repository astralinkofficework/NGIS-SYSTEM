with open('pages/shared/js/lesson-details.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(25, 45):
    print(f'{i+1}: {lines[i]}', end='')
