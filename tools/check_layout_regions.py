with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Lines 2650-2685:')
for i in range(2650, 2686):
    print(f'{i+1}: {lines[i]}', end='')

print('\nLines 3520-3545:')
for i in range(3520, 3546):
    print(f'{i+1}: {lines[i]}', end='')
