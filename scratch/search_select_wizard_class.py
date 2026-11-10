with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'select-wizard-class' in l:
        print(f'{i+1}: {l.strip()}')
        for j in range(i+1, min(len(lines), i+15)):
            print(f'{j+1}: {lines[j]}', end='')

