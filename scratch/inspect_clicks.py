with open('assets/js/khmer-suite-ui.js', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if "addEventListener('click'" in line or 'addEventListener("click"' in line or 'function onClick(' in line or 'function handleAction(' in line:
            print(f'{i+1}: {line.strip()[:100]}')

