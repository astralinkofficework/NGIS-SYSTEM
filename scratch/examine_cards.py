with open("pages/principal/principal-classes.html", "r", encoding="utf-8") as f:
    classes_html = f.read()

with open("pages/principal/principal-departments.html", "r", encoding="utf-8") as f:
    depts_html = f.read()

import re

print("CLASSES CARDS:")
cards = re.findall(r'(<div class="[^"]*telemetry-card[^"]*">.*?</div>\s*</div>)', classes_html, re.DOTALL)
for i, c in enumerate(cards):
    print(f"--- Card {i+1} ---")
    print(c)

print("\n" + "="*50 + "\nDEPTS CARDS:")
cards2 = re.findall(r'(<div class="[^"]*telemetry-card[^"]*">.*?</div>\s*</div>)', depts_html, re.DOTALL)
for i, c in enumerate(cards2):
    print(f"--- Card {i+1} ---")
    print(c)

