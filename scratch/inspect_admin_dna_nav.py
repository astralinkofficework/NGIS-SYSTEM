with open('assets/css/admin-dna.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(54, min(105, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

