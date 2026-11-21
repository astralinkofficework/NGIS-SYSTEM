with open('pages/shared/lesson-details.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(5, 25):
    print(f'{i+1}: {lines[i]}', end='')
