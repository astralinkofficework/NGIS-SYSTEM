import glob
import re

html_files = sorted(glob.glob("pages/**/*.html", recursive=True) + glob.glob("*.html"))

# Filter out external/skill docs if any
project_html_files = [f for f in html_files if not f.startswith(".agents")]

print(f"Targeting {len(project_html_files)} project HTML files for blue color transformation...")

# Replacements dictionary
color_replacements = [
    # Previous soft gray canvas/secondary surface -> Pale Blue #EAF6FF
    (re.compile(r'#F3F3F5', re.I), '#EAF6FF'),
    (re.compile(r'#F8FAFB', re.I), '#EAF6FF'),
    (re.compile(r'#F1F5F9', re.I), '#EAF6FF'),
    (re.compile(r'#ECEEEF', re.I), '#EAF6FF'),
    (re.compile(r'#F8FAFC', re.I), '#EAF6FF'),
    
    # Previous hairline borders -> Light Blue Border #DCE8F3
    (re.compile(r'#E5E5E8', re.I), '#DCE8F3'),
    (re.compile(r'#D1D1D6', re.I), '#DCE8F3'),

    # Previous greens -> Deep Blue #052659 / Midnight Navy #021024 / Light Blue #C1E8FF
    (re.compile(r'#1E4D38', re.I), '#052659'),
    (re.compile(r'#133526', re.I), '#021024'),
    (re.compile(r'#013623', re.I), '#021024'),
    (re.compile(r'#002113', re.I), '#021024'),
    (re.compile(r'#006C49', re.I), '#5483B3'),
    (re.compile(r'#6CF8BB', re.I), '#C1E8FF'),
    (re.compile(r'#BBEED1', re.I), '#C1E8FF'),
    (re.compile(r'#DDEEE5', re.I), '#EAF6FF'),
    (re.compile(r'#BFDECF', re.I), '#C1E8FF'),
    (re.compile(r'#2D6A4F', re.I), '#5483B3'),
    (re.compile(r'#1B4332', re.I), '#052659'),
    
    # Previous navy -> Midnight Navy #021024 or Deep Blue #052659
    (re.compile(r'#202F63', re.I), '#021024'),
    (re.compile(r'#18234D', re.I), '#021024'),
    (re.compile(r'#111A38', re.I), '#021024'),
    
    # Previous burgundy -> Deep Blue #052659 (actions) / Midnight Navy #021024 (hover)
    (re.compile(r'#92243D', re.I), '#052659'),
    (re.compile(r'#7A1D32', re.I), '#021024'),
    (re.compile(r'#7E1E34', re.I), '#021024'),
    (re.compile(r'#FDF2F4', re.I), '#EAF6FF'),
    (re.compile(r'#FCE7EB', re.I), '#C1E8FF'),
]

updated_count = 0
for filepath in project_html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for pattern, repl in color_replacements:
        new_content = pattern.sub(repl, new_content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated_count += 1
        print(f"  Updated colors in {filepath}")

print(f"\nSuccessfully transformed {updated_count} HTML files!")

