with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('pages/admin/admin-school-information.html')
print(text[pos-100:pos+300])

