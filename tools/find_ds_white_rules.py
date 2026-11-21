import re

with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all css blocks
blocks = re.findall(r'([^{}]+)\{([^{}]+)\}', content)
print(f"Total CSS blocks in design-system.css: {len(blocks)}")

white_blocks = []
for sel, body in blocks:
    if 'background' in body and ('#ffffff' in body.lower() or '#fff' in body.lower() or 'white' in body.lower()):
        # check if it applies to card, a, hub, or :hover
        sel_clean = re.sub(r'\s+', ' ', sel.strip())
        white_blocks.append((sel_clean, body.strip()))

print(f"Total white background blocks: {len(white_blocks)}")
for sel, body in white_blocks:
    print("\n--- SELECTOR ---")
    print(sel[:120])
    for line in body.split(';'):
        if 'background' in line:
            print("   ", line.strip())
