import os

target = 'Audit Collision'
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.py')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    if target in content:
                        print(f'Found "{target}" in {p}')
            except Exception:
                pass
print('Done searching for Audit Collision.')

