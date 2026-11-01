with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    text = f.read()

for word in ['Faculty', 'Discipline', 'Mathematics', 'cohort', 'metric', 'stat']:
    idx = text.lower().find(word.lower())
    if idx != -1:
        print(f'Word "{word}" found at {idx}:')
        print(text[max(0, idx-50):min(len(text), idx+100)].replace('\n', ' ').encode('ascii', errors='replace').decode('ascii'))
        print('---')

