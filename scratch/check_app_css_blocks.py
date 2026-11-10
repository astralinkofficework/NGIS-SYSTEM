with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== 515-560 ===")
for i in range(514, 560):
    print(f"{i+1}: {lines[i]}", end='')

print("\n=== 693-712 ===")
for i in range(693, 712):
    print(f"{i+1}: {lines[i]}", end='')

print("\n=== 1015-1038 ===")
for i in range(1015, 1038):
    print(f"{i+1}: {lines[i]}", end='')

