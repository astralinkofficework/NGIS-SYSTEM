with open('pages/student/css/overlap.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['ov-card-head', 'ov-deadline-panel', 'ov-inner-panel', 'ov-inner-head', 'ov-deadline-head', 'sec-head', 'card-head']):
        print(f"Line {i+1}: {l.strip()}")
        for j in range(max(0, i-2), min(i+15, len(lines))):
            print(f"  {j+1}: {lines[j].strip()}")

