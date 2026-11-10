with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function modalHtml(' in l:
        print(f'=== modalHtml (line {i+1}) ===')
        for j in range(i, i+60):
            print(f'{j+1}: {lines[j]}', end='')
        break

