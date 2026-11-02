with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[2868:2910]):
    print(f'{i+2869}: {l.strip().encode("ascii", errors="replace").decode("ascii")}')
