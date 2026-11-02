import os, re, sys

card_hover_rules = []
for root, dirs, files in os.walk('assets'):
    for f in files:
        if f.endswith('.css'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                text = fp.read()
                # Find any rule with card and hover
                matches = re.findall(r'([^{}]*card[^{}]*:(?:hover|active)[^{]*\{[^}]*\})', text, re.I)
                for m in matches:
                    card_hover_rules.append((path, m.strip()))

print(f"Total card hover/active rules in assets: {len(card_hover_rules)}")
for p, r in card_hover_rules[:25]:
    # print one line
    clean_r = ' '.join(r.split())
    print(f"{p}: {clean_r[:120]}")

