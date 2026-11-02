with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """.id-card-wrapper::after {
  content: '';
  position: absolute;
  top: -40%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}"""

replacement = """.id-card-wrapper::after {
  content: none !important;
  display: none !important;
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
    print('Target not matched')

with open('assets/css/portal-dashboard.css', 'w', encoding='utf-8') as f:
    f.write(c)

