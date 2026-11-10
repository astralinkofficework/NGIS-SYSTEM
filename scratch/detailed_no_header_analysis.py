import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.extend(glob.glob('*.html'))

no_headers = []
for p in sorted(pages):
    norm_p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # check for <header> tag
    has_header = bool(re.search(r'<header\b', content, re.I))
    if not has_header:
        # get title
        m_title = re.search(r'<title>(.*?)</title>', content, re.I)
        title = m_title.group(1).strip() if m_title else 'No Title'
        
        # get role / portal
        m_role = re.search(r'data-role=[\'"]([^\'"]+)[\'"]', content, re.I)
        role = m_role.group(1) if m_role else 'unknown'
        
        # get main tag
        has_main = '<main' in content.lower()
        
        # check if it is a standalone / landing page
        is_standalone = 'shell-type' not in content and 'assets/js/layout.js' not in content
        
        no_headers.append({
            'path': norm_p,
            'title': title,
            'role': role,
            'has_main': has_main,
            'is_standalone': is_standalone,
            'has_layout_js': 'assets/js/layout.js' in content or 'layout.js' in content
        })

print(f"Total pages without <header>: {len(no_headers)}")
for nh in no_headers:
    print(f"[{nh['role']}] {nh['path']} | Title: {nh['title']} | has_main={nh['has_main']} | layout={nh['has_layout_js']}")

