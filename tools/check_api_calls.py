with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'api\(', text)]
for m in matches:
    start = max(0, m - 20)
    end = min(len(text), m + 80)
    print("--- API CALL ---")
    print(text[start:end])
