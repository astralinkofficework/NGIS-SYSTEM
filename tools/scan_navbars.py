import os, glob, re
from collections import Counter

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')

header_patterns = Counter()
hero_banner_count = 0
mobile_appbar_count = 0
header_tags = 0
topbar_classes = Counter()

for path in html_files:
    try:
        content = open(path, encoding='utf-8', errors='ignore').read()
        if 'id="heroBanner"' in content:
            hero_banner_count += 1
        if 'mobileMainAppbar' in content or 'mobile-appbar' in content:
            mobile_appbar_count += 1
        
        # Look for headers
        headers = re.findall(r'<header[^>]*>', content)
        for h in headers:
            # extract id or class
            header_patterns[h[:100]] += 1
            
        classes = re.findall(r'class="[^"]*(?:topbar|navbar|app-header|main-header|header)[^"]*"', content)
        for c in classes:
            topbar_classes[c[:80]] += 1
    except Exception as e:
        pass

print(f"Total HTML files: {len(html_files)}")
print(f"Pages with heroBanner: {hero_banner_count}")
print(f"Pages with mobileMainAppbar: {mobile_appbar_count}")
print("\nTop 15 Header tags:")
for h, count in header_patterns.most_common(15):
    print(f"[{count}] {h}")

print("\nTop 15 Header Classes:")
for c, count in topbar_classes.most_common(15):
    print(f"[{count}] {c}")
