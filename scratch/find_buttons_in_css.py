import glob
import re

css_files = glob.glob('assets/css/*.css')

for cf in css_files:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    btn_defs = re.findall(r'(\.btn(?:-[a-zA-Z0-9_-]+)?|\.ngis-btn(?:-[a-zA-Z0-9_-]+)?)\s*\{([^}]+)\}', content)
    if btn_defs:
        print(f"\nIn {cf}:")
        for sel, decl in btn_defs[:8]:
            print(f"  {sel.strip()} => {decl.strip()[:70]}...")
