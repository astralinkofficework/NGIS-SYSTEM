with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("action === 'new'")
print(text[idx-300:idx+300])
