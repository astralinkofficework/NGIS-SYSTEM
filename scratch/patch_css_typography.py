import glob
import re

CANONICAL_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');"

# 1. Update design-system.css
with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    ds_content = f.read()

# Replace :root typography variables
ds_content = re.sub(
    r'/\* Typography \*/\s*--font-primary:[^;]+;\s*--font-heading:[^;]+;\s*--font-khmer:[^;]+;\s*--font-mono:[^;]+;',
    """/* Typography System (Manrope + Plus Jakarta Sans) */
  --font-heading: 'Manrope', sans-serif;
  --font-body:    'Plus Jakarta Sans', sans-serif;
  --font-primary: 'Plus Jakarta Sans', sans-serif;

  --font-size-h1: 28px;
  --font-size-h2: 22px;
  --font-size-h3: 18px;
  --font-size-h4: 16px;

  --font-size-body:  14px;
  --font-size-small: 13px;
  --font-size-label: 12px;

  --font-khmer:   'Kantumruy Pro', 'Plus Jakarta Sans', sans-serif;
  --font-mono:    ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;""",
    ds_content
)

# Replace section 2: Global Canvas & Typography Reset
old_reset_pattern = r'/\* ── 2\. Global Canvas & Typography Reset ──[^\n]*\*/.*?(?=/\* ── Universal Primary Button)'
new_reset_code = """/* ── 2. Global Canvas & Typography Reset ─────────────────────── */
html, body {
  background-color: var(--ngis-canvas) !important;
  color: var(--ngis-text-primary) !important;
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: var(--font-size-body, 14px);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden !important;
  max-width: 100vw;
}

/* Base text elements default to Plus Jakarta Sans */
body, button, input, select, textarea, p, span, div, label, a, table, tr, td, th {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif);
}

/* Icons preserve their icon font family */
.material-symbols-outlined,
.material-icons,
[class*="ph-"],
.ph,
.ph-bold,
.ph-fill {
  font-family: 'Material Symbols Outlined', 'Phosphor', sans-serif !important;
}

/* Typography Weight Rules */
*, b, strong, th, td, button, span, div, input, select, textarea, p, label, a {
  font-weight: 400;
}

/* Medium weight (500) for interactive controls, badges, table headers, labels */
.font-medium, .stat-val, .badge, th, .btn, .nav-link, .nav-group-label,
[class*="font-medium"] {
  font-weight: 500;
}

/* Semi-bold weight (600) for H1-H4 headings and titles */
.font-semibold, h1, h2, h3, h4, .page-title, [class*="font-semibold"] {
  font-weight: 600;
}

/* H1 Page Titles: Manrope, exactly 28px, weight 600, line-height 1.25 */
h1,
.page-title,
.dash-hero-title,
[data-purpose="page-title"],
.masthead-title,
.portal-title {
  font-family: var(--font-heading, 'Manrope', sans-serif) !important;
  font-weight: 600 !important;
  font-size: var(--font-size-h1, 28px) !important;
  line-height: 1.25 !important;
  letter-spacing: -0.02em;
  color: var(--color-text, #29352E) !important;
}

/* H2 Section Headings: Manrope, 22px, weight 600 */
h2,
.section-title,
[data-purpose="section-title"],
.dash-card-title,
.module-title {
  font-family: var(--font-heading, 'Manrope', sans-serif) !important;
  font-weight: 600 !important;
  font-size: var(--font-size-h2, 22px) !important;
  line-height: 1.30 !important;
  color: var(--color-text, #29352E) !important;
}

/* H3 Subsection Headings: Manrope, 18px, weight 600 */
h3,
.subsection-title,
.modal-title,
.dialog-title {
  font-family: var(--font-heading, 'Manrope', sans-serif) !important;
  font-weight: 600 !important;
  font-size: var(--font-size-h3, 18px) !important;
  line-height: 1.35 !important;
  color: var(--color-text, #29352E) !important;
}

/* H4 Small Headings: Manrope, 16px, weight 600 */
h4,
.card-title,
.subcard-title {
  font-family: var(--font-heading, 'Manrope', sans-serif) !important;
  font-weight: 600 !important;
  font-size: var(--font-size-h4, 16px) !important;
  line-height: 1.40 !important;
  color: var(--color-text, #29352E) !important;
}

/* Body & Paragraphs: Plus Jakarta Sans, 14px, weight 400 */
p,
.body-text {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: var(--font-size-body, 14px) !important;
  font-weight: 400;
  line-height: 1.50;
}

/* Supporting Text: Plus Jakarta Sans, 13px, weight 400 */
.supporting-text,
.meta-text,
.sub-info,
.stat-sub,
.desc,
.description,
.breadcrumb-item,
.caption {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: var(--font-size-small, 13px) !important;
  font-weight: 400;
}

/* Small Labels & Badges: Plus Jakarta Sans, 12px, weight 500 */
label,
.label,
.badge,
.pill,
.tag,
.stat-lbl,
.small-label,
.meta-lbl {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: var(--font-size-label, 12px) !important;
  font-weight: 500;
}

/* Buttons: Plus Jakarta Sans, 14px, weight 500 */
button,
.btn,
.button,
input[type="button"],
input[type="submit"] {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: 14px !important;
  font-weight: 500 !important;
}

/* Input Fields: Plus Jakarta Sans, 14px, weight 400 */
input:not([type="checkbox"]):not([type="radio"]):not([type="hidden"]),
select,
textarea {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: 14px !important;
  font-weight: 400;
}

/* Table Content: Plus Jakarta Sans, 13–14px */
table, .tbl, .classes-table, .sk-table {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: 13px !important;
}
th {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}
td {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: 13px !important;
  font-weight: 400 !important;
}

/* Sidebar Navigation: Plus Jakarta Sans, 14px */
.sidebar, .nav-link, .nav-item, .side-brand, .sidebar nav {
  font-family: var(--font-body, 'Plus Jakarta Sans', sans-serif) !important;
  font-size: 14px !important;
}
.sidebar .nav-link {
  font-weight: 400;
}
.sidebar .nav-link.active {
  font-weight: 500 !important;
}

/* Khmer Text Font */
[lang="km"], [data-lang="km"], .font-khmer, .khmer-text {
  font-family: var(--font-khmer, 'Kantumruy Pro', 'Plus Jakarta Sans', sans-serif) !important;
}

"""

