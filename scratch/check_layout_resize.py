with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[60:130], 61):
    cleaned = l.strip().encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {cleaned}")

