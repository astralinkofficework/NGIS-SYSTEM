with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Universal Drawer & Modal delegation' in l:
        for j in range(i, min(len(lines), i+60)):
            print(f'{j+1}: {lines[j]}', end='')
        break
