import glob
import re

print("Auditing navigation, tables, and card backgrounds...")

# Check sidebar navigation active and hover states
for cf in ['assets/css/navbar.css', 'assets/css/mobile-header.css', 'assets/css/shared-components.css', 'assets/css/app.css', 'assets/css/interactions.css', 'assets/css/ui-cleanup.css']:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    nav_active = re.findall(r'(\.nav-link\.active[^{]*|\.nav-item\.active[^{]*|#sidebar[^{]*\.active[^{]*)\{([^}]+)\}', content)
    if nav_active:
        print(f"\nIn {cf} (active nav):")
        for sel, decl in nav_active:
            print(f"  {sel.strip()} => {decl.strip()[:80]}")

# Check table row and cell colors
for cf in ['assets/css/shared-components.css', 'assets/css/app.css', 'assets/css/interactions.css', 'assets/css/design-system.css', 'assets/css/admin-operations-control.css']:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    tbl_rules = re.findall(r'(tr:nth-child[^{]*|table\s+tr[^{]*|\.tbl[^{]*|th\b[^{]*|td\b[^{]*)\{([^}]+)\}', content)
    if tbl_rules:
        print(f"\nIn {cf} (tables):")
        for sel, decl in tbl_rules[:6]:
            print(f"  {sel.strip()} => {decl.strip()[:80]}")
