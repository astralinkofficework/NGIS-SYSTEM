with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    content = f.read()

# CSS to insert
css_rules = """
/* Hub Header & Clean Title Section */
.hub-header-section {
  margin-bottom: 24px;
}
.hub-header-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.hub-back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 500;
  color: var(--charcoal-blue, #2f4550);
  background: #ffffff;
  border: 1px solid rgba(47, 69, 80, 0.12);
  padding: 6px 14px;
  border-radius: 999px;
  text-decoration: none;
  transition: all 0.18s ease;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}
.hub-back-btn:hover {
  background: var(--light-blue, #b8dbd9);
  color: var(--charcoal-blue, #2f4550);
  transform: translateX(-2px);
}
[data-theme="dark"] .hub-back-btn {
  background: #182329;
  border-color: rgba(184, 219, 217, 0.22);
  color: var(--light-blue, #b8dbd9);
}
[data-theme="dark"] .hub-back-btn:hover {
  background: rgba(184, 219, 217, 0.25);
  color: #ffffff;
}
.hub-title-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.hub-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--blue-slate, #586f7c);
  margin-bottom: 2px;
}
[data-theme="dark"] .hub-eyebrow {
  color: var(--light-blue, #b8dbd9);
}
.hub-eyebrow-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--charcoal-blue, #2f4550);
}
[data-theme="dark"] .hub-eyebrow-dot {
  background-color: var(--light-blue, #b8dbd9);
}
.hub-title {
  font-size: 24px;
  font-weight: 500 !important;
  color: var(--charcoal-blue, #2f4550);
  letter-spacing: -0.02em;
  line-height: 1.25;
  margin: 0;
}
[data-theme="dark"] .hub-title {
  color: #ffffff;
}
.hub-subtitle {
  font-size: 13.5px;
  font-weight: 400;
  color: var(--blue-slate, #586f7c);
  line-height: 1.5;
  margin: 0;
  max-width: 820px;
}
[data-theme="dark"] .hub-subtitle {
  color: #9eb8b7;
}
@media (min-width: 640px) {
  .hub-title {
    font-size: 26px;
  }
}
@media (max-width: 480px) {
  .hub-header-top-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
"""

# HTML replacement
old_html = """<!-- ????????????????????????????????????????????????????????
     TOP NAVIGATION BAR (Back to All Departments)
     ???????????????????????????????????????????????????????? -->
<div class="hub-top-nav-bar" aria-label="Department status">
<div class="hub-term-badge">
<span class="material-symbols-outlined">calendar_today</span>
<span>Academic Year 2025?2026 ? Term 2</span>
</div>
</div>"""

# Handle potential variations in old_html
c = content.replace('\r\n', '\n')

# Add CSS before </style>
if '/* Top Nav / Status Bar */' in c:
    c = c.replace('/* Top Nav / Status Bar */', css_rules.replace('\r\n', '\n') + '\n/* Top Nav / Status Bar */')
    print("CSS rules added successfully")
else:
    print("CSS anchor NOT found")

# Replace top nav bar in HTML
html_target_found = False
for nav_target in [
    """<div class="hub-top-nav-bar" aria-label="Department status">
<div class="hub-term-badge">
<span class="material-symbols-outlined">calendar_today</span>
<span>Academic Year 2025–2026 · Term 2</span>
</div>
</div>""",
    """<div class="hub-top-nav-bar" aria-label="Department status">\n<div class="hub-term-badge">\n<span class="material-symbols-outlined">calendar_today</span>\n<span>Academic Year 2025?2026 ? Term 2</span>\n</div>\n</div>"""
]:
    if nav_target in c:
        new_html_block = """<!-- ================================================================
     CLEAN DEPARTMENT TITLE HEADER
     ================================================================ -->
<section class="hub-header-section" aria-label="Department Overview">
  <div class="hub-header-top-row">
    <a href="departments.html" class="hub-back-btn" title="Back to All Departments">
      <span class="material-symbols-outlined text-[17px]">arrow_back</span>
      <span>All Departments</span>
    </a>
    <div class="hub-term-badge">
      <span class="material-symbols-outlined">calendar_today</span>
      <span>Academic Year 2025–2026 · Term 2</span>
    </div>
  </div>

  <div class="hub-title-block">
    <div class="hub-eyebrow" id="hubEyebrow">
      <span class="hub-eyebrow-dot"></span>
      <span id="hubEyebrowText">ACADEMIC OVERVIEW · CAMBRIDGE CURRICULUM</span>
    </div>
    <h1 class="hub-title" id="hubTitle">English Department Hub</h1>
    <p class="hub-subtitle" id="hubSubtitle">English literature syllabi, essay coursework submissions, IGCSE past papers, and evaluations.</p>
  </div>
</section>"""
        c = c.replace(nav_target, new_html_block)
        html_target_found = True
        print("HTML header section replaced successfully")
        break

if not html_target_found:
    import re
    pattern = r'<div class="hub-top-nav-bar"[\s\S]*?</div>\s*</div>'
    match = re.search(pattern, c)
    if match:
        new_html_block = """<!-- ================================================================
     CLEAN DEPARTMENT TITLE HEADER
     ================================================================ -->
<section class="hub-header-section" aria-label="Department Overview">
  <div class="hub-header-top-row">
    <a href="departments.html" class="hub-back-btn" title="Back to All Departments">
      <span class="material-symbols-outlined text-[17px]">arrow_back</span>
      <span>All Departments</span>
    </a>
    <div class="hub-term-badge">
      <span class="material-symbols-outlined">calendar_today</span>
      <span>Academic Year 2025–2026 · Term 2</span>
    </div>
  </div>

  <div class="hub-title-block">
    <div class="hub-eyebrow" id="hubEyebrow">
      <span class="hub-eyebrow-dot"></span>
      <span id="hubEyebrowText">ACADEMIC OVERVIEW · CAMBRIDGE CURRICULUM</span>
    </div>
    <h1 class="hub-title" id="hubTitle">English Department Hub</h1>
    <p class="hub-subtitle" id="hubSubtitle">English literature syllabi, essay coursework submissions, IGCSE past papers, and evaluations.</p>
  </div>
</section>"""
        c = c[:match.start()] + new_html_block + c[match.end():]
        print("HTML header section replaced with regex successfully")
    else:
        print("Could NOT find hub-top-nav-bar to replace")

with open('pages/shared/department.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("UPDATE COMPLETED")

