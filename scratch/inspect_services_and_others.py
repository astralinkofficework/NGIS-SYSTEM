with open('pages/principal/principal-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

print("=== principal-services.html ===")
matches = re.findall(r'<td[^>]*class="[^"]*table-actions[^"]*"[^>]*>.*?</td>', text, re.DOTALL)
for m in matches:
    print(m.strip())

print("\n=== principal-timetables.html ===")
with open('pages/principal/principal-timetables.html', 'r', encoding='utf-8') as f:
    tt_text = f.read()
matches = re.findall(r'<td[^>]*class="[^"]*table-actions[^"]*"[^>]*>.*?</td>', tt_text, re.DOTALL)
for m in matches:
    print(m.strip()[:200])

print("\n=== principal-departments.html ===")
with open('pages/principal/principal-departments.html', 'r', encoding='utf-8') as f:
    dept_text = f.read()
matches = re.findall(r'<td[^>]*class="[^"]*table-actions[^"]*"[^>]*>.*?</td>', dept_text, re.DOTALL)
for m in matches:
    print(m.strip()[:200])

print("\n=== principal-classes.html ===")
with open('pages/principal/principal-classes.html', 'r', encoding='utf-8') as f:
    cls_text = f.read()
matches = re.findall(r'<td[^>]*class="[^"]*table-actions[^"]*"[^>]*>.*?</td>', cls_text, re.DOTALL)
for m in matches:
    print(m.strip()[:200])

print("\n=== student-lost-found.html ===")
with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    lf_text = f.read()
matches = re.findall(r'<td[^>]*class="[^"]*table-actions[^"]*"[^>]*>.*?</td>', lf_text, re.DOTALL)
for m in matches:
    print(m.strip()[:200])

