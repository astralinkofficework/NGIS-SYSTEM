with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1540, 1570):
    print(f'{i+1}: {lines[i]}', end='')

