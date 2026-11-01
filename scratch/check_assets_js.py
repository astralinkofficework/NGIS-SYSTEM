import os

for root, dirs, files in os.walk('assets'):
    for f in files:
        if f.endswith('.js'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                c = file.read()
                if 'redirect' in c.lower() or 'location.href' in c or 'role' in c:
                    print(f'Checking {p}:')
                    for line in c.split('\n'):
                        if any(w in line for w in ['location.href', 'location.replace', 'window.PAGE']):
                            print('  ', line.strip()[:100])

