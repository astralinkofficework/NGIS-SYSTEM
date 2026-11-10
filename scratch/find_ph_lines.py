with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'ph-' in l or 'ph ' in l:
        print(f"{i+1}: {l.strip()}")

