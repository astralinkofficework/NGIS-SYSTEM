for path in [r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\css\hero.css', r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\css\hero.css']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace("'Inter', sans-serif", "'Plus Jakarta Sans', 'Inter', sans-serif")
    c = c.replace("'Inter', 'Kantumruy Pro'", "'Plus Jakarta Sans', 'Inter', 'Kantumruy Pro'")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated", path)
