import os, re

missing = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f).replace('\\', '/')
            with open(p, 'r', encoding='utf-8') as fp:
                txt = fp.read()
                if '<header' not in txt:
                    missing.append(p)

for p in missing:
    with open(p, 'r', encoding='utf-8') as fp:
        txt = fp.read()
    hb_matches = re.findall(r'<div[^>]*id=["\']heroBanner["\'][^>]*>.*?</div>', txt, flags=re.DOTALL)
    print(f"{p}: {hb_matches}")

