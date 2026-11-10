with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'si-subtitle' in l or 'subtitle' in l.lower() or 'manage institutional' in l.lower():
        print(f'{i+1}: {l.strip()[:120]}')

