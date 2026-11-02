with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    c = f.read()

target = """/* 9. Primary Action Buttons Anchored in Institutional Dark Emerald (#202F63) */
body[data-role="admin"] .btn-primary,
body[data-role="admin"] .sk-blue-btn,
body[data-role="admin"] .bg-brand-dark,
body[data-role="admin"] .btn.btn-primary,
body[data-role="admin"] button.btn-primary,
body[data-role="admin"] a.btn-primary,
body[data-role="admin"] #btnAddStudent,
body[data-role="admin"] #btnAddClass,
body[data-role="admin"] #E5E5E8GradeRowBtn,
body[data-role="admin"] [data-role-action="primary"],
body[data-portal="admin"] .btn-primary,
body[data-portal="admin"] .sk-blue-btn,
body[data-portal="admin"] .bg-brand-dark,
body[data-portal="admin"] .btn.btn-primary,
body[data-portal="admin"] button.btn-primary,
body[data-portal="admin"] a.btn-primary,
.sk-blue-btn {
  background-color: #202F63 !important;
  color: #ffffff !important;
  border: 1px solid transparent !important;
  font-weight: 500 !important;
  transition: all 0.15s ease !important;
  border-radius: 8px !important;
}

body[data-role="admin"] .btn-primary:hover,
body[data-role="admin"] .sk-blue-btn:hover,
body[data-role="admin"] .bg-brand-dark:hover,
body[data-role="admin"] .btn.btn-primary:hover,
body[data-role="admin"] button.btn-primary:hover,
body[data-role="admin"] a.btn-primary:hover,
body[data-role="admin"] #btnAddStudent:hover,
body[data-role="admin"] #btnAddClass:hover,
body[data-role="admin"] #E5E5E8GradeRowBtn:hover,
body[data-portal="admin"] .btn-primary:hover,
body[data-portal="admin"] .sk-blue-btn:hover,
body[data-portal="admin"] .bg-brand-dark:hover,
.sk-blue-btn:hover {
  background-color: #000000 !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}"""

replacement = """/* 9. Primary Action Buttons Anchored in Burgundy (#92243D) with White (#FFFFFF) text */
body[data-role="admin"] .btn-primary,
body[data-role="admin"] .sk-blue-btn,
body[data-role="admin"] .bg-brand-dark,
body[data-role="admin"] .btn.btn-primary,
body[data-role="admin"] button.btn-primary,
body[data-role="admin"] a.btn-primary,
body[data-role="admin"] #btnAddStudent,
body[data-role="admin"] #btnAddClass,
body[data-role="admin"] #E5E5E8GradeRowBtn,
body[data-role="admin"] [data-role-action="primary"],
body[data-portal="admin"] .btn-primary,
body[data-portal="admin"] .sk-blue-btn,
body[data-portal="admin"] .bg-brand-dark,
body[data-portal="admin"] .btn.btn-primary,
body[data-portal="admin"] button.btn-primary,
body[data-portal="admin"] a.btn-primary,
.sk-blue-btn {
  background-color: #92243D !important;
  color: #ffffff !important;
  border: 1px solid #92243D !important;
  font-weight: 500 !important;
  transition: all 0.15s ease !important;
  border-radius: 8px !important;
}

body[data-role="admin"] .btn-primary:hover,
body[data-role="admin"] .sk-blue-btn:hover,
body[data-role="admin"] .bg-brand-dark:hover,
body[data-role="admin"] .btn.btn-primary:hover,
body[data-role="admin"] button.btn-primary:hover,
body[data-role="admin"] a.btn-primary:hover,
body[data-role="admin"] #btnAddStudent:hover,
body[data-role="admin"] #btnAddClass:hover,
body[data-role="admin"] #E5E5E8GradeRowBtn:hover,
body[data-portal="admin"] .btn-primary:hover,
body[data-portal="admin"] .sk-blue-btn:hover,
body[data-portal="admin"] .bg-brand-dark:hover,
.sk-blue-btn:hover {
  background-color: #7A1D32 !important;
  border-color: #7A1D32 !important;
  color: #ffffff !important;
  box-shadow: 0 1px 3px rgba(146, 36, 61, 0.2) !important;
}"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced in interactions.css (LF)')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced in interactions.css (CRLF)')
else:
    print('Target not found in interactions.css')

with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
    f.write(c)

