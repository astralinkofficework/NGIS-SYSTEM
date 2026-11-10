import os

targets = ['principal-records.html', 'admin-records.html', 'principal-records', 'admin-records']

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.py', '.json', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    c = fp.read()
                    for t in targets:
                        if t in c:
                            results.append((t, p))
            except Exception:
                pass

print(f'Total matches found: {len(results)}')
for t, p in sorted(set(results)):
    print(f' - Found "{t}" in {p}')

