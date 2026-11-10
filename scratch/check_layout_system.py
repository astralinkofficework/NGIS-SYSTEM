with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('SYSTEM & SECURITY')
print(text[pos-100:pos+500])

