import re

# 1. Update assets/css/hero.css
with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    hero_text = f.read()

# Replace any .hero-title rule that sets font-size: 30px or font-family with multiple blank lines
hero_text = re.sub(
    r'\.hero-title\s*\{[^}]*font-size:\s*30px;[^}]*\}',
    """.hero-title {
  font-family: 'Manrope', sans-serif !important;
  font-size: 28px !important;
  font-weight: 600 !important;
  line-height: 1.25 !important;
  color: #ffffff !important;
  letter-spacing: -0.02em !important;
  margin-bottom: 6px;
}""",
    hero_text
)

with open('assets/css/hero.css', 'w', encoding='utf-8') as f:
    f.write(hero_text)
print('Updated assets/css/hero.css')

# 2. Append Master Typography rules to assets/css/design-system.css
with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    ds_text = f.read()

master_rules = """

/* ============================================================
   MASTER TYPOGRAPHY SPECIFICATION (Manrope + Plus Jakarta Sans)
   H1: Manrope 28px, weight 600, line-height 1.25
   H2: Manrope 22px, weight 600
   H3: Manrope 18px, weight 600
   H4: Manrope 16px, weight 600
   Body: Plus Jakarta Sans 14px, weight 400
   Supporting: Plus Jakarta Sans 13px, weight 400
   Labels: Plus Jakarta Sans 12px, weight 500
   Buttons: Plus Jakarta Sans 14px, weight 500
   Inputs: Plus Jakarta Sans 14px, weight 400
   Tables: Plus Jakarta Sans 13-14px (th: 500, td: 400)
   Sidebar: Plus Jakarta Sans 14px (normal: 400, active: 500)
   ============================================================ */

/* H1 Main Page Titles */
html body h1,
html body .page-title,
html body .hero-title,
html body .dash-hero-title,
html body [data-purpose="page-title"],
html body .masthead-title,
html body .portal-title {
  font-family: 'Manrope', sans-serif !important;
  font-size: 28px !important;
  font-weight: 600 !important;
  line-height: 1.25 !important;
  letter-spacing: -0.02em !important;
}

/* H2 Section Headings */
html body h2,
html body .section-title,
html body [data-purpose="section-title"],
html body .dash-card-title,
html body .module-title {
  font-family: 'Manrope', sans-serif !important;
  font-size: 22px !important;
  font-weight: 600 !important;
  line-height: 1.30 !important;
}

/* H3 Subsection Headings */
html body h3,
html body .subsection-title,
html body .modal-title,
html body .dialog-title {
  font-family: 'Manrope', sans-serif !important;
  font-size: 18px !important;
  font-weight: 600 !important;
  line-height: 1.35 !important;
}

/* H4 Small Headings */
html body h4,
html body .card-title,
html body .subcard-title {
  font-family: 'Manrope', sans-serif !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  line-height: 1.40 !important;
}

/* Body & Paragraphs */
html body,
html body p,
html body .body-text {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 14px !important;
  font-weight: 400;
  line-height: 1.50;
}

/* Supporting text */
html body .supporting-text,
html body .meta-text,
html body .sub-info,
html body .stat-sub,
html body .desc,
html body .description,
html body .breadcrumb-item,
html body .caption {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 400;
}

/* Small labels & badges */
html body label,
html body .label,
html body .badge,
html body .pill,
html body .tag,
html body .stat-lbl,
html body .small-label,
html body .meta-lbl {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}

/* Buttons */
html body button,
html body .btn,
html body .button,
html body input[type="button"],
html body input[type="submit"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 14px !important;
  font-weight: 500 !important;
}

/* Input fields */
html body input:not([type="checkbox"]):not([type="radio"]):not([type="hidden"]),
html body select,
html body textarea {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 14px !important;
}

/* Tables */
html body table,
html body .tbl,
html body .classes-table,
html body .sk-table {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

html body th {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 12px !important;
  font-weight: 500 !important;
}

html body td {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
}

/* Sidebar navigation */
html body .sidebar,
html body .nav-link,
html body .nav-item,
html body .side-brand,
html body .sidebar nav {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 14px !important;
}

html body .sidebar .nav-link {
  font-weight: 400;
}

html body .sidebar .nav-link.active {
  font-weight: 500 !important;
}
"""

if "MASTER TYPOGRAPHY SPECIFICATION" in ds_text:
    idx = ds_text.find("/* ============================================================\n   MASTER TYPOGRAPHY SPECIFICATION")
    ds_text = ds_text[:idx] + master_rules.strip()
else:
    ds_text = ds_text + master_rules

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(ds_text)
print('Updated assets/css/design-system.css')

