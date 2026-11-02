import os, re, sys

results = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.system_generated' in root:
        continue
    for f in files:
        if f.endswith('.css'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                lines = content.splitlines()
                for i, l in enumerate(lines):
                    for kw in ['radial-gradient', 'radial', 'ripple', 'tap-highlight', 'backdrop-filter', 'mask', 'clip-path']:
                        if kw in l.lower():
                            results.append(f"{path}:{i+1}: {l.strip()}")

for r in results:
    sys.stdout.buffer.write((r + '\n').encode('utf-8'))

