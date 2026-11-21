with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('htb-left')
if idx != -1:
    print(text[idx-100:idx+600])
