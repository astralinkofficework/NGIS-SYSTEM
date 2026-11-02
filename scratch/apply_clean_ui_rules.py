import os, glob, re

files = sorted(glob.glob('pages/**/*.html', recursive=True) + ['index.html', 'pages-directory.html'])

def clean_page(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig = content

    # 1. Typography - NO BOLD: Replace heavy font classes in HTML tags
    # Keep tailwind config intact if it already maps them to 500, but in markup replace font-bold/font-extrabold/font-black with font-medium
    def replace_font_classes(match):
        cls_str = match.group(1)
        cls_str = re.sub(r'\bfont-(?:bold|extrabold|black)\b', 'font-medium', cls_str)
        cls_str = re.sub(r'\bfont-semibold\b', 'font-medium', cls_str)
        return f'class="{cls_str}"'

    content = re.sub(r'class="([^"]*)"', replace_font_classes, content)
    content = re.sub(r"class='([^']*)'", lambda m: f"class='{re.sub(r'\bfont-(?:bold|extrabold|black|semibold)\b', 'font-medium', m.group(1))}'", content)

    # 2. Shadows - Replace heavy shadows on cards/panels with hairlines
    def replace_shadow_classes(match):
        cls_str = match.group(1)
        cls_str = re.sub(r'\bshadow-(?:xl|2xl|lg)\b', 'shadow-sm border border-slate-200', cls_str)
        # Avoid duplicate border classes
        cls_str = re.sub(r'\bborder border-slate-200 border\b', 'border border-slate-200', cls_str)
        return f'class="{cls_str}"'

    content = re.sub(r'class="([^"]*)"', replace_shadow_classes, content)

    # 3. Colors - Remove rainbow non-status card/panel backgrounds
    # (replace blue/purple/indigo/violet/cyan/pink container backgrounds with neutral white or subtle slate)
    def calm_rainbow_bg(match):
        cls_str = match.group(1)
        # Keep status colors (emerald/green for success, amber/yellow for warning, red/rose for danger)
        # Replace non-status decorative bgs: blue-50, purple-50, indigo-50, cyan-50, pink-50
        cls_str = re.sub(r'\b(?:bg|border)-(?:purple|indigo|violet|cyan|pink)-(?:50|100|200)\b', 'bg-slate-50 border-slate-200', cls_str)
        cls_str = re.sub(r'\btext-(?:purple|indigo|violet|cyan|pink)-(?:600|700|800)\b', 'text-slate-700', cls_str)
        return f'class="{cls_str}"'

    content = re.sub(r'class="([^"]*)"', calm_rainbow_bg, content)

    # 4. Mandatory Hamburger button check: ensure it has standard attributes
    if path.startswith('pages/') and 'access-denied.html' not in path and 'redirect' not in content.lower():
        # If hamburger button exists, ensure proper attributes
        def update_hamburger(match):
            btn_tag = match.group(0)
            if 'data-action="toggle-sidebar"' not in btn_tag:
                btn_tag = btn_tag.replace('<button ', '<button data-action="toggle-sidebar" ')
            if 'hamburger-btn' not in btn_tag:
                btn_tag = re.sub(r'class="([^"]*)"', r'class="\1 hamburger-btn mobile-hamburger-btn"', btn_tag)
            if 'aria-label=' not in btn_tag:
                btn_tag = btn_tag.replace('<button ', '<button aria-label="Open menu" aria-expanded="false" title="Open navigation" ')
            return btn_tag

        content = re.sub(r'<button[^>]*?(?:htb-hamburger|menu-btn|hamburger)[^>]*?>', update_hamburger, content)

    # 5. Table responsiveness: Ensure tables without responsive wrapper get wrapped or styled
    # (Check if <table> is not inside a div with overflow)

    if content != orig:
        with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    modified_count = 0
    for f in files:
        if clean_page(f):
            modified_count += 1
            print(f"Cleaned {f}")
    print(f"Finished. Modified {modified_count} of {len(files)} files.")

