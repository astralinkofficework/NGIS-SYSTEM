import re
with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("assets/js/app.js length:", len(text))
for kw in ['card', 'hover', 'touch', 'click', 'pointer', 'ripple', 'effect', 'overlay', 'circle', 'glow']:
    print(f"{kw}: {len(re.findall(kw, text, re.I))} hits")
