with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderOverview = function')
if pos == -1: pos = text.find('function renderOverview')
print(text[pos:pos+2000])

