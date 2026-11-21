import glob
import re
from collections import Counter

html_files = glob.glob('pages/**/*.html', recursive=True)

badge_re = re.compile(r'<span[^>]*class=["\']([^"\']*\b(?:rounded-full|rounded-lg|rounded-md|badge|pill|chip)\b[^"\']*)["\'][^>]*>(.*?)</span>', re.IGNORECASE)

portal_badges = Counter()

for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for m in badge_re.finditer(content):
        cls = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if any(c in cls for c in ['bg-purple', 'bg-pink', 'bg-cyan', 'bg-violet', 'bg-indigo', 'bg-blue', 'bg-yellow']):
            portal_badges[f"{cls} => '{text}' ({hf})"] += 1

print(f"Total non-brand/non-semantic badges found: {len(portal_badges)}")
for k, v in portal_badges.most_common(25):
    print(f"  {k}")
