import glob
import re

html_files = glob.glob('pages/**/*.html', recursive=True)

modified_files = []

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content
    
    # Pattern 1: <header id="mobileMainAppbar" class="...bg-white border-b border-slate-200..."
    # Replace bg-white and border-b border-slate-200 on mobile headers with bg-transparent border-none
    def header_sub(match):
        tag = match.group(0)
        # Only clean if it is mobile header
        if 'lg:hidden' in tag or 'md:hidden' in tag or 'mobile-appbar' in tag or 'mobileMainAppbar' in tag:
            # Replace bg-white or bg-white/95 with bg-transparent
            tag = re.sub(r'\bbg-white(?:/\d+)?\b', 'bg-transparent', tag)
            tag = re.sub(r'\bbg-surface-container-lowest(?:/\d+)?\b', 'bg-transparent', tag)
            tag = re.sub(r'\bbackdrop-blur-(?:md|sm|lg)\b', '', tag)
            tag = re.sub(r'\bborder-b\s+border-[a-zA-Z0-9_\-\/\[\]#.]+\b', 'border-none', tag)
            tag = re.sub(r'\bborder-b\b', 'border-none', tag)
            tag = re.sub(r'\s{2,}', ' ', tag)
        return tag

    new_content = re.sub(r'<header[^>]+>', header_sub, content)
    
    if new_content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_files.append(fpath)

print(f"Total HTML files cleaned: {len(modified_files)}")
for mf in modified_files[:15]:
    print(f"  Cleaned: {mf}")
