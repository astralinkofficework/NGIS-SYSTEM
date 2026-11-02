import glob

for f in sorted(glob.glob('pages/principal/*.html')):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    print(f, ':')
    print('  has aside:', '<aside' in c)
    print('  has id="sidebar":', 'id="sidebar"' in c)
    print('  has heroBanner:', 'heroBanner' in c)
    print('  has layout.js:', 'layout.js' in c)

