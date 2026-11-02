with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """/* Strict NO BOLD constraint (AGENTS.md) */
*, h1, h2, h3, h4, h5, h6, b, strong, th, td, button, span, div, input, select, textarea {
  font-weight: 400;
}
.font-medium, .stat-val, .badge, th, h1, h2, h3, h4,
.font-bold, .font-semibold, .font-extrabold, .font-black,
[class*="font-semibold"], [class*="font-bold"], [class*="font-extrabold"], [class*="font-black"], [class*="font-medium"] {
  font-weight: 500 !important;
}"""

replacement = """/* Typography Weight Rules:
   - Regular & Medium for normal content (avoid bold throughout application).
   - 600 or 700 allowed ONLY for page titles and section headings when necessary. */
*, b, strong, th, td, button, span, div, input, select, textarea, p, label, a {
  font-weight: 400;
}

/* Medium weight for interactive controls, badges, table headers, labels */
.font-medium, .stat-val, .badge, th, .btn, .nav-link, .nav-group-label,
.font-semibold, .font-bold, .font-extrabold, .font-black,
[class*="font-semibold"], [class*="font-bold"], [class*="font-extrabold"], [class*="font-black"], [class*="font-medium"] {
  font-weight: 500;
}

/* Page titles and section headings allowed 600 or 700 */
h1, .page-title, .dash-hero-title, [data-purpose="page-title"], .masthead-title {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600;
}

h2, h3, .section-title, [data-purpose="section-title"] {
  font-family: 'Manrope', 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600;
}

/* Khmer Text Font */
[lang="km"], [data-lang="km"], .font-khmer, .khmer-text {
  font-family: 'Kantumruy Pro', 'Manrope', sans-serif !important;
}

/* Supporting Interface Elements (pills, badges, metadata) */
.supporting-ui, .pill, .meta-text, .tag, .stat-lbl, .breadcrumb-item {
  font-family: 'Plus Jakarta Sans', 'Inter', 'Manrope', sans-serif;
}

/* ── Universal Primary Button Engine (Burgundy #92243D + White #FFFFFF) ── */
.btn-primary,
.ngis-btn-primary,
.ov-btn-main,
.tp-btn-primary,
.art-btn-primary,
.sk-blue-btn,
button.btn-primary,
a.btn-primary,
[data-role-action="primary"],
.sh-toolbar-new-btn,
.sh-new-request-btn,
#btnUploadAssignmentOrWork,
#btnAddStudent,
#btnAddClass,
#saveChangesBtn,
#openUploadBtn,
#btnPrimaryAddCourse,
#btnSubmitUpload,
#btnSubmitRequest {
  background: #92243D !important;
  background-color: #92243D !important;
  color: #FFFFFF !important;
  border: 1px solid #92243D !important;
  box-shadow: 0 1px 3px 0 rgba(146, 36, 61, 0.20) !important;
}

.btn-primary:hover,
.ngis-btn-primary:hover,
.ov-btn-main:hover,
.tp-btn-primary:hover,
.art-btn-primary:hover,
.sk-blue-btn:hover,
button.btn-primary:hover,
a.btn-primary:hover,
[data-role-action="primary"]:hover,
.sh-toolbar-new-btn:hover,
.sh-new-request-btn:hover,
#btnUploadAssignmentOrWork:hover,
#btnAddStudent:hover,
#btnAddClass:hover,
#saveChangesBtn:hover,
#openUploadBtn:hover,
#btnPrimaryAddCourse:hover,
#btnSubmitUpload:hover,
#btnSubmitRequest:hover {
  background: #7A1D32 !important;
  background-color: #7A1D32 !important;
  border-color: #7A1D32 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 6px 0 rgba(146, 36, 61, 0.28) !important;
  transform: none !important;
  translate: none !important;
}

.btn-primary *,
.ngis-btn-primary *,
.ov-btn-main *,
.tp-btn-primary *,
.art-btn-primary *,
.sk-blue-btn *,
button.btn-primary *,
a.btn-primary *,
[data-role-action="primary"] *,
.sh-toolbar-new-btn *,
.sh-new-request-btn *,
#btnUploadAssignmentOrWork * {
  color: #FFFFFF !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in design-system.css (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in design-system.css (CRLF)')
else:
    print('Target not found in design-system.css')

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(c)

