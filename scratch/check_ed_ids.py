with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'edName_' in line or 'edDept_' in line or 'saveRowEditor' in line:
        print(f"{i+1}: {line.strip()[:100]}")

