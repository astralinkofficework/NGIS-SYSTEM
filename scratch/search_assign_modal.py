with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'open-assign-modal' in l or 'm.type' in l:
        print(f'{i+1}: {l.strip()[:100]}')

