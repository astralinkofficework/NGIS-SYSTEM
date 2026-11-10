with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[7996:8060]):
    print(f"{i+7997}: {line.rstrip()}")

