import os

pages = [
    {
        "filename": "pages/admin/admin-student-verify.html",
        "role": "admin",
        "active": "verify-student",
        "title": "Verify Student Update",
        "pageTitle": "NGIS • Verify Student Update | School Administration",
        "greeting": "Review and verify student profile updates and documentation submissions.",
        "initFn": "initVerify",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Verify Student Update"}]
    },
    {
        "filename": "pages/principal/principal-student-verify.html",
        "role": "principal",
        "active": "verify-student",
        "title": "Verify Student Update",
        "pageTitle": "NGIS • Verify Student Update | Principal Oversight",
        "greeting": "Review and verify student profile updates and documentation submissions.",
        "initFn": "initVerify",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Verify Student Update"}]
    },
    {
        "filename": "pages/admin/admin-student-assign.html",
        "role": "admin",
        "active": "student-assign",
        "title": "Student Assign To Class",
        "pageTitle": "NGIS • Student Assign To Class | School Administration",
        "greeting": "Manage student class placements, homeroom allocations, and section transfers.",
        "initFn": "initAssign",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Student Assign To Class"}]
    },
    {
        "filename": "pages/principal/principal-student-assign.html",
        "role": "principal",
        "active": "student-assign",
        "title": "Student Assign To Class",
        "pageTitle": "NGIS • Student Assign To Class | Principal Oversight",
        "greeting": "Manage student class placements, homeroom allocations, and section transfers.",
        "initFn": "initAssign",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Student Assign To Class"}]
    },
    {
        "filename": "pages/admin/admin-student-exemption.html",
        "role": "admin",
        "active": "declare-exemption",
        "title": "Declare Exemption",
        "pageTitle": "NGIS • Declare Exemption | School Administration",
        "greeting": "Authorize and record statutory course waivers, medical exemptions, and curriculum dispensations.",
        "initFn": "initExemption",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Declare Exemption"}]
    },
    {
        "filename": "pages/principal/principal-student-exemption.html",
        "role": "principal",
        "active": "declare-exemption",
        "title": "Declare Exemption",
        "pageTitle": "NGIS • Declare Exemption | Principal Oversight",
        "greeting": "Authorize and record statutory course waivers, medical exemptions, and curriculum dispensations.",
        "initFn": "initExemption",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Declare Exemption"}]
    },
    {
        "filename": "pages/admin/admin-subject-gpa.html",
        "role": "admin",
        "active": "subject-gpa",
        "title": "Subject GPA By Exam",
        "pageTitle": "NGIS • Subject GPA By Exam | School Administration",
        "greeting": "Subject-level GPA calculations, examination breakdowns, and cohort performance distributions.",
        "initFn": "initSubjectGpa",
        "heroBadge": "ACADEMIC RESULT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Academic Result"}, {"label": "Subject GPA By Exam"}]
    },
    {
        "filename": "pages/principal/principal-subject-gpa.html",
        "role": "principal",
        "active": "subject-gpa",
        "title": "Subject GPA By Exam",
        "pageTitle": "NGIS • Subject GPA By Exam | Principal Oversight",
        "greeting": "Subject-level GPA calculations, examination breakdowns, and cohort performance distributions.",
        "initFn": "initSubjectGpa",
        "heroBadge": "ACADEMIC RESULT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Academic Result"}, {"label": "Subject GPA By Exam"}]
    },
    {
        "filename": "pages/admin/admin-semester-gpa.html",
        "role": "admin",
        "active": "semester-gpa",
        "title": "Semester GPA",
        "pageTitle": "NGIS • Semester GPA | School Administration",
        "greeting": "Official semester and cumulative grade point averages, credit weights, and honors standing.",
        "initFn": "initSemesterGpa",
        "heroBadge": "ACADEMIC RESULT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Academic Result"}, {"label": "Semester GPA"}]
    },
    {
        "filename": "pages/principal/principal-semester-gpa.html",
        "role": "principal",
        "active": "semester-gpa",
        "title": "Semester GPA",
        "pageTitle": "NGIS • Semester GPA | Principal Oversight",
        "greeting": "Official semester and cumulative grade point averages, credit weights, and honors standing.",
        "initFn": "initSemesterGpa",
        "heroBadge": "ACADEMIC RESULT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Academic Result"}, {"label": "Semester GPA"}]
    },
    {
        "filename": "pages/admin/admin-student-failed.html",
        "role": "admin",
        "active": "student-failed",
        "title": "Student Failed",
        "pageTitle": "NGIS • Student Failed | School Administration",
        "greeting": "Official failing criteria audits (Score < 60% / GPA < 2.0), academic warnings, and remedial pathways.",
        "initFn": "initFailed",
        "heroBadge": "ACADEMIC RESULT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Academic Result"}, {"label": "Student Failed"}]
    },
    {
        "filename": "pages/principal/principal-student-failed.html",
        "role": "principal",
        "active": "student-failed",
        "title": "Student Failed",
        "pageTitle": "NGIS • Student Failed | Principal Oversight",
        "greeting": "Official failing criteria audits (Score < 60% / GPA < 2.0), academic warnings, and remedial pathways.",
        "initFn": "initFailed",
        "heroBadge": "ACADEMIC RESULT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Academic Result"}, {"label": "Student Failed"}]
    },
    {
        "filename": "pages/admin/admin-absence-stats.html",
        "role": "admin",
        "active": "absence-stats",
        "title": "Absence Statistics",
        "pageTitle": "NGIS • Absence Statistics | School Administration",
        "greeting": "Institutional attendance telemetry, chronic absenteeism tracking, and class rate comparisons.",
        "initFn": "initAbsenceStats",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Absence Statistics"}]
    },
    {
        "filename": "pages/principal/principal-absence-stats.html",
        "role": "principal",
        "active": "absence-stats",
        "title": "Absence Statistics",
        "pageTitle": "NGIS • Absence Statistics | Principal Oversight",
        "greeting": "Institutional attendance telemetry, chronic absenteeism tracking, and class rate comparisons.",
        "initFn": "initAbsenceStats",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Absence Statistics"}]
    },
    {
        "filename": "pages/admin/admin-registration-approve.html",
        "role": "admin",
        "active": "registration-approve",
        "title": "Registration Form Approve",
        "pageTitle": "NGIS • Registration Form Approve | School Administration",
        "greeting": "New student admissions pipeline, document verification, matriculation approval, and student ID generation.",
        "initFn": "initRegistration",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Registration Form Approve"}]
    },
    {
        "filename": "pages/principal/principal-registration-approve.html",
        "role": "principal",
        "active": "registration-approve",
        "title": "Registration Form Approve",
        "pageTitle": "NGIS • Registration Form Approve | Principal Oversight",
        "greeting": "New student admissions pipeline, document verification, matriculation approval, and student ID generation.",
        "initFn": "initRegistration",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Registration Form Approve"}]
    },
    {
        "filename": "pages/admin/admin-student-commendation.html",
        "role": "admin",
        "active": "student-commendation",
        "title": "Commendation",
        "pageTitle": "NGIS • Student Commendation | School Administration",
        "greeting": "Official student honors, certificates of excellence, Dean's List citations, and extracurricular awards.",
        "initFn": "initCommendation",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Commendation"}]
    },
    {
        "filename": "pages/principal/principal-student-commendation.html",
        "role": "principal",
        "active": "student-commendation",
        "title": "Commendation",
        "pageTitle": "NGIS • Student Commendation | Principal Oversight",
        "greeting": "Official student honors, certificates of excellence, Dean's List citations, and extracurricular awards.",
        "initFn": "initCommendation",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Commendation"}]
    },
    {
        "filename": "pages/admin/admin-student-discipline.html",
        "role": "admin",
        "active": "student-discipline",
        "title": "Discipline",
        "pageTitle": "NGIS • Student Discipline | School Administration",
        "greeting": "Confidential student conduct management, behavioral incident logs, hearing records, and restorative resolutions.",
        "initFn": "initDiscipline",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Discipline"}]
    },
    {
        "filename": "pages/principal/principal-student-discipline.html",
        "role": "principal",
        "active": "student-discipline",
        "title": "Discipline",
        "pageTitle": "NGIS • Student Discipline | Principal Oversight",
        "greeting": "Confidential student conduct management, behavioral incident logs, hearing records, and restorative resolutions.",
        "initFn": "initDiscipline",
        "heroBadge": "STUDENT MANAGEMENT",
        "breadcrumbs": [{"label": "Student Management"}, {"label": "Discipline"}]
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
        Active Term
      </span>
    </div>
  </header>

  <!-- Hero Banner Anchor -->
  <div id="heroBanner"></div>

  <!-- Dynamic Content Workspace Container -->
  <div class="page p-4 md:p-6" id="studentMgmtRoot">
    <!-- Populated dynamically by student-management.js -->
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
    {{ icon: 'school', text: 'NGIS Student Management' }},
    {{ icon: 'verified', text: '{role_name}' }},
    {{ icon: 'calendar_today', text: 'Academic Year 2025–26' }}
  ]
}};
</script>

<!-- Scripts -->
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>
<script src="../../assets/js/student-management.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    if (window.STUDENT_MGMT && typeof window.STUDENT_MGMT.{p['initFn']} === 'function') {{
      window.STUDENT_MGMT.{p['initFn']}('studentMgmtRoot', '{p['role']}');
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
    print(f"Generated ({count}/20): {p['filename']}")

print("All 20 pages created successfully!")

