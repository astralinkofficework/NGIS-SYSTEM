import sys
with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(0, min(150, len(lines))):
    sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode('utf-8'))

