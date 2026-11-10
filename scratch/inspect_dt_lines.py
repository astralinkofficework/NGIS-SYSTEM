with open('assets/css/design-tokens.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect lines 125-165
lines = text.splitlines()
for i in range(120, min(len(lines), 165)):
    print(f'{i+1}: {lines[i]}'.encode('ascii', 'replace').decode('ascii'))

