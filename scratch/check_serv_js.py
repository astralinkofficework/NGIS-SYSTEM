with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', text)
for s in scripts:
    if 'submitMobileNewRequest' in s or 'REQUEST_DETAILS_DATA' in s:
        lines = s.splitlines()
        print("Script block length:", len(lines))
        for line in lines[:100]:
            print(line)
        break

