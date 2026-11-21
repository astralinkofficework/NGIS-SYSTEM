import os, glob

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if f.endswith('.js') or f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if 'NGISBookmarks' in c:
                    print(f"{p}: mentions NGISBookmarks")
