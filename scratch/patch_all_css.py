import glob
import re

css_files = sorted(glob.glob("assets/css/*.css") + glob.glob("pages/**/css/*.css", recursive=True))

replacements = [
    ("#F3F3F5", "#EAF6FF"),
    ("#f3f3f5", "#EAF6FF"),
    ("#F8FAFB", "#EAF6FF"),
    ("#f8fafb", "#EAF6FF"),
    ("#F1F5F9", "#EAF6FF"),
    ("#f1f5f9", "#EAF6FF"),
    ("#E5E5E8", "#DCE8F3"),
    ("#e5e5e8", "#DCE8F3"),
    ("#202F63", "#052659"),
    ("#202f63", "#052659"),
    ("#18234D", "#021024"),
    ("#18234d", "#021024"),
    ("#1e4d38", "#052659"),
    ("#1E4D38", "#052659"),
    ("#133526", "#021024"),
    ("#013623", "#021024"),
    ("#92243D", "#052659"),
    ("#92243d", "#052659"),
    ("#7A1D32", "#021024"),
    ("#7a1d32", "#021024"),
    ("#7E1E34", "#021024"),
    ("#7e1e34", "#021024"),
    ("#BBEED1", "#C1E8FF"),
    ("#bbeed1", "#C1E8FF"),
]

for filepath in css_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filepath}")

print("All CSS files processed!")

