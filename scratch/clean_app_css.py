with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('#052659', '#176B45')
text = text.replace('#DCE8F3', '#E1E9E3')
text = text.replace('#dce8f3', '#e1e9e3')
text = text.replace('#EAF6FF', '#E8F3ED')
text = text.replace('#eaf6ff', '#e8f3ed')
text = text.replace('#021024', '#29352E')
text = text.replace('#C1E8FF', '#E8F3ED')
text = text.replace('#c1e8ff', '#e8f3ed')

# In comments or titles
text = text.replace('Charcoal Blue', 'Forest Green')
text = text.replace('Midnight Navy', 'Dark Charcoal')
text = text.replace('Light Blue', 'Soft Mint')
text = text.replace('Ghost White', 'Off White')

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(text)

print('app.css clean replacements complete.')

