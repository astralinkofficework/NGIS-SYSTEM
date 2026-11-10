with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

print('File length:', len(text))
for term in ['viewSwitcher', 'Cambodian MoEYS Guidelines', 'drag', 'drop', 'renderBuilder', 'renderGrid']:
    print(f'Count of "{term}":', text.count(term))

