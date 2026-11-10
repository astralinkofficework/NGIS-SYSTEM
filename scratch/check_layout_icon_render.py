with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'sub.icon' in l or 'l.icon' in l or 'g.icon' in l:
        print(f"{i+1}: {l.strip()}")

