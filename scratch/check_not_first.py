import os, re, json

with open('scratch/phase0_inventory.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

pattern = re.compile(r'(?:<button[^>]*class=["\'][^"\']*(?:hamburger|menu-btn)[^"\']*["\'][^>]*>|<button[^>]*data-action=["\']toggle-sidebar["\'][^>]*>)', re.IGNORECASE)

not_first = []

for page in pages:
    p = page['path']
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    
    # find all matching buttons
    for m in pattern.finditer(html):
        start_idx = m.start()
        # find the parent opening tag
        last_open_div = html.rfind('<', 0, start_idx)
        # find lines
        lines_before = html[:start_idx].split('\n')
        line_no = len(lines_before)
        btn_tag = m.group(0)
        
        # Check text between parent tag and button
        # find preceding container opening tag
        preceding_tag = re.search(r'<([a-zA-Z0-9]+)[^>]*>\s*$', html[:start_idx])
        if not preceding_tag:
            # check how much markup exists between the nearest parent opening tag and button
            # find opening tag before this button that isn't closed
            not_first.append((p, line_no, btn_tag))

print(f"Buttons checked. Potential non-first buttons: {len(not_first)}")
for p, l_no, tag in not_first[:15]:
    print(f"In {p}:{l_no} -> {tag[:80]}")

