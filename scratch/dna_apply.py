import re, sys, glob, os, filecmp, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LINK = '<link rel="stylesheet" href="../../assets/css/admin-dna.css?v=1.0">'
ok = miss = skip = 0
for f in sorted(glob.glob('pages/admin/*.html')):
    t = open(f, encoding='utf-8').read()
    if 'admin-dna.css' in t:
        skip += 1
        continue
    new = None
    m = re.search(r'(<link[^>]*design-system\.css[^>]*>)', t)
    if m:
        new = t[:m.end(1)] + '\n' + LINK + t[m.end(1):]
    else:
        m = re.search(r'(<link[^>]*app\.css[^>]*>)', t)
        if m:
            new = t[:m.end(1)] + '\n' + LINK + t[m.end(1):]
    if new is None:
        miss += 1
        print('MISS (no anchor):', f)
        continue
    open(f, 'w', encoding='utf-8').write(new)
    ok += 1
    print('OK :', os.path.basename(f))
print(f'\nlinked={ok} already={skip} no-anchor={miss}')

shutil.copyfile('assets/js/layout.js', 'layout.js')
print('mirror identical:', filecmp.cmp('assets/js/layout.js', 'layout.js', shallow=False))
