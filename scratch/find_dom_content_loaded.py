with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'document.addEventListener("DOMContentLoaded"' in l or "document.addEventListener('DOMContentLoaded'" in l or 'init()' in l:
        print(f'{i+1}: {l}')

