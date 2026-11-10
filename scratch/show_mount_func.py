with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2780, min(2830, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')

