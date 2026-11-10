with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[7904:7940]):
    print(f"{i+7905}: {line.rstrip()}")

