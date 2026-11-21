with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('return `\n          <tr')
if idx == -1:
    idx = text.find('<tr class="border-b border-slate-100')
print('Found <tr at:', idx)
print(repr(text[idx-50:idx+250]))
