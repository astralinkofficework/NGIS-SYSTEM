with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for idx, l in enumerate(lines):
    if 'admin-records.html' in l or 'principal-records.html' in l:
        print(f"L{idx+1}: {l.strip()[:100]}")
        for j in range(max(0, idx-5), min(len(lines), idx+15)):
            print(f"  {j+1}: {lines[j]}")
        break

