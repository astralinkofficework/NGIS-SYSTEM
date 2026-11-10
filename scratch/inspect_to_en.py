with open("assets/js/khmer-suite-data.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, l in enumerate(lines):
    if 'toen' in l.lower() or 'day' in l.lower() and 'mon' in l.lower():
        print(f"L{idx+1}: {l.strip()[:100]}")

