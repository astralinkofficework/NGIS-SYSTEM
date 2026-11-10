import re

for p in [
    'pages/principal/principal-activity.html',
    'pages/principal/principal-lost-found.html',
    'pages/principal/principal-profile.html'
]:
    with open(p, 'r', encoding='utf-8') as f:
        t = f.read()
    print('===', p, '===')
    print('has heroBanner:', 'id="heroBanner"' in t)
    print('has header tag:', bool(re.search(r'<header\b', t, re.I)))
    print('has toggle:', 'data-action="toggle-sidebar"' in t)
    m = re.search(r'<main[^>]*>(.*?)(?:<div class="page|<div class="container|<div class="grid|<div class="table)', t, re.DOTALL | re.I)
    if m:
        print('Top of main:', m.group(1)[:200].strip())

