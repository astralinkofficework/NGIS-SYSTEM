with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1048, min(len(lines), 1150)):
    print(f"{i+1}: {lines[i].rstrip()}")

