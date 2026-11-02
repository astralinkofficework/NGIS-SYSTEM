with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lines = text.split('\n')
for i, l in enumerate(lines[:60]):
    print(f'{i+1}: {l}')

