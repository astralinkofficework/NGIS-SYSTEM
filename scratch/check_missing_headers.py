import os

all_html = []
for root, dirs, files in os.walk('.'):
    if any(ignore in root for ignore in ['node_modules', '.git', '.gemini', '.agents', 'dist', 'build']):
        continue
    for f in files:
        if f.endswith('.html'):
            all_html.append(os.path.join(root, f).replace('\\', '/'))

print(f"Total HTML files found: {len(all_html)}")

missing = []
for p in all_html:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    has_topbar = 'hero-topbar' in c
    has_banner = 'heroBanner' in c
    has_hero_js = 'hero.js' in c
    if not (has_topbar or has_banner or has_hero_js):
        missing.append(p)

print(f"\nMissing hero-topbar / heroBanner / hero.js ({len(missing)} files):")
for m in missing:
    print(f"  {m}")

