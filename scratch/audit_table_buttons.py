import glob, re

button_with_text_files = set()

# Search HTML and JS files
all_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('pages/**/*.js', recursive=True) + glob.glob('assets/**/*.js', recursive=True)

for path in all_files:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
        # Look for buttons in td or table contexts that have text nodes
        # e.g., <button ...>...Word...</button>
        # or inside template literals in JS
        
        # Match table rows or td
        matches = []
        # Pattern 1: action-btn-pill
        if 'action-btn-pill' in content:
            matches.append('action-btn-pill')
        
        # Pattern 2: td with button containing text (e.g. <span>Edit</span> or text after icon)
        # Find all td...</td>
        tds = re.findall(r'<td[^>]*>(.*?)</td>', content, re.DOTALL)
        for td in tds:
            btns = re.findall(r'<button[^>]*>(.*?)</button>', td, re.DOTALL)
            for btn in btns:
                # Strip all tags from btn and check if there are non-whitespace words
                clean_text = re.sub(r'<[^>]+>', '', btn).strip()
                # Exclude purely numbers (like pagination or single char like + or P/L/A/E in attendance cell)
                if clean_text and not re.match(r'^[\d\+\-✕✓•·]$', clean_text) and not clean_text in ['P', 'L', 'A', 'E']:
                    matches.append(f'Text in button: "{clean_text[:30]}"')
                    break
            if len(matches) > 3:
                break
        
        # Pattern 3: Template strings in JS with <button...>word</button>
        js_btn_matches = re.findall(r'<button[^>]*class="[^"]*(?:action|btn)[^"]*"[^>]*>(.*?)</button>', content, re.DOTALL)
        for btn in js_btn_matches:
            clean_text = re.sub(r'<[^>]+>', '', btn).strip()
            if clean_text and not re.match(r'^[\d\+\-✕✓•·]$', clean_text) and not clean_text in ['P', 'L', 'A', 'E']:
                matches.append(f'JS Template button: "{clean_text[:30]}"')
                break

        if matches:
            button_with_text_files.add(path)
            print(f"\n{path}:")
            for m in matches[:4]:
                print(f"  - {m}")

