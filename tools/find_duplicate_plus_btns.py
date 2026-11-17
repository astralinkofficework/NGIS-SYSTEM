import os, re

dup_btn_re = re.compile(r'<button[^>]*>.*?((?:ph-plus|bi-plus|add|icon).*?\+\s*[A-Z]|\+\s*<[^>]+>.*?\+)', re.DOTALL | re.IGNORECASE)

findings = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                # Find buttons that contain an icon or svg AND a '+' sign in their span
                for m in re.finditer(r'<button[^>]*>([\s\S]*?)</button>', content):
                    btn_inner = m.group(1)
                    if ('svg' in btn_inner or 'ph-plus' in btn_inner or 'bi-plus' in btn_inner or 'material-symbols' in btn_inner):
                        # check if span has leading +
                        if re.search(r'<span>\s*\+\s*[A-Za-z]', btn_inner) or re.search(r'>\s*\+\s*[A-Za-z]', btn_inner):
                            findings.append((path, m.group(0).strip()))

print(f"Total buttons with duplicate plus/icon: {len(findings)}")
for path, btn in findings:
    print(f"\n{path}:\n  {btn[:150]}...")
