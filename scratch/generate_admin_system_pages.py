import os

pages = [
    {
        'file': 'pages/admin/admin-system-school-info.html',
        'title': 'School Information | System Admin',
        'active': 'sys-school-info',
        'header': 'School Information',
        'sub': 'Official institutional profile & MOEYS licensing',
        'init': 'window.SYS_MGMT.initSchoolInfo("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-school-year.html',
        'title': 'School Year | System Admin',
        'active': 'sys-school-year',
        'header': 'School Year',
        'sub': 'Academic year cycles, terms & status',
        'init': 'window.SYS_MGMT.initSchoolYear("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-school-week.html',
        'title': 'School Week | System Admin',
        'active': 'sys-school-week',
        'header': 'School Week',
        'sub': '40-week instructional pacing calendar',
        'init': 'window.SYS_MGMT.initSchoolWeek("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-exam-config.html',
        'title': 'School Exam Configuration | System Admin',
        'active': 'sys-exam-config',
        'header': 'School Exam Configuration',
        'sub': 'Assessment weighting, scales & evaluation rules',
        'init': 'window.SYS_MGMT.initExamConfig("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-score-lock.html',
        'title': 'Score Lock Configuration | System Admin',
        'active': 'sys-score-lock',
        'header': 'Score Lock Configuration',
        'sub': 'Term grade finalization & security locks',
        'init': 'window.SYS_MGMT.initScoreLock("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-define-curriculum.html',
        'title': 'Define Curriculum | System Admin',
        'active': 'sys-define-curriculum',
        'header': 'Define Curriculum',
        'sub': 'Subject frameworks & credit allocations',
        'init': 'window.SYS_MGMT.initDefineCurriculum("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-design-curriculum.html',
        'title': 'Design Curriculum | System Admin',
        'active': 'sys-design-curriculum',
        'header': 'Design Curriculum',
        'sub': 'Weekly teaching periods & syllabus structure',
        'init': 'window.SYS_MGMT.initDesignCurriculum("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-declare-class.html',
        'title': 'Declare Class | System Admin',
        'active': 'sys-declare-class',
        'header': 'Declare Class',
        'sub': 'Cohort rosters, capacity & homeroom mapping',
        'init': 'window.SYS_MGMT.initDeclareClass("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-student-transition.html',
        'title': 'Student Transition | System Admin',
        'active': 'sys-student-transition',
        'header': 'Student Transition',
        'sub': 'Annual cohort rollover, promotion & graduations',
        'init': 'window.SYS_MGMT.initStudentTransition("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-technician-assign.html',
        'title': 'Technician & Monitor Assign | System Admin',
        'active': 'sys-technician-assign',
        'header': 'Technician & Monitor Assign',
        'sub': 'Staff delegations for campus labs & terminals',
        'init': 'window.SYS_MGMT.initTechnicianAssign("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-employee-group.html',
        'title': 'Employee Group | System Admin',
        'active': 'sys-employee-group',
        'header': 'Employee Group',
        'sub': 'Organizational staffing groups & roles',
        'init': 'window.SYS_MGMT.initEmployeeGroup("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-employee-accounts.html',
        'title': 'Employee Accounts | System Admin',
        'active': 'sys-employee-accounts',
        'header': 'Employee Accounts',
        'sub': 'Staff portal credentials & access control',
        'init': 'window.SYS_MGMT.initAccounts("systemMgmtRoot", "TEACHER");'
    },
    {
        'file': 'pages/admin/admin-system-student-accounts.html',
        'title': 'Student Accounts | System Admin',
        'active': 'sys-student-accounts',
        'header': 'Student Accounts',
        'sub': 'Learner portal access & credential provisioning',
        'init': 'window.SYS_MGMT.initAccounts("systemMgmtRoot", "STUDENT");'
    },
    {
        'file': 'pages/admin/admin-system-parent-accounts.html',
        'title': 'Parent Accounts | System Admin',
        'active': 'sys-parent-accounts',
        'header': 'Parent Accounts',
        'sub': 'Guardian portal logins & linked dependents',
        'init': 'window.SYS_MGMT.initAccounts("systemMgmtRoot", "PARENT");'
    },
    {
        'file': 'pages/admin/admin-system-schedule.html',
        'title': 'Schedule | System Admin',
        'active': 'sys-schedule',
        'header': 'Schedule',
        'sub': 'Bell schedules, instructional bells & sessions',
        'init': 'window.SYS_MGMT.initSchedule("systemMgmtRoot");'
    },
    {
        'file': 'pages/admin/admin-system-general-setting.html',
        'title': 'General Setting | System Admin',
        'active': 'sys-general-setting',
        'header': 'General Setting',
        'sub': 'System defaults, date formats & operational rules',
        'init': 'window.SYS_MGMT.initGeneralSetting("systemMgmtRoot");'
    }
]

