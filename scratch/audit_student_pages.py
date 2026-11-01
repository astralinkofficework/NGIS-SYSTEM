import os, re

files = [f for f in os.listdir('pages/student') if f.endswith('.html')]
print(f"Checking {len(files)} student files...")

for f in sorted(files):
    p = os.path.join('pages/student', f)
    with open(p, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        
        # Check window.PAGE
        page_match = re.search(r'window\.PAGE\s*=\s*({[^}]+})', content)
        page_cfg = page_match.group(1).replace('\n', ' ') if page_match else "MISSING"
        
        # Check for teacher references
        teacher_refs = re.findall(r'href=[\'"][^\'"]*teacher[^\'"]*[\'"]|location\.href\s*=\s*[\'"][^\'"]*teacher[^\'"]*[\'"]', content, re.IGNORECASE)
        
        # Check for role in data attributes
        data_role = re.search(r'data-role=[\'"]([^\'"]+)[\'"]', content)
        role_attr = data_role.group(1) if data_role else "none"
        
        print(f"\n{f}:")
        print(f"  PAGE: {page_cfg}")
        print(f"  data-role: {role_attr}")
        if teacher_refs:
            print(f"  CRITICAL: Teacher references found ({len(teacher_refs)}): {teacher_refs[:3]}")

