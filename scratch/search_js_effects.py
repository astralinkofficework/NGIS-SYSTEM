import os, re

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.system_generated' in root:
        continue
    for f in files:
        if f.endswith('.js'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                for keyword in ['ripple', 'circle', 'createRipple', 'radial', 'pointerdown', 'mousedown', 'mousemove', 'overlay', 'cursor', 'hover']:
                    if keyword in content:
                        lines = content.splitlines()
                        for i, l in enumerate(lines):
                            if any(k in l for k in ['ripple', 'createRipple', 'radial', 'pointerdown', 'circle']) and not l.strip().startswith('//'):
                                results.append(f"{path}:{i+1}: {l.strip()}")

print(f"Total hits: {len(results)}")
for r in results[:40]:
    print(r)

