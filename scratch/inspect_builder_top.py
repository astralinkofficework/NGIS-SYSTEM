with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().startswith('function builderHtml('):
        print(f'=== builderHtml (line {i+1}) ===')
        for j in range(i, i+70):
            print(f'{j+1}: {lines[j]}', end='')
        break
