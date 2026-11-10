with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos_a = text.find('id:"academic"')
print('Admin academic context:')
print(text[pos_a-100:pos_a+400])

pos_p = text.find('id: "students-mgmt"')
print('\nPrincipal students-mgmt context:')
print(text[pos_p-100:pos_p+400])
