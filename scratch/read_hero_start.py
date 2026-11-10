with open('assets/js/hero.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(0, min(80, len(lines))):
    print(f'{i+1}: {lines[i]}', end='')

