import glob, re

for path in sorted(glob.glob('pages/**/*.html', recursive=True)):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Look for table action columns or tr actions
    row_actions = []
    
    # 1. Action-btn-pill occurrences
    pills = re.findall(r'<button[^>]*class="[^"]*action-btn-pill[^"]*"[^>]*>(.*?)</button>', content, re.DOTALL)
    for p in pills:
        clean = re.sub(r'<[^>]+>', ' ', p).strip()
        clean = ' '.join(clean.split())
        row_actions.append(f"PILL: {clean}")
    
    # 2. Check <td> inside <tbody> that contain buttons with visible text
    tbody_matches = re.findall(r'<tbody[^>]*>(.*?)</tbody>', content, re.DOTALL)
    for tb in tbody_matches:
        trs = re.findall(r'<tr[^>]*>(.*?)</tr>', tb, re.DOTALL)
        for tr in trs:
            tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.DOTALL)
            if tds:
                last_td = tds[-1] # Usually actions column
                btns = re.findall(r'<button[^>]*>(.*?)</button>', last_td, re.DOTALL)
                for b in btns:
                    clean = re.sub(r'<[^>]+>', ' ', b).strip()
                    clean = ' '.join(clean.split())
                    if clean and not re.match(r'^[\d\+\-✕✓•·]$', clean) and not clean in ['P', 'L', 'A', 'E']:
                        row_actions.append(f"STATIC TD BTN: {clean}")

    # 3. Check JS template rows in <script> tags for table row rendering
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for scr in scripts:
        # Look for templates generating <tr> or <td> with <button ...>
        # e.g., `<tr...<td class="...table-actions"...`
        matches = re.findall(r'<td[^>]*class="[^"]*(?:table-actions|text-right)[^"]*"[^>]*>.*?</td>', scr, re.DOTALL)
        for m in matches:
            btns = re.findall(r'<button[^>]*>(.*?)</button>', m, re.DOTALL)
            for b in btns:
                clean = re.sub(r'<[^>]+>', ' ', b).strip()
                clean = ' '.join(clean.split())
                if clean and not clean in ['P', 'L', 'A', 'E']:
                    row_actions.append(f"JS TEMPLATE TD BTN: {clean}")

    if row_actions:
        # Deduplicate
        unique_actions = list(dict.fromkeys(row_actions))
        print(f"\n=== {path} ===")
        for a in unique_actions:
            print(f"  {a}")

