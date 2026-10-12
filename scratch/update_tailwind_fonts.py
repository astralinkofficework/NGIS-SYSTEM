import glob
import re

files = [
    r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student-assignments.html',
    r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student-grades.html',
    r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student-exams.html',
    r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student-services.html',
    r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student-lost-found.html',
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    c = re.sub(r'sans:\s*\[\s*[\'"]Inter[\'"]', 'sans: [\'"Plus Jakarta Sans"\', \'"Inter"\'', c)
    c = re.sub(r'display:\s*\[\s*[\'"]Inter[\'"]', 'display: [\'"Plus Jakarta Sans"\', \'"Inter"\'', c)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated tailwind font in", fpath)
