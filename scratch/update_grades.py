import os

path = 'pages/student/student-grades.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update stylesheet links
c = c.replace('<link rel="stylesheet" href="../../assets/css/app.css">', 
'''<link rel="stylesheet" href="../../assets/css/app.css?v=3.0">
<link rel="stylesheet" href="../../assets/css/mvp-redesign.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="css/overlap.css">
<link rel="stylesheet" href="css/responsive.css">
<link rel="stylesheet" href="../../assets/css/ui-states.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">''')

# 2. Update body attributes
c = c.replace('<body data-page="grades" class="font-sans selection:bg-forest-100 selection:text-forest-800">',
              '<body data-page="student" data-role="student" class="student-dashboard font-sans selection:bg-forest-100 selection:text-forest-800">')

# 3. Update hero script from assets/js/hero.js to js/hero.js
c = c.replace('<script src="../../assets/js/hero.js"></script>', '<script src="js/hero.js"></script>')

# 4. Remove duplicate mobile topbar
dup_mobile_start = '<!-- ═══════════════ MANDATORY MOBILE HAMBURGER BAR (AGENTS.md) ═══════════════ -->'
dup_mobile_end = '<!-- ═══════════════ EDITORIAL WORKSPACE ═══════════════ -->'
if dup_mobile_start in c and dup_mobile_end in c:
    s_idx = c.find(dup_mobile_start)
    e_idx = c.find(dup_mobile_end)
    c = c[:s_idx] + c[e_idx:]

# 5. Replace page container class with subpage-container
c = c.replace('<div class="page space-y-9">', '<div class="subpage-container space-y-8">')

# 6. Set HERO_CONFIG
hero_cfg_old = "window.HERO_CONFIG = {"
hero_cfg_new = """window.PAGE = {"role":"student","active":"grades"};
window.HERO_CONFIG = {
  title: 'Academic Performance & Report Cards',
  greeting: 'Official semester records, monthly reviews, and performance evaluations',"""
c = c.replace(hero_cfg_old, hero_cfg_new, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated student-grades.html")

