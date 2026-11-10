import glob

files = glob.glob('pages/**/*.html', recursive=True)

by_category = {
    'has_hero_js': [],
    'has_hero_banner_tag': [],
    'has_hero_topbar_html': [],
    'missing_everything': []
}

for f in sorted(files):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    hero_js = 'hero.js' in c
    hero_banner = 'id="heroBanner"' in c or "id='heroBanner'" in c
    hero_topbar = 'hero-topbar' in c
    
    if hero_js and hero_banner:
        by_category['has_hero_js'].append(f)
    elif hero_topbar:
        by_category['has_hero_topbar_html'].append(f)
    elif hero_banner:
        by_category['has_hero_banner_tag'].append(f)
    else:
        by_category['missing_everything'].append(f)

print(f"Total files: {len(files)}")
print(f"Has hero.js + heroBanner: {len(by_category['has_hero_js'])}")
print(f"Has raw hero-topbar html: {len(by_category['has_hero_topbar_html'])}")
print(f"Has heroBanner tag only: {len(by_category['has_hero_banner_tag'])}")
print(f"Missing everything: {len(by_category['missing_everything'])}")

print("\n--- Missing Everything ---")
for f in by_category['missing_everything']:
    print(" ", f)

print("\n--- Has raw hero-topbar html ---")
for f in by_category['has_hero_topbar_html']:
    print(" ", f)

