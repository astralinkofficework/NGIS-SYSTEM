import os, re

target_link = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500&family=Inter:wght@300;400;500&family=Kantumruy+Pro:wght@400;500&display=swap" rel="stylesheet">'
mat_icon_link = '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">'

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

updated_count = 0
for path in html_files:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig = content
    # Find all font links: <link href="https://fonts.googleapis.com/css2?..." rel="stylesheet"...>
    # Note: we need to distinguish between pure text font links and Material Symbols icon links
    
    def replacer(match):
        full_tag = match.group(0)
        # If this link contains Material Symbols and ALSO text fonts, we should replace text fonts with target_link
        # and keep Material Symbols
        if 'Material+Symbols' in full_tag or 'Material%20Symbols' in full_tag:
            if any(font_name in full_tag for font_name in ['Manrope', 'Plus+Jakarta', 'Inter', 'Cinzel', 'Kantumruy', 'Playfair', 'Outfit']):
                # Both text font and material symbols are combined
                return target_link + '\n  ' + mat_icon_link
            else:
                # It is ONLY Material Symbols, leave it as is
                return full_tag
        else:
            # It is a text font link, replace with target_link
            return target_link

    # Regex matching css2 font links
    content = re.sub(r'<link[^>]*href=["\']https://fonts\.googleapis\.com/css2\?[^"\']*["\'][^>]*>', replacer, content)
    
    # Also check if there's any preconnect or other outdated font link like Playfair or Cinzel
    content = re.sub(r'<link[^>]*href=["\'][^"\']*Cinzel[^"\']*["\'][^>]*>', '', content)
    content = re.sub(r'<link[^>]*href=["\'][^"\']*Playfair[^"\']*["\'][^>]*>', '', content)
    
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f'Successfully updated Google Fonts in {updated_count} HTML files.')

