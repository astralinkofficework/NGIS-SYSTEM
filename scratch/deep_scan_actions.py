import glob, re

for path in sorted(glob.glob('pages/**/*.html', recursive=True) + glob.glob('pages/**/*.js', recursive=True)):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find any table action patterns
    # Find any <button or <a that has text in an action-group or table row
    # Also find any action-btn-pill
    found = []
    
    # 1. Search for buttons inside action-group with text
    ag_blocks = re.findall(r'<div class="[^"]*action-group[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
    for ag in ag_blocks:
        btns = re.findall(r'<button[^>]*>(.*?)</button>', ag, re.DOTALL)
        for b in btns:
            txt = re.sub(r'<[^>]+>', ' ', b).strip()
            txt = ' '.join(txt.split())
            if txt:
                found.append(f"In action-group: {txt}")

    # 2. Search for action-btn-pill
    pills = re.findall(r'<button[^>]*class="[^"]*action-btn-pill[^"]*"[^>]*>(.*?)</button>', content, re.DOTALL)
    for p in pills:
        txt = re.sub(r'<[^>]+>', ' ', p).strip()
        txt = ' '.join(txt.split())
        found.append(f"action-btn-pill: {txt}")

    # 3. Search for any buttons in <td ...> that are not purely numbers or single char
    # In JS templates or HTML
    td_btns = re.findall(r'<td[^>]*>(.*?)</td>', content, re.DOTALL)
    for td in td_btns:
        if '<button' in td:
            btns = re.findall(r'<button[^>]*>(.*?)</button>', td, re.DOTALL)
            for b in btns:
                txt = re.sub(r'<[^>]+>', ' ', b).strip()
                txt = ' '.join(txt.split())
                # filter out non-actions
                if any(w in txt.lower() for w in ['edit', 'view', 'delete', 'authorize', 'review', 'return', 'approve', 'reject', 'audit', 'manage', 'handover', 'upload', 'notify', 'clear', 'excuse', 'activate', 'deactivate', 'slip', 'memo', 'snapshot', 'sign', 'revision']):
                    found.append(f"td button action word: {txt}")

    if found:
        unique_found = list(dict.fromkeys(found))
        print(f"\nFILE: {path}")
        for item in unique_found:
            print(f"  {item}")

