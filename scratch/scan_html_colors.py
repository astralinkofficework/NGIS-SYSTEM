import glob
import re
from collections import Counter

print("Scanning all HTML files for color hex codes...")
html_files = sorted(glob.glob("pages/**/*.html", recursive=True) + glob.glob("*.html"))

hex_counter = Counter()
for f in html_files:
    with open(f, "r", encoding="utf-8") as fp:
        content = fp.read()
    hexes = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', content)
    for h in hexes:
        hex_counter[h.upper()] += 1

print(f"Total HTML files scanned: {len(html_files)}")
print("Top 25 most frequent hex codes in HTML:")
for h, count in hex_counter.most_common(25):
    print(f"  {h}: {count} occurrences")

