import os

matches = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.css', '.html')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as file:
                    if 'mob-bottomnav' in file.read():
                        matches.append(p)
            except Exception:
                pass
print('Found in:', matches)

