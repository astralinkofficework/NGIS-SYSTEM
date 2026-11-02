with open('pages/shared/css/lessons.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """.subj-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(135deg, var(--primary-soft) 0%, transparent 60%);
  opacity: 0;
  transition: opacity var(--t-base);
  pointer-events: none;
}"""

replacement = """.subj-card::before,
.subj-card::after {
  content: none !important;
  display: none !important;
  background: transparent !important;
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

with open('pages/shared/css/lessons.css', 'w', encoding='utf-8') as f:
    f.write(c)

