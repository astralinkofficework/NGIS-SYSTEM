import os, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'pages'
main_re = re.compile(r'class="[^"]*\bmain\b|<main\b')
for dp, _, fs in os.walk(root):
    for fn in sorted(fs):
        if not fn.endswith('.html'):
            continue
        p = os.path.join(dp, fn)
        src = open(p, encoding='utf-8', errors='replace').read()
        has_main = bool(main_re.search(src))
        asides = re.findall(r'<aside\b[^>]*', src)
        if not has_main or asides:
            print(os.path.relpath(p, root), '| main:', has_main, '| asides:', [a[:90] for a in asides[:3]])
