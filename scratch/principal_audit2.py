"""Compact principal audit summary."""
import glob, re, json

rows = []
for f in sorted(glob.glob('pages/principal/*.html')):
    s = open(f, encoding='utf-8').read()
    name = f.replace('\\', '/').split('/')[-1]
    cont = re.findall(r'class="([^"]*max-w[^"]*)"', s)
    tables = len(re.findall(r'<table', s))
    inline_sp = len(re.findall(r'(?:padding|margin|gap)\s*:\s*[\d.]+px', s))
    apis = sorted(set(re.findall(r'/api/[a-zA-Z0-9_/\-]+', s)))
    jsfiles = sorted(set(re.findall(r'src="[^"]*?js/([^"?]+)', s)))
    cssfiles = sorted(set(re.findall(r'href="[^"]*?css/([^"?]+)', s)))
    print('%-34s tables=%d inline_px=%-3d container=%s' % (
        name, tables, inline_sp, cont[:2]))
    print('    css:', ','.join(cssfiles))
    print('    js :', ','.join(jsfiles))
    print('    apis:', ' '.join(apis))
