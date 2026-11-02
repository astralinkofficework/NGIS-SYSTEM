with open('pages/student/css/service-hub.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """.sh-desktop-view .btn-primary,
.sh-desktop-view .sh-toolbar-new-btn,
.sh-desktop-view .sh-new-request-btn {
  color: #ffffff !important;
  background: #202F63 !important;"""

replacement = """.sh-desktop-view .btn-primary,
.sh-desktop-view .sh-toolbar-new-btn,
.sh-desktop-view .sh-new-request-btn {
  color: #ffffff !important;
  background: #92243D !important;
  border: 1px solid #92243D !important;"""

c = c.replace(target, replacement)
c = c.replace(target.replace('\n', '\r\n'), replacement.replace('\n', '\r\n'))

with open('pages/student/css/service-hub.css', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated service-hub.css')

