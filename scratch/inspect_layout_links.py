with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for idx, l in enumerate(lines):
    if 'sys-school-info' in l or 'admin-system-school-info' in l:
        print(f"L{idx+1}: {l.strip()}")
        for k in range(max(0, idx-5), min(len(lines), idx+10)):
            print(f"  {k+1}: {lines[k]}")
        break

for idx, l in enumerate(lines):
    if 'principal' in l and 'school' in l.lower():
        print(f"Principal school match L{idx+1}: {l.strip()}")

