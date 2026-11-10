import glob, re

for path in sorted(glob.glob('pages/**/*.html', recursive=True)):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Search for table rows with buttons
    td_matches = re.findall(r'<td[^>]*>(.*?)</td>', text, re.DOTALL)
    for td in td_matches:
        if '<button' in td and any(x in td for x in ['action', 'btn', 'edit', 'delete', 'view', 'sign', 'audit', 'authorize', 'review', 'return']):
            # check if there is text outside tags
            btns = re.findall(r'<button[^>]*>(.*?)</button>', td, re.DOTALL)
            for b in btns:
                clean = re.sub(r'<[^>]+>', '', b).strip()
                if clean and not clean in ['P', 'L', 'A', 'E'] and not re.match(r'^[\d\+\-✕✓•·]$', clean):
                    print(f"File: {path}")
                    print(f"   Button text: '{clean[:50]}'")
                    print(f"   Button HTML: '{b[:100]}'")

