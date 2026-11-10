with open('assets/js/ngis-profiles.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines in ngis-profiles.js:", len(lines))
for i, line in enumerate(lines):
    if line.strip().startswith('function '):
        print(f"Line {i+1}: {line.strip()[:60]}")

