import os

pages = [
    {
        "filename": "pages/admin/admin-teacher-verify.html",
        "role": "admin",
        "active": "verify-teacher",
        "title": "Verify Teacher Update",
        "pageTitle": "NGIS • Verify Teacher Update | School Administration",
        "greeting": "Review, verify, and approve faculty profile update requests and credentials.",
        "initFn": "initVerify",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Verify Teacher Update"}]
    },
    {
        "filename": "pages/principal/principal-teacher-verify.html",
        "role": "principal",
        "active": "verify-teacher",
        "title": "Verify Teacher Update",
        "pageTitle": "NGIS • Verify Teacher Update | Principal Oversight",
        "greeting": "Review, verify, and approve faculty profile update requests and credentials.",
        "initFn": "initVerify",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Verify Teacher Update"}]
    },
    {
        "filename": "pages/admin/admin-teacher-assignments.html",
        "role": "admin",
        "active": "teaching-assignment",
        "title": "Teaching Assignment",
        "pageTitle": "NGIS • Teaching Assignment | School Administration",
        "greeting": "Manage subject allocations, class teaching loads, and faculty workload capacity.",
        "initFn": "initAssignments",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Teaching Assignment"}]
    },
    {
        "filename": "pages/principal/principal-teacher-assignments.html",
        "role": "principal",
        "active": "teaching-assignment",
        "title": "Teaching Assignment",
        "pageTitle": "NGIS • Teaching Assignment | Principal Oversight",
        "greeting": "Manage subject allocations, class teaching loads, and faculty workload capacity.",
        "initFn": "initAssignments",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Teaching Assignment"}]
    },
    {
        "filename": "pages/admin/admin-teacher-homeroom.html",
        "role": "admin",
        "active": "homeroom-assign",
        "title": "Homeroom Teacher Assign",
        "pageTitle": "NGIS • Homeroom Teacher Assign | School Administration",
        "greeting": "Allocate homeroom faculty to class sections, maintain coverage, and monitor student counts.",
        "initFn": "initHomeroom",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Homeroom Teacher Assign"}]
    },
    {
        "filename": "pages/principal/principal-teacher-homeroom.html",
        "role": "principal",
        "active": "homeroom-assign",
        "title": "Homeroom Teacher Assign",
        "pageTitle": "NGIS • Homeroom Teacher Assign | Principal Oversight",
        "greeting": "Allocate homeroom faculty to class sections, maintain coverage, and monitor student counts.",
        "initFn": "initHomeroom",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Homeroom Teacher Assign"}]
    },
    {
        "filename": "pages/admin/admin-teacher-attendance.html",
        "role": "admin",
        "active": "teacher-attendance",
        "title": "Teacher Attendance",
        "pageTitle": "NGIS • Teacher Attendance | School Administration",
        "greeting": "Monitor daily faculty arrival telemetry, biometric terminal syncs, and absence leaves.",
        "initFn": "initAttendance",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Teacher Attendance"}]
    },
    {
        "filename": "pages/principal/principal-teacher-attendance.html",
        "role": "principal",
        "active": "teacher-attendance",
        "title": "Teacher Attendance",
        "pageTitle": "NGIS • Teacher Attendance | Principal Oversight",
        "greeting": "Monitor daily faculty arrival telemetry, biometric terminal syncs, and absence leaves.",
        "initFn": "initAttendance",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Teacher Attendance"}]
    },
    {
        "filename": "pages/admin/admin-teacher-commendation.html",
        "role": "admin",
        "active": "teacher-commendation",
        "title": "Commendation",
        "pageTitle": "NGIS • Faculty Commendation | School Administration",
        "greeting": "Official faculty awards, pedagogical honors, and governing body leadership citations.",
        "initFn": "initCommendation",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Commendation"}]
    },
    {
        "filename": "pages/principal/principal-teacher-commendation.html",
        "role": "principal",
        "active": "teacher-commendation",
        "title": "Commendation",
        "pageTitle": "NGIS • Faculty Commendation | Principal Oversight",
        "greeting": "Official faculty awards, pedagogical honors, and governing body leadership citations.",
        "initFn": "initCommendation",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Commendation"}]
    },
    {
        "filename": "pages/admin/admin-teacher-discipline.html",
        "role": "admin",
        "active": "teacher-discipline",
        "title": "Discipline",
        "pageTitle": "NGIS • Faculty Discipline | School Administration",
        "greeting": "Confidential personnel conduct registry, policy compliance reviews, and hearings.",
        "initFn": "initDiscipline",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Discipline"}]
    },
    {
        "filename": "pages/principal/principal-teacher-discipline.html",
        "role": "principal",
        "active": "teacher-discipline",
        "title": "Discipline",
        "pageTitle": "NGIS • Faculty Discipline | Principal Oversight",
        "greeting": "Confidential personnel conduct registry, policy compliance reviews, and hearings.",
        "initFn": "initDiscipline",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Discipline"}]
    },
    {
        "filename": "pages/admin/admin-teacher-efforts.html",
        "role": "admin",
        "active": "teacher-efforts",
        "title": "Input Teacher Efforts",
        "pageTitle": "NGIS • Input Teacher Efforts | School Administration",
        "greeting": "Document beyond-classroom faculty contributions, school initiatives, and duty points.",
        "initFn": "initEfforts",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Input Teacher Efforts"}]
    },
    {
        "filename": "pages/principal/principal-teacher-efforts.html",
        "role": "principal",
        "active": "teacher-efforts",
        "title": "Input Teacher Efforts",
        "pageTitle": "NGIS • Input Teacher Efforts | Principal Oversight",
        "greeting": "Document beyond-classroom faculty contributions, school initiatives, and duty points.",
        "initFn": "initEfforts",
        "heroBadge": "TEACHERS MANAGEMENT",
        "breadcrumbs": [{"label": "Teachers Management"}, {"label": "Input Teacher Efforts"}]
    }
]

