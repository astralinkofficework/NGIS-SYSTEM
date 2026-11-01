import os, glob, re

# 1. AUDIT CSS HOVER RULES
css_files = glob.glob('assets/**/*.css', recursive=True) + glob.glob('pages/**/*.css', recursive=True)
css_files = [f.replace('\\', '/') for f in css_files if 'node_modules' not in f and 'scratch' not in f]

hover_rules = []
for cf in sorted(css_files):
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all selectors with :hover
    matches = re.finditer(r'([^{}]+:hover[^{}]*)\{([^{}]+)\}', content, re.IGNORECASE)
    for m in matches:
        sel = m.group(1).strip()
        body = m.group(2).strip()
        # Check if background or transform is modified
        has_bg = any(k in body.lower() for k in ['background', 'bg-color', 'background-color'])
        has_transform = any(k in body.lower() for k in ['transform', 'scale', 'translate'])
        if has_bg or has_transform:
            hover_rules.append((cf, sel, body))

print(f"Total CSS hover rules modifying background or transform: {len(hover_rules)}")
for cf, sel, body in hover_rules[:30]:
    print(f"  [{cf}] {sel} => {body.replace('\n', ' ')}")

# 2. AUDIT HTML HOVER TAILWIND CLASSES
html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
html_files = [f.replace('\\', '/') for f in html_files if 'node_modules' not in f and 'scratch' not in f]

tailwind_hover_bgs = []
for hf in sorted(html_files):
    with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    matches = re.findall(r'hover:bg-[a-zA-Z0-9\-\/\[\]]+|hover:translate-[a-zA-Z0-9\-\.]+|hover:scale-[0-9]+', content)
    if matches:
        tailwind_hover_bgs.append((hf, len(matches), set(matches)))

print(f"\nTotal HTML files with Tailwind hover:bg-* or hover:transform: {len(tailwind_hover_bgs)}")
for hf, cnt, classes in tailwind_hover_bgs[:20]:
    print(f"  [{hf}] ({cnt} occurrences): {list(classes)[:5]}")