ds_content = re.sub(old_reset_pattern, new_reset_code, ds_content, flags=re.DOTALL)

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(ds_content)
print('Updated assets/css/design-system.css successfully.')

# 2. Update app.css
with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Replace font import in app.css
app_content = re.sub(
    r'@import\s+url\([\'"][^\'"]*fonts\.googleapis\.com[^\'"]*[\'"]\);',
    CANONICAL_IMPORT,
    app_content
)

# Replace typography in :root in app.css
app_content = app_content.replace(
    "'Manrope', 'Plus Jakarta Sans', 'Inter', 'Kantumruy Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important",
    "'Plus Jakarta Sans', -apple-system, sans-serif !important"
)
app_content = app_content.replace(
    "'Kantumruy Pro', 'Inter', -apple-system, sans-serif",
    "'Kantumruy Pro', 'Plus Jakarta Sans', sans-serif"
)
app_content = app_content.replace(
    "'Inter', -apple-system, sans-serif",
    "'Plus Jakarta Sans', -apple-system, sans-serif"
)

# Add font size variables if not present
if '--font-size-h1:' not in app_content:
    app_content = app_content.replace(
        ':root {',
        """:root {
  --font-heading: 'Manrope', sans-serif;
  --font-body:    'Plus Jakarta Sans', sans-serif;
  --font-sans:    'Plus Jakarta Sans', sans-serif;

  --font-size-h1: 28px;
  --font-size-h2: 22px;
  --font-size-h3: 18px;
  --font-size-h4: 16px;

  --font-size-body:  14px;
  --font-size-small: 13px;
  --font-size-label: 12px;"""
    )

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(app_content)
print('Updated assets/css/app.css successfully.')

# 3. Clean remaining CSS files
other_css = [
    'assets/css/hero.css',
    'assets/css/shared-components.css',
    'assets/css/ui-states.css',
    'pages/shared/css/lessons.css',
    'pages/student/css/base.css',
    'pages/student/css/hero.css',
    'pages/student/css/overlap.css',
    'pages/student/css/service-hub.css',
]

for p in other_css:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        
        orig = c
        # Replace imports
        c = re.sub(
            r'@import\s+url\([\'"][^\'"]*fonts\.googleapis\.com[^\'"]*[\'"]\);',
            CANONICAL_IMPORT,
            c
        )
        # Replace Inter and others
        c = c.replace("'Inter', -apple-system, sans-serif", "'Plus Jakarta Sans', sans-serif")
        c = c.replace("'Inter', sans-serif", "'Plus Jakarta Sans', sans-serif")
        c = c.replace('"Inter", sans-serif', '"Plus Jakarta Sans", sans-serif')
        c = c.replace('Inter, sans-serif', "'Plus Jakarta Sans', sans-serif")
        c = c.replace("'Inter',", "'Plus Jakarta Sans',")
        c = c.replace('"Inter",', '"Plus Jakarta Sans",')
        c = c.replace("'Manrope', 'Plus Jakarta Sans', 'Inter', 'Kantumruy Pro', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                      "'Plus Jakarta Sans', sans-serif")
        c = c.replace("'Plus Jakarta Sans', 'Inter', 'Kantumruy Pro', system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif",
                      "'Plus Jakarta Sans', sans-serif")
        
        if c != orig:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f'Updated {p}')
    except Exception as e:
        print(f'Error on {p}: {e}')

print('CSS typography patching complete.')

