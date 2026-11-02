import urllib.request, urllib.error, py_compile, io

# 1. /staff must be gone
for path in ('/staff', '/staff/', '/api/staff/stats', '/api/staff/tasks'):
    try:
        code = urllib.request.urlopen('http://localhost:3000' + path, timeout=5).status
    except urllib.error.HTTPError as e:
        code = e.code
    print(path, '->', code)

# 2. other portals still serve
for path in ('/', '/pages/student/student.html', '/pages/teacher/teacher.html',
             '/pages/admin/admin.html', '/pages/principal/principal.html'):
    try:
        code = urllib.request.urlopen('http://localhost:3000' + path, timeout=5).status
    except urllib.error.HTTPError as e:
        code = e.code
    print(path, '->', code)

# 3. edited tests compile
for f in ('tests/e2e-portals.test.py', 'tests/portal-routing.test.py',
          'tests/test_all_portals_ui_clean.py', 'tests/test_all_portals_viewport.py',
          'tests/audit_detailed_headers.py', 'academic_store.py'):
    py_compile.compile(f, doraise=True)
    print('compile OK', f)
