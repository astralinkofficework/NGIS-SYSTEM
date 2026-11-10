with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<h1' in l or 'h1' in l:
        print(f'{i+1}: {l.strip()[:100]}')

