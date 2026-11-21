import os
import re

attr_re = re.compile(r'\btitle\s*=\s*(["\'])(.*?)\1', re.IGNORECASE)

script_matches = []
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            # find all script contents
            scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', c, flags=re.I|re.S)
            for s in scripts:
                # find html tags generated in string templates like <button ... title="..." ...>
                # or title="..." in html-like strings
                found = re.findall(r'<[a-zA-Z0-9\-]+[^>]*?\btitle\s*=\s*([\\\'"])(.*?)\1', s, flags=re.I)
                if found:
                    script_matches.append((p, found))

print(f"Files with HTML template title attributes in script tags: {len(script_matches)}")
for p, found in script_matches[:10]:
    print(f"  {p}: {len(found)} titles in templates:")
    for quote, text in found[:3]:
        print(f"     title={text[:40]}")
