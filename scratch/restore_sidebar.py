with open('pages/student/css/base.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """body.student-dashboard .main,
body[data-page="student"] .main,
body[data-role="student"] .main {
  margin-left: 0 !important;
  width: 100% !important;
  min-width: 0 !important;
}

body.student-dashboard .sidebar:not(.open),
body[data-page="student"] .sidebar:not(.open),
body[data-role="student"] .sidebar:not(.open) {
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
body[data-page="student"] .sidebar.open,
body[data-role="student"] .sidebar.open {
  transform: translateX(0) !important;
  visibility: visible !important;
  pointer-events: auto !important;
  position: fixed !important;
  top: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  z-index: 1000 !important;
}"""

if target in c:
    c = c.replace(target, "/* Standard responsive sidebar integration */")
    with open('pages/student/css/base.css', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Updated pages/student/css/base.css")
else:
    print("Target not found in base.css")

# Also update assets/js/layout.js and layout.js line 1095 to:
# const isDrawerMode = window.innerWidth <= 1024;
for lp in ['assets/js/layout.js', 'layout.js']:
    try:
        with open(lp, 'r', encoding='utf-8') as f:
            lc = f.read()
        l_target = 'const isDrawerMode = window.innerWidth <= 1024 || document.body.classList.contains("student-dashboard") || document.body.dataset.page === "student" || document.body.dataset.role === "student" || (window.location.pathname.indexOf("/pages/student/") !== -1);'
        l_repl = 'const isDrawerMode = window.innerWidth <= 1024;'
        if l_target in lc:
            lc = lc.replace(l_target, l_repl)
            with open(lp, 'w', encoding='utf-8') as f:
                f.write(lc)
            print(f"Updated {lp}")
        else:
            print(f"Drawer target not found in {lp}")
    except Exception as e:
        print(f"Error {lp}: {e}")

