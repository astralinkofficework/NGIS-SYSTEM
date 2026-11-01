import os

root_loads = []
assets_loads = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                c = file.read()
                if 'src="layout.js"' in c or "src='layout.js'" in c:
                    root_loads.append(p)
                if 'assets/js/layout.js' in c:
                    assets_loads.append(p)
print('Root layout loads:', len(root_loads))
print('Assets layout loads:', len(assets_loads))

