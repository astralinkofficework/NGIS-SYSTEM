with open('assets/css/school-information.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'si-title' in l or 'si-subtitle' in l:
        print(f'{i+1}: {l.strip()[:100]}')

