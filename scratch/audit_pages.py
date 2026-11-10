import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.sort()

missing_css = []
missing_js = []
missing_hamburger = []
bold_violations = []

print(f"Total HTML pages found in pages/: {len(pages)}")

for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Check action-icons.css
    if 'action-icons.css' not in html and 'design-system.css' not in html:
        missing_css.append(p)

    # Check action-icons.js
    if 'action-icons.js' not in html:
        missing_js.append(p)

    # Check hamburger button on pages that have a mobile header or layout
    # Exclude 404, access-denied, onboarding
    if not any(x in p for x in ['404.html', 'access-denied.html', 'onboarding.html']):
        if 'data-action="toggle-sidebar"' not in html and 'toggle-sidebar' not in html and 'hamburger' not in html:
            missing_hamburger.append(p)

    # Check font-bold / font-extrabold / font-black / font-weight: 700 / 800
    bolds = re.findall(r'(?:font-bold|font-extrabold|font-black|font-weight:\s*(?:700|800))', html)
    if bolds:
        bold_violations.append((p, len(bolds)))

print("\n--- Missing action-icons.js ---")
for p in missing_js:
    print(f"  {p}")

print("\n--- Missing hamburger button ---")
for p in missing_hamburger:
    print(f"  {p}")

print("\n--- Bold font occurrences ---")
for p, count in bold_violations:
    print(f"  {p}: {count} occurrences")

