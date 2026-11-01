import glob, re

files = [
    'pages/student/css/overlap.css',
    'pages/student/css/responsive.css',
    'assets/css/design-system.css',
    'assets/css/interactions.css',
    'assets/css/ui-cleanup.css'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    for m in re.finditer(r'([^{}]*(?:ov-inner-panel|ov-deadline-panel)[^{}]*\{[^}]+\})', c):
        print(f"=== {fname} ===")
        print(m.group(1).strip()[:200].encode('ascii', 'ignore').decode())
