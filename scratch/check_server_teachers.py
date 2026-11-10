with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("'teachers': [")
print(text[pos+1100:pos+1800])
