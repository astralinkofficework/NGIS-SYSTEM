with open('assets/js/khmer-suite-ui.js', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'cell' in line and ('act' in line or 'dataset' in line or 'handleClick' in line or 'onClick' in line):
            print(f'{i+1}: {line.strip()[:100]}')

