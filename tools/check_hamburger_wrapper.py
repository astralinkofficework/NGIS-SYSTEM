with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('htb-hamburger')
print(text[idx-200:idx+300])
