with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('data-action="new"')
while idx != -1:
    print("Found at", idx)
    print(text[idx-100:idx+300])
    print("-" * 50)
    idx = text.find('data-action="new"', idx+1)
