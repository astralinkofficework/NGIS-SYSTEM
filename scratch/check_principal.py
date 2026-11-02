with open('pages/principal/principal.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('has <aside>:', '<aside' in text)
print('has id="sidebar":', 'id="sidebar"' in text)
print('has sidebar class:', 'class="sidebar"' in text or "class='sidebar'" in text)

