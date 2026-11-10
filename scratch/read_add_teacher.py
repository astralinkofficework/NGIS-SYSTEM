with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[7940:7996]):
    print(f"{i+7941}: {line.rstrip()}")

