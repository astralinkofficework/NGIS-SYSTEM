import os
import glob
import re

# Comprehensive mapping of all remaining non-5-color hexes
EXTENDED_HEX_MAP = {
    # Charts & Rainbow accents in admin.html and admin-lifecycle.html
    '#00E5FF': '#202F63', # Cyan -> Navy
    '#80DEEA': '#E5E5E8', # Light cyan -> Soft gray hairline
    '#FF9800': '#202F63', # Orange -> Navy
    '#FFD54F': '#E5E5E8', # Light orange -> Soft gray hairline
    '#9C27B0': '#202F63', # Purple -> Navy
    '#BA68C8': '#E5E5E8', # Light purple -> Soft gray hairline
    '#E91E63': '#92243D', # Hot pink -> Burgundy accent
    '#F06292': '#92243D', # Light pink -> Burgundy accent
    '#757575': '#555555', # Gray -> Neutral muted text
    '#9333EA': '#202F63', # Purple -> Navy
    '#A855F7': '#202F63',
    '#8B5CF6': '#202F63',
    '#7C3AED': '#202F63',
    '#6D28D9': '#202F63',
    '#4F46E5': '#202F63',
    '#6366F1': '#202F63',
    '#3B82F6': '#202F63',
    '#60A5FA': '#202F63',
    '#93C5FD': '#F3F3F5',
    '#BFDBFE': '#F3F3F5',
    '#DBEAFE': '#F3F3F5',
    '#EFF6FF': '#F3F3F5',

    # Greens / Teals
    '#6EE7B7': '#F3F3F5',
    '#A7F3D0': '#E5E5E8',
    '#4ADE80': '#000000',
    '#86EFAC': '#E5E5E8',
    '#BBF7D0': '#F3F3F5',
    '#DCFCE7': '#F3F3F5',
    '#F0FDF4': '#F3F3F5',
    '#ECFDF5': '#F3F3F5',
    '#D1FAE5': '#F3F3F5',
    '#A0D2B6': '#E5E5E8',
    '#4EDEA3': '#E5E5E8',
    '#6FFBBE': '#F3F3F5',
    '#6CF8BB': '#F3F3F5',
    '#86F2E4': '#F3F3F5',
    '#89F5E7': '#F3F3F5',
    '#6BD8CB': '#E5E5E8',
    '#BBEED1': '#F3F3F5',
    '#8CBDA2': '#555555',
    '#002113': '#000000',
    '#013623': '#202F63',
    '#0F291E': '#000000',
    '#13392E': '#000000',
    '#163B2B': '#18234D',
    '#111B15': '#000000',
    '#204F3A': '#000000',
    '#006A61': '#202F63',
    '#00714D': '#000000',
    '#006F66': '#000000',
    '#00201D': '#000000',
    '#005236': '#000000',
    '#005049': '#000000',
    '#1E7552': '#000000',
    '#175E41': '#000000',
    '#144C35': '#000000',
    '#103D2B': '#000000',
    '#0B261B': '#000000',
    '#396751': '#202F63',
    '#4E5D54': '#555555',
    '#7D8D83': '#555555',
    '#9EB8B7': '#E5E5E8',
    '#22323A': '#000000',
    '#F0F7F3': '#F3F3F5',
    '#DCEEE3': '#F3F3F5',
    '#BBDDCB': '#E5E5E8',
    '#E9F0EC': '#F3F3F5',

    # Surfaces & Canvas Grays
    '#F8FAFC': '#F3F3F5',
    '#F3F4F6': '#F3F3F5',
    '#F5F3FF': '#F3F3F5',
    '#F8F9FF': '#F3F3F5',
    '#E5EEFF': '#F3F3F5',
    '#EFF4FF': '#F3F3F5',
    '#F2F4F5': '#F3F3F5',
    '#ECEEEF': '#F3F3F5',
    '#E6E8E9': '#F3F3F5',
    '#E1E3E4': '#E5E5E8',
    '#D8DADB': '#F3F3F5',
    '#D3E4FE': '#F3F3F5',
    '#CBDBF5': '#F3F3F5',
    '#DAE2FD': '#F3F3F5',
    '#DBE1FF': '#F3F3F5',
    '#B4C5FF': '#E5E5E8',
    '#BEC6E0': '#E5E5E8',
    '#EAF1FF': '#FFFFFF',
    '#EFF1F2': '#FFFFFF',

    # Dark Neutrals & Texts
    '#191C1D': '#000000',
    '#0B1C30': '#000000',
    '#111A24': '#000000',
    '#131B2E': '#202F63',
    '#213145': '#000000',
    '#2E3132': '#000000',
    '#414943': '#555555',
    '#45464D': '#555555',
    '#3F465C': '#555555',
    '#76777D': '#77777F',
    '#717973': '#77777F',
    '#C0C9C1': '#E5E5E8',
    '#C6C6CD': '#E5E5E8',
    '#565E74': '#202F63',
    '#7C839B': '#555555',

    # Reds / Pinks / Errors -> Burgundy #92243D!
    '#B91C1C': '#92243D',
    '#BA1A1A': '#92243D',
    '#93000A': '#92243D',
    '#5F0E00': '#92243D',
    '#7F2512': '#92243D',
    '#822714': '#92243D',
    '#3D0600': '#92243D',
    '#FFDAD6': '#F3F3F5',
    '#FFDAD2': '#F3F3F5',
    '#FFB4A3': '#E5E5E8',
    '#FF967E': '#92243D',
    '#FCA5A5': '#92243D',
    '#FECACA': '#92243D',
    '#FEE2E2': '#F3F3F5',
    '#FEF2F2': '#F3F3F5',

    # Ambers / Yellows / Blues misc
    '#FCD34D': '#E5E5E8',
    '#FDE68A': '#E5E5E8',
    '#FEF3C7': '#F3F3F5',
    '#FFFBEB': '#F3F3F5',
    '#003EA8': '#202F63',
    '#00174B': '#202F63',
    '#497CFF': '#202F63',
    '#E8EEEE': '#F3F3F5',
}

