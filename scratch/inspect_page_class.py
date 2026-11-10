import re

files = ['assets/css/app.css', 'assets/css/design-system.css', 'assets/css/khmer-suite.css', 'assets/css/hero.css']

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    matches = re.findall(r'\.page\b[^{]*\{[^}]*\}', c)
    if matches:
        print(f, matches[:3])

