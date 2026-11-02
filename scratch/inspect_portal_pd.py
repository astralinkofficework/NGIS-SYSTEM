with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[200:270], 201):
    cleaned = l.strip().encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {cleaned}")

