with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(630, 670):
    if i < len(lines):
        print(f"{i+1}: {lines[i].rstrip()}")

