with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'nav-link-icon' in l or 'nav-group-icon' in l or 'nav-icon' in l:
        print(f"{i+1}: {l.strip()}")

