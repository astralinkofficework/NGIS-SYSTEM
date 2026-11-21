import os, re

files_to_check = [
    'pages/admin/admin-classes.html',
    'pages/admin/admin-news.html',
    'pages/admin/admin-services.html',
    'pages/principal/principal-classes.html',
    'pages/principal/principal-departments.html',
    'assets/js/ngis-users.js',
    'assets/js/student-management.js',
    'assets/js/timetable-monitoring.js'
]

for f in files_to_check:
    print(f"=== {f} ===")
    if not os.path.exists(f):
        print("Not found")
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    
    # Find pagination HTML containers
    html_pag = re.findall(r'(<[^>]+(?:pagination|page-nav|pag-btn)[^>]*>[\s\S]*?<\/[^>]+>)', text, re.I)
    print(f"HTML pagination snippets: {len(html_pag)}")
    for s in html_pag[:2]:
        print("  SNIPPET:", s[:200].replace('\n', ' '))
    
    # Find pagination JS logic
    js_pag = re.findall(r'((?:function\s+|const\s+|let\s+|var\s+)[a-zA-Z0-9_]*(?:pag|renderPagination)[a-zA-Z0-9_]*[\s\S]*?\{[\s\S]*?^\})', text, re.M | re.I)
    print(f"JS pagination functions: {len(js_pag)}")
    for j in js_pag[:2]:
        print("  JS:", j[:250].replace('\n', ' '))
    print()
