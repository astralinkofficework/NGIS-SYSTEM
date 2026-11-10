import glob, re

pages_with_actions = [
    'pages/admin/admin-assignments.html',
    'pages/admin/admin-attendance.html',
    'pages/admin/admin-campus.html',
    'pages/admin/admin-classes.html',
    'pages/admin/admin-department-detail.html',
    'pages/admin/admin-exams.html',
    'pages/admin/admin-grade-release.html',
    'pages/admin/admin-grades.html',
    'pages/admin/admin-lessons.html',
    'pages/admin/admin-logs.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-services.html',
    'pages/admin/admin-timetables.html',
    'pages/admin/admin-users.html',
    'pages/admin/admin.html',
    'pages/principal/principal-activity.html',
    'pages/principal/principal-attendance.html',
    'pages/principal/principal-classes.html',
    'pages/principal/principal-departments.html',
    'pages/principal/principal-reports.html',
    'pages/principal/principal-services.html',
    'pages/principal/principal-timetables.html',
    'pages/student/student-assignments.html',
    'pages/student/student-lost-found.html',
    'pages/teacher/teacher-lessons.html',
    'pages/teacher/teacher-reports.html',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-submissions.html'
]

for p in pages_with_actions:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Search for action button markup in content
    # Find any <button or <a that has visible text in an action group, or action-btn-pill, or td
    has_text_action = False
    details = []

    # Check for action-btn-pill
    pills = re.findall(r'<button[^>]*class="[^"]*action-btn-pill[^"]*"[^>]*>(.*?)</button>', content, re.DOTALL)
    for pill in pills:
        has_text_action = True
        clean = re.sub(r'<[^>]+>', ' ', pill).strip()
        clean = ' '.join(clean.split())
        details.append(f"PILL: {clean}")

    # Check for td with button with text
    tds = re.findall(r'<td[^>]*class="[^"]*(?:table-actions|text-right)[^"]*"[^>]*>(.*?)</td>', content, re.DOTALL)
    for td in tds:
        btns = re.findall(r'<button[^>]*>(.*?)</button>', td, re.DOTALL)
        for b in btns:
            clean = re.sub(r'<[^>]+>', ' ', b).strip()
            clean = ' '.join(clean.split())
            if clean and not clean in ['P', 'L', 'A', 'E'] and not re.match(r'^[\d\+\-✕✓•·]$', clean):
                has_text_action = True
                details.append(f"TD BTN: {clean}")

    # Also search for template literal rows in scripts
    # e.g. `<button class="action-btn-pill...` or `<button class="...action...`
    btn_templates = re.findall(r'<button[^>]*class="[^"]*(?:action|btn)[^"]*"[^>]*>(.*?)</button>', content, re.DOTALL)
    for bt in btn_templates:
        if 'action-btn-pill' in bt:
            pass # handled above
        clean = re.sub(r'<[^>]+>', ' ', bt).strip()
        clean = ' '.join(clean.split())
        # Check if it has action words
        if any(w in clean.lower() for w in ['authorize', 'review', 'return', 'edit', 'delete', 'view syllabi', 'deactivate class', 'activate class', 'handover', 'notify parent', 'audit']):
            has_text_action = True
            details.append(f"SCRIPT BTN: {clean}")

    print(f"\n{p}: {'HAS TEXT IN ROW ACTIONS' if has_text_action else 'ICON-ONLY OK'}")
    for d in list(dict.fromkeys(details))[:6]:
        print(f"   {d}")

