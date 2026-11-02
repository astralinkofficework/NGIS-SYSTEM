import sys
with open('assets/css/shared-components.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(360, min(440, len(lines))):
    sys.stdout.buffer.write(f"{i+1}: {lines[i]}".encode('utf-8'))

