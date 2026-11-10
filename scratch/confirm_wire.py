"""Confirm path prefixes, anchors, dropdown markup, and collisions."""
import glob, re

pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']

print('=== app.css link prefix per location ===')
seen = set()
for p in pages:
    s = open(p, encoding='utf-8').read()
    m = re.search(r'href="([^"]*assets/css/app\.css)"', s)
    pref = m.group(1) if m else '(no app.css link)'
    key = (p.split('\\')[1] if '\\' in p else 'root', pref.replace('assets/css/app.css',''))
    if key not in seen:
        seen.add(key)
        print('%-40s -> %s' % (p, pref))

print('\n=== pages WITHOUT app.css link ===')
for p in pages:
    s = open(p, encoding='utf-8').read()
    if 'assets/css/app.css' not in s:
        print('  ', p)

print('\n=== has </body> and </head> anchors ===')
nb = [p for p in pages if '</body>' not in open(p, encoding='utf-8').read()]
nh = [p for p in pages if '</head>' not in open(p, encoding='utf-8').read()]
print('  missing </body>:', nb)
print('  missing </head>:', nh)

print('\n=== dropdown / kebab structure samples ===')
for p in pages:
    s = open(p, encoding='utf-8').read()
    if 'action-dropdown' in s or 'data-dropdown-toggle' in s or 'more_vert' in s or 'data-ngis-icon="more"' in s:
        for mm in re.finditer(r'(action-dropdown[\w-]*|data-dropdown-toggle|data-ngis-icon="more")', s):
            pass
        cnt = len(re.findall(r'action-dropdown', s))
        kt = len(re.findall(r'data-ngis-icon="more"', s)) + len(re.findall(r'more_vert', s))
        print('  %-44s action-dropdown=%d  more-trigger=%d' % (p, cnt, kt))

print('\n=== existing class collision: .action-icon-btn/.action-group defined in page <style>? ===')
for p in pages:
    s = open(p, encoding='utf-8').read()
    for cls in ['.action-icon-btn', '.action-group', '.action-dropdown-menu', '.action-btn-pill']:
        if re.search(re.escape(cls) + r'\s*\{', s):
            print('  %-44s redefines %s' % (p, cls))
