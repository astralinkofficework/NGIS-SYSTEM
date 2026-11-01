import glob, re

bold_patterns = [r'font-bold', r'font-extrabold', r'font-black', r'font-weight:\s*700', r'font-weight:\s*800', r'font-weight:\s*900']

for f in sorted(glob.glob('pages/student/*.html')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    found = []
    for pat in bold_patterns:
        matches = re.findall(pat, c, flags=re.IGNORECASE)
        if matches:
            found.append(f"{pat} ({len(matches)})")
    if found:
        print(f"{f}: {', '.join(found)}")
    else:
        print(f"{f}: CLEAN (No heavy bold fonts found)")

