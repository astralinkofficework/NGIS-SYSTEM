import os
import glob
import re

font_link_replacement = 'family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter'

student_html_files = glob.glob(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\*.html')
shared_html_files = glob.glob(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\shared\*.html')

all_files = student_html_files + shared_html_files

updated_count = 0

for fpath in all_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    
    # If file doesn't have Plus Jakarta Sans in google font link
    if 'Plus+Jakarta+Sans' not in content:
        # If it has family=Inter
        if 'family=Inter' in content:
            content = content.replace('family=Inter', font_link_replacement)
            modified = True
        elif 'fonts.googleapis.com' in content:
            # Add before </head>
            link_tag = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">\n'
            content = content.replace('</head>', link_tag + '</head>')
            modified = True

    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated font in {os.path.basename(fpath)}")
        updated_count += 1
    else:
        print(f"Already had font or untouched: {os.path.basename(fpath)}")

print(f"\nTotal files updated with Plus Jakarta Sans: {updated_count}")
