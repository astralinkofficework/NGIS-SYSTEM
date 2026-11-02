# 1. Update pages/student/css/overlap.css
with open('pages/student/css/overlap.css', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('background: #000000;\n  color: #ffffff;', 'background: #92243D;\n  color: #ffffff;\n  border: 1px solid #92243D;')
c = c.replace('background: #000000;\r\n  color: #ffffff;', 'background: #92243D;\r\n  color: #ffffff;\r\n  border: 1px solid #92243D;')
c = c.replace('.ov-btn-main:hover {\n  background: #000000;', '.ov-btn-main:hover {\n  background: #7A1D32;')
c = c.replace('.ov-btn-main:hover {\r\n  background: #000000;', '.ov-btn-main:hover {\r\n  background: #7A1D32;')

with open('pages/student/css/overlap.css', 'w', encoding='utf-8') as f:
    f.write(c)

# 2. Update assets/css/portal-dashboard.css
with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    c2 = f.read()

c2 = c2.replace('background: var(--primary, #202F63);\n  color: #ffffff !important;', 'background: #92243D;\n  color: #ffffff !important;\n  border: 1px solid #92243D;')
c2 = c2.replace('background: var(--primary, #202F63);\r\n  color: #ffffff !important;', 'background: #92243D;\r\n  color: #ffffff !important;\r\n  border: 1px solid #92243D;')
c2 = c2.replace('.ov-btn-main:hover {\n  background: #18234D;', '.ov-btn-main:hover {\n  background: #7A1D32;')
c2 = c2.replace('.ov-btn-main:hover {\r\n  background: #18234D;', '.ov-btn-main:hover {\r\n  background: #7A1D32;')

with open('assets/css/portal-dashboard.css', 'w', encoding='utf-8') as f:
    f.write(c2)

print('Updated ov-btn-main in overlap.css and portal-dashboard.css')

