with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('server.py lines:', len(lines))
for i, l in enumerate(lines[:100]):
    print(f'{i+1}: {l}', end='')

