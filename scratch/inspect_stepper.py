with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'workflowStepperHtml' in line:
        print(f'{i+1}: {line}', end='')
        for j in range(i+1, i+40):
            print(f'{j+1}: {lines[j]}', end='')
        break

