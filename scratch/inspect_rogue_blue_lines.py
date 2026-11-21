import re

files = [
    'assets/css/app.css',
    'assets/css/hero.css',
    'assets/css/interactions.css',
    'assets/css/portal-dashboard.css'
]

pattern = re.compile(r'rgba?\(\s*36\s*,\s*85\s*,\s*214')

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n=== {fpath} ===")
    for i, line in enumerate(lines):
        if pattern.search(line):
            print(f"  Line {i+1:4d}: {line.strip()}")
