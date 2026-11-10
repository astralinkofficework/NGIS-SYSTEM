with open('assets/css/school-information.css', 'r', encoding='utf-8') as f:
    text = f.read()

for term in ['si-title', 'si-subtitle']:
    print(term, 'count:', text.count(term))

