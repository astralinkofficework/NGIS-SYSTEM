with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('SYSTEM & SECURITY')
print(c[idx-100:idx+350])

