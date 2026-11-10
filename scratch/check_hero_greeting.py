with open('assets/js/hero.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('greeting')
while pos != -1:
    print(text[pos-30:pos+150])
    print('---')
    pos = text.find('greeting', pos + 1)

