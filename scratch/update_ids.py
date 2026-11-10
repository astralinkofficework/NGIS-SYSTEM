with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace in teachers-mgmt-drop for admin
text = text.replace(
    '              { id: "commendation", label: "Commendation", href: "pages/admin/admin-services.html?category=commendation" },\n              { id: "discipline", label: "Discipline", href: "pages/admin/admin-services.html?category=discipline" },',
    '              { id: "teacher-commendation", label: "Commendation", href: "pages/admin/admin-services.html?category=commendation" },\n              { id: "teacher-discipline", label: "Discipline", href: "pages/admin/admin-services.html?category=discipline" },'
)

# Replace in student-mgmt-drop for admin
text = text.replace(
    '              { id: "commendation", label: "Commendation", href: "pages/admin/admin-student-commendation.html" },\n              { id: "discipline", label: "Discipline", href: "pages/admin/admin-student-discipline.html" },',
    '              { id: "student-commendation", label: "Commendation", href: "pages/admin/admin-student-commendation.html" },\n              { id: "student-discipline", label: "Discipline", href: "pages/admin/admin-student-discipline.html" },'
)

# Replace in teachers-mgmt-drop for principal
text = text.replace(
    '              { id: "commendation", label: "Commendation", href: "pages/principal/principal-services.html?category=commendation" },\n              { id: "discipline", label: "Discipline", href: "pages/principal/principal-services.html?category=discipline" },',
    '              { id: "teacher-commendation", label: "Commendation", href: "pages/principal/principal-services.html?category=commendation" },\n              { id: "teacher-discipline", label: "Discipline", href: "pages/principal/principal-services.html?category=discipline" },'
)

# Replace in student-mgmt-drop for principal
text = text.replace(
    '              { id: "commendation", label: "Commendation", href: "pages/principal/principal-student-commendation.html" },\n              { id: "discipline", label: "Discipline", href: "pages/principal/principal-student-discipline.html" },',
    '              { id: "student-commendation", label: "Commendation", href: "pages/principal/principal-student-commendation.html" },\n              { id: "student-discipline", label: "Discipline", href: "pages/principal/principal-student-discipline.html" },'
)

with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(text)

with open('layout.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated layout.js and assets/js/layout.js successfully!")

