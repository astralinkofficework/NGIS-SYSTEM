import glob, re

css_files = glob.glob('assets/**/*.css', recursive=True) + glob.glob('pages/**/*.css', recursive=True)
for f in css_files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    if 'sidebar' in c:
        for m in re.finditer(r'([^{}]*nav-link\.active[^{}]*\{[^}]*\})', c):
            print(f"{f}: {m.group(0).strip()[:140]}")

