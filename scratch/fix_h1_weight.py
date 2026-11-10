with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    """/* H1 Main Page Titles */
html body h1,
html body .page-title,
html body .hero-title,
html body .dash-hero-title,
html body [data-purpose="page-title"],
html body .masthead-title,
html body .portal-title {""",
    """/* H1 Main Page Titles */
html body h1,
html body h1[class*="font-"],
html body .page-title,
html body .page-title[class*="font-"],
html body .hero-title,
html body .dash-hero-title,
html body [data-purpose="page-title"],
html body .masthead-title,
html body .portal-title {"""
)

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated H1 font-weight rule in design-system.css')

