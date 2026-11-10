import glob

for f in sorted(glob.glob('pages/principal/*.html')):
    src = open(f, encoding='utf-8', errors='replace').read()
    print(
        f.split('\\')[-1].ljust(32),
        'heroBanner:', 'id="heroBanner"' in src,
        '| hero.js:', 'js/hero.js' in src,
        '| HERO_CONFIG:', 'HERO_CONFIG' in src,
        '| hamburger:', 'toggle-sidebar' in src,
        '| layout.js:', 'js/layout.js' in src,
    )
