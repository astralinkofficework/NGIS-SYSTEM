with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length:", len(text))
print("Categories:")
cats = re.findall(r'data-category="([^"]+)"', text)
print(set(cats))
# Find headings and main cards
h2s = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', text)
print("Headings:", [h.strip() for h in h2s if h.strip()][:15])

