import re

with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract NAV object
m = re.search(r'const NAV = \{([\s\S]*?)\n  \};\s*\n\s*(?:const|function|let|var)', text)
if not m:
    print("Could not find NAV block")
    exit(1)

nav_code = m.group(1)

# Find each role definition: e.g. admin: { ... }, teacher: { ... }, etc.
# Roles in order: admin, teacher, student, principal, staff
roles = ['admin', 'teacher', 'student', 'principal', 'staff']
for i, role in enumerate(roles):
    next_role = roles[i+1] if i+1 < len(roles) else None
    if next_role:
        pattern = rf'^\s*{role}:\s*\{{([\s\S]*?)^\s*{next_role}:'
    else:
        pattern = rf'^\s*{role}:\s*\{{([\s\S]*?)\Z'
    rm = re.search(pattern, nav_code, re.M)
    if rm:
        rbody = rm.group(1)
        links = re.findall(r'\{\s*id:\s*[\'"]([^\'"]+)[\'"],\s*label:\s*[\'"]([^\'"]+)[\'"],\s*icon:\s*[\'"]([^\'"]+)[\'"],\s*href:\s*[\'"]([^\'"]+)[\'"]', rbody)
        print(f"=== {role.upper()} ({len(links)} links) ===")
        for lid, lbl, icon, href in links:
            print(f"  {lid:15} | {lbl:28} | {href}")
