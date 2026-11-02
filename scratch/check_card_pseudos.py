import os, re, sys

for root, dirs, files in os.walk('.'):
    if any(ign in root for ign in ['.git', 'node_modules', '.system_generated', 'skills']):
        continue
    for f in files:
        if f.endswith('.css'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                text = fp.read()
                matches = re.findall(r'([^{}]*card[^{}]*::(?:before|after)[^{]*\{[^}]*\})', text, re.I)
                if matches:
                    print(f"=== {path} ({len(matches)} card pseudo rules) ===")
                    for m in matches:
                        print("  ", ' '.join(m.split())[:120])

