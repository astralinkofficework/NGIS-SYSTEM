with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

for marker in ['studentMobileView', 'idModal', 'layout.js']:
    idx = text.find(marker)
    print(f'Marker {marker}:')
    snippet = text[max(0, idx-100):min(len(text), idx+150)].replace('\n', ' ')
    print(snippet.encode('ascii', errors='replace').decode('ascii'))
    print('---')
