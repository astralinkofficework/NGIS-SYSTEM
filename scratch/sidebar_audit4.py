import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'pages'
target_re = re.compile(r'class="[^"]*(htb-left|hero-topbar|topbar|lh-inner|dir-header-inner)|<header\b')
hamb_re = re.compile(r'hamburger|data-action="toggle-sidebar"|menu-btn|#menuBtn')
for dp, _, fs in os.walk(root):
    for fn in sorted(fs):
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dp, fn)
        src = open(p, encoding='utf-8', errors='replace').read()
        # skip redirect stubs
        if len(src) < 2000:
            continue
        info = []
        if not target_re.search(src):
            info.append('NO-header-target')
        if 'hero.js' in src:
            info.append('hero.js')
        if 'premium-header.js' in src:
            info.append('premium-header.js')
        if hamb_re.search(src):
            info.append('own-hamburger-markup')
        print('%-52s %s' % (os.path.relpath(p, root), ' '.join(info) or '-'))
