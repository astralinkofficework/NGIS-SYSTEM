with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function mount(' in l or 'const mount =' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i, min(len(lines), i+60)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break

