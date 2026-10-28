with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "'classes': [" in l or '"classes": [' in l:
        print(f"Line {i+1}: {l.strip()}")
        for j in range(i+1, min(i+40, len(lines))):
            print(f"  {lines[j].strip()}")
