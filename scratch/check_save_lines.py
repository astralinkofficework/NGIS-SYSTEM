with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[965:985]):
    print(f"{i+966}: {repr(l)}")

