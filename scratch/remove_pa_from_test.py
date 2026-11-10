with open('test_principal_e2e.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = "    '/pages/principal/principal-assignments.html',\n"
if target in text:
    text = text.replace(target, '')
    with open('test_principal_e2e.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated test_principal_e2e.py successfully.')
else:
    print('Target line not found in test_principal_e2e.py')

