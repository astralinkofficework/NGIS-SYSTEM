with open('assets/css/shared-components.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
btns = re.findall(r'(\.(?:ngis-)?btn[^{]*)\{([^}]+)\}', text)
print(f"Found {len(btns)} button rules in shared-components.css:")
for sel, decl in btns:
    if any(k in sel for k in ['primary', 'secondary', 'ghost', 'danger', 'tertiary']):
        print(f"  {sel.strip()} => {decl.strip()[:65]}")
