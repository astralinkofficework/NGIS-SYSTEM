with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j, l in enumerate(lines):
    if "ROLE === 'student'" in l or 'function render' in l:
        print(f'{j+1}: {l.strip()[:100]}')
