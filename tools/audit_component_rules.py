import re, glob

css_files = [
    'assets/css/design-system.css',
    'assets/css/app.css',
    'assets/css/ui-cleanup.css',
    'assets/css/hero.css',
    'assets/css/interactions.css',
    'assets/css/shared-components.css',
    'assets/css/portal-dashboard.css',
    'assets/css/admin-dna.css'
]

print("=== CHECKING CARD PADDING IN CSS ===")
for cf in css_files:
    try:
        with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # find card padding rules
            matches = re.findall(r'(\.[\w-]*card[\w-]*\s*\{[^}]*padding[^;]+;[^}]*\})', content)
            if matches:
                print(f"[{cf}] found {len(matches)} card padding rules:")
                for m in matches[:3]:
                    clean = ' '.join(m.split())
                    print("  ", clean[:120])
    except Exception as e:
        pass

print("\n=== CHECKING TABLE PADDING IN CSS ===")
for cf in css_files:
    try:
        with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = re.findall(r'((?:th|td|\.tbl\s+t[hd])\s*\{[^}]*padding[^;]+;[^}]*\})', content)
            if matches:
                print(f"[{cf}] found {len(matches)} table padding rules:")
                for m in matches[:3]:
                    clean = ' '.join(m.split())
                    print("  ", clean[:120])
    except Exception as e:
        pass

print("\n=== CHECKING BUTTON AND INPUT HEIGHTS IN CSS ===")
for cf in css_files:
    try:
        with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = re.findall(r'(\.(?:btn|input|select)[\w-]*\s*\{[^}]*height:[^;]+;[^}]*\})', content)
            if matches:
                print(f"[{cf}] found {len(matches)} height rules:")
                for m in matches[:3]:
                    clean = ' '.join(m.split())
                    print("  ", clean[:120])
    except Exception as e:
        pass
