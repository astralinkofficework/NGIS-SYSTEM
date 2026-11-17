import glob, re

for ext in ['assets/js/*.js', 'assets/css/*.css']:
    for f in glob.glob(ext):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            if 'ph-bold' in c:
                print(f"{f}: contains ph-bold ({c.count('ph-bold')} times)")
            if 'font-weight' in c and ('nav-icon' in c or 'sidebar' in c):
                for m in re.finditer(r'([^{}]*?(?:nav-icon|sidebar|nav-link-icon)[^{}]*?\{[^}]*?font-weight[^}]*?\})', c):
                    print(f"{f} match: {m.group(0).strip()[:150]}")
