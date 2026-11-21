with open('pages/shared/lesson-details.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(192, 242):
    print(f'{i+1}: {lines[i]}', end='')
