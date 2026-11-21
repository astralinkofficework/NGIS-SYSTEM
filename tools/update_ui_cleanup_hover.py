with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the interactive cards from the blanket hover lockdown in ui-cleanup.css:
interactive_selectors = [
    ".portal-card:hover,",
    ".card-hover:hover,",
    ".card-hover-sm:hover,",
    ".ql-card:hover,",
    ".module-card:hover,",
    ".dept-card:hover,",
    ".task-card:hover,",
    ".ann-card:hover,",
    ".exam-card:hover,",
    ".subj-card:hover,",
    ".exw-timeline-card:hover,",
    ".interactive-card:hover,"
]

for sel in interactive_selectors:
    if sel in text:
        text = text.replace(sel, "/* " + sel + " */")
        print(f"Removed {sel} from blanket lockdown in ui-cleanup.css")

# Also ensure [class*="card"] doesn't block interactive cards:
old_match = '[class*="card"]:not([style*="background"]):hover,'
new_match = '[class*="card"]:not([style*="background"]):not(.portal-card):not(.card-hover):not(.ql-card):not(.module-card):not(.dept-card):not(.task-card):not(.ann-card):not(.exam-card):not(.subj-card):not(.exw-timeline-card):not(.interactive-card):hover,'

if old_match in text:
    text = text.replace(old_match, new_match)
    print("Exempted interactive cards from [class*=\"card\"] hover lockdown in ui-cleanup.css")

with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved assets/css/ui-cleanup.css successfully!")
