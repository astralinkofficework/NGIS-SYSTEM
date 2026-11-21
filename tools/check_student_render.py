with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- renderStudent (lines 388-446) ---")
for j in range(387, min(len(lines), 446)):
    print(f'{j+1}: {lines[j].rstrip()[:110]}')

print("\n--- studentShell (lines 900-923) ---")
for j in range(899, min(len(lines), 923)):
    print(f'{j+1}: {lines[j].rstrip()[:110]}')
