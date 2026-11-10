with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('--- Toolbar ---')
for i in range(1170, 1195):
    print(f'{i+1}: {repr(lines[i])}')

print('--- Line 2216 ---')
for i in range(2210, 2225):
    print(f'{i+1}: {repr(lines[i])}')

