with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """/* Institutional Crest & Brand Headings with Cinzel */
#sidebar .side-brand-name,
.sidebar .side-brand-name,
.side-brand-name,
.brand-title,
.brand-heading {
  font-family: 'Cinzel', 'Plus Jakarta Sans', serif !important;
  font-weight: 500 !important;
  letter-spacing: 0.04em !important;
}"""

replacement = """/* Institutional Crest & Brand Headings with Manrope */
#sidebar .side-brand-name,
.sidebar .side-brand-name,
.side-brand-name,
.brand-title,
.brand-heading {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 500 !important;
  letter-spacing: 0.02em !important;
}"""

target2 = """/* Strict NO BOLD: Max 500 for headings, badges, labels, buttons */
h1, h2, h3, h4, h5, h6,
th, dt,
.font-medium, .font-semibold, .font-bold, .font-extrabold, .font-black,
[class*="font-semibold"], [class*="font-bold"], [class*="font-extrabold"], [class*="font-black"], [class*="font-medium"],
.stat-val, .badge, .tp-btn, .tp-badge, .tp-label,
.nav-group-label, .nav-link.active, .nav-item.active,
.side-brand-name, .side-user-name {
  font-weight: 500 !important;
}"""

replacement2 = """/* Typography Weights:
   - Regular (400) & Medium (500) for normal content (avoid bold).
   - 600 or 700 allowed ONLY for page titles & section headings when necessary. */
th, dt,
.font-medium, .font-semibold, .font-bold, .font-extrabold, .font-black,
[class*="font-semibold"], [class*="font-bold"], [class*="font-extrabold"], [class*="font-black"], [class*="font-medium"],
.stat-val, .badge, .tp-btn, .tp-badge, .tp-label,
.nav-group-label, .nav-link.active, .nav-item.active,
.side-brand-name, .side-user-name {
  font-weight: 500 !important;
}

h1, .page-title, .dash-hero-title, [data-purpose="page-title"] {
  font-weight: 600;
}

h2, h3, .section-title, [data-purpose="section-title"] {
  font-weight: 600;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

target2_crlf = target2.replace('\r\n', '\n').replace('\n', '\r\n')
replacement2_crlf = replacement2.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced target (Cinzel) LF')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced target (Cinzel) CRLF')

if target2 in c:
    c = c.replace(target2, replacement2)
    print('Replaced target2 (Weights) LF')
elif target2_crlf in c:
    c = c.replace(target2_crlf, replacement2_crlf)
    print('Replaced target2 (Weights) CRLF')

# Also clean any other 'Cinzel' in app.css
c = c.replace("'Cinzel',", "")

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(c)

