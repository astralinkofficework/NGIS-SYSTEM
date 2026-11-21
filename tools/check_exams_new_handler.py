with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('action === \'new\'')
if idx == -1:
    idx = text.find("action === 'new'")
if idx == -1:
    idx = text.find("action === \"new\"")
if idx == -1:
    idx = text.find("data-action=\"new\"")
    idx = text.find("case 'new'", idx)
print("new handler idx:", idx)
if idx != -1:
    print(text[idx-100:idx+300])
