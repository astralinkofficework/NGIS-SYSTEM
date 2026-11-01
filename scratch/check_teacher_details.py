with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Has tailwindcss:', 'cdn.tailwindcss.com' in text)
print('Has promo-slideshow in dash-overlap:', 'promo-slideshow' in text[text.find('dash-overlap'):text.find('dash-banner')])
print('Overlap style:')
idx = text.find('dash-overlap')
print(text[idx-50:idx+250].replace('\n', ' ').encode('ascii', errors='replace').decode('ascii'))

