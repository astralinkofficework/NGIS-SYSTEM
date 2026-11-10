with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'h1' in l.lower() or 'si-subtitle' in l or 'switchrole' in l.lower() or 'persona' in l.lower():
        print(f'{i+1}: {l.strip()[:120]}')

