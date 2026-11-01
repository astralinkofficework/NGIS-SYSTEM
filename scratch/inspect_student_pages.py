import glob, os

files = glob.glob('pages/student/*.html')
for f in sorted(files):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
        title = [l.strip().encode('ascii', 'ignore').decode() for l in lines if '<title>' in l]
        has_hero = any('heroBanner' in l or 'hero.js' in l or 'hero-banner' in l for l in lines)
        has_overlap = any('dash-overlap' in l for l in lines)
        has_sidebar_layout = any('layout.js' in l for l in lines)
        print(f"{os.path.basename(f)}: {len(lines)} lines | title: {title[0] if title else 'None'} | hero: {has_hero} | layout.js: {has_sidebar_layout}")
