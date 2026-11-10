with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1030, min(1065, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

