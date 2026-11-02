with open('pages/student/css/base.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """/* Strict Neutral Card States — Zero hover/touch overlay, tint, or glow */
body.student-dashboard .card:hover,
body[data-role="student"] .card:hover,
body.student-dashboard .stat:hover,
body[data-role="student"] .stat:hover,
body.student-dashboard .card:active,
body[data-role="student"] .card:active,
body.student-dashboard .stat:active,
body[data-role="student"] .stat:active {
  box-shadow: inherit !important;
  border-color: inherit !important;
  background-color: inherit !important;
  transform: none !important;
}"""

replacement = """/* Strict Neutral Card States — Zero hover/touch overlay, tint, or glow */
body.student-dashboard .card:hover,
body[data-role="student"] .card:hover,
body.student-dashboard .stat:hover,
body[data-role="student"] .stat:hover,
body.student-dashboard .card:active,
body[data-role="student"] .card:active,
body.student-dashboard .stat:active,
body[data-role="student"] .stat:active,
body.student-dashboard .card:focus,
body[data-role="student"] .card:focus {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
  border-color: #E5E5E8 !important;
  background-color: #ffffff !important;
  transform: none !important;
  translate: none !important;
  scale: 1 !important;
  -webkit-tap-highlight-color: transparent !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in base.css (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in base.css (CRLF)')
else:
    print('Target not found in base.css')

with open('pages/student/css/base.css', 'w', encoding='utf-8') as f:
    f.write(c)

