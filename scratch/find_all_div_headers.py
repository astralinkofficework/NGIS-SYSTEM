import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.extend(glob.glob('*.html'))

div_headers = []
for p in sorted(pages):
    norm_p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    
    # Check for <div class="...lg:hidden..." or <div class="...mobile..." containing toggle-sidebar
    m = re.findall(r'<div[^>]*class=[\'"][^\'"]*(?:lg:hidden|md:hidden|mobile-appbar|mobile-bar|mobile-header|mobile-top)[^\'"]*[\'"][^>]*>[\s\S]*?toggle-sidebar[\s\S]*?</div>', t, re.I)
    if m:
        div_headers.append(norm_p)

print(f"Pages with <div> instead of <header> for mobile bar ({len(div_headers)}):")
for p in div_headers:
    print('  ', p)

