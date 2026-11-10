import os

missing = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f).replace('\\', '/')
            with open(p, 'r', encoding='utf-8') as fp:
                txt = fp.read()
                if '<header' not in txt:
                    missing.append(p)

print(f'Count missing <header>: {len(missing)}')
for p in missing:
    with open(p, 'r', encoding='utf-8') as fp:
        txt = fp.read()
    has_hb = 'id="heroBanner"' in txt or "id='heroBanner'" in txt
    has_mobile_btn = 'data-action="toggle-sidebar"' in txt
    print(f'{p} | has_hb={has_hb} | has_mobile_btn={has_mobile_btn}')

