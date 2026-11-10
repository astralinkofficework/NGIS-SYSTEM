with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines in khmer-suite-ui.js:", len(lines))
for idx, line in enumerate(lines):
    if 'ondrag' in line.lower() or 'dragstart' in line.lower() or 'drop' in line.lower() or 'renderbox' in line.lower() or 'slot-card' in line.lower() or 'ks-slot' in line.lower() or '7A · K1' in line:
        print(f"L{idx+1}: {line.strip()[:100]}")

