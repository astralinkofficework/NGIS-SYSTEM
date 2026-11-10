import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open('assets/js/layout.js', encoding='utf-8', errors='replace').read()
lines = src.splitlines()
for i, l in enumerate(lines):
    if re.search(r'buildTopbar|topbar|htb-left|heroTopbar|hero-topbar|HERO', l):
        print(i + 1, l.strip()[:160])
