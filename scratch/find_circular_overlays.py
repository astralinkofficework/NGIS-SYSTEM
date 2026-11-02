import os, re

for root, dirs, files in os.walk('.'):
    if any(ign in root for ign in ['.git', 'node_modules', '.system_generated', 'skills']):
        continue
    for f in files:
        if f.endswith(('.css', '.html', '.js')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    # Check for overlay, ripple, touch or circle on cards
                    matches = re.findall(r'(\.?[a-zA-Z0-9_\-\s,>]+(?:card|item|tile|box|btn)[^{]*\{[^}]*(?:border-radius:\s*(?:50%|9999px)|radial-gradient|ripple|circle|backdrop-filter)[^}]*\})', content, re.I)
                    if matches:
                        print(f"=== {path} ({len(matches)} matches) ===")
                        for m in matches[:5]:
                            one_line = ' '.join(m.split())
                            print("  ", one_line[:130])
            except Exception as e:
                pass

