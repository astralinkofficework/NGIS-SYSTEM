with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Modals in student-services:", re.findall(r'id="[^"]*modal[^"]*"', text, re.I))
