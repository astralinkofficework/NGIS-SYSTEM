import glob
import re

css_files = glob.glob('assets/css/*.css')
print(f"Scanning {len(css_files)} CSS files...")

for cf in css_files:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # check badge definitions
    badges = re.findall(r'(\.badge[^{]*)\{([^}]+)\}', content)
    if badges:
        print(f"\nIn {cf}:")
        for sel, decl in badges[:5]:
            print(f"  {sel.strip()} => {decl.strip()[:60]}...")
            
    # check chip definitions
    chips = re.findall(r'(\.chip[^{]*|\.tt-chip[^{]*)\{([^}]+)\}', content)
    if chips:
        print(f"\nIn {cf} (chips):")
        for sel, decl in chips[:5]:
            print(f"  {sel.strip()} => {decl.strip()[:60]}...")