def generate_page_html(p):
    role_name = "School Administrator" if p["role"] == "admin" else "Executive Principal"
    admin_name = "Mr. Heng Samnang" if p["role"] == "admin" else "Dr. Sophal Meas"
    admin_id = "ADM-2026-001" if p["role"] == "admin" else "PRL-2026-004"
    avatar = "https://images.pexels.com/photos/3184339/pexels-photo-3184339.jpeg?auto=compress&cs=tinysrgb&w=160" if p["role"] == "admin" else "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=160"
    
    breadcrumbs_json = str(p["breadcrumbs"]).replace("'", '"')

    return f"""<!doctype html>
<html lang="en" data-theme="light" class="h-full">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>{p['pageTitle']}</title>

<!-- Fonts: Strictly light & medium weights (NO BOLD FONTS per AGENTS.md) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet">

<!-- Phosphor Icons for Mobile Hamburger Menu & Controls -->
<script src="https://unpkg.com/@phosphor-icons/web"></script>

<!-- Tailwind CSS CDN -->
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script>
  tailwind.config = {{
    darkMode: ['selector', '[data-theme="dark"]'],
    theme: {{
      extend: {{
        colors: {{
          forest: {{ 50: '#F0FDF4', 100: '#DCFCE7', 500: '#22C55E', 700: '#15803D', 800: '#176B45', 900: '#14532D' }},
          ink: {{ main: '#1A202C', light: '#4A5568', muted: '#718096' }},
          border: {{ subtle: '#E2E8F0', light: '#EDF2F7' }}
        }},
        fontFamily: {{
          sans: ['"Plus Jakarta Sans"', 'Manrope', 'sans-serif'],
          mono: ['"JetBrains Mono"', 'monospace']
        }},
        fontWeight: {{
          normal: '400',
          medium: '500'
        }}
      }}
    }}
  }};
</script>

<!-- NGIS Design System & Global Styles -->
<link rel="stylesheet" href="../../assets/css/app.css">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
<link rel="stylesheet" href="../../assets/css/action-icons.css">
<script src="../../assets/js/action-icons.js" defer></script>
</head>

<body class="min-h-screen bg-slate-50 font-sans text-slate-800 antialiased flex">

<!-- Main Layout Structure -->
<main class="main flex-1 min-w-0 flex flex-col">

  <!-- Mandatory Mobile Appbar with Hamburger Menu (AGENTS.md Compliance) -->
  <header class="mobile-appbar md:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-border-subtle sticky top-0 z-30 min-h-[44px]">
    <div class="flex items-center gap-3">
      <button type="button" 
              class="hamburger-btn mobile-hamburger-btn p-2 rounded-xl text-ink-main hover:bg-slate-100 active:scale-95 transition-all flex items-center justify-center min-w-[40px] min-h-[40px]" 
              data-action="toggle-sidebar" 
              aria-label="Open menu" 
              aria-expanded="false" 
              title="Open navigation">
        <i class="ph ph-list text-xl text-slate-700"></i>
      </button>
      <span class="text-xs font-medium text-forest-800 tracking-wide uppercase">{p['title']}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-[#176B45] border border-emerald-200">
        Faculty Active
      </span>
    </div>
  </header>

  <!-- Hero Banner Anchor -->
  <div id="heroBanner"></div>

  <!-- Dynamic Content Workspace Container -->
  <div class="page p-4 md:p-6" id="teacherMgmtRoot">
    <!-- Populated dynamically by teacher-management.js -->
    <div class="flex items-center justify-center py-20 text-slate-400">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping"></span>
        <span class="text-xs font-medium">Loading {p['title']}...</span>
      </div>
    </div>
  </div>

</main>

<!-- Configuration for Hero and Layout Navigation -->
<script>
window.PAGE = {{
  role: "{p['role']}",
  active: "{p['active']}"
}};

window.HERO_CONFIG = {{
  name: "{admin_name}",
  id: "{admin_id}",
  grade: "{role_name}",
  avatar: "{avatar}",
  avatarSm: "{avatar}",
  title: "{p['title']}",
  greeting: "{p['greeting']}",
  badge: "{p['heroBadge']}",
  breadcrumbs: {breadcrumbs_json},
  homeLink: "../../index.html",
  signOutLink: "../../index.html",
  profileLink: "{p['role']}-settings.html",
  notifLink: "{p['role']}-logs.html",
  notifCount: 3,
  ddRows: [
    {{ icon: 'co_present', text: 'NGIS Teachers Management' }},
    {{ icon: 'verified', text: '{role_name}' }},
    {{ icon: 'calendar_today', text: 'Academic Year 2025–26' }}
  ]
}};
</script>

<!-- Scripts -->
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>
<script src="../../assets/js/teacher-management.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    if (window.TEACHER_MGMT && typeof window.TEACHER_MGMT.{p['initFn']} === 'function') {{
      window.TEACHER_MGMT.{p['initFn']}('teacherMgmtRoot', '{p['role']}');
    }}
  }});
</script>

</body>
</html>
"""

count = 0
for p in pages:
    html = generate_page_html(p)
    with open(p["filename"], "w", encoding="utf-8") as f:
        f.write(html)
    count += 1
    print(f"Generated ({count}/14): {p['filename']}")

print("All 14 Teacher Management pages created successfully!")

