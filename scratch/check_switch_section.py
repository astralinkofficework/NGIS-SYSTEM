with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('switchSection')
print(text[pos:pos+500])

