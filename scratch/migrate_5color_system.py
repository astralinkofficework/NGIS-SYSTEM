import os
import glob
import re

# The Approved 5-Color System:
# Navy: #202F63
# Burgundy: #92243D
# White: #FFFFFF
# Black: #000000
# Soft Gray: #F3F3F5
# Derived subtle hairlines: #E5E5E8
# Derived burgundy hover: #7E1E34
# Derived neutral text: #333333, #555555, #77777F

COLOR_REPLACEMENTS = [
    # 1. Royal Blues & Bright Blues -> Navy #202F63 or Burgundy #92243D
    (re.compile(r'#2455D6', re.IGNORECASE), '#202F63'),
    (re.compile(r'#193DAA', re.IGNORECASE), '#18234D'),
    (re.compile(r'#2563EB', re.IGNORECASE), '#202F63'),
    (re.compile(r'#3B82F6', re.IGNORECASE), '#202F63'),
    (re.compile(r'#1D4ED8', re.IGNORECASE), '#18234D'),
    (re.compile(r'#0284C7', re.IGNORECASE), '#202F63'),
    (re.compile(r'#0EA5E9', re.IGNORECASE), '#202F63'),
    (re.compile(r'#38BDF8', re.IGNORECASE), '#202F63'),
    (re.compile(r'#7DD3FC', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#0E7490', re.IGNORECASE), '#202F63'),
    (re.compile(r'#0891B2', re.IGNORECASE), '#202F63'),
    (re.compile(r'#0369A1', re.IGNORECASE), '#202F63'),
    (re.compile(r'#155E75', re.IGNORECASE), '#202F63'),
    (re.compile(r'#1995AD', re.IGNORECASE), '#202F63'),

    # 2. Soft Blues / Pastels -> Soft Gray #F3F3F5
    (re.compile(r'#EAF2FF', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#F2F6FC', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#E0F2FE', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#BAE6FD', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#F0F9FF', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#EFF6FF', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#ECFEFF', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#D8EEF0', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#E8F5F6', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#C9DEFF', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#F8FAFB', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#F4F7FA', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#F4F4F9', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#EDF1F5', re.IGNORECASE), '#F3F3F5'),

    # 3. Greens / Emeralds -> Neutral Soft Gray #F3F3F5 or Black #000000
    (re.compile(r'#ECFDF5', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#F0FDF4', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#DCFCE7', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#D1FAE5', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#BBF7D0', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#A7F3D0', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#86EFAC', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#4ADE80', re.IGNORECASE), '#555555'),
    (re.compile(r'#22C55E', re.IGNORECASE), '#000000'),
    (re.compile(r'#16A34A', re.IGNORECASE), '#000000'),
    (re.compile(r'#15803D', re.IGNORECASE), '#000000'),
    (re.compile(r'#10B981', re.IGNORECASE), '#000000'),
    (re.compile(r'#059669', re.IGNORECASE), '#000000'),
    (re.compile(r'#047857', re.IGNORECASE), '#000000'),
    (re.compile(r'#006C49', re.IGNORECASE), '#000000'),
    (re.compile(r'#005237', re.IGNORECASE), '#000000'),
    (re.compile(r'#2E6F5E', re.IGNORECASE), '#000000'),
    (re.compile(r'#1F6B3A', re.IGNORECASE), '#000000'),

    # 4. Ambers / Yellows / Oranges -> Neutral Soft Gray #F3F3F5 or Black #000000
    (re.compile(r'#FFFBEB', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FEF3C7', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FEF9C3', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FFF7ED', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FDE68A', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#FCD34D', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#F59E0B', re.IGNORECASE), '#000000'),
    (re.compile(r'#D97706', re.IGNORECASE), '#000000'),
    (re.compile(r'#B45309', re.IGNORECASE), '#000000'),
    (re.compile(r'#A16207', re.IGNORECASE), '#000000'),
    (re.compile(r'#EA580C', re.IGNORECASE), '#000000'),
    (re.compile(r'#EAB308', re.IGNORECASE), '#000000'),
    (re.compile(r'#8C622B', re.IGNORECASE), '#000000'),
    (re.compile(r'#7A5C00', re.IGNORECASE), '#000000'),
    (re.compile(r'#F97316', re.IGNORECASE), '#000000'),

    # 5. Purples / Violets -> Soft Gray #F3F3F5 or Navy #202F63 / Black #000000
    (re.compile(r'#EDE9FE', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FAF5FF', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#DDD6FE', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#C4B5FD', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#A855F7', re.IGNORECASE), '#202F63'),
    (re.compile(r'#8B5CF6', re.IGNORECASE), '#202F63'),
    (re.compile(r'#7C3AED', re.IGNORECASE), '#202F63'),
    (re.compile(r'#6D28D9', re.IGNORECASE), '#202F63'),
    (re.compile(r'#4F46E5', re.IGNORECASE), '#202F63'),
    (re.compile(r'#6366F1', re.IGNORECASE), '#202F63'),

    # 6. Reds / Roses / Pinks / Danger -> Burgundy #92243D!
    (re.compile(r'#FEF2F2', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FEE2E2', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#FECACA', re.IGNORECASE), '#92243D'),
    (re.compile(r'#FCA5A5', re.IGNORECASE), '#92243D'),
    (re.compile(r'#F87171', re.IGNORECASE), '#92243D'),
    (re.compile(r'#EF4444', re.IGNORECASE), '#92243D'),
    (re.compile(r'#DC2626', re.IGNORECASE), '#92243D'),
    (re.compile(r'#E11D48', re.IGNORECASE), '#92243D'),
    (re.compile(r'#B42332', re.IGNORECASE), '#92243D'),
    (re.compile(r'#991B1B', re.IGNORECASE), '#92243D'),
    (re.compile(r'#963B3B', re.IGNORECASE), '#92243D'),

    # 7. Old Grays / Slates / Borders
    (re.compile(r'#E5EAF2', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#E2E8F0', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#CBD5E1', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#E0E6ED', re.IGNORECASE), '#E5E5E8'),
    (re.compile(r'#F1F5F9', re.IGNORECASE), '#F3F3F5'),
    (re.compile(r'#243247', re.IGNORECASE), '#000000'),
    (re.compile(r'#182329', re.IGNORECASE), '#000000'),
    (re.compile(r'#0F172A', re.IGNORECASE), '#000000'),
    (re.compile(r'#1E293B', re.IGNORECASE), '#000000'),
    (re.compile(r'#1F2937', re.IGNORECASE), '#000000'),
    (re.compile(r'#0B1A30', re.IGNORECASE), '#202F63'),
    (re.compile(r'#0A192F', re.IGNORECASE), '#202F63'),
    (re.compile(r'#64748B', re.IGNORECASE), '#555555'),
    (re.compile(r'#475569', re.IGNORECASE), '#333333'),
    (re.compile(r'#334155', re.IGNORECASE), '#333333'),
    (re.compile(r'#5D7288', re.IGNORECASE), '#555555'),
    (re.compile(r'#5B6677', re.IGNORECASE), '#555555'),
    (re.compile(r'#7A929F', re.IGNORECASE), '#555555'),
    (re.compile(r'#94A3B8', re.IGNORECASE), '#77777F'),
    (re.compile(r'#9CA3AF', re.IGNORECASE), '#77777F'),
]

# Tailwind class replacements for HTML files
TAILWIND_CLASS_REPLACEMENTS = [
    # Emerald / Green -> Neutral
    (re.compile(r'\bbg-emerald-(?:50|100|200)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-green-(?:50|100|200)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-teal-(?:50|100|200)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\btext-emerald-(?:600|700|800|900|500)\b'), 'text-[#000000]'),
    (re.compile(r'\btext-green-(?:600|700|800|900|500)\b'), 'text-[#000000]'),
    (re.compile(r'\btext-teal-(?:600|700|800|900|500)\b'), 'text-[#000000]'),
    (re.compile(r'\bborder-emerald-(?:200|300|600)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bborder-green-(?:200|300|600)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bbg-emerald-(?:500|600|700)\b'), 'bg-[#202F63]'),

    # Amber / Yellow / Orange -> Neutral
    (re.compile(r'\bbg-amber-(?:50|100|200)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-yellow-(?:50|100|200)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-orange-(?:50|100|200)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\btext-amber-(?:600|700|800|900|500)\b'), 'text-[#000000]'),
    (re.compile(r'\btext-yellow-(?:600|700|800|900|500)\b'), 'text-[#000000]'),
    (re.compile(r'\btext-orange-(?:600|700|800|900|500)\b'), 'text-[#000000]'),
    (re.compile(r'\bborder-amber-(?:200|300|600)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bborder-yellow-(?:200|300|600)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bbg-amber-(?:500|600)\b'), 'bg-[#202F63]'),

    # Blue / Sky / Indigo -> Navy or Soft Gray
    (re.compile(r'\bbg-blue-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-sky-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-indigo-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\btext-blue-(?:600|700|800|900)\b'), 'text-[#202F63]'),
    (re.compile(r'\btext-sky-(?:600|700|800)\b'), 'text-[#202F63]'),
    (re.compile(r'\btext-indigo-(?:600|700|800)\b'), 'text-[#202F63]'),
    (re.compile(r'\bborder-blue-(?:200|300)\b'), 'border-[#E5E5E8]'),
    (re.compile(r'\bborder-sky-(?:200|300)\b'), 'border-[#E5E5E8]'),

    # Purple / Violet -> Neutral Soft Gray / Navy
    (re.compile(r'\bbg-purple-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-violet-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\btext-purple-(?:600|700|800)\b'), 'text-[#202F63]'),
    (re.compile(r'\btext-violet-(?:600|700|800)\b'), 'text-[#202F63]'),
    (re.compile(r'\bborder-purple-(?:200|300)\b'), 'border-[#E5E5E8]'),

    # Rose / Red -> Burgundy #92243D!
    (re.compile(r'\bbg-rose-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\bbg-red-(?:50|100)\b'), 'bg-[#F3F3F5]'),
    (re.compile(r'\btext-rose-(?:500|600|700|800)\b'), 'text-[#92243D]'),
    (re.compile(r'\btext-red-(?:500|600|700|800)\b'), 'text-[#92243D]'),
    (re.compile(r'\bborder-rose-(?:200|300|600)\b'), 'border-[#92243D]'),
    (re.compile(r'\bborder-red-(?:200|300|600)\b'), 'border-[#92243D]'),
    (re.compile(r'\bbg-rose-(?:500|600)\b'), 'bg-[#92243D]'),
    (re.compile(r'\bbg-red-(?:500|600)\b'), 'bg-[#92243D]'),

    # Button classes with blue-600 / blue-500
    (re.compile(r'class="([^"]*)\bbg-blue-600\b([^"]*)"'), r'class="\1bg-[#92243D] text-[#FFFFFF]\2"'),
    (re.compile(r'class="([^"]*)\bbg-blue-500\b([^"]*)"'), r'class="\1bg-[#92243D] text-[#FFFFFF]\2"'),
    (re.compile(r'\bhover:bg-blue-700\b'), 'hover:bg-[#7E1E34]'),
    (re.compile(r'\bhover:bg-blue-600\b'), 'hover:bg-[#7E1E34]'),

    # Enforce NO BOLD FONTS per AGENTS.md
    (re.compile(r'\bfont-bold\b'), 'font-medium'),
    (re.compile(r'\bfont-extrabold\b'), 'font-medium'),
    (re.compile(r'\bfont-black\b'), 'font-medium'),
    (re.compile(r'\bfont-semibold\b'), 'font-medium'),
]

def migrate_text(content, is_html=False):
    # Apply color replacements
    for pat, rep in COLOR_REPLACEMENTS:
        content = pat.sub(rep, content)
    
    # If HTML, apply tailwind class replacements
    if is_html:
        for pat, rep in TAILWIND_CLASS_REPLACEMENTS:
            content = pat.sub(rep, content)
            
    return content

def run_migration():
    css_files = glob.glob('assets/css/*.css') + glob.glob('pages/**/css/*.css', recursive=True)
    # Exclude design-tokens.css and shared-components.css, design-system.css as we already crafted them directly
    exclude_css = {
        os.path.normpath('assets/css/design-tokens.css'),
        os.path.normpath('assets/css/shared-components.css'),
        os.path.normpath('assets/css/design-system.css')
    }
    
    modified_css = 0
    for cf in css_files:
        if os.path.normpath(cf) in exclude_css:
            continue
        with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
            old_content = f.read()
        new_content = migrate_text(old_content, is_html=False)
        if new_content != old_content:
            with open(cf, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_css += 1

    print(f"Updated {modified_css} CSS files.")

    # JS files
    js_files = glob.glob('assets/js/*.js')
    modified_js = 0
    for jf in js_files:
        with open(jf, 'r', encoding='utf-8', errors='ignore') as f:
            old_content = f.read()
        new_content = migrate_text(old_content, is_html=False)
        if new_content != old_content:
            with open(jf, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_js += 1
    print(f"Updated {modified_js} JS files.")

    # HTML files
    html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
    modified_html = 0
    for hf in html_files:
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            old_content = f.read()
        new_content = migrate_text(old_content, is_html=True)
        if new_content != old_content:
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_html += 1
    print(f"Updated {modified_html} HTML files out of {len(html_files)}.")

if __name__ == '__main__':
    run_migration()