template = '''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
<title>NGIS — {title}</title>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined" rel="stylesheet">

<!-- NGIS Stylesheets -->
<link rel="stylesheet" href="../../assets/css/app.css?v=3.1">
<link rel="stylesheet" href="../../assets/css/hero.css">
<link rel="stylesheet" href="../../assets/css/interactions.css">
<link rel="stylesheet" href="../../assets/css/design-system.css">
<link rel="stylesheet" href="../../assets/css/profiles.css">

<!-- Phosphor Icons for Mobile Hamburger Navigation (AGENTS.md Critical Rule) -->
<script src="https://unpkg.com/@phosphor-icons/web"></script>

<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
tailwind.config = {{
  darkMode: "class",
  theme: {{
    extend: {{
      colors: {{
        "on-error": "#ffffff",
        "on-tertiary": "#ffffff",
        "on-primary-container": "#176B45",
        "primary": "#29352E",
        "error": "#176B45",
        "inverse-on-surface": "#FFFFFF",
        "inverse-surface": "#000000",
        "on-primary": "#ffffff",
        "surface-container": "#F7F9F7",
        "surface-dim": "#F7F9F7",
        "outline-variant": "#E1E9E3",
        "on-error-container": "#176B45",
        "on-primary-fixed-variant": "#000000",
        "primary-fixed-dim": "#E1E9E3",
        "surface-tint": "#29352E",
        "secondary": "#000000",
        "surface": "#F7F9F7",
        "surface-container-lowest": "#ffffff",
        "tertiary-fixed-dim": "#E1E9E3"
      }},
      fontFamily: {{
        headline: ["Manrope", "sans-serif"],
        body: ["Plus Jakarta Sans", "sans-serif"]
      }}
    }}
  }}
}};
</script>

<link rel="stylesheet" href="../../assets/css/action-icons.css">
<script src="../../assets/js/action-icons.js" defer></script>
</head>

<body data-role="admin" data-portal="admin" data-page="{active}" class="ngis-system-mgmt bg-background font-body text-on-surface antialiased">
<main class="main">

  <!-- Desktop Hero Banner -->
  <div id="heroBanner" class="hidden lg:block"></div>

  <!-- ═══ MANDATORY MOBILE / TABLET APP BAR (AGENTS.md CRITICAL RULE) ═══ -->
  <header class="lg:hidden bg-white border-b border-surface-container px-4 py-3 flex items-center justify-between sticky top-0 z-30 shadow-xs no-print">
    <div class="flex items-center gap-3 min-w-0">
      <button type="button" class="hamburger-btn mobile-hamburger-btn p-1.5 -ml-1 text-slate-700 hover:bg-surface-container-low rounded-lg active:scale-95 transition flex items-center justify-center min-w-[38px] min-h-[38px]" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">
        <i class="ph-bold ph-list text-xl"></i>
      </button>
      <div class="min-w-0 truncate">
        <h1 class="text-sm font-medium text-primary leading-tight truncate">{header}</h1>
        <p class="text-[11px] text-slate-500 leading-none mt-0.5 truncate">{sub}</p>
      </div>
    </div>
    <div class="flex items-center gap-2 flex-shrink-0">
      <span class="px-2.5 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-[11px] font-medium text-[#176B45]">System Admin</span>
    </div>
  </header>

  <!-- ═══ MAIN WORKSPACE CONTAINER ═══ -->
  <div class="page p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto flex flex-col gap-6 pb-28 lg:pb-12" id="systemMgmtRoot">
    <div class="flex items-center justify-center py-16 text-slate-400 gap-2 text-xs">
      <span class="material-symbols-outlined animate-spin text-lg">progress_activity</span>
      <span>Loading system configuration...</span>
    </div>
  </div>

</main>

<script>
  window.PAGE = {{ role: "admin", active: "{active}" }};
</script>
<script src="../../assets/js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>
<script src="../../assets/js/system-management.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    if (window.SYS_MGMT) {{
      {init}
    }}
  }});
</script>
</body>
</html>
'''

os.makedirs('pages/admin', exist_ok=True)

for p in pages:
    content = template.format(
        title=p['title'],
        active=p['active'],
        header=p['header'],
        sub=p['sub'],
        init=p['init']
    )
    with open(p['file'], 'w', encoding='utf-8') as f:
        f.write(content)
    print('Created:', p['file'])

print('All 16 pages generated successfully!')

