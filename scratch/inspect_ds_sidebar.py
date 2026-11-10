with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length:", len(text))
lines = text.splitlines()
for i, l in enumerate(lines):
    if 'sidebar' in l.lower():
        print(f"{i+1}: {l[:100]}")

