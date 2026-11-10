import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

hj = open('assets/js/hero.js', encoding='utf-8').read()
print('=== hero.js backgrounds ===')
for m in re.finditer(r"background(?:-image)?\s*:\s*[^;\"']{10,120}", hj):
    print(' ', ' '.join(m.group(0).split())[:115])

av = open('assets/css/admin-view.css', encoding='utf-8').read()
print('=== admin-view.css hero-ish rules ===')
for m in re.findall(r"[^{}]*hero[^{}]*\{[^}]{0,200}\}", av, re.I)[:8]:
    print(' ', ' '.join(m.split())[:175])

pd = open('assets/css/portal-dashboard.css', encoding='utf-8').read()
print('=== portal-dashboard.css hero-ish rules ===')
for m in re.findall(r"([^{}]*hero[^{}]*\{[^}]{0,160}\})", pd, re.I)[:8]:
    print(' ', ' '.join(m.split())[:170])

ac = open('assets/css/app.css', encoding='utf-8').read()
print('=== app.css: what paints the green band? (search gradients) ===')
for m in re.findall(r"[^{}]{0,60}\{[^}]*linear-gradient[^}]{0,140}\}", ac)[:10]:
    print(' ', ' '.join(m.split())[:170])
print('=== sidebar bg rules (app.css) ===')
for m in re.findall(r"\.sidebar\s*\{[^}]{0,220}\}", ac)[:3]:
    print(' ', ' '.join(m.split())[:200])
