import glob
import re

html_files = sorted(glob.glob("pages/**/*.html", recursive=True) + glob.glob("*.html"))

for f in html_files:
    with open(f, "r", encoding="utf-8") as fp:
        c = fp.read()
    m = re.search(r'tailwind\.config\s*=\s*\{.*?\};?', c, re.DOTALL)
    if m:
        block = m.group(0)
        # Check if colors are defined
        if "colors:" in block or "colors :" in block:
            print(f"[{f}] has tailwind.config with custom colors")

