import os

targets = [
    'switchRole',
    'si-subtitle',
    'Manage institutional profile'
]

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.py')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    c = fp.read()
                    for t in targets:
                        if t in c:
                            print(f'Found "{t}" in {p}')
            except Exception:
                pass
print('Search complete.')

