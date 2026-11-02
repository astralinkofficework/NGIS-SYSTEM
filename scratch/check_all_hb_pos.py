import os, re

pattern = re.compile(r'class=["\'][^"\']*(?:hamburger|menu-btn|toggle-sidebar)[^"\']*["\']|data-action=["\']toggle-sidebar["\']')

all_pages = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            all_pages.append(os.path.join(root, f))
all_pages.append('index.html')
all_pages.append('pages-directory.html')

for p in all_pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
    for idx, l in enumerate(lines):
        if pattern.search(l):
            # check previous 3 lines
            prev = ''.join(lines[max(0, idx-3):idx])
            print(f"File: {p} (L{idx+1})")
            print("  Context before:")
            for pl in lines[max(0, idx-2):idx]:
                print(f"    {pl.strip()[:80]}")
            print(f"  BUTTON: {l.strip()[:80]}")
            print("---")

