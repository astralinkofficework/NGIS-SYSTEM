import glob, re

pages = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
pages = [p.replace('\\', '/') for p in pages if 'node_modules' not in p and 'scratch' not in p]

modal_headers = []
for p in sorted(pages):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Check if a modal or drawer contains <header> or if layout.js injects into modals
    for m in re.finditer(r'<div[^>]*class=["\'][^"\']*(?:modal|drawer)[^"\']*["\'][^>]*>(.*?)</div>\s*</div>', text, re.DOTALL | re.IGNORECASE):
        modal_html = m.group(0)
        if '<header' in modal_html.lower():
            modal_headers.append((p, modal_html[:150].replace('\n', ' ')))

print(f"Modals containing <header>: {len(modal_headers)}")
for p, snippet in modal_headers:
    print(f"  {p}: {snippet}")

