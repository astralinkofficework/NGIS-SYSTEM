import re

# 1. Update design-system.css
with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    ds = f.read()

interactive_cards = [
    '.portal-card:hover,',
    '.ql-card:hover,',
    '.module-card:hover,',
    '.dept-card:hover,',
    '.task-card:hover,',
    '.ann-card:hover,',
    '.exam-card:hover,',
    '.subj-card:hover,',
    '.card-hover:hover,',
    '.card-hover-sm:hover,',
    '.lesson-card:hover,'
]

for ic in interactive_cards:
    if ic in ds:
        ds = ds.replace(ic, "/* " + ic + " */")
        print(f"Exempted {ic} in design-system.css")

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(ds)

# 2. Update interactions.css
with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    it = f.read()

# Replace old lockdown selectors in interactions.css
for ic in ['.portal-card:hover,', '.ql-card:hover,', '.module-card:hover,', '.dept-card:hover,', '.task-card:hover,', '.ann-card:hover,', '.exam-card:hover,', '.subj-card:hover,', '.card-hover:hover,']:
    if ic in it:
        it = it.replace(ic, "/* " + ic + " */")
        print(f"Exempted {ic} in interactions.css")

with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
    f.write(it)

# 3. Also in ui-cleanup.css, ensure html body .card:hover does not override interactive cards
with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    uc = f.read()

target_card = 'html body .card:hover,'
target_card_new = 'html body .card:not(.portal-card):not(.card-hover):not(.ql-card):not(.module-card):not(.dept-card):not(.task-card):not(.ann-card):not(.exam-card):not(.subj-card):not(.exw-timeline-card):not(.interactive-card):hover,'
if target_card in uc:
    uc = uc.replace(target_card, target_card_new)
    print("Exempted interactive cards from html body .card:hover in ui-cleanup.css")

with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
    f.write(uc)

print("Harmonized interactive card lift across all stylesheets successfully!")
