import os

for f in ['hero.css', 'app.css', 'ui-cleanup.css', 'design-system.css', 'profiles.css']:
    path = os.path.join('assets', 'css', f)
    if os.path.exists(path):
        with open(path, encoding='utf-8', errors='ignore') as fp:
            for i, line in enumerate(fp, 1):
                if 'mobile-appbar' in line or 'mobile-hamburger-btn' in line:
                    print(f"{f}:{i}: {line.strip()[:90]}")
