with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1615, 1655):
    if i < len(lines):
        print(f"{i+1}: {lines[i].rstrip()}")

