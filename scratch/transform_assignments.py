import os, re

path = 'pages/student/student-assignments.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update css links in head
css_block = '''<link rel="stylesheet" href="../../assets/css/app.css?v=3.0">
<link rel="stylesheet" href="../../assets/css/mvp-redesign.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="css/overlap.css">
<link rel="stylesheet" href="css/responsive.css">
<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/ui-states.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">'''

c = re.sub(r'<link rel="stylesheet" href="\.\./\.\./assets/css/app\.css">', css_block, c)

# 2. Update body tag
c = re.sub(r'<body[^>]*>', '<body data-page="student" data-role="student" class="student-dashboard font-sans selection:bg-forest-100 selection:text-forest-800">', c)

# 3. Update hero script
c = c.replace('<script src="../../assets/js/hero.js"></script>', '<script src="js/hero.js"></script>')

# 4. Remove duplicate mobile bars if any
c = re.sub(r'<div class="lg:hidden bg-white border-b.*?</div>\s*</div>', '', c, flags=re.DOTALL)

# 5. Update page container to subpage-container
c = c.replace('<div class="page space-y-7">', '<div class="subpage-container space-y-7">')
c = c.replace('<div class="page space-y-8">', '<div class="subpage-container space-y-8">')
c = c.replace('<div class="page">', '<div class="subpage-container">')

# 6. Set HERO_CONFIG
c = re.sub(r'window\.HERO_CONFIG\s*=\s*\{', '''window.PAGE = {"role":"student","active":"assignments"};
window.HERO_CONFIG = {
  title: 'Assignments & Coursework',
  greeting: 'Track upcoming homework, submitted problem sets, lab reports, and feedback',
''', c, count=1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Updated student-assignments.html")

