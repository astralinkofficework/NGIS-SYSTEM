with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's check exact lines we plan to modify
sub1 = '.nav-link-icon { font-size: 20px !important; color: var(--color-mint, #E8F3ED) !important; line-height: 1; flex-shrink: 0; transition: color 150ms ease; }'
sub2 = '.nav-link:hover .nav-link-icon { font-size: 20px !important; color: var(--color-mint, #E8F3ED) !important; line-height: 1; flex-shrink: 0; transition: color 150ms ease; }'

print('sub1 in text:', sub1 in text)
print('sub2 in text:', sub2 in text)

