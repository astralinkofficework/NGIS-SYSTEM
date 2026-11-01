import os

for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                if 'Department of Mathematics' in content or 'Dr. Alan Vance' in content:
                    print('MATCH:', p)

