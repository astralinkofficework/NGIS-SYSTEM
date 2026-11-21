with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Lines 20-45:')
for i in range(20, 45):
    print(f'{i+1}: {lines[i]}', end='')

for i, l in enumerate(lines):
    if 'async function reload' in l:
        print(f'\nreload starts at {i+1}:')
        for j in range(i, min(len(lines), i+30)):
            print(f'{j+1}: {lines[j]}', end='')
        break
