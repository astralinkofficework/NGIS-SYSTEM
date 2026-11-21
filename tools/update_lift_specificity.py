with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Update the end lift rule in ui-cleanup.css with high-specificity selectors
old_lift = """@media (hover: hover) and (pointer: fine) {
  .portal-card:hover,
  .card-hover:hover,
  .ql-card:hover,
  .module-card:hover,
  .dept-card:hover,
  .task-card:hover,
  .ann-card:hover,
  .exam-card:hover,
  .subj-card:hover,
  .exw-timeline-card:hover,
  .interactive-card:hover,
  .ngis-card-lifted {
    transform: translateY(-2.5px) scale(1.007) !important;
    box-shadow: 0 8px 24px -4px rgba(15, 23, 20, 0.08), 0 2px 6px -2px rgba(15, 23, 20, 0.04) !important;
    transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
}"""

new_lift = """@media (hover: hover) and (pointer: fine) {
  a.portal-card[href]:hover,
  .portal-card:hover,
  a.card-hover[href]:hover,
  .card-hover:hover,
  a.ql-card[href]:hover,
  .ql-card:hover,
  a.module-card[href]:hover,
  .module-card:hover,
  a.dept-card[href]:hover,
  .dept-card:hover,
  a.task-card[href]:hover,
  .task-card:hover,
  a.ann-card[href]:hover,
  .ann-card:hover,
  a.exam-card[href]:hover,
  .exam-card:hover,
  a.subj-card[href]:hover,
  .subj-card:hover,
  .exw-timeline-card:hover,
  .interactive-card:hover,
  .ngis-card-lifted {
    transform: translateY(-2.5px) scale(1.007) !important;
    box-shadow: 0 8px 24px -4px rgba(15, 23, 20, 0.08), 0 2px 6px -2px rgba(15, 23, 20, 0.04) !important;
    transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
}"""

if old_lift in text:
    text = text.replace(old_lift, new_lift)
    print("Updated lift rule in ui-cleanup.css")
else:
    print("old_lift not found in ui-cleanup.css")

# Also in ui-cleanup.css exempt interactive cards from a[href] lockdown:
old_a_lock = 'a[href]:not(.btn):not([class*="btn"]):not([class*="border"]):not([class*="bg-"]):not([role="button"]):hover,'
new_a_lock = 'a[href]:not(.btn):not([class*="btn"]):not([class*="border"]):not([class*="bg-"]):not([role="button"]):not(.portal-card):not(.card-hover):not(.ql-card):not(.module-card):not(.dept-card):not(.task-card):not(.ann-card):not(.exam-card):not(.subj-card):not(.interactive-card):hover,'

if old_a_lock in text:
    text = text.replace(old_a_lock, new_a_lock)
    print("Exempted interactive card links from a[href] lockdown in ui-cleanup.css")

with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
    f.write(text)

# Also update interactions.css with the high-specificity selector
with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    it_text = f.read()

if old_lift in it_text:
    it_text = it_text.replace(old_lift, new_lift)
    with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
        f.write(it_text)
    print("Updated lift rule in interactions.css")

print("Saved stylesheets successfully!")
