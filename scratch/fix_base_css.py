with open('pages/student/css/base.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """/* NO ROUNDED COLORED HOVER BLOBS OR WEIRD HOVER ARTIFACTS */
body.student-dashboard .card:hover,
body[data-role="student"] .card:hover,
body.student-dashboard .stat:hover,
body[data-role="student"] .stat:hover {
  box-shadow: 0 4px 16px rgba(19, 130, 155, 0.08);
  border-color: rgba(19, 130, 155, 0.35);
  border-radius: 16px !important;
}

body.student-dashboard table tbody tr:hover td,
body[data-role="student"] table tbody tr:hover td {
  background: rgba(184, 219, 217, 0.08) !important;
  border-radius: 0 !important;
}"""

replacement = """/* Strict Neutral Card States — Zero hover/touch overlay, tint, or glow */
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
}

body.student-dashboard table tbody tr:hover td,
body[data-role="student"] table tbody tr:hover td {
  background: #F3F3F5 !important;
  border-radius: 0 !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced LF')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced CRLF')
else:
    print('Target not matched exactly')

with open('pages/student/css/base.css', 'w', encoding='utf-8') as f:
    f.write(c)

