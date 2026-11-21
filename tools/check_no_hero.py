import glob

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
no_hero = []

for path in html_files:
    content = open(path, encoding='utf-8', errors='ignore').read()
    if 'id="heroBanner"' not in content and 'heroBanner' not in content:
        no_hero.append(path)

print(f"Pages without heroBanner: {len(no_hero)}")
for p in sorted(no_hero):
    print(" -", p)
