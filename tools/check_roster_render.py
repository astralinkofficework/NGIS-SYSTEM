with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_fn = text.find('function renderRoster')
if idx_fn == -1:
    idx_fn = text.find('renderRoster')
print(text[idx_fn:idx_fn+600])
