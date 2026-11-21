with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('return `\n\n        <tr')
if idx == -1:
    idx = text.find('return `\n        <tr')
if idx == -1:
    idx = text.find('<tr class="border-b')
print('Found <tr in renderTable at:', idx)
print(repr(text[idx-50:idx+350]))
