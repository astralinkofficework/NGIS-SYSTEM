import os

files = []
for root, dirs, fnames in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated']):
        continue
    for f in fnames:
        if f.endswith(('.css', '.html', '.js')):
            files.append(os.path.join(root, f))

found = []
for path in files:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if 'radial-gradient' in line or 'circle' in line:
                found.append((path, i+1, line.strip()))
    except Exception as e:
        pass

for p, lnum, l in found:
    if any(k in l.lower() for k in ['gradient', 'background', 'hover', 'overlay', 'ripple', 'touch']):
        print(f'{p}:{lnum} -> {l}')

