import glob
import re
from collections import Counter

APPROVED_HEX = {
    '#202F63', '#92243D', '#FFFFFF', '#000000', '#F3F3F5',
    '#E5E5E8', '#7E1E34', '#18234D', '#681729',
    '#333333', '#555555', '#77777F', '#FFF', '#000'
}

hex_pat = re.compile(r'#[0-9a-fA-F]{3,8}')
files = glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True) + glob.glob('assets/js/*.js') + glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')

outside_config_unapproved = Counter()
file_map = {}

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    # Remove tailwind.config blocks to see what's in the actual markup / css / js
    c_clean = re.sub(r'tailwind\.config\s*=\s*\{.*?\n\s*\};?', '', c, flags=re.DOTALL)
    for h in hex_pat.findall(c_clean):
        h_norm = h.upper()
        if h_norm not in APPROVED_HEX:
            outside_config_unapproved[h_norm] += 1
            if h_norm not in file_map:
                file_map[h_norm] = set()
            file_map[h_norm].add(f)

print(f"Total outside-config unapproved hex values: {len(outside_config_unapproved)}")
for h, count in outside_config_unapproved.most_common(30):
    print(f"{h}: {count} in {len(file_map[h])} files -> {list(file_map[h])[:3]}")

