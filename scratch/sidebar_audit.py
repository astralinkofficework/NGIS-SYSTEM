import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages'
asset_pat = re.compile(r'(?:href|src)="([^"]+\.(?:css|js))[^"]*"', re.I)
rows = []
for dirpath, _, files in os.walk(root):
    for fn in sorted(files):
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dirpath, fn)
        src = open(p, encoding='utf-8', errors='replace').read()
        assets = [os.path.basename(m) for m in asset_pat.findall(src)]
        css = [a for a in assets if a.endswith('.css')]
        js = [a for a in assets if a.endswith('.js')]
        sigs = []
        if re.search(r'id="sidebar"|class="[^"]*\bsidebar', src):
            sigs.append('markup-sidebar')
        if re.search(r'\.sidebar\s*\{|#sidebar\s*\{', src):
            sigs.append('inline-css')
        if re.search(r'toggle-sidebar|toggleSidebar|openSidebar|closeSidebar|menuBtn|sidebarCollapse|sidebarToggle|hamburger', src):
            sigs.append('js-hooks')
        if 'layout.js' not in js:
            sigs.append('NO-layout')
        if '.main' not in src and 'class="main"' not in src:
            sigs.append('NO-main')
        rows.append((os.path.relpath(p, root), ' '.join(sigs) or '-', ','.join(css)))
for r in sorted(rows):
    print('%-52s %-38s %s' % r)
