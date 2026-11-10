with open('assets/js/khmer-suite-ui.js', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if '<style' in line or 'style.textContent' in line or 'createElement' in line:
            print(f'{i+1}: {line.strip()[:100]}')

