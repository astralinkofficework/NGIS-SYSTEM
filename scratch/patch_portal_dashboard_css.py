import re

path = "assets/css/portal-dashboard.css"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace any old canvas background (#F3F3F5) with #EAF6FF
content = content.replace("#F3F3F5", "#EAF6FF")
content = content.replace("var(--bg, #F3F3F5)", "var(--color-pale-blue, #EAF6FF)")

# Update hero body background to Deep Blue gradient
hero_pattern = r'body:not\(\[data-role="admin"\]\)\s*\.hero:has\(\.hero-body\),\s*body:not\(\[data-role="admin"\]\)\s*\.hero\.hero-main\s*\{[^}]*\}'
new_hero = '''body:not([data-role="admin"]) .hero:has(.hero-body),
body:not([data-role="admin"]) .hero.hero-main,
.hero:has(.hero-body),
.hero.hero-main {
  background: linear-gradient(135deg, var(--color-midnight, #021024) 0%, var(--color-deep-blue, #052659) 100%) !important;
  color: #ffffff !important;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(2, 16, 36, 0.15) !important;
}'''

content = re.sub(hero_pattern, new_hero, content)

# Update hero subtitle / dates
content = re.sub(
    r'\.hero-date\s*\{[^}]*\}',
    '''.hero-date {
  font-size: 13px;
  color: var(--color-light-blue, #C1E8FF);
  font-weight: 500;
  margin-bottom: 6px;
  letter-spacing: 0.01em;
}''',
    content
)

content = re.sub(
    r'\.hero-greeting\s*\{[^}]*\}',
    '''.hero-greeting {
  font-size: 14px;
  color: var(--color-light-blue, #C1E8FF);
  font-weight: 400;
  margin: 0;
}''',
    content
)

# Replace old Navy #202F63 with #021024 / #052659
content = content.replace("#202F63", "#021024")

# Replace old Burgundy #92243D with #052659
content = content.replace("#92243D", "#052659")

# Replace old borders #E5E5E8 with #DCE8F3
content = content.replace("#E5E5E8", "#DCE8F3")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated assets/css/portal-dashboard.css successfully!")

