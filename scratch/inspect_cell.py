with open('assets/js/khmer-suite-ui.js', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'local.targetKey' in line or "data-act='cell'" in line or 'data-act="cell"' in line:
            print(f'{i+1}: {line.strip()[:100]}')

