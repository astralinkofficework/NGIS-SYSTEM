import glob, re, difflib

# 1) engine-API references in pages (parse-time risk)
pages = glob.glob('pages/**/*.html', recursive=True) + ['index.html']
pat = re.compile(r'(?:window\.)?(?:NGIS\.icon|NGIS_ICONS|NGIS\.icons|ActionDropdown|NGISActionIcons|NGIS\.hydrate)')
hits = []
for p in pages:
    s = open(p, encoding='utf-8').read()
    for m in pat.finditer(s):
        hits.append((p, m.group(0)))
print('engine-API references in pages:', len(hits))
for h in hits[:20]:
    print('  ', h)

# 2) layout.js mirror diff (I did not edit these; check drift)
a = open('assets/js/layout.js', encoding='utf-8').read()
b = open('layout.js', encoding='utf-8').read()
print('\nlayout.js mirror identical:', a == b, '| sizes', len(a), len(b))
if a != b:
    al, bl = a.splitlines(), b.splitlines()
    sm = difflib.SequenceMatcher(None, al, bl)
    shown = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        print('\n%s  assets[%d:%d] vs root[%d:%d]' % (tag, i1, i2, j1, j2))
        for line in al[i1:i2][:6]:
            print('   A:', line[:120])
        for line in bl[j1:j2][:6]:
            print('   B:', line[:120])
        shown += 1
        if shown >= 8:
            print('  ... (more diffs)')
            break
# does either layout.js contain my injected marker? (should be NO)
print('\ninjected marker in assets/js/layout.js:', 'action-icon engine' in a)
print('injected marker in root layout.js:', 'action-icon engine' in b)
