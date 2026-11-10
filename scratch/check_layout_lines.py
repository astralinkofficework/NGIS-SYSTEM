with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(607, 675):
    print(f"{i+1}: {lines[i]}")

