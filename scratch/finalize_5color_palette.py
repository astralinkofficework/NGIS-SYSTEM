import os
import glob
import re
import colorsys

APPROVED_HEX = {
    '#202F63', '#92243D', '#FFFFFF', '#000000', '#F3F3F5',
    '#E5E5E8', '#7E1E34', '#18234D', '#681729',
    '#333333', '#555555', '#77777F',
    '#0D1322', '#141D33', '#1F2B49', '#A5A5AA', # Dark theme core tokens
    '#FFF', '#000'
}

EXCLUDE_FILES = {
    os.path.normpath('assets/css/design-tokens.css'),
    os.path.normpath('assets/css/shared-components.css'),
    os.path.normpath('assets/css/design-system.css')
}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    elif len(hex_str) == 8:
        hex_str = hex_str[:6] # drop alpha
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)

def map_color_to_5palette(hex_str):
    hex_upper = hex_str.upper()
    if hex_upper in APPROVED_HEX:
        return hex_upper
    
    try:
        r, g, b = hex_to_rgb(hex_str)
    except Exception:
        return '#000000'
    
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    lum = 0.299*r + 0.587*g + 0.114*b

    # Pure white
    if lum >= 253:
        return '#FFFFFF'
    # Light canvas / soft background
    if lum >= 225:
        return '#F3F3F5'
    # Subtle hairline border
    if lum >= 195 and s < 0.25:
        return '#E5E5E8'
    # Deep Black
    if lum <= 30:
        return '#000000'
    
    # Red / Rose / Crimson / Danger -> Burgundy #92243D
    h_deg = h * 360
    if (h_deg >= 335 or h_deg <= 25) and s > 0.25:
        return '#92243D'
    
    # Blue / Indigo / Navy hues (190..260)
    if 190 <= h_deg <= 260:
        if lum < 120:
            return '#202F63' # Navy
        elif lum >= 180:
            return '#F3F3F5' # Light soft blue surface -> Soft gray
        else:
            return '#202F63'
            
    # Muted secondary text
    if s < 0.2:
        if lum < 120:
            return '#333333'
        else:
            return '#555555'

    # Any remaining greens, yellows, ambers, purples:
    if lum >= 180:
        return '#F3F3F5'
    if lum < 100:
        return '#000000'
    return '#202F63'

def map_tailwind_class(m):
    prefix = m.group(1) # bg, text, border, ring, stroke, fill
    color = m.group(2)  # emerald, blue, etc.
    shade = int(m.group(3)) # 50, 600, etc.

    if prefix == 'bg':
        if shade <= 200:
            return 'bg-[#F3F3F5]'
        elif color in ('rose', 'red'):
            return 'bg-[#92243D]'
        else:
            return 'bg-[#202F63]'

    elif prefix == 'text':
        if shade <= 200:
            return 'text-[#FFFFFF]' if shade <= 100 else 'text-[#000000]'
        elif color in ('rose', 'red'):
            return 'text-[#92243D]'
        elif color in ('blue', 'sky', 'indigo', 'purple', 'violet'):
            return 'text-[#202F63]'
        else:
            return 'text-[#000000]'

    elif prefix == 'border':
        if color in ('rose', 'red'):
            return 'border-[#92243D]'
        elif color in ('blue', 'sky') and shade >= 500:
            return 'border-[#202F63]'
        else:
            return 'border-[#E5E5E8]'

    elif prefix == 'ring':
        if color in ('rose', 'red'):
            return 'ring-[#92243D]'
        else:
            return 'ring-[#202F63]'

    return f'{prefix}-[{map_color_to_5palette("#333")}]'

tailwind_pattern = re.compile(r'\b(bg|text|border|ring|stroke|fill)-(blue|emerald|green|amber|yellow|purple|indigo|violet|cyan|sky|teal|rose|red|orange|lime|fuchsia|pink)-(\d{2,3})\b')
hex_pattern = re.compile(r'#[0-9a-fA-F]{3,8}')

def process_file(filepath, is_html=False):
    if os.path.normpath(filepath) in EXCLUDE_FILES:
        return False
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    orig = content

    # 1. Replace tailwind color classes in HTML
    if is_html:
        content = tailwind_pattern.sub(map_tailwind_class, content)

    # 2. Replace any unapproved hex colors
    def replace_hex(match):
        h = match.group(0)
        h_upper = h.upper()
        if h_upper in APPROVED_HEX:
            return h
        return map_color_to_5palette(h)

    content = hex_pattern.sub(replace_hex, content)

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run_all():
    css_files = glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True)
    js_files = glob.glob('assets/js/*.js')
    html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')

    c_count = sum(1 for cf in css_files if process_file(cf, False))
    j_count = sum(1 for jf in js_files if process_file(jf, False))
    h_count = sum(1 for hf in html_files if process_file(hf, True))

    print(f"Finalization complete:")
    print(f"  {c_count} CSS files updated")
    print(f"  {j_count} JS files updated")
    print(f"  {h_count} HTML files updated")

if __name__ == '__main__':
    run_all()

