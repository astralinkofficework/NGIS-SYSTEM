with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = """.ws-card:hover,
.ws-card:active,
.ws-card:focus {
  transform: none !important;
  box-shadow: none !important;
  border-color: #E5E5E8 !important;
  background-color: inherit !important;
}"""

replacement = """.ws-card:hover,
.ws-card:active,
.ws-card:focus {
  transform: none !important;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04) !important;
  border-color: #E5E5E8 !important;
  background-color: #ffffff !important;
  outline: none !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in teacher-classes.html (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in teacher-classes.html (CRLF)')
else:
    print('Target not found in teacher-classes.html')

with open('pages/teacher/teacher-classes.html', 'w', encoding='utf-8') as f:
    f.write(c)

