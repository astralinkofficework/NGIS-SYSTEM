import os, glob, re
from collections import Counter

css_counter = Counter()
pages = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')

for p in pages:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            links = re.findall(r'<link[^>]+rel=[\"\']stylesheet[\"\'][^>]+href=[\"\']([^\"\']+)[\"\']', content)
            for link in links:
                base = os.path.basename(link.split('?')[0])
                css_counter[base] += 1
    except Exception as e:
        pass

print("=== TOP CSS FILES LOADED BY PAGES ===")
for css, count in css_counter.most_common(25):
    print(f"{css:35}: loaded by {count} pages")

js_counter = Counter()
for p in pages:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            scripts = re.findall(r'<script[^>]+src=[\"\']([^\"\']+)[\"\']', content)
            for s in scripts:
                base = os.path.basename(s.split('?')[0])
                js_counter[base] += 1
    except Exception as e:
        pass

print("\n=== TOP JS FILES LOADED BY PAGES ===")
for js, count in js_counter.most_common(20):
    print(f"{js:35}: loaded by {count} pages")
