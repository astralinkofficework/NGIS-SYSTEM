with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect buildSidebar lines 608 to 680
lines = text.splitlines()
for i in range(607, 720):
    print(f"{i+1}: {lines[i]}")

