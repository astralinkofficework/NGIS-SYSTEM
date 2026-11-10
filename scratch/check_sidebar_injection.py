with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('buildSidebar')
if pos == -1: pos = text.find('sidebar')
print(text[pos:pos+1000])

