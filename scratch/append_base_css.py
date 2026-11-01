import os

path = 'pages/student/css/base.css'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

subpage_css = """
/* ══════════════════════════════════════════════════════════════
   STUDENT PORTAL FULL-BLEED LAYOUT & SUBPAGE OVERLAP SCAFFOLDING
   Matches Dashboard Structure (Teal Hero + Off-canvas Drawer)
   ══════════════════════════════════════════════════════════════ */

body.student-dashboard .main,
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
}

/* Subpage Content Container (Clean overlap with teal banner) */
.subpage-container,
.subpage-deck,
body.student-dashboard .page,
body[data-role="student"] .page,
body.student-dashboard .page-container,
body[data-role="student"] .page-container {
  max-width: 1280px;
  margin: -48px auto 48px auto !important;
  padding: 0 24px;
  position: relative;
  z-index: 20;
  box-sizing: border-box;
}

/* Clean White Card Surfaces matching reference design */
body.student-dashboard .card,
body[data-role="student"] .card,
body.student-dashboard .stat,
body[data-role="student"] .stat,
body.student-dashboard .hub-card,
body[data-role="student"] .hub-card,
body.student-dashboard .portal-card,
body[data-role="student"] .portal-card,
body.student-dashboard .section-card,
body[data-role="student"] .section-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid rgba(184, 219, 217, 0.45);
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

/* Dark Mode Token Alignment */
[data-theme="dark"] body.student-dashboard,
[data-theme="dark"] body[data-role="student"] {
  background: #0c121e !important;
}

[data-theme="dark"] body.student-dashboard .card,
[data-theme="dark"] body[data-role="student"] .card,
[data-theme="dark"] body.student-dashboard .stat,
[data-theme="dark"] body[data-role="student"] .stat,
[data-theme="dark"] body.student-dashboard .hub-card,
[data-theme="dark"] body[data-role="student"] .hub-card,
[data-theme="dark"] body.student-dashboard .portal-card,
[data-theme="dark"] body[data-role="student"] .portal-card {
  background: #182329 !important;
  border-color: rgba(184, 219, 217, 0.18) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
}

/* NO ROUNDED COLORED HOVER BLOBS OR WEIRD HOVER ARTIFACTS */
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
}

[data-theme="dark"] body.student-dashboard table tbody tr:hover td,
[data-theme="dark"] body[data-role="student"] table tbody tr:hover td {
  background: rgba(255, 255, 255, 0.04) !important;
}

/* Hide duplicate old mobile topbars when hero banner is present */
.hero-topbar ~ .lg\\:hidden,
.hero ~ .lg\\:hidden,
#heroBanner ~ .lg\\:hidden {
  display: none !important;
}
"""

if "STUDENT PORTAL FULL-BLEED LAYOUT" not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(subpage_css)
    print("Appended student subpage layout to pages/student/css/base.css")
else:
    print("Already in pages/student/css/base.css")

