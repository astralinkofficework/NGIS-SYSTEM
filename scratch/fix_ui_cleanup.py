with open('assets/css/ui-cleanup.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """.card:hover,
.module-card:hover,
.dept-card:hover,
.hub-card:hover,
.stat-card:hover,
.stat:hover,
.lesson-card:hover,
.ann-card:hover,
.exam-card:hover,
.rc-filecard:hover,
.card-hover:hover,
.card-hover-sm:hover,
.candidate-card:hover,
.club-card:hover,
.cert-card:hover,
.portal-card:hover,
.role-card:hover,
.news-card:hover,
.subj-card:hover,
.cal-card:hover,
.att-card:hover,
.ql-card:hover,
.pf-card:hover,
.ov-profile:hover,
.ov-upcoming:hover,
.ov-deadlines:hover,
.ov-inner-panel:hover,
.ov-deadline-panel:hover,
.sh-card:hover,
.sh-stat-card:hover,
.sh-request-item:hover,
.task-card:hover,
.quick:hover,
.student-gov-card:hover,
[class*="card"]:hover {
  background-color: inherit !important;
  transform: none !important;
  box-shadow: inherit !important;
  translate: none !important;
  scale: none !important;
}"""

replacement = """.card:hover,
.module-card:hover,
.dept-card:hover,
.hub-card:hover,
.stat-card:hover,
.stat:hover,
.lesson-card:hover,
.ann-card:hover,
.exam-card:hover,
.rc-filecard:hover,
.card-hover:hover,
.card-hover-sm:hover,
.candidate-card:hover,
.club-card:hover,
.cert-card:hover,
.portal-card:hover,
.role-card:hover,
.news-card:hover,
.subj-card:hover,
.cal-card:hover,
.att-card:hover,
.ql-card:hover,
.pf-card:hover,
.ov-profile:hover,
.ov-upcoming:hover,
.ov-deadlines:hover,
.ov-inner-panel:hover,
.ov-deadline-panel:hover,
.sh-card:hover,
.sh-stat-card:hover,
.sh-request-item:hover,
.task-card:hover,
.quick:hover,
.student-gov-card:hover,
[class*="card"]:hover,
.card:active,
.module-card:active,
.dept-card:active,
.hub-card:active,
.stat-card:active,
.stat:active,
.ws-card:active,
.ov-profile:active,
.ov-upcoming:active,
.ov-deadlines:active,
[class*="card"]:active,
.card:focus,
.ws-card:focus,
[class*="card"]:focus {
  background: #ffffff !important;
  background-color: #ffffff !important;
  border-color: #E5E5E8 !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
  outline: none !important;
  -webkit-tap-highlight-color: transparent !important;
}

/* Strip any pseudo-element hover/touch overlays on cards */
:where(
  .card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .rc-filecard, .card-hover,
  .ws-card, .candidate-card, .club-card, .cert-card, .portal-card,
  .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .ov-profile, .ov-upcoming, .ov-deadlines, .ov-inner-panel,
  .sh-card, .sh-stat-card, .task-card, .student-gov-card, [class*="card"]
)::before,
:where(
  .card, .module-card, .dept-card, .hub-card, .stat-card, .stat,
  .lesson-card, .ann-card, .exam-card, .rc-filecard, .card-hover,
  .ws-card, .candidate-card, .club-card, .cert-card, .portal-card,
  .role-card, .news-card, .subj-card, .cal-card, .att-card, .ql-card,
  .pf-card, .ov-profile, .ov-upcoming, .ov-deadlines, .ov-inner-panel,
  .sh-card, .sh-stat-card, .task-card, .student-gov-card, [class*="card"]
)::after {
  content: none !important;
  display: none !important;
  background: transparent !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in ui-cleanup.css (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in ui-cleanup.css (CRLF)')
else:
    print('Target not found in ui-cleanup.css')

with open('assets/css/ui-cleanup.css', 'w', encoding='utf-8') as f:
    f.write(c)

