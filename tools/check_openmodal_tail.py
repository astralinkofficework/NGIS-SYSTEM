with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function openModal(')
print(text[idx+1200:idx+2000])
