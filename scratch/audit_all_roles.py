import os, re

for role in ['teacher', 'admin', 'principal', 'staff', 'shared']:
    p = os.path.join('pages', role)
    if not os.path.exists(p):
        continue
    files = [f for f in os.listdir(p) if f.endswith('.html')]
    print(f"\n==================== CHECKING {role.upper()} ({len(files)} files) ====================")
    for f in sorted(files):
        fp = os.path.join(p, f)
        with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            page_match = re.search(r'window\.PAGE\s*=\s*({[^}]+})', content)
            page_cfg = page_match.group(1).replace('\n', ' ') if page_match else "MISSING"
            data_role = re.search(r'data-role=[\'"]([^\'"]+)[\'"]', content)
            role_attr = data_role.group(1) if data_role else "none"
            
            # Check for cross-portal redirects or links
            # (e.g. In student, pointing to teacher; in teacher, pointing to student)
            redirs = re.findall(r'(?:window\.)?location\.(?:href|replace)\s*=\s*[\'"`]([^\'"`]+)[\'"`]', content)
            
            print(f"{f}: PAGE={page_cfg} | data-role={role_attr} | redirs={redirs if redirs else 'none'}")

