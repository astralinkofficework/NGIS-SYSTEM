with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('admin_operations_bp')
print(text[pos-100:pos+300])

