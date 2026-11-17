with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('sa-directories-drop')
print(text[pos-50:pos+800])
