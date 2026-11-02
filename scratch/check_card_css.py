import re

files = [
    'pages/student/css/base.css',
    'pages/student/css/overlap.css',
    'pages/student/css/student.css',
    'pages/student/css/responsive.css',
    'assets/css/portal-dashboard.css',
    'assets/css/design-system.css',
    'assets/css/interactions.css',
    'assets/css/shared-components.css',
    'assets/css/app.css'
]

selectors_to_check = ['ov-', 'ws-card', 'card', 'stat', 'id-card', 'deadline']

for path in files:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for m in re.finditer(r'([^{}]+)\{([^{}]+)\}', content):
            sel, body = m.group(1).strip(), m.group(2).strip()
            if any(k in sel for k in selectors_to_check):
                if any(st in sel for st in [':hover', ':active', ':focus', '::before', '::after', 'group']):
                    print(f'[{path}] {sel}')
                    print(f'    {body[:120]}...\n')
    except Exception as e:
        print(f'Error {path}: {e}')

