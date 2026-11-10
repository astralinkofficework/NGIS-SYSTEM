with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('school-information')
while pos != -1:
    print(text[pos-100:pos+150])
    print('---')
    pos = text.find('school-information', pos + 1)

