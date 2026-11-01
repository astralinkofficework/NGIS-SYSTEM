with open('pages/student/css/responsive.css', 'r', encoding='utf-8') as f:
    s = f.read()

target = """body[data-role="student"] { overflow-x: clip; }
body[data-role="student"] .main { min-width: 0; width: 100%; max-width: 100%; overflow: visible; }
body[data-role="student"] .hero-body,
.student-desktop-view .hero-body {
  padding-bottom: 76px !important;
}

body[data-role="student"] .dash-deck > *,
body[data-role="student"] .dash-overlap > *,
body[data-role="student"] .dash > * { min-width: 0; }
body[data-role="student"] .activity-feed-list { max-height: none; overflow: visible; }"""

replacement = """body[data-role="student"],
body[data-role="teacher"] { overflow-x: clip; }
body[data-role="student"] .main,
body[data-role="teacher"] .main { min-width: 0; width: 100%; max-width: 100%; overflow: visible; }
body[data-role="student"] .hero-body,
body[data-role="teacher"] .hero-body,
.student-desktop-view .hero-body,
.teacher-desktop-view .hero-body {
  padding-bottom: 76px !important;
}

body[data-role="student"] .dash-deck > *,
body[data-role="teacher"] .dash-deck > *,
body[data-role="student"] .dash-overlap > *,
body[data-role="teacher"] .dash-overlap > *,
body[data-role="student"] .dash > *,
body[data-role="teacher"] .dash > * { min-width: 0; }
body[data-role="student"] .activity-feed-list,
body[data-role="teacher"] .activity-feed-list { max-height: none; overflow: visible; }"""

if target in s:
    s = s.replace(target, replacement)
    with open('pages/student/css/responsive.css', 'w', encoding='utf-8') as f:
        f.write(s)
    print('Updated responsive.css')
else:
    print('Target not found in responsive.css')

