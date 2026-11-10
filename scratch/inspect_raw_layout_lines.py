with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(600, 675):
    print(f"{i+1}: {repr(lines[i])}")

