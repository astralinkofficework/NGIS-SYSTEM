with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts_block = '''<!-- ═══════════════ PAGE SCRIPTS ═══════════════ -->
<script src="js/hero.js"></script>
<script src="js/subjects.js"></script>
<script src="js/calendar.js"></script>
<script src="js/attendance.js"></script>
<script src="js/student-inline.js"></script>

<!-- Layout engine (must be last) -->
<script>window.PAGE = {"role":"student","active":"dashboard"};</script>
<script src="../../assets/js/layout.js?v=3.0"></script>
'''

if '<script src="js/hero.js"></script>' not in content:
    content = content.replace('</body>', scripts_block + '\n</body>')

with open('pages/student/student.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Scripts properly inserted before </body>!')

