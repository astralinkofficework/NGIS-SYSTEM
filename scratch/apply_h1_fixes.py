# 1. Patch assets/css/hero.css
with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    hero_css = f.read()

# Replace font-size: 30px with 28px and weight 600
hero_css = hero_css.replace(
    """.hero-title {

font-family: 'Manrope', 'Plus Jakarta Sans', 'Plus Jakarta Sans', 'Kantumruy Pro', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

font-size: 30px;

font-weight: 400;""",
    """.hero-title {

font-family: 'Manrope', sans-serif !important;

font-size: 28px !important;

font-weight: 600 !important;

line-height: 1.25 !important;"""
)

hero_css = hero_css.replace(
    ".hero-title { font-size: clamp(22px, 2.6vw, 30px) !important; line-height: 1.2; }",
    ".hero-title { font-family: 'Manrope', sans-serif !important; font-size: 28px !important; font-weight: 600 !important; line-height: 1.25 !important; }"
)

with open('assets/css/hero.css', 'w', encoding='utf-8') as f:
    f.write(hero_css)
print('assets/css/hero.css updated.')

# 2. Patch pages/student/css/hero.css
with open('pages/student/css/hero.css', 'r', encoding='utf-8') as f:
    st_hero_css = f.read()

st_hero_css = st_hero_css.replace(
    """.hero-title {
font-family: 'Manrope', 'Plus Jakarta Sans', 'Plus Jakarta Sans', 'Kantumruy Pro', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-size: 26px;
font-weight: 400;""",
    """.hero-title {
font-family: 'Manrope', sans-serif !important;
font-size: 28px !important;
font-weight: 600 !important;
line-height: 1.25 !important;"""
)

st_hero_css = st_hero_css.replace(
    ".hero-title {\nfont-size: 24px !important;\n}",
    ".hero-title {\nfont-family: 'Manrope', sans-serif !important;\nfont-size: 28px !important;\nfont-weight: 600 !important;\nline-height: 1.25 !important;\n}"
)

with open('pages/student/css/hero.css', 'w', encoding='utf-8') as f:
    f.write(st_hero_css)
print('pages/student/css/hero.css updated.')

# 3. Patch pages/admin/admin.html
with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

admin_html = admin_html.replace(
    """.hero-title {

font-size: 24px !important;

font-weight: 500 !important;

color: #ffffff !important;

letter-spacing: -0.015em !important;

}""",
    """.hero-title {

font-family: 'Manrope', sans-serif !important;

font-size: 28px !important;

font-weight: 600 !important;

line-height: 1.25 !important;

color: #ffffff !important;

letter-spacing: -0.015em !important;

}"""
)

admin_html = admin_html.replace(
    '<h1 class="text-sm font-medium text-slate-800 truncate" id="mobAdminName">Sok Panha Heng</h1>',
    '<span class="text-sm font-medium text-slate-800 truncate" id="mobAdminName">Sok Panha Heng</span>'
)

with open('pages/admin/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)
print('pages/admin/admin.html updated.')

# 4. Patch pages/teacher/teacher-gradebook.html
with open('pages/teacher/teacher-gradebook.html', 'r', encoding='utf-8') as f:
    tg_html = f.read()

tg_html = tg_html.replace(
    '<h1 class="text-base sm:text-xl lg:text-2xl font-medium text-slate-900 font-khmer tracking-tight">',
    '<h1 class="page-title text-[28px] font-semibold text-slate-900 tracking-tight" style="font-family:\'Manrope\', sans-serif !important; font-size:28px !important; font-weight:600 !important; line-height:1.25 !important;">'
)

with open('pages/teacher/teacher-gradebook.html', 'w', encoding='utf-8') as f:
    f.write(tg_html)
print('pages/teacher/teacher-gradebook.html updated.')

