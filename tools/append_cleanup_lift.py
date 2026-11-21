with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    text = f.read()

lift_rule = """
/* ==========================================================================
   NGIS Global Motion System — Subtle Card Lift Effect on Interactive Cards
   ========================================================================== */
@media (hover: hover) and (pointer: fine) {
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
}
"""

if "NGIS Global Motion System — Subtle Card Lift Effect" not in text:
    text += "\n\n" + lift_rule.strip()
    with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Appended subtle card lift to assets/css/ui-cleanup.css!")
else:
    print("Already in ui-cleanup.css")
