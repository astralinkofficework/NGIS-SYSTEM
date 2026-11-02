import glob
import re
from collections import Counter

# Approved palette:
# Navy: #202F63
# Burgundy: #92243D
# White: #FFFFFF
# Black: #000000
# Soft Gray: #F3F3F5
# Approved subtle tones:
# #E5E5E8 (Soft hairline border)
# #7E1E34 (Burgundy hover)
# #18234D (Dark navy hover)
# #681729 (Burgundy active)
# #333333 (Neutral high contrast text)
# #555555 (Neutral muted text)
# #77777F (Neutral faint text)

APPROVED_HEX = {
    '#202F63', '#92243D', '#FFFFFF', '#000000', '#F3F3F5',
    '#E5E5E8', '#7E1E34', '#18234D', '#681729',
    '#333333', '#555555', '#77777F',
    '#FFF', '#000'
}

def audit():
    css_files = glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True)
    js_files = glob.glob('assets/js/*.js')
    html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
    
    hex_pat = re.compile(r'#[0-9a-fA-F]{3,8}')
    tailwind_pat = re.compile(r'\b(?:bg|text|border|ring|stroke|fill)-(?:blue|emerald|green|amber|yellow|purple|indigo|violet|cyan|sky|teal|rose|red|orange|lime|fuchsia|pink)-\d{2,3}\b')

    unapproved_hex = Counter()
    unapproved_tailwind = Counter()

    for cf in css_files:
        with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        hexes = [h.upper() for h in hex_pat.findall(content)]
        for h in hexes:
            if h not in APPROVED_HEX:
                unapproved_hex[h] += 1

    for jf in js_files:
        with open(jf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        hexes = [h.upper() for h in hex_pat.findall(content)]
        for h in hexes:
            if h not in APPROVED_HEX:
                unapproved_hex[h] += 1

    for hf in html_files:
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        hexes = [h.upper() for h in hex_pat.findall(content)]
        for h in hexes:
            if h not in APPROVED_HEX:
                unapproved_hex[h] += 1
        tw = tailwind_pat.findall(content)
        for t in tw:
            unapproved_tailwind[t] += 1

    print(f"Total unapproved unique hex codes: {len(unapproved_hex)}")
    print(f"Top 20 unapproved hex codes:")
    for h, cnt in unapproved_hex.most_common(20):
        print(f"  {h}: {cnt}")

    print(f"\nTotal unapproved tailwind classes: {len(unapproved_tailwind)}")
    print(f"Top 20 unapproved tailwind classes:")
    for t, cnt in unapproved_tailwind.most_common(20):
        print(f"  {t}: {cnt}")

if __name__ == '__main__':
    audit()

