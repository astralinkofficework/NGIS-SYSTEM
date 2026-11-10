# Post-D1 link integrity: every local href/src in live HTML must resolve to an existing file.
import re, os, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

pages = glob.glob('pages/**/*.html', recursive=True) + ['index.html', 'sitemap.html', 'pages-directory.html']
broken = []
pat = re.compile(r'(?:href|src)\s*=\s*["\']([^"\'#]+?(?:\.html|\.css|\.js|\.png|\.json|\.svg|\.ico))(\?[^"\']*)?["\']', re.I)
for p in pages:
    t = open(p, encoding='utf-8', errors='replace').read()
    d = os.path.dirname(p)
    for m in pat.finditer(t):
        raw = m.group(1)
        if raw.startswith(('http', 'mailto', 'data:', 'javascript:', '//')):
            continue
        raw = raw.split('?')[0]
        import urllib.parse
        raw = urllib.parse.unquote(raw)
        cands = [os.path.normpath(os.path.join(d, raw)), os.path.normpath(raw)]
        # root-relative with leading ../ chains already handled; also try pages/<role> sibling
        if not any(os.path.isfile(c) for c in cands):
            broken.append((p, raw))
print('pages scanned:', len(pages))
print('BROKEN LINKS:', len(broken))
seen = set()
for p, r in broken:
    k = (p, r)
    if k in seen: continue
    seen.add(k)
    print(f'  {p} -> {r}')
