with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'document.body.insertBefore' in l or 'document.body.prepend' in l or 'sidebar' in l and 'appendChild' in l or 'buildSidebar' in l:
        print(f'{i+1}: {l.strip()[:100]}')

