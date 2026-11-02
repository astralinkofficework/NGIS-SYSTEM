import glob, re, os, json

files = sorted(glob.glob('pages/**/*.html', recursive=True) + ['index.html', 'pages-directory.html', 'sitemap.html'])

inventory = []

def get_module(path):
    p = path.replace('\\', '/')
    name = os.path.basename(p)
    if p.startswith('pages/admin/'):
        if name in ['admin.html', 'admin-lifecycle.html']:
            return 'Admin: Overview & Institutional'
        elif name in ['admin-users.html', 'admin-accounts.html', 'admin-students.html', 'admin-teachers.html', 'admin-principals.html', 'admin-admins.html', 'admin-student-profile.html']:
            return 'Admin: User Management'
        elif name in ['admin-departments.html', 'admin-department-detail.html', 'admin-campuses.html', 'admin-campus.html', 'admin-classes.html', 'admin-timetables.html']:
            return 'Admin: Academic Structure'
        elif name in ['admin-lessons.html', 'admin-assignments.html', 'admin-exams.html', 'admin-grades.html', 'admin-attendance.html']:
            return 'Admin: Curriculum & Learning'
        elif name in ['admin-services.html', 'admin-reports.html']:
            return 'Admin: Institutional Records'
        elif name in ['admin-news.html']:
            return 'Admin: Communication'
        elif name in ['admin-logs.html', 'admin-audit.html', 'admin-settings.html']:
            return 'Admin: System & Security'
        return 'Admin: General'
    elif p.startswith('pages/principal/'):
        if name == 'principal.html': return 'Principal: Executive Overview'
        elif name in ['principal-approvals.html', 'principal-reports.html']: return 'Principal: Leadership & Governance'
        return 'Principal: Account & Profile'
    elif p.startswith('pages/teacher/'):
        if name == 'teacher.html': return 'Teacher: Workspace Overview'
        elif name in ['teacher-classes.html', 'teacher-attendance.html', 'teacher-roster.html', 'teacher-lessons.html', 'teacher-departments.html', 'teacher-calendar.html']:
            return 'Teacher: Teaching & Classes'
        elif name in ['teacher-submissions.html', 'teacher-reports.html', 'teacher-grades.html', 'teacher-gradebook.html', 'teacher-grade.html', 'teacher-documents.html']:
            return 'Teacher: Assessment & Grading'
        elif name in ['teacher-announcements.html', 'teacher-notifications.html']:
            return 'Teacher: Communication'
        return 'Teacher: Account & Profile'
    elif p.startswith('pages/student/'):
        if name == 'student.html': return 'Student: Dashboard Overview'
        elif name in ['student-calendar.html', 'student-timetable.html', 'student-id.html', 'student-attendance.html', 'student-assignments.html', 'student-exams.html', 'student-grades.html']:
            return 'Student: Academics & Learning'
        elif name in ['student-services.html', 'student-clubs.html', 'student-lost-found.html']:
            return 'Student: Campus Life'
        elif name in ['student-announcements.html', 'student-notifications.html']:
            return 'Student: Communication'
        return 'Student: Account & Profile'
    elif p.startswith('pages/staff/'):
        if name == 'staff.html': return 'Staff: Operations Overview'
        elif name == 'staff-services.html': return 'Staff: Logistics & Services'
        return 'Staff: Account & Profile'
    elif p.startswith('pages/shared/'):
        return 'Shared: Cross-Portal Modules'
    return 'Public & System Directory'

