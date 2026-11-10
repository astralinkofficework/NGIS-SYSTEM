with open('assets/js/ngis-profiles.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[1098:1170]):
    print(f"{i+1099}: {line.rstrip()}")

