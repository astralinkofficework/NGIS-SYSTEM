import re

def clean_file(path, removals):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for r in removals:
        if r not in content:
            print(f"WARNING: Target not found in {path}: {repr(r[:40])}")
        content = content.replace(r, '', 1)
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully cleaned duplicates in {path}")
    else:
        print(f"No changes in {path}")

# 1. admin-department-detail.html
clean_file('pages/admin/admin-department-detail.html', [
"""<!-- NGIS global action-icon engine -->
<link rel="stylesheet" href="../../assets/css/action-icons.css?v=1.13.2">
<script src="../../assets/js/action-icons.js?v=1.13.2" defer></script>
"""
])

# 2. admin-departments.html
clean_file('pages/admin/admin-departments.html', [
"""  <link rel="stylesheet" href="../../assets/css/app.css">
  <link rel="stylesheet" href="../../assets/css/hero.css">
"""
])

# 3. admin-grade-release.html
clean_file('pages/admin/admin-grade-release.html', [
"""<!-- NGIS global action-icon engine -->
<link rel="stylesheet" href="../../assets/css/action-icons.css?v=1.13.2">
<script src="../../assets/js/action-icons.js?v=1.13.2" defer></script>
"""
])

# 4. principal-reports.html
clean_file('pages/principal/principal-reports.html', [
"""<!-- NGIS global action-icon engine -->
<link rel="stylesheet" href="../../assets/css/action-icons.css?v=1.13.2">
<script src="../../assets/js/action-icons.js?v=1.13.2" defer></script>
"""
])

# 5. student-assignments.html
clean_file('pages/student/student-assignments.html', [
"""<link rel="stylesheet" href="../../assets/css/hero.css">
""",
"""<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
"""
])

# 6. student-calendar.html
clean_file('pages/student/student-calendar.html', [
"""<link rel="stylesheet" href="../../assets/css/hero.css">
""",
"""<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
"""
])

# 7. student-grades.html
clean_file('pages/student/student-grades.html', [
"""<link rel="stylesheet" href="../../assets/css/hero.css">
"""
])

# 8. student-lost-found.html
clean_file('pages/student/student-lost-found.html', [
"""<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
""",
"""<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
"""
])

# 9. student-notifications.html
clean_file('pages/student/student-notifications.html', [
"""<link rel="stylesheet" href="../../assets/css/hero.css">
""",
"""<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
"""
])

# 10. student-profile.html
clean_file('pages/student/student-profile.html', [
"""<link rel="stylesheet" href="../../assets/css/hero.css">
""",
"""<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
"""
])

# 11. student-services.html
clean_file('pages/student/student-services.html', [
"""<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
""",
"""<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
"""
])

# 12. teacher-submissions.html
clean_file('pages/teacher/teacher-submissions.html', [
"""<link rel="stylesheet" href="../../assets/css/action-icons.css?v=1.13.2">
<script src="../../assets/js/action-icons.js?v=1.13.2" defer></script>
"""
])

print("Finished cleaning duplicate tags.")
