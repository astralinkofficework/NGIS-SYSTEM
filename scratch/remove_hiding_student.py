with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect the style block in student.html
hiding_rule = """/* Full-bleed dashboard layout: hero and topbar span 100%, sidebar acts as drawer */
body.student-dashboard .main,
body[data-page="student"] .main {
  margin-left: 0 !important;
  width: 100% !important;
  min-width: 0 !important;
}

body.student-dashboard .sidebar:not(.open),
body[data-page="student"] .sidebar:not(.open) {
  transform: translateX(-100%) !important;
  visibility: hidden !important;
  pointer-events: none !important;
  position: fixed !important;
  top: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  z-index: 1000 !important;
}

body.student-dashboard .sidebar.open,
body[data-page="student"] .sidebar.open {
  transform: translateX(0) !important;
  visibility: visible !important;
  pointer-events: auto !important;
  position: fixed !important;
  top: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  z-index: 1000 !important;
}"""

c_new = c.replace(hiding_rule, "/* Standard responsive sidebar integration */")

with open('pages/student/student.html', 'w', encoding='utf-8') as f:
    f.write(c_new)

print("Updated student.html")

