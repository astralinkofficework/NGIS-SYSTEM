import re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# rgba() green-family -> orange/ink DNA family (whitespace-tolerant)
PAIRS = [
  (r'rgba\(\s*23\s*,\s*107\s*,\s*69', 'rgba(247, 116, 66'),
  (r'rgba\(\s*18\s*,\s*86\s*,\s*56',  'rgba(224, 82, 31'),
  (r'rgba\(\s*41\s*,\s*53\s*,\s*46',  'rgba(29, 29, 27'),
  (r'rgba\(\s*100\s*,\s*116\s*,\s*106', 'rgba(117, 115, 113'),
  (r'rgba\(\s*143\s*,\s*160\s*,\s*149', 'rgba(157, 154, 151'),
  (r'rgba\(\s*232\s*,\s*243\s*,\s*237', 'rgba(253, 235, 223'),
  (r'rgba\(\s*225\s*,\s*233\s*,\s*227', 'rgba(236, 231, 226'),
]
pats = [(re.compile(p, re.I), r) for p, r in PAIRS]

files = sorted(glob.glob('pages/admin/*.html')) + ['assets/css/admin-view.css']
total = 0
for f in files:
    t = open(f, encoding='utf-8').read()
    n = 0
    for p, r in pats:
        t, k = p.subn(r, t)
        n += k
    if n:
        open(f, 'w', encoding='utf-8').write(t)
        total += n
        print(f'{os.path.basename(f):38} {n}')
print('total rgba swaps:', total)
