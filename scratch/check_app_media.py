with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'max-width: 1024px' in l or 'max-width: 768px' in l:
        cleaned = l.strip().encode('ascii', errors='replace').decode('ascii')
        print(f"{i}: {cleaned}")