# Remaining Tailwind classes to normalize
REMAINING_TAILWIND = [
    (re.compile(r'\btext-emerald-(?:100|200|300|400|950)\b'), 'text-[#000000]'),
    (re.compile(r'\btext-teal-(?:100|200)\b'), 'text-[#000000]'),
    (re.compile(r'\bborder-emerald-(?:100|400|500)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bbg-emerald-(?:400|800|950)\b'), 'bg-[#202F63]'),
    (re.compile(r'\bring-emerald-(?:400|500)\b'), 'ring-[#202F63]'),
    (re.compile(r'\bbg-amber-400\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bborder-amber-(?:100|500)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bborder-blue-500\b'), 'border-[#202F63]'),
    (re.compile(r'\bborder-rose-100\b'), 'border-[#92243D]'),
    (re.compile(r'\btext-rose-900\b'), 'text-[#92243D]'),
    (re.compile(r'\bbg-purple-600\b'), 'bg-[#202F63]'),
    (re.compile(r'\btext-purple-600\b'), 'text-[#202F63]'),
]

def clean_file(filepath, is_html=False):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    orig = content
    # Replace all hexes in EXTENDED_HEX_MAP (case-insensitive)
    for k, v in EXTENDED_HEX_MAP.items():
        pattern = re.compile(re.escape(k), re.IGNORECASE)
        content = pattern.sub(v, content)

    if is_html:
        for pat, rep in REMAINING_TAILWIND:
            content = pat.sub(rep, content)

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    css_files = glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True)
    js_files = glob.glob('assets/js/*.js')
    html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')

    c_count = sum(1 for cf in css_files if clean_file(cf, False))
    j_count = sum(1 for jf in js_files if clean_file(jf, False))
    h_count = sum(1 for hf in html_files if clean_file(hf, True))

    print(f"Deep refactor completed: {c_count} CSS, {j_count} JS, {h_count} HTML files modified.")

if __name__ == '__main__':
    run()

