with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id: "school-information"')
print(text[pos-400:pos+300])

