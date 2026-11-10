with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(920, 1020):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')

