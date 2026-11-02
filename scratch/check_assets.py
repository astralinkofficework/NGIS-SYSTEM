import json, os, re

with open('scratch/phase0_inventory.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

missing_assets = []
total_checked = 0

for page in pages:
    fpath = page['path']
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    
    # Find links
    matches = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', html)
    pdir = os.path.dirname(fpath)
    for m in matches:
        if m.startswith(('http://', 'https://', '//', 'data:', 'javascript:', '#', 'mailto:', 'tel:')):
            continue
        if '${' in m or '{' in m:
            continue
        clean = m.split('?')[0].split('#')[0]
        if not clean:
            continue
        total_checked += 1
        # Resolve target
        if clean.startswith('/'):
            target = os.path.normpath(clean.lstrip('/'))
        else:
            target = os.path.normpath(os.path.join(pdir, clean))
        
        if not os.path.exists(target):
            missing_assets.append((fpath, m, target))

print(f"Total assets checked: {total_checked}")
print(f"Missing assets: {len(missing_assets)}")
for p, m, t in missing_assets[:20]:
    print(f"In {p}: missing {m} -> {t}")

