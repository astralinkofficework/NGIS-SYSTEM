import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.extend(glob.glob('*.html'))

has_herobanner_div = []
has_hero_js = []
missing_hero_js = []

for p in sorted(pages):
    norm_p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_div = 'id="heroBanner"' in content or 'id=\'heroBanner\'' in content
    has_js = 'hero.js' in content
    
    if has_div:
        has_herobanner_div.append(norm_p)
    if has_js:
        has_hero_js.append(norm_p)
    if has_div and not has_js:
        missing_hero_js.append(norm_p)

print(f"Pages with id='heroBanner' div: {len(has_herobanner_div)}")
print(f"Pages with hero.js script: {len(has_hero_js)}")
print(f"Pages with id='heroBanner' but MISSING hero.js: {len(missing_hero_js)}")
for p in missing_hero_js:
    print('  ', p)

