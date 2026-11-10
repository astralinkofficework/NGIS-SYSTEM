with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1173, 1192):
    print(f'{i+1}: {repr(lines[i])}')

