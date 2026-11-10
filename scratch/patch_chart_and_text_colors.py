import glob
import re

html_files = sorted(glob.glob("pages/**/*.html", recursive=True) + glob.glob("*.html"))
project_html_files = [f for f in html_files if not f.startswith(".agents")]

replacements = [
    (re.compile(r'#555555\b', re.I), '#5483B3'),
    (re.compile(r'#77777F\b', re.I), '#7DA0CA'),
    (re.compile(r'#333333\b', re.I), '#5483B3'),
]

updated = 0
for filepath in project_html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for pattern, repl in replacements:
        new_content = pattern.sub(repl, new_content)

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        updated += 1
        print(f"  Mapped secondary/chart colors in {filepath}")

print(f"Updated {updated} files with Steel Blue and Muted Blue!")

