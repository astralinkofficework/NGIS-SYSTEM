with open('assets/js/ngis-profiles.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[180:360]):
    print(f"{i+181}: {line.rstrip()}")

