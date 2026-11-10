with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1019, min(1060, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

