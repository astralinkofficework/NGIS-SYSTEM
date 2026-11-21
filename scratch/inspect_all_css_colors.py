import glob
import re

css_files = glob.glob('assets/css/*.css')
print(f"Scanning {len(css_files)} CSS files for rogue colors...")

color_re = re.compile(r'rgba?\(\s*36\s*,\s*85\s*,\s*214|rgba?\(\s*234\s*,\s*242\s*,\s*255|#[0-9a-fA-F]{6}')

for cf in css_files:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # search for rgba(36, 85, 214
    blues = re.findall(r'[^\n]*rgba?\(\s*36\s*,\s*85\s*,\s*214[^\n]*', content)
    if blues:
        print(f"\nRogue blue in {cf}:")
        for b in blues[:4]:
            print(f"  {b.strip()[:90]}")
