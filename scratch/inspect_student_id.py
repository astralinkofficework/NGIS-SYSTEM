with open('pages/student/student-id.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("--- student-id.html snippet ---")
print(text[text.find('<main'):text.find('</main>')][:1000])

