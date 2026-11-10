with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2700, 2780):
    print(f'{i+1}: {lines[i]}', end='')

