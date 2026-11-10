import re

principal_pages = [
    {
        "path": "pages/principal/principal-records.html",
        "active": "ks-records",
        "title": "Data Entry & Records",
        "greeting": "Manage teacher, class, and room records with spreadsheet precision.",
        "breadcrumbs": "[{ label: 'Academics', href: 'principal-timetables.html' }, { label: 'Data Entry & Records' }]"
    },
    {
        "path": "pages/principal/principal-subjects.html",
        "active": "ks-subjects",
        "title": "Curriculum Subjects",
        "greeting": "Review MoEYS standard and school-wide curriculum subjects.",
        "breadcrumbs": "[{ label: 'Academics', href: 'principal-timetables.html' }, { label: 'Subjects' }]"
    },
    {
        "path": "pages/principal/principal-teacher-class-assignment.html",
        "active": "ks-wizard",
        "title": "Teacher Assignment Matrix",
        "greeting": "Assign specialized faculty cohorts and verify weekly period allocations.",
        "breadcrumbs": "[{ label: 'Academics', href: 'principal-timetables.html' }, { label: 'Teacher Assignment' }]"
    },
    {
        "path": "pages/principal/principal-timetables.html",
        "active": "ks-viewer",
        "title": "Master Timetables",
        "greeting": "Inspect, filter, and print master class, teacher, and room timetables.",
        "breadcrumbs": "[{ label: 'Academics', href: 'principal-timetables.html' }, { label: 'Master Timetables' }]"
    }
]

admin_pages = [
    {
        "path": "pages/admin/admin-records.html",
        "active": "ks-records",
        "title": "Data Entry & Records",
        "greeting": "Manage teacher, class, and room records with spreadsheet precision.",
        "breadcrumbs": "[{ label: 'Academics', href: 'admin-timetables.html' }, { label: 'Data Entry & Records' }]"
    },
    {
        "path": "pages/admin/admin-subjects.html",
        "active": "ks-subjects",
        "title": "Curriculum Subjects",
        "greeting": "Review MoEYS standard and school-wide curriculum subjects.",
        "breadcrumbs": "[{ label: 'Academics', href: 'admin-timetables.html' }, { label: 'Subjects' }]"
    },
    {
        "path": "pages/admin/admin-teacher-class-assignment.html",
        "active": "ks-wizard",
        "title": "Teacher Assignment Matrix",
        "greeting": "Assign specialized faculty cohorts and verify weekly period allocations.",
        "breadcrumbs": "[{ label: 'Academics', href: 'admin-timetables.html' }, { label: 'Teacher Assignment' }]"
    },
    {
        "path": "pages/admin/admin-timetable-builder.html",
        "active": "ks-builder",
        "title": "Timetable Builder",
        "greeting": "Drag, schedule, and resolve period conflicts across all classes and rooms.",
        "breadcrumbs": "[{ label: 'Academics', href: 'admin-timetables.html' }, { label: 'Timetable Builder' }]"
    },
    {
        "path": "pages/admin/admin-timetables.html",
        "active": "ks-viewer",
        "title": "Master Timetables",
        "greeting": "Inspect, filter, and print master class, teacher, and room timetables.",
        "breadcrumbs": "[{ label: 'Academics', href: 'admin-timetables.html' }, { label: 'Master Timetables' }]"
    }
]

def update_page(cfg, role):
    path = cfg["path"]
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add hero.css in head if missing
    if 'hero.css' not in content:
        content = content.replace(
            '<link rel="stylesheet" href="../../assets/css/app.css?v=3.1">',
            '<link rel="stylesheet" href="../../assets/css/app.css?v=3.1">\n<link rel="stylesheet" href="../../assets/css/hero.css">'
        )
        # fallback if app.css has no version
        if 'hero.css' not in content:
            content = content.replace(
                '<link rel="stylesheet" href="../../assets/css/app.css">',
                '<link rel="stylesheet" href="../../assets/css/app.css">\n<link rel="stylesheet" href="../../assets/css/hero.css">'
            )

    # 2. Add <header id="heroBanner" role="banner"></header> inside <main class="main">
    # Replace the redundant mobile-appbar if present, or add heroBanner at top of main
    if 'id="heroBanner"' not in content:
        # Check if mobile-appbar is inside main
        mobile_appbar_pattern = r'<main class="main">\s*<!-- Mandatory Mobile Appbar with Hamburger Menu \(AGENTS\.md Compliance\) -->\s*<header class="mobile-appbar.*?</header>'
        if re.search(mobile_appbar_pattern, content, re.DOTALL):
            content = re.sub(
                mobile_appbar_pattern,
                '<main class="main">\n  <header id="heroBanner" role="banner"></header>',
                content,
                flags=re.DOTALL
            )
        else:
            content = content.replace(
                '<main class="main">',
                '<main class="main">\n  <header id="heroBanner" role="banner"></header>'
            )

    # 3. Add HERO_CONFIG and hero.js before layout.js
    if 'hero.js' not in content:
        if role == 'principal':
            hero_script = f"""<script>
window.HERO_CONFIG = {{
  role: 'principal', active: '{cfg["active"]}', isDashboard: false,
  name: 'Dr. Ly Bunheng', id: 'PRN-2024-001', grade: 'Principal',
  avatar: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=160',
  homeLink: '../../index.html', signOutLink: '../../index.html',
  profileLink: 'principal-profile.html', notifLink: 'principal.html', notifCount: 3,
  title: '{cfg["title"]}',
  greeting: '{cfg["greeting"]}',
  breadcrumbs: {cfg["breadcrumbs"]},
  ddRows: [
    {{ icon: 'school', text: 'New Gateway International School' }},
    {{ icon: 'verified', text: 'School Principal' }}
  ]
}};
</script>
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>"""
        else: # admin
            hero_script = f"""<script>
window.HERO_CONFIG = {{
  role: 'admin', active: '{cfg["active"]}', isDashboard: false,
  name: 'Mr. Heng Samnang', id: 'ADM-2026-001', grade: 'School Administrator',
  avatar: 'https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=160',
  homeLink: '../../index.html', signOutLink: '../../index.html',
  profileLink: 'admin-settings.html', notifLink: 'admin-logs.html', notifCount: 4,
  title: '{cfg["title"]}',
  greeting: '{cfg["greeting"]}',
  breadcrumbs: {cfg["breadcrumbs"]},
  ddRows: [
    {{ icon: 'admin_panel_settings', text: 'School Administration' }},
    {{ icon: 'groups', text: '5,200 active users' }},
    {{ icon: 'email', text: 'heng.samnang@ngis.edu.kh' }},
    {{ icon: 'verified', text: 'Principal Administrator' }}
  ]
}};
</script>
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>"""

        content = content.replace('<script src="../../assets/js/layout.js"></script>', hero_script)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {path}")

for p in principal_pages:
    update_page(p, "principal")

for p in admin_pages:
    update_page(p, "admin")

print("All pages successfully updated!")

