with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:120]):
    if 'DIR' in line or 'upload' in line.lower() or 'static' in line.lower():
        print(f"Line {i+1}: {line.strip()}")

