with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(714, 765):
    print(f'{i+1}: {lines[i]}', end='')

