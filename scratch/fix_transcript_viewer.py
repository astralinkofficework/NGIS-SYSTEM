with open('pages/shared/transcript-viewer.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<!-- Google Fonts: Plus Jakarta Sans & Playfair Display -->', '<!-- Google Fonts: Manrope, Plus Jakarta Sans, Inter & Kantumruy Pro -->')
c = c.replace('serif: [\'"Playfair Display"\', \'Georgia\', \'serif\'],', 'serif: [\'"Manrope"\', \'"Plus Jakarta Sans"\', \'serif\'],')

with open('pages/shared/transcript-viewer.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated transcript-viewer.html')
