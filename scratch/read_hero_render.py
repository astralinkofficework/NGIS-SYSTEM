with open('assets/js/hero.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(110, 160):
    print(f'{i+1}: {lines[i]}', end='')