for f in files:
    f_norm = f.replace('\\', '/')
    content = open(f, encoding='utf-8', errors='ignore').read()
    
    t_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = t_match.group(1).strip() if t_match else os.path.basename(f)
    title = re.sub(r'\s*[\-—\|]\s*NGIS.*$', '', title, flags=re.I).strip()
    title = re.sub(r'[\r\n\t]+', ' ', title).strip()

    route = '/' + f_norm

    if 'pages/admin/' in f_norm:
        roles_allowed = ['admin']
    elif 'pages/principal/' in f_norm:
        roles_allowed = ['principal', 'admin']
    elif 'pages/staff/' in f_norm:
        roles_allowed = ['staff', 'admin']
    elif 'pages/teacher/' in f_norm:
        roles_allowed = ['teacher', 'admin']
    elif 'pages/student/' in f_norm:
        roles_allowed = ['student']
    elif 'pages/shared/' in f_norm:
        roles_allowed = ['admin', 'principal', 'teacher', 'student', 'staff']
    else:
        roles_allowed = ['public (all)']

    comps = []
    if re.search(r'(class=[\x22\x27][^\x22\x27]*modal|id=[\x22\x27][^\x22\x27]*modal|<dialog)', content, re.I): comps.append('Modal')
    if re.search(r'(class=[\x22\x27][^\x22\x27]*drawer|data-drawer)', content, re.I): comps.append('Drawer')
    if re.search(r'<form', content, re.I) or len(re.findall(r'<input|<select|<textarea', content, re.I)) >= 3: comps.append('Form/Inputs')
    if re.search(r'<table', content, re.I) or 'data-table' in content: comps.append('Data Table')
    if re.search(r'role=[\x22\x27]tab[\x22\x27]|class=[\x22\x27][^\x22\x27]*tab', content, re.I): comps.append('Tabs')
    if re.search(r'stat-card|stat-tile|stats-grid|\.stat\b', content, re.I): comps.append('Stat Tiles')
    if re.search(r'class=[\x22\x27][^\x22\x27]*card\b', content, re.I): comps.append('Cards')
    if re.search(r'<canvas|chart\.js', content, re.I): comps.append('Charts')
    if not comps: comps.append('Standard Layout')

    problems = []
    rainbow = len(re.findall(r'(?:bg|text|border)-(?:emerald|green|red|rose|amber|yellow|blue|indigo|purple|violet|pink|orange|teal|cyan)-\d{2,3}', content))
    if rainbow > 0:
        problems.append(f'Rainbow colors ({rainbow} utility color classes)')
    
    bolds = len(re.findall(r'font-(?:bold|extrabold|semibold|black)|font-weight:\s*(?:600|700|800|900|bold)', content))
    if bolds > 0:
        problems.append(f'Heavy font weights ({bolds} bold/semibold instances - violates NO BOLD)')
    
    shadows = len(re.findall(r'shadow-(?:md|lg|xl|2xl)|box-shadow:\s*0\s+(?:[5-9]|\d{2,})px', content))
    if shadows > 0:
        problems.append(f'Heavy shadows ({shadows} instances - violates hairlines)')
        
    centered = len(re.findall(r'text-center', content))
    if centered > 3:
        problems.append(f'Mixed alignment ({centered} text-center classes)')

    if f_norm.startswith('pages/') and f_norm != 'pages/shared/access-denied.html':
        if not re.search(r'(toggle-sidebar|hamburger-btn|mobile-hamburger-btn)', content, re.I):
            problems.append('Missing explicit hamburger button in markup')

    if re.search(r'(Nrinphouneta|Sarah Jenkins|Grade 10-A|\$3,200|KHR 13,000,000)', content):
        problems.append('Hardcoded sample records in markup')

    has_loading = bool(re.search(r'(skeleton|loading-state|is-loading)', content, re.I))
    has_empty = bool(re.search(r'(empty-state|no-data|no-results)', content, re.I))
    has_error = bool(re.search(r'(error-state|error-message|alert-danger)', content, re.I))
    missing_states = []
    if not has_loading: missing_states.append('loading')
    if not has_empty: missing_states.append('empty')
    if not has_error: missing_states.append('error')
    if missing_states:
        problems.append('Missing data states (' + ', '.join(missing_states) + ')')

    inventory.append({
        'name': os.path.basename(f),
        'title': title,
        'path': f_norm,
        'route': route,
        'module': get_module(f_norm),
        'roles': ', '.join(roles_allowed),
        'components': ', '.join(comps),
        'problems': '; '.join(problems) if problems else 'None detected'
    })

with open('scratch/phase0_inventory.json', 'w', encoding='utf-8') as out:
    json.dump(inventory, out, indent=2)

print(f'Saved {len(inventory)} items to scratch/phase0_inventory.json')
