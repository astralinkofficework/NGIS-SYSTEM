with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the anchor hover lockdown
target_a1 = 'a:not(.btn):not([class*="btn"]):not([class*="border"]):not([class*="bg-"]):not([role="button"]):hover,'
target_a1_new = 'a:not(.btn):not([class*="btn"]):not([class*="border"]):not([class*="bg-"]):not([role="button"]):not([class*="card"]):not(.card-hover):hover,'
text = text.replace(target_a1, target_a1_new)

target_a2 = 'a[href]:not(.btn):not([class*="btn"]):not([class*="border"]):not([class*="bg-"]):not([role="button"]):not(.portal-card):not(.card-hover):not(.ql-card):not(.module-card):not(.dept-card):not(.task-card):not(.ann-card):not(.exam-card):not(.subj-card):not(.interactive-card):hover,'
target_a2_new = 'a[href]:not(.btn):not([class*="btn"]):not([class*="border"]):not([class*="bg-"]):not([role="button"]):not([class*="card"]):not(.card-hover):hover,'
text = text.replace(target_a2, target_a2_new)

# Update the end lift rule
old_lift = """@media (hover: hover) and (pointer: fine) {
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

new_lift = """@media (hover: hover) and (pointer: fine) {
  html body [class*="card"]:not(.stat-card):not(.stat):not(.smx-kpi):not(.telemetry-card):not(.student-gov-card):hover,
  html body .portal-card:hover,
  html body .card-hover:hover,
  html body .ql-card:hover,
  html body .module-card:hover,
  html body .dept-card:hover,
  html body .task-card:hover,
  html body .ann-card:hover,
  html body .exam-card:hover,
  html body .subj-card:hover,
  html body .interactive-card:hover,
  html body .exw-timeline-card:hover,
  html body .ngis-card-lifted {
    transform: translateY(-2.5px) scale(1.007) !important;
    box-shadow: 0 8px 24px -4px rgba(15, 23, 20, 0.08), 0 2px 6px -2px rgba(15, 23, 20, 0.04) !important;
    transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), box-shadow 180ms cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
}"""

text = text.replace(old_lift, new_lift)

with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
    f.write(text)

# Also in interactions.css
with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    it = f.read()

it = it.replace(old_lift, new_lift)
with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
    f.write(it)

print("Updated ui-cleanup.css and interactions.css successfully!")
