with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function init')
if pos == -1: pos = text.find('initLayout')
if pos == -1: pos = text.find('init(')
print(text[pos:pos+1200])

