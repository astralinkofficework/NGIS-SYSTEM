with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[8010:8055]):
    print(f"{i+8011}: {line.rstrip()}")

