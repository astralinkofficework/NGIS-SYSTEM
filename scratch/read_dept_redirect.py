with open('pages/shared/departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('window.location.href = \'../teacher')
print(text[max(0, idx-400):min(len(text), idx+600)].encode('ascii', errors='replace').decode('ascii'))

