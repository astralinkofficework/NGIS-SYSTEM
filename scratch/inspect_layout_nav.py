with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:300]):
    if any(k in line for k in ['NAV', 'MENU', 'sidebar', 'items', 'student', 'teacher', 'admin', 'principal', 'staff', 'role']):
        print(f'{i+1}: {line.strip()[:100]}')

